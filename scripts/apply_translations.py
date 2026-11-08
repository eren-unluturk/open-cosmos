"""Merge hand-written translations (scripts/translation_content/*.py) into src/data/*.json.

No API key needed. Each content module exposes build() -> {entry id: {"title": {lang: str}, "desc": {lang: str}}}.
Existing text for other languages is kept; `ai_translated` gets the languages written here (they are AI-written).
Idempotent. Run after fetch/categorize and before mark_reuse/freeze checks. Usage: python scripts/apply_translations.py
"""
import importlib
import json
import pkgutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
DATA = ROOT / "src" / "data"
LANGS = ("es", "ar", "hi", "pt")


def collect():
    merged = {}
    for m in pkgutil.iter_modules([str(ROOT / "scripts" / "translation_content")]):
        if m.name.startswith("_"):
            continue
        mod = importlib.import_module(f"translation_content.{m.name}")
        for eid, tr in mod.build().items():
            assert eid not in merged, f"duplicate translation for {eid}"
            merged[eid] = tr
    return merged


def main():
    tr = collect()
    seen = set()
    for name in ("learn", "build", "kids"):
        path = DATA / f"{name}.json"
        entries = json.loads(path.read_text(encoding="utf-8"))
        changed = 0
        for e in entries:
            t = tr.get(e["id"])
            if not t:
                continue
            seen.add(e["id"])
            for lang in LANGS:
                if lang in t["title"] and lang in t["desc"]:
                    if e["title"].get(lang) != t["title"][lang] or e["desc"].get(lang) != t["desc"][lang]:
                        changed += 1
                    e["title"][lang] = t["title"][lang]
                    e["desc"][lang] = t["desc"][lang]
            e["ai_translated"] = sorted(set(e.get("ai_translated", [])) | {l for l in LANGS if l in t["title"] and l in t["desc"]})
        path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{name}: {changed} translations written")
    missing = sorted(set(tr) - seen)
    if missing:
        print("WARNING: no such entry ids:", missing)


if __name__ == "__main__":
    main()
