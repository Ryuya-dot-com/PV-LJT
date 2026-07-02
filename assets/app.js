const TASKS = {
  ljt_a: {
    label: "Aural PV-LJT List A",
    path: "materials/pilot_trial_file_ljt_list_A_v1.tsv",
    kind: "ljt",
    promptTitle: "Acceptable or unacceptable?",
    promptCopy: "Judge the sentence meaning from the audio.",
    responseField: "expected_response",
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
    responses: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
    ],
  },
};

const state = {
  taskKey: "ljt_a",
  voice: "male",
  reviewerId: "",
  trials: [],
  currentIndex: 0,
  responses: {},
};

const els = {
  reviewerId: document.getElementById("reviewerId"),
  taskSelect: document.getElementById("taskSelect"),
  showText: document.getElementById("showText"),
  taskLabel: document.getElementById("taskLabel"),
  progressText: document.getElementById("progressText"),
  progressBar: document.getElementById("progressBar"),
  trialNav: document.getElementById("trialNav"),
  phaseLabel: document.getElementById("phaseLabel"),
  trialCounter: document.getElementById("trialCounter"),
  audioPlayer: document.getElementById("audioPlayer"),
  replayButton: document.getElementById("replayButton"),
  promptTitle: document.getElementById("promptTitle"),
  promptCopy: document.getElementById("promptCopy"),
  responseButtons: document.getElementById("responseButtons"),
  textReveal: document.getElementById("textReveal"),
  stimulusText: document.getElementById("stimulusText"),
  commentBox: document.getElementById("commentBox"),
  prevButton: document.getElementById("prevButton"),
  nextButton: document.getElementById("nextButton"),
  exportButton: document.getElementById("exportButton"),
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

function trialKey(index = state.currentIndex) {
  const trial = state.trials[index];
  const id = trial.item_id || trial.trial_id || `trial_${index + 1}`;
  return `${state.taskKey}:${state.voice}:${id}`;
}

function storageKey() {
  return `pv-ljt-review:${state.taskKey}:${state.voice}`;
}

function blankResponse() {
  return {
    response: "",
    flags: [],
    comment: "",
    playbackCount: 0,
    updatedAt: "",
  };
}

function currentResponse() {
  const key = trialKey();
  if (!state.responses[key]) {
    state.responses[key] = blankResponse();
  }
  return state.responses[key];
}

function loadSavedResponses() {
  const saved = localStorage.getItem(storageKey());
  state.responses = saved ? JSON.parse(saved) : {};
}

function saveResponses() {
  localStorage.setItem(storageKey(), JSON.stringify(state.responses));
  els.saveStatus.textContent = "Saved";
  window.setTimeout(() => {
    els.saveStatus.textContent = "Ready";
  }, 900);
}

async function loadTask() {
  const task = TASKS[state.taskKey];
  const response = await fetch(task.path);
  if (!response.ok) {
    throw new Error(`Could not load ${task.path}`);
  }
  state.trials = parseTsv(await response.text());
  state.currentIndex = 0;
  loadSavedResponses();
  render();
}

function completedCount() {
  return state.trials.filter((_, index) => {
    const key = trialKey(index);
    return state.responses[key]?.response;
  }).length;
}

function renderNav() {
  els.trialNav.innerHTML = "";
  state.trials.forEach((trial, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = String(index + 1);
    button.className = [
      index === state.currentIndex ? "current" : "",
      state.responses[trialKey(index)]?.response ? "done" : "",
    ]
      .filter(Boolean)
      .join(" ");
    button.addEventListener("click", () => {
      persistCurrentFields();
      state.currentIndex = index;
      render();
    });
    els.trialNav.append(button);
  });
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
      saved.response = option.value;
      saved.updatedAt = new Date().toISOString();
      saveResponses();
      render();
    });
    els.responseButtons.append(button);
  });
}

function renderQualityFields() {
  const saved = currentResponse();
  document.querySelectorAll(".quality-grid input").forEach((input) => {
    input.checked = saved.flags.includes(input.value);
  });
  els.commentBox.value = saved.comment;
}

function render() {
  const task = TASKS[state.taskKey];
  const trial = state.trials[state.currentIndex];
  if (!trial) {
    return;
  }

  els.taskLabel.textContent = task.label;
  els.promptTitle.textContent = task.promptTitle;
  els.promptCopy.textContent = task.promptCopy;
  els.phaseLabel.textContent = trial.phase === "practice" ? "Practice" : "Main";
  els.trialCounter.textContent = `Trial ${state.currentIndex + 1} of ${state.trials.length}`;
  els.audioPlayer.src = audioPath(trial);
  els.stimulusText.textContent = trial.stimulus_text || "";
  els.textReveal.hidden = !(els.showText.checked && currentResponse().response);
  els.prevButton.disabled = state.currentIndex === 0;
  els.nextButton.textContent = state.currentIndex === state.trials.length - 1 ? "Finish" : "Next";

  const done = completedCount();
  els.progressText.textContent = `${done} / ${state.trials.length}`;
  els.progressBar.style.width = `${state.trials.length ? (done / state.trials.length) * 100 : 0}%`;

  renderResponseButtons();
  renderQualityFields();
  renderNav();
}

function persistCurrentFields() {
  if (!state.trials.length) {
    return;
  }
  const saved = currentResponse();
  saved.flags = Array.from(document.querySelectorAll(".quality-grid input:checked")).map(
    (input) => input.value,
  );
  saved.comment = els.commentBox.value.trim();
  saved.updatedAt = new Date().toISOString();
  saveResponses();
}

function csvEscape(value) {
  const text = String(value ?? "");
  if (/[",\n\r]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

function exportCsv() {
  persistCurrentFields();
  const task = TASKS[state.taskKey];
  const headers = [
    "reviewer_id",
    "exported_at",
    "task",
    "voice",
    "trial_order",
    "phase",
    "item_id",
    "trial_id",
    "pv",
    "response",
    "expected_response",
    "response_correct",
    "quality_flags",
    "comment",
    "playback_count",
    "audio_file",
    "stimulus_text",
  ];
  const exportedAt = new Date().toISOString();
  const rows = state.trials.map((trial, index) => {
    const saved = state.responses[trialKey(index)] || blankResponse();
    const expected = trial[task.responseField] || "";
    const correct = saved.response ? String(saved.response === expected) : "";
    return [
      state.reviewerId,
      exportedAt,
      task.label,
      state.voice,
      trial.trial_order || index + 1,
      trial.phase,
      trial.item_id || "",
      trial.trial_id || "",
      trial.pv || "",
      saved.response,
      expected,
      correct,
      saved.flags.join(";"),
      saved.comment,
      saved.playbackCount,
      audioPath(trial),
      trial.stimulus_text || "",
    ];
  });

  const csv = [headers, ...rows].map((row) => row.map(csvEscape).join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  const reviewer = state.reviewerId || "reviewer";
  link.href = url;
  link.download = `pv_ljt_audio_review_${reviewer}_${state.voice}_${state.taskKey}.csv`;
  link.click();
  URL.revokeObjectURL(url);
}

function bindEvents() {
  els.reviewerId.addEventListener("input", () => {
    state.reviewerId = els.reviewerId.value.trim();
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
    saveResponses();
  });

  els.replayButton.addEventListener("click", () => {
    els.audioPlayer.currentTime = 0;
    els.audioPlayer.play();
  });

  document.querySelectorAll(".quality-grid input").forEach((input) => {
    input.addEventListener("change", persistCurrentFields);
  });
  els.commentBox.addEventListener("blur", persistCurrentFields);

  els.prevButton.addEventListener("click", () => {
    persistCurrentFields();
    state.currentIndex = Math.max(0, state.currentIndex - 1);
    render();
  });

  els.nextButton.addEventListener("click", () => {
    persistCurrentFields();
    if (state.currentIndex < state.trials.length - 1) {
      state.currentIndex += 1;
      render();
    } else {
      exportCsv();
    }
  });

  els.exportButton.addEventListener("click", exportCsv);

  els.resetButton.addEventListener("click", () => {
    if (!window.confirm("Clear saved responses for this task and voice?")) {
      return;
    }
    localStorage.removeItem(storageKey());
    state.responses = {};
    render();
  });
}

bindEvents();
loadTask().catch((error) => {
  els.saveStatus.textContent = "Load error";
  console.error(error);
});
