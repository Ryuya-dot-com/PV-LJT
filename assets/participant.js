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
const DEFAULTS = {
  seed: "PV-LJT-20260703",
  keymap: "counterbalanced",
  maxAnswerRun: 2,
  sameWordGap: 8,
  postResponseMs: 700,
  practiceFeedbackMs: 1400,
};

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
  responseMapping: null,
  active: null,
  advanceTimer: null,
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

function mulberry32(seed) {
  return function rng() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, rng) {
  const arr = values.slice();
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function maxObservedRun(items, field) {
  let maxRun = 0;
  let run = 0;
  let previous = "";
  items.forEach((item) => {
    const value = String(item[field] || "");
    if (value && value === previous) {
      run += 1;
    } else {
      run = 1;
      previous = value;
    }
    maxRun = Math.max(maxRun, run);
  });
  return maxRun;
}

function orderWord(item) {
  return String(item.pv || item.matched_target_pv || item.stimulus_text || item.trial_id || item.item_id || "")
    .trim()
    .toLowerCase();
}

function countSameWordGapViolations(items, gap) {
  let violations = 0;
  const lastSeen = new Map();
  items.forEach((item, index) => {
    const word = orderWord(item);
    if (!word) {
      return;
    }
    if (lastSeen.has(word) && index - lastSeen.get(word) <= gap) {
      violations += 1;
    }
    lastSeen.set(word, index);
  });
  return violations;
}

function randomAnswerPattern(countsByAnswer, rng, maxRun) {
  const counts = { ...countsByAnswer };
  const answers = Object.keys(counts);
  const total = answers.reduce((sum, answer) => sum + counts[answer], 0);
  const pattern = [];
  let last = "";
  let run = 0;

  for (let slot = 0; slot < total; slot += 1) {
    const choices = answers.filter((answer) => {
      if (counts[answer] <= 0) {
        return false;
      }
      return !(answer === last && run >= maxRun);
    });
    if (!choices.length) {
      return null;
    }

    const totalWeight = choices.reduce((sum, answer) => sum + counts[answer], 0);
    let pick = rng() * totalWeight;
    let chosen = choices[choices.length - 1];
    for (const answer of choices) {
      pick -= counts[answer];
      if (pick <= 0) {
        chosen = answer;
        break;
      }
    }

    pattern.push(chosen);
    counts[chosen] -= 1;
    if (chosen === last) {
      run += 1;
    } else {
      last = chosen;
      run = 1;
    }
  }

  return pattern;
}

function diagnoseOrder(items, task, maxRun, gap, attempts) {
  const observedRun = maxObservedRun(items, task.balanceField);
  const sameWordGapViolations = countSameWordGapViolations(items, gap);
  const score = Math.max(0, observedRun - maxRun) * 100 + sameWordGapViolations * 10;
  return {
    maxObservedRun: observedRun,
    sameWordGapViolations,
    attempts,
    score,
  };
}

function buildConstrainedOrder(items, task, seed, maxRun, requestedGap) {
  if (items.length < 2) {
    return {
      items: items.slice(),
      diagnostics: {
        maxObservedRun: items.length,
        sameWordGapViolations: 0,
        attempts: 0,
        score: 0,
        sameWordGapRequested: requestedGap,
        sameWordGapUsed: requestedGap,
        status: "trivial_order",
      },
    };
  }

  const rng = mulberry32(hashString(seed));
  const grouped = new Map();
  items.forEach((item, index) => {
    const answer = String(item[task.balanceField] || "");
    if (!grouped.has(answer)) {
      grouped.set(answer, []);
    }
    grouped.get(answer).push({ ...item, order_uid: `${item.item_id || item.trial_id || "item"}_${index}` });
  });

  const countsByAnswer = Object.fromEntries([...grouped.entries()].map(([answer, group]) => [answer, group.length]));
  let best = null;
  for (let gap = requestedGap; gap >= 0; gap -= 1) {
    for (let attempt = 1; attempt <= 3000; attempt += 1) {
      const pattern = randomAnswerPattern(countsByAnswer, rng, maxRun);
      if (!pattern) {
        continue;
      }

      const shuffledByAnswer = new Map([...grouped.entries()].map(([answer, group]) => [answer, shuffle(group, rng)]));
      const cursor = Object.fromEntries([...grouped.keys()].map((answer) => [answer, 0]));
      const candidate = pattern.map((answer) => {
        const item = shuffledByAnswer.get(answer)[cursor[answer]];
        cursor[answer] += 1;
        return item;
      });
      const diagnostics = diagnoseOrder(candidate, task, maxRun, gap, attempt);
      if (diagnostics.maxObservedRun <= maxRun && diagnostics.sameWordGapViolations === 0) {
        return {
          items: candidate,
          diagnostics: {
            ...diagnostics,
            sameWordGapRequested: requestedGap,
            sameWordGapUsed: gap,
            status: gap === requestedGap ? "requested_constraints_satisfied" : "gap_relaxed",
          },
        };
      }
      if (!best || diagnostics.score < best.diagnostics.score) {
        best = { items: candidate, diagnostics: { ...diagnostics, sameWordGapUsed: gap } };
      }
    }
  }

  if (!best) {
    const fallback = shuffle(items, rng);
    best = {
      items: fallback,
      diagnostics: {
        ...diagnoseOrder(fallback, task, maxRun, 0, 0),
        sameWordGapUsed: 0,
      },
    };
  }
  best.diagnostics.sameWordGapRequested = requestedGap;
  best.diagnostics.status = "fallback_best_available";
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
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "_")
    .replace(/[^a-z0-9_-]/g, "")
    .slice(0, 40);
}

function createParticipantId() {
  return `PVLJT-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
}

function randomizationSeed() {
  const id = normalizeParticipantId(state.participantId) || "anonymous";
  return `${DEFAULTS.seed}|${id}|${state.taskKey}|${state.voice}|${APP_VERSION}`;
}

function makeResponseMapping(task, participantId, seed) {
  const [left, right] = task.responses.map((option) => option.value);
  let fLeft = true;
  if (DEFAULTS.keymap === "counterbalanced") {
    fLeft = hashString(`${seed}|${participantId}|keymap`) % 2 === 0;
  }
  const mapping = fLeft
    ? { F: left, J: right, keymapId: `F_${left}_J_${right}` }
    : { F: right, J: left, keymapId: `F_${right}_J_${left}` };
  mapping[left] = fLeft ? "F" : "J";
  mapping[right] = fLeft ? "J" : "F";
  return mapping;
}

function buildTrialPlan(rawTrials) {
  const task = TASKS[state.taskKey];
  const practice = rawTrials.filter((trial) => trial.phase === "practice");
  const main = rawTrials.filter((trial) => trial.phase !== "practice");
  const seed = randomizationSeed();
  const randomized = buildConstrainedOrder(main, task, seed, DEFAULTS.maxAnswerRun, DEFAULTS.sameWordGap);
  const practicePlan = withPlanMetadata(practice, "practice", 1);
  const mainPlan = withPlanMetadata(randomized.items, "main", practicePlan.length + 1);
  state.randomization = {
    seed,
    ...randomized.diagnostics,
    maxAnswerRun: DEFAULTS.maxAnswerRun,
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
  state.advanceTimer = null;

  try {
    const response = await fetch(TASKS[state.taskKey].path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Could not load ${TASKS[state.taskKey].path}`);
    }
    state.rawTrials = parseTsv(await response.text());
    state.responseMapping = makeResponseMapping(TASKS[state.taskKey], state.participantId, DEFAULTS.seed);
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
        Audio starts automatically when each trial opens. Use the F/J keys or the matching buttons after the audio ends.
      </div>
      <table class="summary-table">
        ${responseKeyRowsMarkup()}
      </table>
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

function responseOption(value) {
  return currentTask().responses.find((option) => option.value === value) || currentTask().responses[0];
}

function responseKeyRowsMarkup() {
  return ["F", "J"].map((key) => {
    const value = state.responseMapping?.[key] || currentTask().responses[key === "F" ? 0 : 1].value;
    const option = responseOption(value);
    return `<tr><th>${escapeHtml(key)}</th><td>${escapeHtml(option.label)}</td></tr>`;
  }).join("");
}

function responseButtonsMarkup() {
  return ["F", "J"].map((key) => {
    const value = state.responseMapping?.[key] || currentTask().responses[key === "F" ? 0 : 1].value;
    const option = responseOption(value);
    return `
      <button class="btn ${option.className}" type="button" data-response="${escapeHtml(value)}" disabled>
        <span class="key">${escapeHtml(key)}</span>${escapeHtml(option.label)}
      </button>
    `;
  }).join("");
}

function renderTrial() {
  if (state.advanceTimer) {
    window.clearTimeout(state.advanceTimer);
    state.advanceTimer = null;
  }
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
          ${responseButtonsMarkup()}
        </div>
        <div id="feedback" class="feedback"></div>
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
    button.addEventListener("click", () => commitResponse(button.dataset.response, "button"));
  });
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

function commitResponse(responseValue, responseModality = "button") {
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
  const responseKey = state.responseMapping?.[responseValue] || "";

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
    response_key: responseKey,
    response_modality: responseModality,
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
  state.advanceTimer = window.setTimeout(
    nextTrial,
    trial.phase === "practice" ? DEFAULTS.practiceFeedbackMs : DEFAULTS.postResponseMs
  );
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
      <table class="summary-table">
        ${responseKeyRowsMarkup()}
      </table>
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
    if (state.advanceTimer) {
      window.clearTimeout(state.advanceTimer);
      state.advanceTimer = null;
    }
    state.currentIndex = 0;
    state.responses = [];
    state.startedAt = "";
    state.completedAt = "";
    state.responseMapping = null;
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
    randomization_attempt: state.randomization?.attempts ?? "",
    randomization_constraints_met: state.randomization
      ? String(state.randomization.maxObservedRun <= state.randomization.maxAnswerRun && state.randomization.sameWordGapViolations === 0)
      : "",
    randomization_score: state.randomization?.score ?? "",
    keymap_id: state.responseMapping?.keymapId ?? "",
    order_status: state.randomization?.status ?? "",
    order_max_answer_run: state.randomization?.maxObservedRun ?? "",
    order_same_word_gap_requested: state.randomization?.sameWordGapRequested ?? "",
    order_same_word_gap_used: state.randomization?.sameWordGapUsed ?? "",
    order_same_word_gap_violations: state.randomization?.sameWordGapViolations ?? "",
    order_attempts: state.randomization?.attempts ?? "",
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
    response_mapping: state.responseMapping,
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

function responseIsOpen() {
  if (!state.active || state.active.response) {
    return false;
  }
  return [...document.querySelectorAll("[data-response]")].some((button) => !button.disabled);
}

function handleKeydown(event) {
  const key = event.key.toLowerCase();
  if (key === "f" || key === "j") {
    if (!responseIsOpen()) {
      return;
    }
    event.preventDefault();
    const response = state.responseMapping?.[key.toUpperCase()];
    if (response) {
      commitResponse(response, "keyboard");
    }
  } else if (key === " " || key === "enter") {
    const replay = document.getElementById("replayButton");
    if (replay && !replay.disabled && !state.active?.response) {
      event.preventDefault();
      replayAudio();
    }
  }
}

window.addEventListener("keydown", handleKeydown);

renderSetup();
