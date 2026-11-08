/* Problem page: editor, Run / Check, hints, answer, and "Guide me" steps.
   Your code runs in a Web Worker (runner.js). Nothing is sent to our server except requests for
   hints and answers. Progress saving is done elsewhere: when every test passes we only announce it
   (a "problem:solved" event, and HackProgress.markSolved(id) if that exists). */
"use strict";

(() => {
  const data = JSON.parse(document.getElementById("problem-data").textContent);
  const ui = data.ui;
  const $ = (id) => document.getElementById(id);
  const editor = $("code");
  const statusEl = $("status");
  const outputEl = $("output");
  const resultsEl = $("results");
  const summaryEl = $("summary");

  let mode = "alone"; // "alone" | "guided"
  let stage = 0; // guided: 0..stages.length (the last one is "pass every test")
  let hintsShown = 0;
  let worker = null;
  let jobId = 0;
  let busy = false;
  const lastStage = data.stages.length;

  const fmt = (text, vars) => text.replace(/\{(\w+)\}/g, (_, k) => (k in vars ? vars[k] : `{${k}}`));
  const say = (text) => { statusEl.textContent = text || ""; };

  // ---------- running code ----------
  function startWorker() {
    stopWorker();
    worker = new Worker("/static/runner.js");
  }
  function stopWorker() {
    if (worker) { worker.terminate(); worker = null; }
  }

  function runJob(kind, tests) {
    return new Promise((resolve) => {
      if (!worker) startWorker();
      const id = ++jobId;
      let runTimer = null;
      const loadTimer = setTimeout(() => finish({ type: "fatal", message: ui.p_cannot_load }), 90000);
      const finish = (msg) => {
        clearTimeout(loadTimer);
        clearTimeout(runTimer);
        if (msg.type !== "done") stopWorker(); // a fresh worker next time
        resolve(msg);
      };
      worker.onmessage = (e) => {
        const msg = e.data;
        if (msg.id !== id) return;
        if (msg.type === "running") {
          say(ui.p_running);
          clearTimeout(loadTimer);
          runTimer = setTimeout(() => finish({ type: "timeout" }), 5000);
        } else {
          finish(msg);
        }
      };
      worker.onerror = () => finish({ type: "fatal", message: ui.p_cannot_load });
      say(data.language === "python" && !worker.warm ? ui.p_loading : ui.p_running);
      worker.warm = true;
      worker.postMessage({
        id, mode: kind, language: data.language, prelude: data.prelude, preamble: data.preamble,
        code: editor.value, tests,
      });
    });
  }

  function currentTests() {
    return mode === "guided" && stage < lastStage ? data.stages[stage].tests : data.tests;
  }

  function setBusy(on) {
    busy = on;
    document.querySelectorAll("[data-needs-idle]").forEach((b) => { b.disabled = on; });
  }

  function showOutput(res) {
    outputEl.textContent = res.output ? res.output : (res.error || res.type === "timeout" ? "" : ui.p_ran_quiet);
  }

  async function act(kind) {
    if (busy) return;
    if (editor.value.length > data.max_code) { say(ui.p_too_long); return; }
    setBusy(true);
    resultsEl.replaceChildren();
    summaryEl.textContent = "";
    const res = await runJob(kind, kind === "check" ? currentTests() : []);
    setBusy(false);
    say("");
    if (res.type === "timeout") { summaryEl.textContent = ui.p_timeout; outputEl.textContent = ""; return; }
    if (res.type === "fatal") { summaryEl.textContent = res.message; return; }
    showOutput(res);
    if (res.error) { summaryEl.textContent = `${ui.p_error} ${res.error}`; return; }
    if (kind !== "check") return;
    renderResults(res.results);
  }

  function renderResults(results) {
    for (const r of results) {
      const li = document.createElement("li");
      li.className = r.passed ? "ok" : "no";
      li.textContent = `${r.passed ? ui.p_ok : ui.p_notok}: ${r.name}`;
      if (!r.passed && r.message) {
        const why = document.createElement("div");
        why.className = "text-sm";
        why.textContent = r.message;
        li.appendChild(why);
      }
      resultsEl.appendChild(li);
    }
    const failed = results.filter((r) => !r.passed).length;
    if (failed) { summaryEl.textContent = fmt(ui.p_failed, { n: failed }); return; }
    const full = mode === "alone" || stage === lastStage;
    summaryEl.textContent = full ? ui.p_passed : ui.p_step_passed;
    if (full) announceSolved();
  }

  function announceSolved() {
    document.dispatchEvent(new CustomEvent("problem:solved", { detail: { id: data.id } }));
    if (window.HackProgress && typeof window.HackProgress.markSolved === "function") {
      window.HackProgress.markSolved(data.id, { title: data.title, galaxy: data.galaxy, url: data.url });
    }
  }

  // ---------- hints and answers (fetched one at a time) ----------
  async function getJSON(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(String(r.status));
    return r.json();
  }

  async function nextHint() {
    if (hintsShown >= data.hint_count) return;
    const res = await getJSON(`/api/problems/${encodeURIComponent(data.id)}/hint/${hintsShown + 1}?lang=${data.lang}`);
    hintsShown += 1;
    const li = document.createElement("li");
    li.textContent = res.hint;
    $("hint-list").appendChild(li);
    updateHintButton();
  }
  function updateHintButton() {
    const b = $("hint");
    if (hintsShown >= data.hint_count) { b.disabled = true; b.textContent = ui.p_no_more_hints; return; }
    b.textContent = `${ui.p_hint} (${fmt(ui.p_hint_n, { i: hintsShown + 1, n: data.hint_count })})`;
  }

  async function showAnswer(stageNo) {
    if (!window.confirm(ui.p_solution_confirm)) return;
    const q = stageNo ? `&stage=${stageNo}` : "";
    const res = await getJSON(`/api/problems/${encodeURIComponent(data.id)}/solution?lang=${data.lang}${q}`);
    $("answer-code").textContent = res.solution;
    $("answer-note").textContent = res.note || "";
    $("answer").hidden = false;
    $("answer").scrollIntoView({ block: "nearest" });
  }

  // ---------- guided steps ----------
  function renderStage() {
    const panel = $("guide-panel");
    panel.hidden = mode !== "guided";
    if (mode !== "guided") return;
    const last = stage === lastStage;
    $("stage-count").textContent = fmt(ui.p_stage, { i: stage + 1, n: lastStage + 1 });
    $("stage-goal").textContent = last ? ui.p_final_step : data.stages[stage].goal;
    $("stage-explain").textContent = last ? "" : data.stages[stage].explain;
    $("prev").disabled = stage === 0;
    $("next").disabled = last;
    $("example").hidden = last;
    resultsEl.replaceChildren();
    summaryEl.textContent = "";
  }

  function setMode(next) {
    mode = next;
    if (mode === "guided" && stage === 0 && editor.value === data.starter && data.stages.length) {
      editor.value = data.stages[0].starter || data.starter;
    }
    renderStage();
  }

  // ---------- wiring ----------
  $("run").addEventListener("click", () => act("run"));
  $("check").addEventListener("click", () => act("check"));
  $("hint").addEventListener("click", () => nextHint().catch(() => say(ui.p_cannot_load)));
  $("solution").addEventListener("click", () => showAnswer(0).catch(() => say(ui.p_cannot_load)));
  $("example").addEventListener("click", () => showAnswer(stage + 1).catch(() => say(ui.p_cannot_load)));
  $("reset").addEventListener("click", () => {
    editor.value = mode === "guided" && stage === 0 && data.stages.length ? (data.stages[0].starter || data.starter) : data.starter;
    resultsEl.replaceChildren(); summaryEl.textContent = ""; outputEl.textContent = "";
  });
  $("next").addEventListener("click", () => { if (stage < lastStage) { stage += 1; renderStage(); } });
  $("prev").addEventListener("click", () => { if (stage > 0) { stage -= 1; renderStage(); } });
  document.querySelectorAll('input[name="mode"]').forEach((r) =>
    r.addEventListener("change", () => setMode(r.value)));

  // Tab indents. Esc then Tab leaves the box (so keyboard users are never trapped).
  let tabLeaves = false;
  editor.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { tabLeaves = true; return; }
    if (e.key !== "Tab" || e.shiftKey || e.ctrlKey || e.altKey || e.metaKey) { tabLeaves = false; return; }
    if (tabLeaves) { tabLeaves = false; return; }
    e.preventDefault();
    const { selectionStart: s, selectionEnd: t, value } = editor;
    editor.value = value.slice(0, s) + "    " + value.slice(t);
    editor.selectionStart = editor.selectionEnd = s + 4;
  });
  editor.addEventListener("blur", () => { tabLeaves = false; });

  editor.value = data.starter;
  if (!data.stages.length) {
    $("mode-guided-wrap").hidden = true;
  }
  updateHintButton();
  renderStage();
  window.addEventListener("pagehide", stopWorker);
})();
