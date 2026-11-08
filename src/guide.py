"""'What should I learn?' guide.

Takes only multiple-choice answers (no free text, nothing stored), so no personal
data is collected from children and prompt injection isn't possible. There is no AI call
at all: the path is picked by the rules below, so it can never invent a link.

Selection rules (pure code, no API key):
  1. kid-safe entries only, whatever the grown-up switch says.
  2. entry age_group <= chosen age (teen+ is never shown to a child).
  3. goal topic first, then "general" topic, at the chosen level.
  4. still short? repeat at the next lower level.
  5. show easier levels first.
  6. ages 5-10 only get Beginner entries, whatever level was picked.
  7. the path may be shorter than PATH_LEN. The page says "more is coming". Never padded with unsafe entries.
"""
import gate

GOALS = {"games": "games", "art": "art", "web": "web", "general": "general"}
AGES = ["5-7", "8-10", "11-13"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
AGE_ORDER = ["5-7", "8-10", "11-13", "teen+"]
PATH_LEN = 6


def age_fits(entry, age):
    group = entry.get("age_group")
    return group in AGE_ORDER and AGE_ORDER.index(group) <= AGE_ORDER.index(age)


def candidates(entries, age, goal, level, limit=40):
    """Ranked pool: best fit first."""
    topic = GOALS.get(goal, "general")
    # Children under 11 only get Beginner. The data has nothing above it that fits them.
    level_idx = 0 if AGE_ORDER.index(age) <= 1 else LEVELS.index(level)
    ranked = []
    for e in entries:
        if gate.tier(e) != gate.KID_SAFE or not age_fits(e, age):
            continue
        if e.get("level") not in LEVELS or LEVELS.index(e["level"]) > level_idx:
            continue
        distance = level_idx - LEVELS.index(e["level"])  # 0 = chosen level
        if e.get("topic") == topic:
            match = 0
        elif e.get("topic") == "general":
            match = 1
        else:
            continue
        kids_bonus = 0 if (e.get("side") == "kids" and AGE_ORDER.index(age) <= 1) else 1
        ranked.append(((distance, match, kids_bonus), e))
    ranked.sort(key=lambda t: t[0])
    return [e for _, e in ranked[:limit]]


def build_path(entries, age, goal, level):
    """Rule-based only: no API, no key, nothing sent anywhere. Easier first."""
    pool = candidates(entries, age, goal, level)
    chosen = pool[:PATH_LEN]
    # Easier first. sort() is stable, so the ranked order holds inside a level.
    chosen.sort(key=lambda e: LEVELS.index(e["level"]))
    return chosen
