"""Translate entries with Claude (optional: needs an API key). Run AFTER categorize.py.

Fills title/desc for es, ar, hi, pt and marks them in `ai_translated`. It never overwrites
`level`/`age_group` set by categorize.py. By default only kid-safe entries are translated, in priority
order (CS Unplugged first, then Beginner, then Intermediate...). Five requests run at a time.

Usage: python scripts/translate.py [--limit N] [--all]
Requires ANTHROPIC_API_KEY in a local .env (never committed).
(No API key? Translations can also be written by hand into scripts/cache/entry_translations.json
and merged with scripts/apply_translations.py.)
"""
import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "src" / "data"
LANGS = {"es": "Spanish", "ar": "Arabic", "hi": "Hindi", "pt": "Portuguese"}
LEVELS = ["Beginner", "Intermediate", "Advanced"]
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")
WORKERS = 5

PROMPT = """You help make open-source programming resources accessible.
Given an English resource title and description, return ONLY JSON:
{{"level": one of {levels}, "age_group": one of ["5-7","8-10","11-13","teen+"] (youngest age it suits),
  "translations": {{"es": {{"title": "", "desc": ""}}, "ar": {{...}}, "hi": {{...}}, "pt": {{...}}}}}}
Rules: keep code, product names and technical terms in English (add a short
translated gloss in parentheses only if helpful). Be faithful; add nothing new.

Title: {title}
Description: {desc}"""

FENCE = re.compile(r"^\s*```[A-Za-z]*\s*|\s*```\s*$")


def parse_json_reply(text):
    """JSON from a model reply, even if wrapped in a ```json fence or surrounded by prose. Raises ValueError."""
    text = FENCE.sub("", FENCE.sub("", text or ""))
    try:
        return json.loads(text)
    except ValueError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except ValueError:
            pass
    raise ValueError("model reply is not valid JSON")


def translate_entry(ask, entry):
    """Ask once; on a parse error (or a reply without translations) ask one more time, then give up."""
    last = None
    for _ in range(2):
        try:
            out = parse_json_reply(ask(entry))
            if not isinstance(out.get("translations"), dict):
                raise ValueError("reply has no translations")
            return out
        except ValueError as ex:
            last = ex
    raise last


def apply_result(entry, out):
    # categorize.py owns level/age_group; only fill them if it hasn't run.
    entry["level"] = entry.get("level") or out.get("level")
    entry["age_group"] = entry.get("age_group") or out.get("age_group")
    for lang, tr in out["translations"].items():
        if lang in LANGS and isinstance(tr, dict):
            entry["title"][lang] = tr["title"]
            entry["desc"][lang] = tr["desc"]
    entry["ai_translated"] = sorted(l for l in out["translations"] if l in LANGS)  # label AI output


def pick_todo(entries, include_all=False):
    """Entries missing a language. Kid-safe only unless include_all; CS Unplugged, then Beginner first."""
    todo = [e for e in entries if any(l not in e["title"] for l in LANGS)
            and (include_all or e.get("safety") == "kid-safe")]
    rank = {l: i for i, l in enumerate(LEVELS)}
    return sorted(todo, key=lambda e: (not e["id"].startswith("kids-"), rank.get(e.get("level"), 9), e["id"]))


def main():
    from dotenv import load_dotenv
    import anthropic
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="max entries per file (for testing)")
    ap.add_argument("--all", action="store_true", help="also translate entries that are not kid-safe")
    args = ap.parse_args()
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def ask(entry):
        msg = client.messages.create(model=MODEL, max_tokens=1000, messages=[{"role": "user", "content": PROMPT.format(
            levels=LEVELS, title=entry["title"]["en"], desc=entry["desc"]["en"])}])
        return msg.content[0].text

    for name in ("learn", "build", "kids"):
        path = DATA / f"{name}.json"
        if not path.exists():
            continue
        entries = json.loads(path.read_text(encoding="utf-8"))
        todo = pick_todo(entries, args.all)[: args.limit]

        def work(e):
            try:
                return e, translate_entry(ask, e), None
            except Exception as ex:  # keep going; one bad entry must not stop the batch
                return e, None, ex
        done = 0
        with ThreadPoolExecutor(WORKERS) as pool:
            for e, out, err in pool.map(work, todo):  # results come back in order; only this thread writes
                done += 1
                if err:
                    print(f"{name}: skipped {e['id']} ({type(err).__name__}: {err})")
                    continue
                apply_result(e, out)
                print(f"{name}: {done}/{len(todo)}")
                path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
