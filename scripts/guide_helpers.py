"""Pure helpers for guides and lessons. No Flask, no network; importable by src/ and tests.

An entry always resolves to a guide: a handwritten group guide if one exists, else the fallback
for its topic. Text in guides is {"en": "..."} dicts (translate later; keep {placeholders} intact).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REMOVED = ROOT / "scripts" / "cache" / "removed_links.json"
AGES = ["5-7", "8-10", "11-13", "teen+"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
PLACEHOLDERS = {"age", "level", "minutes", "sessions", "entry_title"}
TOPICS = ["games", "art", "web", "general", "systems", "security", "other"]
LEAVING = ("We don't control that site. Ask a grown-up before you go. Check the original for details.")
LANGUAGE_TIP = ("This site may not be in your language. Your browser can translate the page: look for the translate button near the address bar, or ask a grown-up to help.")


def side_of(entry):
    return entry["id"].split("-")[0]


def group_of(entry):
    """Group key for handwritten guides: '<side>:<category>' (CS Unplugged units are their own categories)."""
    return f"{side_of(entry)}:{entry['category']}"


def guide_for(entry, guides, lessons=None):
    """Handwritten group guide, else the topic fallback. If the entry has a lesson, the last slide is go_lesson.

    Returns a new dict: {"guide": <guide>, "source": "group"|"fallback", "slides": [...]}.
    """
    g = guides.get("groups", {}).get(group_of(entry))
    source = "group"
    if g is None:
        g = guides["fallback"].get(entry.get("topic")) or guides["fallback"]["other"]
        source = "fallback"
    slides = list(g["slides"])
    if lessons is not None and lesson_for(entry, lessons) is not None and g.get("go_lesson_slide"):
        slides[-1] = g["go_lesson_slide"]
    return {"guide": g, "source": source, "slides": slides}


def build_timeline(entry, age=None):
    """Rule-based plan: {"minutes": per session, "sessions": count, "total_minutes": int, "label": 'estimate'}."""
    age = age if age in AGES else entry.get("age_group", "11-13")
    base = {"5-7": (15, 3), "8-10": (25, 4), "11-13": (40, 4), "teen+": (45, 5)}[age]
    level = entry.get("level", "Beginner")
    extra = {"Beginner": (1.0, 0), "Intermediate": (1.4, 2), "Advanced": (1.8, 4)}[level]
    minutes = int(round(base[0] * extra[0] / 5.0) * 5)
    sessions = base[1] + extra[1] + (1 if side_of(entry) == "build" else 0)
    if side_of(entry) == "kids":  # lessons are one sitting plus follow-ups; use the lesson length if the entry says it
        sessions = max(2, sessions - 1)
    return {"minutes": minutes, "sessions": sessions, "total_minutes": minutes * sessions, "label": "estimate"}


def _removed_urls():
    return set(json.loads(REMOVED.read_text(encoding="utf-8"))) if REMOVED.exists() else set()


def related_entries(entry, entries, n=4, age=None, removed=None):
    """Up to n kid-safe, age-appropriate, live entries: same category first, then same topic at the next level."""
    removed = _removed_urls() if removed is None else removed
    cap = AGES.index(age if age in AGES else entry.get("age_group", "teen+"))

    def ok(e):
        return (e["id"] != entry["id"] and e.get("safety") == "kid-safe" and e["url"] not in removed
                and AGES.index(e["age_group"]) <= cap)

    pool = [e for e in entries if ok(e)]
    same_cat = [e for e in pool if e["category"] == entry["category"]]
    lvl = LEVELS.index(entry["level"])
    nxt = LEVELS[min(lvl + 1, len(LEVELS) - 1)]
    same_topic = [e for e in pool if e["topic"] == entry["topic"] and e["level"] == nxt and e not in same_cat]
    out, seen = [], set()
    for e in sorted(same_cat, key=lambda e: (abs(LEVELS.index(e["level"]) - lvl), e["id"])) + sorted(same_topic, key=lambda e: e["id"]):
        if e["id"] not in seen:
            seen.add(e["id"])
            out.append(e)
    return out[:n]


def lesson_for(entry, lessons):
    """Our adapted lesson for an open-content entry, else None."""
    if entry.get("reuse") != "open-content":
        return None
    for ls in lessons:
        if ls["entry_id"] == entry["id"]:
            return ls
    return None


def fill(text, entry, age=None, lang="en"):
    """Replace {placeholders} in a guide string for one entry."""
    t = build_timeline(entry, age)
    vals = {"age": age or entry.get("age_group", ""), "level": entry.get("level", ""),
            "minutes": t["minutes"], "sessions": t["sessions"],
            "entry_title": entry["title"].get(lang) or entry["title"]["en"]}
    for k, v in vals.items():
        text = text.replace("{" + k + "}", str(v))
    return text
