"""Rewrite docs/TRANSLATE_QUEUE.md: kid-safe entries still missing es/ar/hi/pt, in priority order.

Usage: python scripts/translate_queue.py
"""
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import translate  # noqa: E402

SRC = {"learn": "awesome", "build": "build-your-own-x", "kids": "CS Unplugged"}


def main():
    es = [e for n in SRC for e in json.loads((ROOT / "src" / "data" / f"{n}.json").read_text(encoding="utf-8"))]
    todo = translate.pick_todo(es)
    src = lambda e: SRC[e["id"].split("-")[0]]  # noqa: E731
    c = collections.Counter((src(e), e["level"]) for e in todo)
    out = [f"# Translation queue (kid-safe entries not yet translated into es/ar/hi/pt)\n\n",
           f"Regenerate with `python scripts/translate_queue.py`. **{len(todo)} entries** still need es, ar, hi and pt for `title` and `desc`. "
           "Priority: CS Unplugged first, then Beginner, then Intermediate, then Advanced.\n\n",
           "## Counts\n\n| Source | Beginner | Intermediate | Advanced | Total |\n|---|---|---|---|---|\n"]
    for s in SRC.values():
        r = [c[(s, l)] for l in translate.LEVELS]
        out.append(f"| {s} | {r[0]} | {r[1]} | {r[2]} | {sum(r)} |\n")
    tot = [sum(c[(s, l)] for s in SRC.values()) for l in translate.LEVELS]
    out.append(f"| **All** | {tot[0]} | {tot[1]} | {tot[2]} | {len(todo)} |\n\n")
    out.append("""## How to work through it
- **By hand (no API key):** add a module in `scripts/translation_content/` with `build()` returning `{entry id: {"title": {lang: ...}, "desc": {lang: ...}}}` for es, ar, hi, pt (see `kids_activities.py`), then run `python scripts/apply_translations.py` and the tests. Keep code and technical terms in English. They are labeled `ai_translated`.
- **With an API key:** `python scripts/translate.py --limit N` (kid-safe only, priority order, 5 requests at a time; add `--all` for everything).
- Still needs native-speaker checks for all four languages.

## Queue

| # | id | source | level | age | topic | title (en) |
|---|---|---|---|---|---|---|
""")
    for i, e in enumerate(todo, 1):
        out.append(f"| {i} | {e['id']} | {src(e)} | {e['level']} | {e['age_group']} | {e['topic']} | {e['title']['en'][:70].replace('|', '/')} |\n")
    (ROOT / "docs" / "TRANSLATE_QUEUE.md").write_text("".join(out), encoding="utf-8")
    print(f"{len(todo)} entries in the queue")


if __name__ == "__main__":
    main()
