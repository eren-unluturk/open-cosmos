/* Code runner. Runs inside a Web Worker, so the learner's code cannot touch the page,
   its cookies or its storage. The main page stops this worker if the code runs too long.

   Message in:  { id, language, prelude, preamble, code, tests: [{name, code}], mode: "run" | "check" }
   Messages out: { id, type: "running" }   when the code is about to run (after Python has loaded)
                 { id, type: "done", output, error, results: [{name, passed, message}] }
                 { id, type: "fatal", message }                       the runner itself failed
*/
"use strict";

const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
let pyodide = null;

self.onmessage = async (event) => {
  const job = event.data;
  try {
    const result = job.language === "python" ? await runPython(job) : runJavaScript(job);
    self.postMessage({ id: job.id, type: "done", ...result });
  } catch (err) {
    self.postMessage({ id: job.id, type: "fatal", message: String((err && err.message) || err) });
  }
};

function errorText(e) {
  return String((e && e.message) || e);
}

function show(value) {
  return typeof value === "string" ? value : JSON.stringify(value) ?? String(value);
}

function runJavaScript(job) {
  self.postMessage({ id: job.id, type: "running" });
  const logs = [];
  const loud = { log: (...a) => logs.push(a.map(show).join(" ")) };
  loud.error = loud.warn = loud.info = loud.log;
  const quiet = { log() {}, error() {}, warn() {}, info() {} };
  const head = job.prelude + "\n" + job.preamble + "\n";

  let error = null;
  try {
    new Function("console", head + job.code)(loud);
  } catch (e) {
    error = errorText(e);
  }
  const output = logs.join("\n");
  if (job.mode !== "check" || error) return { output, error, results: [] };

  const results = job.tests.map((t) => {
    try {
      // The test sits in its own block so its names never clash with the learner's names.
      new Function("console", "output", head + job.code + "\n;{\n" + t.code + "\n}")(quiet, output);
      return { name: t.name, passed: true };
    } catch (e) {
      return { name: t.name, passed: false, message: errorText(e) };
    }
  });
  return { output, error: null, results };
}

function pythonError(e) {
  const text = String((e && e.message) || e).trim();
  const lines = text.split("\n").filter((l) => l.trim());
  const last = lines[lines.length - 1] || text;
  let lineNo = null;
  for (const m of text.matchAll(/File "<exec>", line (\d+)/g)) lineNo = m[1];
  return lineNo ? `${last} (line ${lineNo})` : last;
}

async function runPython(job) {
  if (!pyodide) {
    importScripts(PYODIDE_URL + "pyodide.js");
    pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
  }
  self.postMessage({ id: job.id, type: "running" });
  const logs = [];
  pyodide.setStdout({ batched: (s) => logs.push(s) });
  pyodide.setStderr({ batched: (s) => logs.push(s) });
  const scope = pyodide.globals.get("dict")();
  let error = null;
  try {
    pyodide.runPython(job.prelude, { globals: scope });
    if (job.preamble) pyodide.runPython(job.preamble, { globals: scope });
    pyodide.runPython(job.code, { globals: scope });
  } catch (e) {
    error = pythonError(e);
  }
  const output = logs.join("\n");
  if (job.mode !== "check" || error) {
    scope.destroy();
    return { output, error, results: [] };
  }
  scope.set("output", output);
  const results = job.tests.map((t) => {
    try {
      pyodide.runPython(t.code, { globals: scope });
      return { name: t.name, passed: true };
    } catch (e) {
      return { name: t.name, passed: false, message: pythonError(e) };
    }
  });
  scope.destroy();
  return { output, error: null, results };
}
