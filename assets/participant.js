const TASKS = {
  ljt_a: {
    label: "PV-LJT List A",
    path: "materials/pilot_trial_file_ljt_list_A_v5_production.tsv",
    kind: "ljt",
    audioFolder: "ljt_v5",
    practiceAudioFolder: "ljt_practice_v5",
    responseField: "expected_response",
    balanceField: "expected_response",
    prompt: "Is the sentence acceptable?",
    responses: [
      { value: "acceptable", label: "Acceptable", className: "yes" },
      { value: "unacceptable", label: "Unacceptable", className: "no" },
    ],
  },
  ljt_b: {
    label: "PV-LJT List B",
    path: "materials/pilot_trial_file_ljt_list_B_v5_production.tsv",
    kind: "ljt",
    audioFolder: "ljt_v5",
    practiceAudioFolder: "ljt_practice_v5",
    responseField: "expected_response",
    balanceField: "expected_response",
    prompt: "Is the sentence acceptable?",
    responses: [
      { value: "acceptable", label: "Acceptable", className: "yes" },
      { value: "unacceptable", label: "Unacceptable", className: "no" },
    ],
  },
  audio_decision: {
    label: "Audio PV Decision",
    path: "materials/pilot_trial_file_audio_decision_v1.tsv",
    kind: "audio_decision",
    responseField: "correct_response",
    balanceField: "correct_response",
    prompt: "Is this a common English phrasal verb?",
    responses: [
      { value: "yes", label: "Yes", className: "yes" },
      { value: "no", label: "No", className: "no" },
    ],
  },
};

const APP_VERSION = "pv-ljt-simple-v1";
const MAX_RUN_LENGTH = 3;

const app = document.getElementById("participantApp");

const state = {
  stage: "setup",
  participantId: "",
  voice: "male",
  taskKey: "ljt_a",
  rawTrials: [],
  trialPlan: [],
  currentIndex: 0,
  responses: [],
  startedAt: "",
  completedAt: "",
  randomization: null,
  active: null,
};

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function parseTsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines.shift().split("\t");
  return lines.map((line) => {
    const cells = line.split("\t");
    return Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
  });
}

function hashString(text) {
  let hash = 2166136261;
  for (let i = 0; i < text.length; i += 1) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function seededUnit(seed) {
  let x = hashString(seed) || 1;
  x ^= x << 13;
  x ^= x >>> 17;
  x ^= x << 5;
  return (x >>> 0) / 4294967296;
}

function shuffleDeterministic(values, seed) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(seededUnit(`${seed}:${i}`) * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function countRunViolations(trials, field) {
  let violations = 0;
  let run = 0;
  let previous = "";
  trials.forEach((trial) => {
    const value = String(trial[field] || "");
    if (value && value === previous) {
      run += 1;
    } else {
      run = 1;
      previous = value;
    }
    if (run > MAX_RUN_LENGTH) {
      violations += run - MAX_RUN_LENGTH;
    }
  });
  return violations;
}

function countAdjacentMatches(trials, field) {
  let matches = 0;
  for (let i = 1; i < trials.length; i += 1) {
    const current = String(trials[i][field] || "");
    const previous = String(trials[i - 1][field] || "");
    if (current && current === previous) {
      matches += 1;
    }
  }
  return matches;
}

function randomizationScore(trials, task) {
  const answerRuns = countRunViolations(trials, task.balanceField);
  const typeRuns = task.kind === "audio_decision" ? countRunViolations(trials, "item_type") : 0;
  const pvAdjacency = countAdjacentMatches(trials, "pv") + countAdjacentMatches(trials, "matched_target_pv");
  return (answerRuns + typeRuns) * 1000 + pvAdjacency;
}

function pseudoRandomizeMainTrials(mainTrials, task, seed) {
  if (mainTrials.length < 2) {
    return { trials: mainTrials.slice(), attempt: 0, constraintsMet: true, score: 0 };
  }

  let best = null;
  for (let attempt = 0; attempt < 400; attempt += 1) {
    const candidate = shuffleDeterministic(mainTrials, `${seed}:attempt:${attempt}`);
    const score = randomizationScore(candidate, task);
    const result = { trials: candidate, attempt, constraintsMet: score === 0, score };
    if (!best || result.score < best.score) {
      best = result;
    }
    if (result.constraintsMet) {
      return result;
    }
  }
  return best;
}

function withPlanMetadata(trials, phase, startOrder) {
  return trials.map((trial, index) => ({
    ...trial,
    phase,
    phase_order: index + 1,
    display_order: startOrder + index,
    original_trial_order: trial.trial_order || "",
    randomized_phase: phase === "practice" ? "fixed_practice" : "pseudo_randomized",
  }));
}

function normalizeParticipantId(value) {
  return String(value || "").trim().replace(/\s+/g, "_").replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 40);
}

function createParticipantId() {
  return `PVLJT-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
}

function randomizationSeed() {
  const id = normalizeParticipantId(state.participantId) || "anonymous";
  return `${APP_VERSION}:${state.taskKey}:${state.voice}:${id}`;
}

function buildTrialPlan(rawTrials) {
  const task = TASKS[state.taskKey];
  const practice = rawTrials.filter((trial) => trial.phase === "practice");
  const main = rawTrials.filter((trial) => trial.phase !== "practice");
  const seed = randomizationSeed();
  const randomized = pseudoRandomizeMainTrials(main, task, seed);
  const practicePlan = withPlanMetadata(practice, "practice", 1);
  const mainPlan = withPlanMetadata(randomized.trials, "main", practicePlan.length + 1);
  state.randomization = {
    seed,
    attempt: randomized.attempt,
    constraintsMet: randomized.constraintsMet,
    score: randomized.score,
    nPractice: practicePlan.length,
    nMain: mainPlan.length,
  };
  return practicePlan.concat(mainPlan);
}

function audioName(name) {
  return String(name || "").replace(/\.[^.]+$/, ".mp3");
}

function audioPath(trial) {
  const name = audioName(trial.audio_file_name);
  if (trial.phase === "practice") {
    const practiceFolder = TASKS[state.taskKey].practiceAudioFolder || "practice_v1";
    return `audio/raw/elevenlabs/${state.voice}/${practiceFolder}/${name}`;
  }
  if (TASKS[state.taskKey].kind === "audio_decision") {
    return `audio/raw/elevenlabs/${state.voice}/audio_decision_v2/${name}`;
  }
  const folder = TASKS[state.taskKey].audioFolder || "ljt_v5";
  return `audio/raw/elevenlabs/${state.voice}/${folder}/${name}`;
}

function topbar(label = "") {
  return `
    <div class="topbar">
      <div class="brand">
        <h1>PV-LJT</h1>
        <span>Listening test</span>
      </div>
      <span class="pill">${escapeHtml(label)}</span>
    </div>
  `;
}

function renderSetup() {
  const suggested = createParticipantId();
  state.stage = "setup";
  app.innerHTML = `${topbar("Setup")}
    <section class="panel">
      <h2 class="section-title">Start</h2>
      <p class="lead">Enter an ID, choose a voice and task, then begin.</p>
      <div class="grid">
        <div class="field">
          <label for="participantId">Participant ID</label>
          <input id="participantId" type="text" autocomplete="off" value="${escapeHtml(state.participantId || suggested)}">
          <small>No email address is collected.</small>
        </div>
        <fieldset class="segmented">
          <legend>Voice</legend>
          <div class="segmented-row">
            <label><input type="radio" name="voice" value="male"${state.voice === "male" ? " checked" : ""}><span>Male</span></label>
            <label><input type="radio" name="voice" value="female"${state.voice === "female" ? " checked" : ""}><span>Female</span></label>
          </div>
        </fieldset>
        <div class="field">
          <label for="taskKey">Task</label>
          <select id="taskKey">
            ${Object.entries(TASKS).map(([key, task]) => (
              `<option value="${key}"${state.taskKey === key ? " selected" : ""}>${escapeHtml(task.label)}</option>`
            )).join("")}
          </select>
        </div>
      </div>
      <div id="setupError" class="notice error hidden"></div>
      <div class="actions">
        <button id="startButton" class="btn" type="button">Begin</button>
        <a class="btn ghost" href="index.html">Audio review page</a>
      </div>
    </section>`;

  document.getElementById("startButton").addEventListener("click", startSession);
}

async function startSession() {
  const id = normalizeParticipantId(document.getElementById("participantId").value) || createParticipantId();
  const taskKey = document.getElementById("taskKey").value;
  const voice = document.querySelector('input[name="voice"]:checked')?.value || "male";
  const error = document.getElementById("setupError");

  state.participantId = id;
  state.taskKey = taskKey;
  state.voice = voice;
  state.responses = [];
  state.currentIndex = 0;
  state.startedAt = new Date().toISOString();
  state.completedAt = "";

  try {
    const response = await fetch(TASKS[state.taskKey].path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Could not load ${TASKS[state.taskKey].path}`);
    }
    state.rawTrials = parseTsv(await response.text());
    state.trialPlan = buildTrialPlan(state.rawTrials);
    renderInstructions();
  } catch (err) {
    error.textContent = "Task data could not be loaded.";
    error.classList.remove("hidden");
    console.error(err);
  }
}

function renderInstructions() {
  const task = TASKS[state.taskKey];
  const nPractice = state.randomization?.nPractice ?? 0;
  const nMain = state.randomization?.nMain ?? 0;
  app.innerHTML = `${topbar(task.label)}
    <section class="panel">
      <h2 class="section-title">Instructions</h2>
      <p class="lead">Listen to each item and choose your answer.</p>
      <div class="result-grid compact">
        <div class="result-card">
          <span>Practice</span>
          <strong>${nPractice}</strong>
        </div>
        <div class="result-card">
          <span>Main</span>
          <strong>${nMain}</strong>
        </div>
      </div>
      <div class="notice">
        Practice trials come first and show feedback. The main task begins after practice.
      </div>
      <div class="notice muted">
        Audio starts automatically when each trial opens. If it does not start, press play.
      </div>
      <div class="actions">
        <button id="continueButton" class="btn" type="button">Start practice</button>
        <button id="backButton" class="btn ghost" type="button">Back</button>
      </div>
    </section>`;
  document.getElementById("continueButton").addEventListener("click", () => renderTrial());
  document.getElementById("backButton").addEventListener("click", renderSetup);
}

function currentTrial() {
  return state.trialPlan[state.currentIndex];
}

function currentTask() {
  return TASKS[state.taskKey];
}

function phaseLabel(trial) {
  return trial.phase === "practice" ? "Practice" : "Main";
}

function renderTrial() {
  const trial = currentTrial();
  const task = currentTask();
  if (!trial) {
    renderResults();
    return;
  }

  const total = state.trialPlan.length;
  const progress = total ? (state.currentIndex / total) * 100 : 0;
  state.stage = "trial";
  state.active = {
    trialStartedAt: new Date().toISOString(),
    startedPerf: performance.now(),
    audioStartedAt: "",
    audioEndedAt: "",
    audioEndedPerf: null,
    playbackCount: 0,
    response: "",
  };

  app.innerHTML = `
    <section class="trial-shell">
      ${topbar(task.label)}
      <div class="trial-panel">
        <div class="trial-head">
          <span>${escapeHtml(phaseLabel(trial))}</span>
          <span>Trial ${state.currentIndex + 1} of ${total}</span>
        </div>
        <div class="progress-track" aria-hidden="true">
          <div class="progress-bar" style="width:${progress}%"></div>
        </div>
        <div class="audio-card">
          <strong>${escapeHtml(task.prompt)}</strong>
          <audio id="audioPlayer" class="audio-hidden" preload="auto" playsinline autoplay src="${escapeHtml(audioPath(trial))}"></audio>
          <div id="audioCard" class="audio-presenter" data-audio-state="loading" aria-live="polite">
            <div class="audio-symbol" aria-hidden="true"></div>
            <div class="audio-copy">
              <span class="audio-kicker">Audio</span>
              <div id="status" class="status">Starting audio. Answer after it finishes.</div>
              <div class="audio-indicator" aria-hidden="true"><span></span></div>
            </div>
            <button id="replayButton" class="btn secondary audio-action" type="button" disabled>Replay</button>
          </div>
        </div>
        <div id="responses" class="response-grid">
          ${task.responses.map((option) => (
            `<button class="btn ${option.className}" type="button" data-response="${option.value}" disabled>${escapeHtml(option.label)}</button>`
          )).join("")}
        </div>
        <div id="feedback" class="feedback"></div>
        <div class="actions">
          <button id="nextButton" class="btn" type="button" disabled>${state.currentIndex === total - 1 ? "Finish" : "Next"}</button>
        </div>
      </div>
    </section>`;

  const audio = document.getElementById("audioPlayer");
  audio.addEventListener("play", () => {
    state.active.playbackCount += 1;
    if (!state.active.audioStartedAt) {
      state.active.audioStartedAt = new Date().toISOString();
    }
    setAudioUi("playing", "Audio is playing. Answer after it finishes.");
  });
  audio.addEventListener("ended", () => enableResponses());
  audio.addEventListener("error", () => {
    setAudioUi("blocked", "Audio could not be played. Try reloading the page.");
  });
  document.querySelectorAll("[data-response]").forEach((button) => {
    button.addEventListener("click", () => commitResponse(button.dataset.response));
  });
  document.getElementById("nextButton").addEventListener("click", nextTrial);
  document.getElementById("replayButton").addEventListener("click", replayAudio);
  startAudio(audio);
}

function startAudio(audio) {
  setAudioUi("loading", "Starting audio. Answer after it finishes.");
  const playPromise = audio.play();
  if (playPromise && typeof playPromise.catch === "function") {
    playPromise.catch(() => {
      setAudioUi("blocked", "Press play to begin. The answer buttons unlock after the audio finishes.");
    });
  }
}

function setAudioUi(stateName, message) {
  const card = document.getElementById("audioCard");
  const status = document.getElementById("status");
  const replay = document.getElementById("replayButton");
  if (card) {
    card.dataset.audioState = stateName;
  }
  if (status) {
    status.textContent = message;
  }
  if (replay && !state.active?.response) {
    replay.disabled = !(stateName === "ready" || stateName === "blocked");
    replay.textContent = stateName === "blocked" ? "Play audio" : "Replay";
  }
}

function disableResponses() {
  document.querySelectorAll("[data-response]").forEach((button) => {
    button.disabled = true;
  });
}

function replayAudio() {
  if (!state.active || state.active.response) {
    return;
  }
  const audio = document.getElementById("audioPlayer");
  if (!audio) {
    return;
  }
  state.active.audioEndedAt = "";
  state.active.audioEndedPerf = null;
  disableResponses();
  audio.currentTime = 0;
  startAudio(audio);
}

function enableResponses() {
  if (!state.active || state.active.response) {
    return;
  }
  const status = document.getElementById("status");
  if (!status) {
    return;
  }
  state.active.audioEndedAt = new Date().toISOString();
  state.active.audioEndedPerf = performance.now();
  setAudioUi("ready", "Choose your answer.");
  document.querySelectorAll("[data-response]").forEach((button) => {
    button.disabled = false;
  });
}

function commitResponse(responseValue) {
  if (!state.active || state.active.response) {
    return;
  }
  const trial = currentTrial();
  const task = currentTask();
  const expected = trial[task.responseField] || "";
  const responseAt = new Date().toISOString();
  const now = performance.now();
  const rt = state.active.audioEndedPerf ? Math.round(now - state.active.audioEndedPerf) : "";
  const correct = responseValue === expected;

  state.active.response = responseValue;
  document.querySelectorAll("[data-response]").forEach((button) => {
    button.disabled = true;
    if (button.dataset.response === responseValue) {
      button.classList.add("selected");
    }
  });
  const replay = document.getElementById("replayButton");
  if (replay) {
    replay.disabled = true;
  }

  state.responses.push({
    participant_id: state.participantId,
    task_key: state.taskKey,
    task_label: task.label,
    voice: state.voice,
    randomization_seed: state.randomization.seed,
    display_order: trial.display_order || state.currentIndex + 1,
    phase_order: trial.phase_order || "",
    original_trial_order: trial.original_trial_order || "",
    randomized_phase: trial.randomized_phase || "",
    phase: trial.phase,
    item_id: trial.item_id || trial.trial_id || "",
    trial_id: trial.trial_id || "",
    pv: trial.pv || trial.matched_target_pv || "",
    item_type: trial.item_type || trial.condition || "",
    response: responseValue,
    response_correct: String(correct),
    trial_started_at: state.active.trialStartedAt,
    audio_started_at: state.active.audioStartedAt,
    audio_ended_at: state.active.audioEndedAt,
    response_at: responseAt,
    response_rt_ms: rt,
    playback_count: state.active.playbackCount,
  });

  if (trial.phase === "practice") {
    const feedback = document.getElementById("feedback");
    feedback.textContent = correct ? "Correct" : "Incorrect";
    feedback.className = `feedback ${correct ? "good" : "bad"}`;
  }
  document.getElementById("status").textContent = "Response recorded.";
  document.getElementById("nextButton").disabled = false;
}

function nextTrial() {
  const previous = currentTrial();
  state.currentIndex += 1;
  if (state.currentIndex >= state.trialPlan.length) {
    state.completedAt = new Date().toISOString();
    renderResults();
    return;
  }
  const next = currentTrial();
  if (previous?.phase === "practice" && next?.phase === "main") {
    renderPracticeComplete();
    return;
  }
  renderTrial();
}

function practiceRows() {
  return state.responses.filter((row) => row.phase === "practice");
}

function practiceSummary() {
  const rows = practiceRows();
  const correct = rows.filter((row) => row.response_correct === "true").length;
  const total = rows.length;
  return {
    correct,
    total,
    accuracy: total ? correct / total : 0,
  };
}

function mainRows() {
  return state.responses.filter((row) => row.phase === "main");
}

function scoreSummary() {
  const rows = mainRows();
  const correct = rows.filter((row) => row.response_correct === "true").length;
  const total = rows.length;
  return {
    correct,
    total,
    accuracy: total ? correct / total : 0,
  };
}

function renderPracticeComplete() {
  const summary = practiceSummary();
  const percent = `${Math.round(summary.accuracy * 100)}%`;
  app.innerHTML = `${topbar(currentTask().label)}
    <section class="panel">
      <h2 class="section-title">Practice complete</h2>
      <p class="lead">The main task starts next. Feedback will no longer be shown.</p>
      <div class="result-grid compact">
        <div class="result-card">
          <span>Practice score</span>
          <strong>${summary.correct} / ${summary.total}</strong>
        </div>
        <div class="result-card">
          <span>Accuracy</span>
          <strong>${percent}</strong>
        </div>
      </div>
      <div class="notice muted">
        Audio will continue to start automatically. Answer after each audio item finishes.
      </div>
      <div class="actions">
        <button id="startMainButton" class="btn" type="button">Start main task</button>
      </div>
    </section>`;
  document.getElementById("startMainButton").addEventListener("click", renderTrial);
}

function renderResults() {
  const summary = scoreSummary();
  const percent = `${Math.round(summary.accuracy * 100)}%`;
  app.innerHTML = `${topbar("Complete")}
    <section class="panel">
      <h2 class="section-title">Complete</h2>
      <p class="lead">Your responses have been recorded in this browser.</p>
      <div class="result-grid">
        <div class="result-card">
          <span>Score</span>
          <strong>${summary.correct} / ${summary.total}</strong>
        </div>
        <div class="result-card">
          <span>Accuracy</span>
          <strong>${percent}</strong>
        </div>
      </div>
      <div class="notice success">Download the result file before closing this page.</div>
      <div class="actions">
        <button id="downloadCsv" class="btn" type="button">Download CSV</button>
        <button id="downloadJson" class="btn secondary" type="button">Download JSON</button>
        <button id="newSession" class="btn ghost" type="button">New session</button>
      </div>
    </section>`;
  document.getElementById("downloadCsv").addEventListener("click", downloadCsv);
  document.getElementById("downloadJson").addEventListener("click", downloadJson);
  document.getElementById("newSession").addEventListener("click", () => {
    state.currentIndex = 0;
    state.responses = [];
    state.startedAt = "";
    state.completedAt = "";
    renderSetup();
  });
  setTimeout(downloadCsv, 300);
}

function csvCell(value) {
  const text = String(value ?? "");
  if (/[",\n\r]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

function resultRows() {
  const summary = scoreSummary();
  return state.responses.map((row) => ({
    ...row,
    session_started_at: state.startedAt,
    session_completed_at: state.completedAt,
    raw_score: summary.correct,
    n_main_trials: summary.total,
    accuracy: summary.total ? summary.accuracy.toFixed(4) : "",
    randomization_attempt: state.randomization?.attempt ?? "",
    randomization_constraints_met: state.randomization?.constraintsMet ?? "",
    randomization_score: state.randomization?.score ?? "",
    app_version: APP_VERSION,
  }));
}

function downloadCsv() {
  const rows = resultRows();
  if (!rows.length) {
    return;
  }
  const headers = Object.keys(rows[0]);
  const csv = [headers.join(","), ...rows.map((row) => headers.map((header) => csvCell(row[header])).join(","))].join("\n");
  downloadText(`${fileBase()}_trials.csv`, `\ufeff${csv}`, "text/csv;charset=utf-8");
}

function downloadJson() {
  const payload = {
    participant_id: state.participantId,
    task_key: state.taskKey,
    task_label: currentTask().label,
    voice: state.voice,
    started_at: state.startedAt,
    completed_at: state.completedAt,
    randomization: state.randomization,
    summary: scoreSummary(),
    rows: resultRows(),
    app_version: APP_VERSION,
  };
  downloadText(`${fileBase()}_session.json`, JSON.stringify(payload, null, 2), "application/json;charset=utf-8");
}

function fileBase() {
  const id = normalizeParticipantId(state.participantId) || "participant";
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z");
  return `PV-LJT_${id}_${state.voice}_${state.taskKey}_${stamp}`;
}

function downloadText(fileName, text, mime) {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
}

renderSetup();
