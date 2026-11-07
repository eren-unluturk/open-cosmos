"""Translate entries and assign levels with Claude. Run AFTER scripts/fetch.py.

Reads src/data/{learn,build}.json, fills title/desc for each language and sets
`level`. Results are cached so re-runs only process new entries.

Usage: python scripts/translate.py [--limit N]
Requires ANTHROPIC_API_KEY in a local .env (never committed).
"""
import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
import anthropic

DATA = Path(__file__).resolve().parent.parent / "src" / "data"
LANGS = {"es": "Spanish", "ar": "Arabic", "hi": "Hindi", "pt": "Portuguese"}
LEVELS = ["Beginner", "Intermediate", "Advanced"]
MODEL = "claude-haiku-5-5"

PROMPT = """You help make open-source programming resources accessible.
Given an English resource title and description, return ONLY JSON:
{{"level": one of {levels}, "age_group": one of ["5-7","8-10","11-13","teen+"] (youngest age it suits),
  "translations": {{"es": {{"title": "", "desc": ""}}, "ar": {{...}}, "hi": {{...}}, "pt": {{...}}}}}}
Rules: keep code, product names and technical terms in English (add a short
translated gloss in parentheses only if helpful). Be faithful; add nothing new.

Title: {title}
Description: {desc}"""


def process(client, entry):
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": PROMPT.format(
            levels=LEVELS, title=entry["title"]["en"], desc=entry["desc"]["en"])}],
    )
    out = json.loads(msg.content[0].text)
    # categorize.py owns level/age_group; only fill them if it hasn't run.
    entry["level"] = entry.get("level") or out["level"]
    entry["age_group"] = entry.get("age_group") or out.get("age_group")
    for lang, tr in out["translations"].items():
        entry["title"][lang] = tr["title"]
        entry["desc"][lang] = tr["desc"]
    entry["ai_translated"] = sorted(out["translations"])  # label AI output (see docs/PLAN.md)


def main():
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="max entries per file (for testing)")
    args = ap.parse_args()
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    for name in ("learn", "build", "kids"):
        path = DATA / f"{name}.json"
        if not path.exists():
            continue
        entries = json.loads(path.read_text())
        todo = [e for e in entries if any(l not in e["title"] for l in LANGS)][: args.limit]
        for i, e in enumerate(todo, 1):
            process(client, e)
            print(f"{name}: {i}/{len(todo)}")
            path.write_text(json.dumps(entries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
