"""'What should I learn?' guide.

Takes only multiple-choice answers (no free text, nothing stored), so no personal
data is collected from children and prompt injection isn't possible. The AI may
only re-order entry ids we pass in, so it can never invent a link.

Selection rules (pure code, no API key needed):
  1. kid-safe entries only, whatever the grown-up switch says.
  2. entry age_group <= chosen age (teen+ is never shown to a child).
  3. goal topic first, then "general" topic, at the chosen level.
  4. still short? repeat at the next lower level.
  5. show easier levels first.
  6. ages 5-10 only get Beginner entries, whatever level was picked.
  7. the path may be shorter than PATH_LEN. The page says "more is coming". Never padded with unsafe entries.
"""
import json
import os

import gate

GOALS = {"games": "games", "art": "art", "web": "web", "general": "general"}
AGES = ["5-7", "8-10", "11-13"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
AGE_ORDER = ["5-7", "8-10", "11-13", "teen+"]
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")
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


def ai_pick(pool, age, goal, level):
    import anthropic  # imported lazily so the app runs without the key
    client = anthropic.Anthropic()
    menu = [{"id": e["id"], "title": e["title"]["en"], "desc": e["desc"]["en"]} for e in pool]
    prompt = (
        f"A child aged {age} is just starting to learn programming. Goal: {goal}. Level: {level}.\n"
        f"Choose the {PATH_LEN} best resources from this list and order them as a learning path "
        "(easiest first). Prefer free, friendly, hands-on ones. Use ONLY ids from the list.\n"
        'Return ONLY JSON: {"ids": ["..."]}\n\n' + json.dumps(menu)
    )
    msg = client.messages.create(model=MODEL, max_tokens=300,
                                 messages=[{"role": "user", "content": prompt}])
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    return json.loads(text)["ids"]


def build_path(entries, age, goal, level):
    pool = candidates(entries, age, goal, level)
    by_id = {e["id"]: e for e in pool}
    ids = []
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            ids = list(dict.fromkeys(i for i in ai_pick(pool, age, goal, level) if i in by_id))
        except Exception:
            ids = []
    if len(ids) < PATH_LEN:  # AI off, failed, or returned too few: fill from the ranked pool
        ids += [e["id"] for e in pool if e["id"] not in ids]
    chosen = [by_id[i] for i in ids[:PATH_LEN]]
    # Easier first. sort() is stable, so the AI/ranked order holds inside a level.
    chosen.sort(key=lambda e: LEVELS.index(e["level"]))
    return chosen
