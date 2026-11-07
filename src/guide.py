"""'What should I learn?' guide.

Takes only multiple-choice answers (no free text, nothing stored), so no personal
data is collected from children and prompt injection isn't possible. The AI may
only pick from entry ids we pass in, so it can never invent a link.
Falls back to simple keyword/level matching when there is no API key or the call fails.
"""
import json
import os

GOALS = {
    "games": ["game", "scratch", "play"],
    "art": ["art", "draw", "music", "creative", "animation", "design"],
    "web": ["web", "html", "css", "javascript", "site"],
    "general": [],
}
AGES = ["5-7", "8-10", "11-13"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
MODEL = "claude-haiku-5-5"
PATH_LEN = 6


def candidates(entries, goal, level, limit=40):
    words = GOALS.get(goal, [])
    scored = []
    for e in entries:
        if e.get("level") and e["level"] != level:
            continue
        text = (e["title"]["en"] + " " + e["desc"]["en"] + " " + e["category"]).lower()
        score = sum(w in text for w in words) + (1 if e.get("age_group") else 0)
        scored.append((score, e))
    scored.sort(key=lambda t: -t[0])
    return [e for _, e in scored[:limit]]


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
    return json.loads(msg.content[0].text)["ids"]


def build_path(entries, age, goal, level):
    pool = candidates(entries, goal, level)
    by_id = {e["id"]: e for e in pool}
    ids = []
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            ids = [i for i in ai_pick(pool, age, goal, level) if i in by_id]
        except Exception:
            ids = []
    if not ids:  # fallback
        ids = [e["id"] for e in pool]
    return [by_id[i] for i in ids[:PATH_LEN]]
