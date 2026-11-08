"""Coding problems: format, checks, and a server-side runner used only by tests and the build script.

The learner's code runs in THEIR browser (public/static/runner.js, in a Web Worker), never on our server.
This file never executes learner code. It only runs our own reference solutions, to prove every
problem and every guided step can really be solved.

Problem format (src/data/problems.json, a list; text fields are {"en": ...} so we can translate later):
  id, language ("python" | "javascript"), level, age_group, topic, license, source,
  title, prompt, concepts {"en": [..]},
  starter            code the editor starts with
  preamble (optional) hidden code that runs BEFORE the learner's code (for example, to switch off a built-in)
  tests              [{"name": {"en"}, "code": str}]   run AFTER the learner's code, same scope
  hints              {"en": [..]}                      shown one at a time, on request
  guided             [{"goal", "explain", "starter"?, "solution", "tests"}]   "Guide me" stages
  solution           reference code
  solution_note      {"en"}  short explanation shown with the solution

Test code sees: `output` (what the program printed) and a check helper:
  python      check(actual, expected)        plain `assert` also works
  javascript  assertEqual(actual, expected)  and assert(condition, message)
"""
import json
import shutil
import subprocess
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

LANGUAGES = ("python", "javascript")
LEVELS = ("Beginner", "Intermediate", "Advanced")
AGES = ("5-7", "8-10", "11-13", "teen+")
MAX_CODE = 20000  # characters; the page refuses more than this

PRELUDE_PY = '''def check(actual, expected):
    if actual != expected:
        raise AssertionError(f"Expected {expected!r} but got {actual!r}")
'''

PRELUDE_JS = '''function assert(condition, message) {
  if (!condition) throw new Error(message || "That is not right yet.");
}
function assertEqual(actual, expected) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error("Expected " + JSON.stringify(expected) + " but got " + JSON.stringify(actual));
  }
}
'''

REQUIRED = ("id", "language", "level", "age_group", "topic", "title", "prompt", "starter", "tests",
            "hints", "solution", "license")


def validate(problem):
    """Return a list of problems with this problem's data (empty = fine)."""
    errs = []
    pid = problem.get("id", "?")
    for key in REQUIRED:
        if key not in problem:
            errs.append(f"{pid}: missing {key}")
    if errs:
        return errs
    if problem["language"] not in LANGUAGES:
        errs.append(f"{pid}: bad language")
    if problem["level"] not in LEVELS:
        errs.append(f"{pid}: bad level")
    if problem["age_group"] not in AGES:
        errs.append(f"{pid}: bad age_group")
    for field in ("title", "prompt"):
        if not problem[field].get("en"):
            errs.append(f"{pid}: {field} needs English text")
    if len(problem["hints"].get("en", [])) < 3:
        errs.append(f"{pid}: needs at least 3 hints")
    if not problem["tests"]:
        errs.append(f"{pid}: needs tests")
    for t in problem["tests"]:
        if not t.get("code") or not t.get("name", {}).get("en"):
            errs.append(f"{pid}: every test needs a name and code")
    for i, stage in enumerate(problem.get("guided", [])):
        for key in ("goal", "explain", "solution", "tests"):
            if not stage.get(key):
                errs.append(f"{pid}: guided stage {i + 1} missing {key}")
    if problem.get("guided") and not problem["guided"][0].get("starter"):
        errs.append(f"{pid}: the first guided stage needs a starter")
    for field in ("starter", "solution"):
        if len(problem[field]) > MAX_CODE:
            errs.append(f"{pid}: {field} too long")
    return errs


def public_view(problem):
    """What the page may carry from the start: no hints text, no solutions."""
    view = {k: v for k, v in problem.items() if k not in ("hints", "solution", "solution_note", "guided")}
    view["hint_count"] = len(problem["hints"]["en"])
    view["guided"] = [{"goal": s["goal"], "explain": s["explain"], "starter": s.get("starter", ""),
                       "tests": s["tests"]} for s in problem.get("guided", [])]
    return view


# --- Running our own reference solutions (tests and build script only) --------------------------

def _run_python(code, test_code, preamble=""):
    """Run code then test_code in one namespace. Returns None if it passes, else the error text."""
    ns = {}
    out = StringIO()
    try:
        exec(PRELUDE_PY, ns)
        exec(preamble, ns)
        with redirect_stdout(out):
            exec(code, ns)
        ns["output"] = out.getvalue()
        exec(test_code, ns)
    except Exception as exc:  # noqa: BLE001  (a failing reference solution is what we want to report)
        return f"{type(exc).__name__}: {exc}"
    return None


_NODE_HARNESS = '''
const fs = require("fs");
const job = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const logs = [];
const fake = { log: (...a) => logs.push(a.map(String).join(" ")) };
const none = { log() {} };
let error = null;
try {
  new Function("console", job.prelude + "\\n" + job.preamble + "\\n" + job.code)(fake);
  const output = logs.join("\\n");
  new Function("console", "output", job.prelude + "\\n" + job.preamble + "\\n" + job.code + "\\n;" + job.test)(none, output);
} catch (e) { error = String(e && e.message || e); }
process.stdout.write(JSON.stringify({ error }));
'''


def node_available():
    return shutil.which("node") is not None


def _run_js(code, test_code, preamble=""):
    with tempfile.TemporaryDirectory() as tmp:
        harness = Path(tmp) / "h.js"
        job = Path(tmp) / "job.json"
        harness.write_text(_NODE_HARNESS, encoding="utf-8")
        job.write_text(json.dumps({"prelude": PRELUDE_JS, "preamble": preamble, "code": code, "test": test_code}), encoding="utf-8")
        done = subprocess.run(["node", str(harness), str(job)], capture_output=True, text=True, timeout=20)
    if done.returncode != 0:
        return done.stderr.strip() or "node failed"
    return json.loads(done.stdout)["error"]


def run_reference(problem, code, test_code):
    """None if `code` passes `test_code` for this problem's language, else an error string."""
    pre = problem.get("preamble", "")
    if problem["language"] == "python":
        return _run_python(code, test_code, pre)
    return _run_js(code, test_code, pre)


def verify(problem, js=True):
    """Check every claim in a problem: the solution passes all tests, the starter does NOT,
    and each guided stage's solution passes its own tests. Returns a list of error strings."""
    errs = validate(problem)
    if errs:
        return errs
    if problem["language"] == "javascript" and not (js and node_available()):
        return []  # cannot run JavaScript here; the caller decides whether that is acceptable
    pid = problem["id"]
    for t in problem["tests"]:
        err = run_reference(problem, problem["solution"], t["code"])
        if err:
            errs.append(f"{pid}: solution fails '{t['name']['en']}': {err}")
    if all(run_reference(problem, problem["starter"], t["code"]) is None for t in problem["tests"]):
        errs.append(f"{pid}: the starter code already passes every test")
    for i, stage in enumerate(problem.get("guided", []), start=1):
        for t in stage["tests"]:
            err = run_reference(problem, stage["solution"], t["code"])
            if err:
                errs.append(f"{pid}: stage {i} solution fails '{t['name']['en']}': {err}")
        if i == 1 and all(run_reference(problem, stage["starter"], t["code"]) is None for t in stage["tests"]):
            errs.append(f"{pid}: stage 1 starter already passes")
    return errs
