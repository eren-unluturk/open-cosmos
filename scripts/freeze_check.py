"""Data freeze check. Run before submitting (and Sunday 8 AM). Does NOT call fetch.py (it re-downloads upstream lists).

Re-runs categorize.py --no-ai (applies cache + overrides), coverage.py and the tests, then checks:
  - app code in src/ (everything except src/data/) is unchanged since this branch split from the base branch (default: main)
  - no .env / env file is tracked by git
  - every entry has a license and source; kids.json entries are CC-BY-SA-4.0; CC0 files are CC0-1.0
  - safety_overrides.json entries are applied
Usage: python scripts/freeze_check.py [--base main]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
bad = []


def run(*cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def check(ok, msg):
    print(("PASS  " if ok else "FAIL  ") + msg)
    if not ok:
        bad.append(msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="main")
    base = ap.parse_args().base

    code, out = run(PY, "scripts/categorize.py", "--no-ai")
    check(code == 0, "categorize.py --no-ai ran: " + out.splitlines()[-1] if out else "categorize.py ran")
    code, out = run(PY, "scripts/coverage.py")
    print(out.splitlines()[0] if out else "")
    below = [l for l in out.splitlines() if l.startswith("Combinations below 6")]
    print("      " + (below[0] if below else "coverage printed"))
    code, out = run(PY, "-m", "unittest", "discover", "-s", "tests")
    check(code == 0, "tests: " + (out.splitlines()[-1] if out else ""))

    # compare against where this branch started (the base may have moved on with teammates' work)
    _, fork = run("git", "merge-base", "HEAD", base)
    code, out = run("git", "diff", "--name-only", fork, "--", "src", ":!src/data")
    check(code == 0 and not out, f"src/ app code unchanged since this branch left {base}" + (": " + out.replace("\n", ", ") if out else ""))
    code, out = run("git", "ls-files")
    env = [f for f in out.splitlines() if Path(f).name.startswith(".env") or f.endswith(".env")]
    check(not env, "no env files tracked" + (": " + ", ".join(env) if env else ""))

    n = 0
    for name, lic in (("learn", "CC0-1.0"), ("build", "CC0-1.0"), ("kids", "CC-BY-SA-4.0")):
        for e in json.loads((ROOT / "src" / "data" / f"{name}.json").read_text()):
            n += 1
            if not e.get("license") or not e.get("source") or e["license"] != lic:
                check(False, f"{e['id']} has license {e.get('license')!r} / source {e.get('source')!r}, expected {lic}")
    check(not [b for b in bad if "license" in b], f"all {n} entries have a source and the right license")

    ov = json.loads((ROOT / "scripts" / "cache" / "safety_overrides.json").read_text())
    by_id = {e["id"]: e for name in ("learn", "build", "kids")
             for e in json.loads((ROOT / "src" / "data" / f"{name}.json").read_text())}
    wrong = [i for i, o in ov.items() if i not in by_id or by_id[i]["safety"] != o["safety"]]
    check(not wrong, f"{len(ov)} safety overrides applied")

    code, out = run("git", "status", "--short")
    print("\nWorking tree:", "clean" if not out else "\n" + out)
    print("\nREMINDER: never re-run scripts/fetch.py after the freeze unless you mean it.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
