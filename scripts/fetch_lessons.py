"""Build src/data/lessons.json from our adapted CS Unplugged lessons (CC BY-SA 4.0).

The lesson text lives in scripts/lesson_content/*.py (rewritten and shortened by Claude Code from the
CS Unplugged lesson plans: no long passages, no images). This script adds the metadata that must be exact:
entry_id (from kids.json), age_group, duration (from the repo's lessons.yaml), attribution and license.
Order: ages 5-7, then 8-10, then 11-13. Only kid-safe, open-content entries get a lesson.

Usage: python scripts/fetch_lessons.py          (uses the network once for lesson durations; falls back to defaults)
"""
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
DATA = ROOT / "src" / "data"
AGES = ["5-7", "8-10", "11-13"]
ATTRIBUTION = ("Adapted from CS Unplugged by the University of Canterbury Computer Science Education Research Group "
               "(CS Unplugged), licensed CC BY-SA 4.0.")
CHANGES = "Simplified, shortened and translated by Hackcessability with AI"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"


def T(s):
    return {"en": s}


def durations():
    try:
        import fetch_kids as k
        out = {}
        S = k.get("structure/structure.yaml")
        for t in re.findall(r"^  - ([a-z0-9-]+)\s*$", S.split("age-groups:")[0], re.M):
            for slug, m in k.parse_durations(k.get(f"structure/{t}/lessons/lessons.yaml")).items():
                out[f"{t}__{slug}"] = m
        return out
    except Exception:  # offline: keep the file buildable with a default
        return {}


def content():
    merged = {}
    for name in ("ages_5_7", "ages_8_10"):
        merged.update(importlib.import_module(f"lesson_content.{name}").L)
    return merged


def main():
    kids = json.loads((DATA / "kids.json").read_text(encoding="utf-8"))
    by_key = {}
    for e in kids:
        m = re.match(r"https://www\.csunplugged\.org/en/topics/([a-z0-9-]+)/([a-z0-9-]+)/$", e["url"])
        if m and e["reuse"] == "open-content" and e["safety"] == "kid-safe" and not e["title"]["en"].endswith("(unit)"):
            by_key[f"{m.group(1)}__{m.group(2)}"] = e
    text, mins = content(), durations()
    old = {}
    p = DATA / "lessons.json"
    if p.exists():
        old = {ls["entry_id"]: ls for ls in json.loads(p.read_text(encoding="utf-8"))}
    lessons = []
    for key, c in text.items():
        e = by_key.get(key)
        if e is None:
            print(f"skip {key}: no matching open-content, kid-safe entry")
            continue
        prev = old.get(e["id"], {})
        title = e["title"]["en"]
        lessons.append({
            "id": "lesson-" + e["id"].split("-", 1)[1], "entry_id": e["id"],
            "title": {**prev.get("title", {}), "en": title},
            "age_group": e["age_group"],
            "duration_minutes": mins.get(key) or prev.get("duration_minutes") or 45,
            "summary": {**prev.get("summary", {}), "en": c["summary"]},
            "objectives": {**prev.get("objectives", {}), "en": c["objectives"]},
            "materials": {**prev.get("materials", {}), "en": c["materials"]},
            "steps": {**prev.get("steps", {}), "en": c["steps"]},
            "talk_about": {**prev.get("talk_about", {}), "en": c["talk_about"]},
            "grown_up_note": {**prev.get("grown_up_note", {}), "en": c["grown_up"]},
            "license": "CC-BY-SA-4.0", "attribution": ATTRIBUTION, "source_url": e["url"],
            "license_url": LICENSE_URL, "changes_made": CHANGES,
        })
    lessons.sort(key=lambda l: (AGES.index(l["age_group"]), l["title"]["en"].lower()))
    p.write_text(json.dumps(lessons, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    left = sorted(set(by_key) - set(text))
    print(f"lessons.json: {len(lessons)} lessons; kid-safe CS Unplugged lessons without text yet: {len(left)} {left}")


if __name__ == "__main__":
    main()
