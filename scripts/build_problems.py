"""Check every coding problem, then write src/data/problems.json.

For each problem this proves: the reference solution passes every test, the starter code does not,
and each guided stage's solution passes that stage's tests. JavaScript needs `node` on PATH.

Usage: python scripts/build_problems.py [--no-node]
--no-node: when node is missing, still write the file but check only the Python problems. Use it only for
text-only changes (names, wording); never when a JavaScript solution or test changed.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import problems  # noqa: E402
from problem_content import PROBLEMS as OUR_PROBLEMS  # noqa: E402
from problem_content_unplugged import PROBLEMS as UNPLUGGED  # noqa: E402  (CC BY-SA 4.0, adapted)

PROBLEMS = OUR_PROBLEMS + UNPLUGGED


def main():
    if not problems.node_available():
        if "--no-node" not in sys.argv:
            print("node was not found. JavaScript problems cannot be checked, so nothing was written.")
            return 1
        print("WARNING: node not found; JavaScript problems were NOT re-checked (--no-node, text-only change).")
    errors, seen = [], set()
    for p in PROBLEMS:
        if p["id"] in seen:
            errors.append(f"duplicate id {p['id']}")
        seen.add(p["id"])
        errors += problems.verify(p)
    if errors:
        print("\n".join(errors))
        return 1
    out = ROOT / "src" / "data" / "problems.json"
    out.write_text(json.dumps(PROBLEMS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    levels = {}
    for p in PROBLEMS:
        levels[p["level"]] = levels.get(p["level"], 0) + 1
    print(f"{len(PROBLEMS)} problems written, all checked. {levels}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
