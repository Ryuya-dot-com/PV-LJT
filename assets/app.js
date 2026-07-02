const TASKS = {
  ljt_a: {
    label: "Aural PV-LJT List A",
    path: "materials/pilot_trial_file_ljt_list_A_v1.tsv",
    kind: "ljt",
    promptTitle: "Acceptable or unacceptable?",
    promptCopy: "Judge the sentence meaning from the audio.",
    responseField: "expected_response",
    balanceField: "expected_response",
    responses: [
      { value: "acceptable", label: "Acceptable" },
      { value: "unacceptable", label: "Unacceptable" },
    ],
  },
  ljt_b: {
    label: "Aural PV-LJT List B",
    path: "materials/pilot_trial_file_ljt_list_B_v1.tsv",
    kind: "ljt",
    promptTitle: "Acceptable or unacceptable?",
    promptCopy: "Judge the sentence meaning from the audio.",
    responseField: "expected_response",
    balanceField: "expected_response",
    responses: [
      { value: "acceptable", label: "Acceptable" },
      { value: "unacceptable", label: "Unacceptable" },
    ],
  },
  audio_decision: {
    label: "Audio PV decision",
    path: "materials/pilot_trial_file_audio_decision_v1.tsv",
    kind: "audio_decision",
    promptTitle: "Common English phrasal verb?",
    promptCopy: "Judge the two-word audio stimulus.",
    responseField: "correct_response",
    balanceField: "correct_response",
    responses: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
    ],
  },
};

const STORAGE_VERSION = "v2";
const MAX_RUN_LENGTH = 3;

const state = {
  taskKey: "ljt_a",
  voice: "male",
  reviewerId: "",
  rawTrials: [],
  trialPlan: [],
  currentIndex: 0,
  responses: {},
  randomization: null,
  browserSeed: "",
};

const els = {
  reviewerId: document.getElementById("reviewerId"),
  taskSelect: document.getElementById("taskSelect"),
  showText: document.getElementById("showText"),
  taskLabel: document.getElementById("taskLabel"),
  progressText: document.getElementById("progressText"),
  progressBar: document.getElementById("progressBar"),
  voiceLabel: document.getElementById("voiceLabel"),
  sidePhaseLabel: document.getElementById("sidePhaseLabel"),
  orderStatus: document.getElementById("orderStatus"),
  seedLabel: document.getElementById("seedLabel"),
  phaseLabel: document.getElementById("phaseLabel"),
  trialCounter: document.getElementById("trialCounter"),
  audioPlayer: document.getElementById("audioPlayer"),
  replayButton: document.getElementById("replayButton"),
  promptTitle: document.getElementById("promptTitle"),
  promptCopy: document.getElementById("promptCopy"),
  responseButtons: document.getElementById("responseButtons"),
  textReveal: document.getElementById("textReveal"),
  stimulusText: document.getElementById("stimulusText"),
  easeSlider: document.getElementById("easeSlider"),
  easeValue: document.getElementById("easeValue"),
  naturalnessSlider: document.getElementById("naturalnessSlider"),
  naturalnessValue: document.getElementById("naturalnessValue"),
  commentBox: document.getElementById("commentBox"),
  backButton: document.getElementById("backButton"),
  nextButton: document.getElementById("nextButton"),
  exportButton: document.getElementById("exportButton"),
  exportStatus: document.getElementById("exportStatus"),
  resetButton: document.getElementById("resetButton"),
  saveStatus: document.getElementById("saveStatus"),
};

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

function browserSeed() {
  const key = "pv-ljt-browser-seed";
  let value = localStorage.getItem(key);
  if (!value) {
    value = `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
    localStorage.setItem(key, value);
  }
  return value;
}

function seedInfo() {
  const reviewer = state.reviewerId.trim();
  if (reviewer) {
    return {
      basis: "reviewer_id",
      seed: `reviewer:${reviewer}`,
      shortLabel: reviewer,
    };
  }
  return {
    basis: "browser_fallback",
    seed: `browser:${state.browserSeed}`,
    shortLabel: "browser fallback",
  };
}

function mainRandomizationSeed() {
  const info = seedInfo();
  return `pv-ljt:${STORAGE_VERSION}:${state.taskKey}:${state.voice}:${info.seed}`;
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

function hardViolationCount(trials, task) {
  const runViolations = countRunViolations(trials, task.balanceField);
  const itemTypeRuns = task.kind === "audio_decision" ? countRunViolations(trials, "item_type") : 0;
  return runViolations + itemTypeRuns;
}

function randomizationScore(trials, task) {
  const hardViolations = hardViolationCount(trials, task);
  const pvAdjacency = countAdjacentMatches(trials, "pv") + countAdjacentMatches(trials, "matched_target_pv");
  return hardViolations * 1000 + pvAdjacency;
}

function balancedGreedyPlan(mainTrials, task, seed) {
  const groups = new Map();
  mainTrials.forEach((trial) => {
    const value = String(trial[task.balanceField] || "unclassified");
    if (!groups.has(value)) {
      groups.set(value, []);
    }
    groups.get(value).push(trial);
  });
  groups.forEach((items, value) => {
    groups.set(value, shuffleDeterministic(items, `${seed}:greedy:${value}`));
  });

  const out = [];
  let previous = "";
  let run = 0;
  while (out.length < mainTrials.length) {
    let candidates = Array.from(groups.keys()).filter((value) => {
      const items = groups.get(value);
      if (!items || items.length === 0) return false;
      return !(value === previous && run >= MAX_RUN_LENGTH);
    });
    if (!candidates.length) {
      return null;
    }

    const maxRemaining = Math.max(...candidates.map((value) => groups.get(value).length));
    candidates = candidates.filter((value) => groups.get(value).length >= maxRemaining - 1);
    const chosenIndex = Math.floor(
      seededUnit(`${seed}:greedy:pick:${out.length}`) * candidates.length,
    );
    const chosen = candidates[chosenIndex];
    out.push(groups.get(chosen).shift());
    if (chosen === previous) {
      run += 1;
    } else {
      previous = chosen;
      run = 1;
    }
  }
  return out;
}

function pseudoRandomizeMainTrials(mainTrials, task, seed) {
  if (mainTrials.length < 2) {
    return {
      trials: mainTrials.slice(),
      attempt: 0,
      constraintsMet: true,
      score: 0,
    };
  }

  let best = null;
  for (let attempt = 0; attempt < 400; attempt += 1) {
    const candidate = shuffleDeterministic(mainTrials, `${seed}:attempt:${attempt}`);
    const score = randomizationScore(candidate, task);
    const hardViolations = hardViolationCount(candidate, task);
    if (!best || score < best.score) {
      best = {
        trials: candidate,
        attempt,
        constraintsMet: hardViolations === 0,
        hardViolations,
        score,
      };
    }
    if (hardViolations === 0) {
      return best;
    }
  }

  const greedy = balancedGreedyPlan(mainTrials, task, seed);
  if (greedy) {
    const score = randomizationScore(greedy, task);
    const hardViolations = hardViolationCount(greedy, task);
    if (!best || score < best.score) {
      best = {
        trials: greedy,
        attempt: "greedy",
        constraintsMet: hardViolations === 0,
        hardViolations,
        score,
      };
    }
  }
  return best;
}

function withPlanMetadata(trials, phase, startOrder) {
  return trials.map((trial, index) => ({
    ...trial,
    display_order: startOrder + index,
    phase_order: index + 1,
    original_trial_order: trial.trial_order || "",
    randomized_phase: phase === "main" ? "pseudo_randomized" : "fixed_practice",
  }));
}

function buildTrialPlan(rawTrials) {
  const task = TASKS[state.taskKey];
  const practice = rawTrials.filter((trial) => trial.phase === "practice");
  const main = rawTrials.filter((trial) => trial.phase !== "practice");
  const seed = mainRandomizationSeed();
  const randomized = pseudoRandomizeMainTrials(main, task, seed);
  const practicePlan = withPlanMetadata(practice, "practice", 1);
  const mainPlan = withPlanMetadata(randomized.trials, "main", practicePlan.length + 1);

  state.randomization = {
    seed,
    seedBasis: seedInfo().basis,
    attempt: randomized.attempt,
    constraintsMet: randomized.constraintsMet,
    hardViolations: randomized.hardViolations,
    score: randomized.score,
    nPractice: practicePlan.length,
    nMain: mainPlan.length,
  };
  return practicePlan.concat(mainPlan);
}

function audioName(name) {
  return name.replace(/\.[^.]+$/, ".mp3");
}

function audioPath(trial) {
  const name = audioName(trial.audio_file_name);
  const voice = state.voice;
  if (trial.phase === "practice") {
    return `audio/raw/elevenlabs/${voice}/practice_v1/${name}`;
  }
  if (TASKS[state.taskKey].kind === "audio_decision") {
    return `audio/raw/elevenlabs/${voice}/audio_decision_v2/${name}`;
  }
  return `audio/raw/elevenlabs/${voice}/ljt_v4/${name}`;
}

function trialId(trial) {
  return trial.item_id || trial.trial_id || `trial_${trial.display_order}`;
}

function trialKey(index = state.currentIndex) {
  const trial = state.trialPlan[index];
  return `${state.taskKey}:${state.voice}:${seedInfo().seed}:${trialId(trial)}`;
}

function storageKey() {
  return `pv-ljt-review:${STORAGE_VERSION}:${state.taskKey}:${state.voice}:${seedInfo().seed}`;
}

function blankResponse() {
  return {
    response: "",
    responseAt: "",
    responseRtMs: "",
    trialStartedAt: "",
    playbackCount: 0,
    easeRating: "",
    easeTouched: false,
    naturalnessRating: "",
    naturalnessTouched: false,
    flags: [],
    comment: "",
    updatedAt: "",
  };
}

function loadSavedSession() {
  const saved = localStorage.getItem(storageKey());
  if (!saved) {
    state.responses = {};
    state.currentIndex = 0;
    return;
  }
  try {
    const parsed = JSON.parse(saved);
    state.responses = parsed.responses || {};
    state.currentIndex = Math.min(parsed.currentIndex || 0, Math.max(0, state.trialPlan.length - 1));
  } catch (error) {
    state.responses = {};
    state.currentIndex = 0;
  }
}

function saveSession() {
  localStorage.setItem(
    storageKey(),
    JSON.stringify({
      reviewerId: state.reviewerId,
      voice: state.voice,
      taskKey: state.taskKey,
      currentIndex: state.currentIndex,
      randomization: state.randomization,
      responses: state.responses,
      savedAt: new Date().toISOString(),
    }),
  );
  els.saveStatus.textContent = "Saved";
  window.setTimeout(() => {
    els.saveStatus.textContent = "Ready";
  }, 900);
}

function currentResponse() {
  const key = trialKey();
  if (!state.responses[key]) {
    state.responses[key] = blankResponse();
  }
  return state.responses[key];
}

function ensureTrialStarted() {
  const saved = currentResponse();
  if (!saved.trialStartedAt) {
    saved.trialStartedAt = new Date().toISOString();
    saved.trialStartedAtMs = performance.now();
    saveSession();
  }
}

async function loadTask() {
  const task = TASKS[state.taskKey];
  const response = await fetch(task.path);
  if (!response.ok) {
    throw new Error(`Could not load ${task.path}`);
  }
  state.rawTrials = parseTsv(await response.text());
  state.trialPlan = buildTrialPlan(state.rawTrials);
  loadSavedSession();
  render();
}

function completedCount() {
  return state.trialPlan.filter((_, index) => {
    const saved = state.responses[trialKey(index)];
    return isComplete(saved);
  }).length;
}

function allTrialsComplete(done = completedCount()) {
  return state.trialPlan.length > 0 && done === state.trialPlan.length;
}

function isComplete(saved) {
  return !!(
    saved &&
    saved.response &&
    saved.easeTouched &&
    saved.naturalnessTouched
  );
}

function missingRequirements(saved) {
  const missing = [];
  if (!saved || !saved.response) missing.push("response");
  if (!saved || !saved.easeTouched) missing.push("clarity");
  if (!saved || !saved.naturalnessTouched) missing.push("naturalness");
  return missing;
}

function ratingLabel(value, touched) {
  return touched ? `${value} / 6` : "Not rated";
}

function setSlider(slider, output, value, touched) {
  slider.value = value || "3";
  slider.classList.toggle("unrated", !touched);
  output.textContent = ratingLabel(slider.value, touched);
}

function renderResponseButtons() {
  const task = TASKS[state.taskKey];
  const saved = currentResponse();
  els.responseButtons.innerHTML = "";
  task.responses.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = option.label;
    button.className = saved.response === option.value ? "selected" : "";
    button.addEventListener("click", () => {
      const now = performance.now();
      saved.response = option.value;
      saved.responseAt = new Date().toISOString();
      const started = Number(saved.trialStartedAtMs || now);
      saved.responseRtMs = String(Math.max(0, Math.round(now - started)));
      saved.updatedAt = new Date().toISOString();
      saveSession();
      render();
    });
    els.responseButtons.append(button);
  });
}

function renderReviewFields() {
  const saved = currentResponse();
  setSlider(els.easeSlider, els.easeValue, saved.easeRating, saved.easeTouched);
  setSlider(
    els.naturalnessSlider,
    els.naturalnessValue,
    saved.naturalnessRating,
    saved.naturalnessTouched,
  );
  document.querySelectorAll(".quality-grid input").forEach((input) => {
    input.checked = saved.flags.includes(input.value);
  });
  els.commentBox.value = saved.comment;
}

function render() {
  const task = TASKS[state.taskKey];
  const trial = state.trialPlan[state.currentIndex];
  if (!trial) {
    return;
  }
  ensureTrialStarted();
  const saved = currentResponse();
  const done = completedCount();
  const remaining = Math.max(0, state.trialPlan.length - done);
  const canExport = allTrialsComplete(done);
  const phase = trial.phase === "practice" ? "Practice" : "Main";
  const randomization = state.randomization || {};

  els.taskLabel.textContent = task.label;
  els.voiceLabel.textContent = state.voice === "male" ? "Male" : "Female";
  els.sidePhaseLabel.textContent = phase;
  els.orderStatus.textContent = randomization.constraintsMet
    ? (randomization.attempt === "greedy" ? "balanced" : `attempt ${randomization.attempt}`)
    : `best effort (${randomization.score})`;
  els.seedLabel.textContent = seedInfo().shortLabel;
  els.promptTitle.textContent = task.promptTitle;
  els.promptCopy.textContent = task.promptCopy;
  els.phaseLabel.textContent = phase;
  els.trialCounter.textContent = `Trial ${state.currentIndex + 1} of ${state.trialPlan.length}`;
  els.audioPlayer.src = audioPath(trial);
  els.stimulusText.textContent = trial.stimulus_text || "";
  els.textReveal.hidden = !(els.showText.checked && saved.response);

  els.progressText.textContent = `${done} / ${state.trialPlan.length}`;
  els.progressBar.style.width = `${state.trialPlan.length ? (done / state.trialPlan.length) * 100 : 0}%`;
  els.backButton.disabled = state.currentIndex === 0;
  els.nextButton.disabled = !isComplete(saved);
  if (state.currentIndex === state.trialPlan.length - 1) {
    els.nextButton.textContent = canExport ? "Download Excel" : "Finish trial";
  } else {
    els.nextButton.textContent = "Next";
  }
  els.exportButton.disabled = !canExport;
  const missing = missingRequirements(saved);
  if (missing.length) {
    els.exportStatus.textContent = `Needs ${missing.join(", ")}`;
  } else {
    els.exportStatus.textContent = canExport
      ? "All trials complete"
      : `${remaining} trial${remaining === 1 ? "" : "s"} remaining before Excel`;
  }

  renderResponseButtons();
  renderReviewFields();
}

function persistCurrentFields() {
  if (!state.trialPlan.length) {
    return;
  }
  const saved = currentResponse();
  saved.flags = Array.from(document.querySelectorAll(".quality-grid input:checked")).map(
    (input) => input.value,
  );
  saved.comment = els.commentBox.value.trim();
  saved.updatedAt = new Date().toISOString();
  saveSession();
}

function setRating(kind, value) {
  const saved = currentResponse();
  if (kind === "ease") {
    saved.easeRating = value;
    saved.easeTouched = true;
  } else {
    saved.naturalnessRating = value;
    saved.naturalnessTouched = true;
  }
  saved.updatedAt = new Date().toISOString();
  saveSession();
  render();
}

function csvEscape(value) {
  const text = String(value ?? "");
  if (/[",\n\r]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

function buildExportData() {
  const task = TASKS[state.taskKey];
  const exportedAt = new Date().toISOString();
  const randomization = state.randomization || {};
  const responseHeaders = [
    "reviewer_id",
    "exported_at",
    "task",
    "voice",
    "randomization_seed",
    "randomization_seed_basis",
    "randomization_attempt",
    "randomization_constraints_met",
    "randomization_hard_violations",
    "randomization_score",
    "display_order",
    "phase_order",
    "original_trial_order",
    "phase",
    "item_id",
    "trial_id",
    "pv",
    "item_type",
    "response",
    "expected_response",
    "response_correct",
    "trial_started_at",
    "response_at",
    "response_rt_ms",
    "playback_count",
    "ease_of_listening_1_6",
    "naturalness_of_english_1_6",
    "quality_flags",
    "comment",
    "audio_file",
    "stimulus_text",
  ];
  const responseRows = state.trialPlan.map((trial, index) => {
    const saved = state.responses[trialKey(index)] || blankResponse();
    const expected = trial[task.responseField] || "";
    const correct = saved.response ? String(saved.response === expected) : "";
    return [
      state.reviewerId,
      exportedAt,
      task.label,
      state.voice,
      randomization.seed || "",
      randomization.seedBasis || "",
      randomization.attempt ?? "",
      randomization.constraintsMet ?? "",
      randomization.hardViolations ?? "",
      randomization.score ?? "",
      trial.display_order || index + 1,
      trial.phase_order || "",
      trial.original_trial_order || "",
      trial.phase,
      trial.item_id || "",
      trial.trial_id || "",
      trial.pv || trial.matched_target_pv || "",
      trial.item_type || "",
      saved.response,
      expected,
      correct,
      saved.trialStartedAt || "",
      saved.responseAt || "",
      saved.responseRtMs || "",
      saved.playbackCount,
      saved.easeTouched ? saved.easeRating : "",
      saved.naturalnessTouched ? saved.naturalnessRating : "",
      saved.flags.join(";"),
      saved.comment,
      audioPath(trial),
      trial.stimulus_text || "",
    ];
  });

  const trialOrderHeaders = [
    "display_order",
    "phase_order",
    "original_trial_order",
    "randomized_phase",
    "phase",
    "item_id",
    "trial_id",
    "pv",
    "matched_target_pv",
    "item_type",
    "expected_response",
    "audio_file",
    "stimulus_text",
  ];
  const trialOrderRows = state.trialPlan.map((trial, index) => [
    trial.display_order || index + 1,
    trial.phase_order || "",
    trial.original_trial_order || "",
    trial.randomized_phase || "",
    trial.phase || "",
    trial.item_id || "",
    trial.trial_id || "",
    trial.pv || "",
    trial.matched_target_pv || "",
    trial.item_type || "",
    trial[task.responseField] || "",
    audioPath(trial),
    trial.stimulus_text || "",
  ]);

  const completed = completedCount();
  const sessionRows = [
    ["field", "value"],
    ["exported_at", exportedAt],
    ["reviewer_id", state.reviewerId],
    ["task_key", state.taskKey],
    ["task_label", task.label],
    ["voice", state.voice],
    ["total_trials", state.trialPlan.length],
    ["completed_trials", completed],
    ["practice_trials", randomization.nPractice ?? ""],
    ["main_trials", randomization.nMain ?? ""],
    ["randomization_seed", randomization.seed || ""],
    ["randomization_seed_basis", randomization.seedBasis || ""],
    ["randomization_attempt", randomization.attempt ?? ""],
    ["randomization_constraints_met", randomization.constraintsMet ?? ""],
    ["randomization_hard_violations", randomization.hardViolations ?? ""],
    ["randomization_score", randomization.score ?? ""],
    ["storage_version", STORAGE_VERSION],
    ["source_url", window.location.href],
  ];

  const codebookRows = [
    ["sheet", "variable", "description"],
    ["Session", "reviewer_id", "Reviewer identifier entered at the top of the page."],
    ["Session", "randomization_seed", "Seed used for deterministic main-trial randomization."],
    ["Responses", "display_order", "Order shown to the reviewer, including fixed practice trials."],
    ["Responses", "response", "Reviewer answer for the task."],
    ["Responses", "expected_response", "Keyed correct or expected answer from the trial file."],
    ["Responses", "response_correct", "TRUE/FALSE string when a response was present."],
    ["Responses", "response_rt_ms", "Milliseconds from trial start to task response click."],
    ["Responses", "playback_count", "Number of audio play events recorded by the browser."],
    ["Responses", "ease_of_listening_1_6", "Listening clarity rating: 1 = hard to hear, 6 = very easy to hear."],
    ["Responses", "naturalness_of_english_1_6", "English naturalness rating: 1 = unnatural, 6 = natural English."],
    ["Responses", "quality_flags", "Optional semicolon-delimited audio issue flags."],
    ["Trial_Order", "randomized_phase", "fixed_practice or pseudo_randomized."],
    ["Trial_Order", "audio_file", "Repo-relative audio path used by the page."],
  ];

  return {
    exportedAt,
    responseHeaders,
    responseRows,
    trialOrderHeaders,
    trialOrderRows,
    sessionRows,
    codebookRows,
  };
}

function ensureExportReady() {
  persistCurrentFields();
  if (!allTrialsComplete()) {
    const remaining = Math.max(0, state.trialPlan.length - completedCount());
    els.saveStatus.textContent = `${remaining} remaining`;
    render();
    return false;
  }
  return true;
}

function exportCsv() {
  if (!ensureExportReady()) {
    return;
  }

  const data = buildExportData();
  const csv = [data.responseHeaders, ...data.responseRows]
    .map((row) => row.map(csvEscape).join(","))
    .join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  downloadBlob(blob, resultFileName("csv"));
}

function xmlEscape(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function columnName(index) {
  let n = index + 1;
  let name = "";
  while (n > 0) {
    const rem = (n - 1) % 26;
    name = String.fromCharCode(65 + rem) + name;
    n = Math.floor((n - 1) / 26);
  }
  return name;
}

function worksheetXml(rows) {
  const sheetRows = rows.map((row, rowIndex) => {
    const cells = row.map((value, colIndex) => {
      const ref = `${columnName(colIndex)}${rowIndex + 1}`;
      if (typeof value === "number" && Number.isFinite(value)) {
        return `<c r="${ref}"><v>${value}</v></c>`;
      }
      if (typeof value === "boolean") {
        return `<c r="${ref}" t="b"><v>${value ? 1 : 0}</v></c>`;
      }
      return `<c r="${ref}" t="inlineStr"><is><t xml:space="preserve">${xmlEscape(value)}</t></is></c>`;
    }).join("");
    return `<row r="${rowIndex + 1}">${cells}</row>`;
  }).join("");
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>${sheetRows}</sheetData></worksheet>`;
}

function makeXlsxBlob(sheets) {
  const sheetOverrides = sheets.map((_, index) => (
    `<Override PartName="/xl/worksheets/sheet${index + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`
  )).join("");
  const workbookSheets = sheets.map((sheet, index) => (
    `<sheet name="${xmlEscape(sheet.name)}" sheetId="${index + 1}" r:id="rId${index + 1}"/>`
  )).join("");
  const workbookRels = sheets.map((_, index) => (
    `<Relationship Id="rId${index + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${index + 1}.xml"/>`
  )).join("");

  const files = [
    {
      name: "[Content_Types].xml",
      content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>${sheetOverrides}</Types>`,
    },
    {
      name: "_rels/.rels",
      content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`,
    },
    {
      name: "xl/workbook.xml",
      content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>${workbookSheets}</sheets></workbook>`,
    },
    {
      name: "xl/_rels/workbook.xml.rels",
      content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${workbookRels}</Relationships>`,
    },
    ...sheets.map((sheet, index) => ({
      name: `xl/worksheets/sheet${index + 1}.xml`,
      content: worksheetXml(sheet.rows),
    })),
  ];
  return new Blob([zipFiles(files)], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
}

function makeCrcTable() {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i += 1) {
    let c = i;
    for (let k = 0; k < 8; k += 1) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[i] = c >>> 0;
  }
  return table;
}

const CRC_TABLE = makeCrcTable();

function crc32(bytes) {
  let crc = 0xffffffff;
  bytes.forEach((byte) => {
    crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  });
  return (crc ^ 0xffffffff) >>> 0;
}

function uint16(value) {
  const bytes = new Uint8Array(2);
  new DataView(bytes.buffer).setUint16(0, value, true);
  return bytes;
}

function uint32(value) {
  const bytes = new Uint8Array(4);
  new DataView(bytes.buffer).setUint32(0, value >>> 0, true);
  return bytes;
}

function concatBytes(chunks) {
  const total = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const out = new Uint8Array(total);
  let offset = 0;
  chunks.forEach((chunk) => {
    out.set(chunk, offset);
    offset += chunk.length;
  });
  return out;
}

function dosDateTime(date = new Date()) {
  const year = Math.max(1980, date.getFullYear());
  const dosTime = (date.getHours() << 11) | (date.getMinutes() << 5) | Math.floor(date.getSeconds() / 2);
  const dosDate = ((year - 1980) << 9) | ((date.getMonth() + 1) << 5) | date.getDate();
  return { dosDate, dosTime };
}

function zipFiles(files) {
  const encoder = new TextEncoder();
  const localParts = [];
  const centralParts = [];
  let offset = 0;
  const { dosDate, dosTime } = dosDateTime();

  files.forEach((file) => {
    const nameBytes = encoder.encode(file.name);
    const dataBytes = typeof file.content === "string" ? encoder.encode(file.content) : file.content;
    const crc = crc32(dataBytes);
    const localHeader = concatBytes([
      uint32(0x04034b50),
      uint16(20),
      uint16(0),
      uint16(0),
      uint16(dosTime),
      uint16(dosDate),
      uint32(crc),
      uint32(dataBytes.length),
      uint32(dataBytes.length),
      uint16(nameBytes.length),
      uint16(0),
      nameBytes,
    ]);
    localParts.push(localHeader, dataBytes);

    centralParts.push(concatBytes([
      uint32(0x02014b50),
      uint16(20),
      uint16(20),
      uint16(0),
      uint16(0),
      uint16(dosTime),
      uint16(dosDate),
      uint32(crc),
      uint32(dataBytes.length),
      uint32(dataBytes.length),
      uint16(nameBytes.length),
      uint16(0),
      uint16(0),
      uint16(0),
      uint16(0),
      uint32(0),
      uint32(offset),
      nameBytes,
    ]));
    offset += localHeader.length + dataBytes.length;
  });

  const local = concatBytes(localParts);
  const central = concatBytes(centralParts);
  const end = concatBytes([
    uint32(0x06054b50),
    uint16(0),
    uint16(0),
    uint16(files.length),
    uint16(files.length),
    uint32(central.length),
    uint32(local.length),
    uint16(0),
  ]);
  return concatBytes([local, central, end]);
}

function resultFileName(extension) {
  const reviewer = (state.reviewerId || "reviewer").replace(/[^a-z0-9_-]+/gi, "_");
  return `pv_ljt_audio_review_${reviewer}_${state.voice}_${state.taskKey}.${extension}`;
}

function downloadBlob(blob, fileName) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
}

function exportWorkbook() {
  if (!ensureExportReady()) {
    return;
  }
  const data = buildExportData();
  const workbook = makeXlsxBlob([
    { name: "Session", rows: data.sessionRows },
    { name: "Responses", rows: [data.responseHeaders, ...data.responseRows] },
    { name: "Trial_Order", rows: [data.trialOrderHeaders, ...data.trialOrderRows] },
    { name: "Codebook", rows: data.codebookRows },
  ]);
  downloadBlob(workbook, resultFileName("xlsx"));
}

function advanceOrExport() {
  persistCurrentFields();
  if (!isComplete(currentResponse())) {
    return;
  }
  if (state.currentIndex >= state.trialPlan.length - 1) {
    exportWorkbook();
    return;
  }
  state.currentIndex += 1;
  saveSession();
  render();
}

function goBack() {
  persistCurrentFields();
  if (state.currentIndex > 0) {
    state.currentIndex -= 1;
    saveSession();
    render();
  }
}

function bindEvents() {
  state.browserSeed = browserSeed();
  let reviewerReloadTimer = null;

  function applyReviewerIdChange() {
    const nextReviewerId = els.reviewerId.value.trim();
    if (nextReviewerId === state.reviewerId) {
      return;
    }
    persistCurrentFields();
    state.reviewerId = nextReviewerId;
    if (state.rawTrials.length) {
      state.trialPlan = buildTrialPlan(state.rawTrials);
      loadSavedSession();
      render();
    } else {
      loadTask().catch((error) => {
        els.saveStatus.textContent = "Load error";
        console.error(error);
      });
    }
  }

  els.reviewerId.addEventListener("input", () => {
    window.clearTimeout(reviewerReloadTimer);
    reviewerReloadTimer = window.setTimeout(applyReviewerIdChange, 250);
  });

  els.reviewerId.addEventListener("change", () => {
    window.clearTimeout(reviewerReloadTimer);
    applyReviewerIdChange();
  });

  document.querySelectorAll('input[name="voice"]').forEach((input) => {
    input.addEventListener("change", async () => {
      persistCurrentFields();
      state.voice = input.value;
      await loadTask();
    });
  });

  els.taskSelect.addEventListener("change", async () => {
    persistCurrentFields();
    state.taskKey = els.taskSelect.value;
    await loadTask();
  });

  els.showText.addEventListener("change", render);

  els.audioPlayer.addEventListener("play", () => {
    const saved = currentResponse();
    saved.playbackCount += 1;
    saved.updatedAt = new Date().toISOString();
    saveSession();
  });

  els.replayButton.addEventListener("click", () => {
    els.audioPlayer.currentTime = 0;
    els.audioPlayer.play();
  });

  els.easeSlider.addEventListener("input", () => setRating("ease", els.easeSlider.value));
  els.naturalnessSlider.addEventListener("input", () => (
    setRating("naturalness", els.naturalnessSlider.value)
  ));

  document.querySelectorAll(".quality-grid input").forEach((input) => {
    input.addEventListener("change", persistCurrentFields);
  });
  els.commentBox.addEventListener("blur", persistCurrentFields);
  els.backButton.addEventListener("click", goBack);
  els.nextButton.addEventListener("click", advanceOrExport);
  els.exportButton.addEventListener("click", exportWorkbook);

  els.resetButton.addEventListener("click", async () => {
    if (!window.confirm("Clear saved responses for this task, voice, and reviewer ID?")) {
      return;
    }
    localStorage.removeItem(storageKey());
    state.responses = {};
    state.currentIndex = 0;
    await loadTask();
  });
}

bindEvents();
loadTask().catch((error) => {
  els.saveStatus.textContent = "Load error";
  console.error(error);
});
