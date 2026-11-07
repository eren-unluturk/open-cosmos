"""Galaxy model for the frontend.

Turns the flat entry lists (learn/build/kids) into a space map:
    galaxy (subject, e.g. "Programming languages")
      -> system (sub-track, e.g. "Python")
         -> stops (the existing open-licensed entries, ordered easiest first)

Nothing here creates content: every stop is an existing entry, matched by its
tag / topic / title / category. Rules are plain regexes so the team can tweak them.
"""
import datetime
import hashlib
import math
import re

import gate

LEVEL_RANK = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
AGE_RANK = {"5-7": 0, "8-10": 1, "11-13": 2, "teen+": 3}
LEVEL_ICON = {"Beginner": "robot", "Intermediate": "alien", "Advanced": "astronaut"}  # SVG symbol ids


def _rx(pattern):
    r = re.compile(pattern, re.I)
    return lambda e: bool(r.search(_text(e)))


def _text(e):
    return f"{e['title']['en']} {e['desc']['en']} {e['category']} {e.get('tag', '')}"


def _tag(*names):
    names = {n.lower() for n in names}
    return lambda e: any(t.strip().lower() in names for t in re.split(r"[/,]", e.get("tag") or ""))


def _any(*fns):
    return lambda e: any(f(e) for f in fns)


def _cat(prefix):
    return lambda e: e["category"].lower().startswith(prefix.lower())


def _side(side):
    return lambda e: e["id"].startswith(side + "-")


def _topic(*topics):
    return lambda e: e.get("topic") in topics


_py = _any(_tag("Python"), _rx(r"\bpython\b"))
_java = _any(_tag("Java", "Kotlin", "Scala"), _rx(r"\bjava\b(?!\s*script)"))
_web = _any(_tag("JavaScript", "TypeScript", "Node.js"), _topic("web"), _rx(r"\b(html|css|javascript)\b"))

# Each system: id, look (how it is drawn on the orbit map), match rule.
# Order matters only for display; an entry can live in several systems.
GALAXIES = [
    {"id": "code", "icon": "g-code", "hue": "violet", "systems": [
        {"id": "python", "look": "sun", "match": _py},
        {"id": "java", "look": "star", "match": _java},
        {"id": "web", "look": "spiral", "match": _web},
        {"id": "more-langs", "look": "ringed",
         "match": lambda e: (bool(e.get("tag")) or e["category"] == "Programming Languages")
         and not (_py(e) or _java(e) or _web(e))},
    ]},
    {"id": "art", "icon": "g-art", "hue": "pink", "systems": [
        {"id": "drawing", "look": "sun", "match": _rx(r"pixel|draw|icon|svg|paint|illustrat|\bdesign|colou?r|font|typograph")},
        {"id": "animation", "look": "spiral", "match": _rx(r"animat|motion|\bgif|video|film")},
        {"id": "3d", "look": "ringed", "match": _rx(r"\b3d\b|render|ray ?trac|graphics|opengl|webgl|shader|voxel")},
        {"id": "music", "look": "star", "match": _rx(r"music|audio|sound|synth|midi")},
    ]},
    {"id": "games", "icon": "g-games", "hue": "gold", "systems": [
        {"id": "make-games", "look": "sun", "match": lambda e: _side("build")(e) and (_topic("games")(e) or _cat("Build your own Game")(e))},
        {"id": "game-worlds", "look": "ringed", "match": lambda e: not _side("build")(e) and (_topic("games")(e) or _rx(r"minecraft|scratch|game")(e))},
    ]},
    {"id": "science", "icon": "g-science", "hue": "teal", "systems": [
        {"id": "binary", "look": "sun", "match": _cat("CS Unplugged: Binary")},
        {"id": "search-sort", "look": "spiral", "match": _any(_cat("CS Unplugged: Search"), _cat("CS Unplugged: Sorting"), _cat("CS Unplugged: Data structures"))},
        {"id": "kidbots", "look": "star", "match": _cat("CS Unplugged: Kidbots")},
        {"id": "codes-pictures", "look": "ringed", "match": _any(_cat("CS Unplugged: Error"), _cat("CS Unplugged: Image"))},
        {"id": "math-science", "look": "moon", "match": lambda e: not _side("kids")(e) and _rx(r"\bmath|physics|chemistr|astronom|\bsteam\b|\bscience\b(?! fiction)")(e)},
    ]},
    {"id": "robotics", "icon": "robot", "hue": "violet", "systems": [
        {"id": "robots", "look": "sun", "match": _rx(r"robot|drone|\bfpv\b|plotter")},
        {"id": "tiny-computers", "look": "ringed", "match": _rx(r"raspberry|arduino|micro:?bit|microcontroller|circuitpython|esp32|embedded")},
        {"id": "chat-bots", "look": "star", "match": _rx(r"\bbots?\b|chatbot|chatgpt|conversational ai")},
    ]},
    {"id": "electricity", "icon": "g-electricity", "hue": "gold", "systems": [
        {"id": "circuits", "look": "sun", "match": _rx(r"electronic|circuit|electric(?!on)|solder|\bfpga|\biot\b|bluetooth|\bradio|\bsdr\b|ads-b")},
        {"id": "inside-computers", "look": "spiral", "match": _rx(r"nand2tetris|\bcpu\b|processor|logic gate|computer architecture|emulator|virtual machine|assembly|operating system")},
    ]},
    {"id": "environment", "icon": "g-environment", "hue": "teal", "systems": [
        {"id": "earth-maps", "look": "ringed", "match": _rx(r"\bmaps?\b|\bgeo|\bgis\b|\bearth\b|weather|climat|ocean")},
        {"id": "green-energy", "look": "sun", "match": _rx(r"energy|sustainab|\bgreen\b|ecolog|environmental|carbon|solar")},
    ]},
    {"id": "health", "icon": "g-health", "hue": "pink", "systems": [
        {"id": "body-mind", "look": "sun", "match": _rx(r"health|medic|mental|biolog|bioinformatic|fitness|neuro")},
        {"id": "people-history", "look": "spiral", "match": _rx(r"history|humanit|diversity|empathy|psycholog|econom|social science|ethic")},
        {"id": "access", "look": "star", "match": _rx(r"accessib|\ba11y\b|assistive|screen ?reader|inclusive")},
    ]},
]

# Rough "connections" between galaxies, drawn as constellation lines.
LINKS = [("code", "games"), ("code", "art"), ("art", "games"), ("code", "robotics"),
         ("robotics", "electricity"), ("electricity", "environment"), ("science", "environment"),
         ("science", "health"), ("science", "code"), ("health", "environment")]

# Where each galaxy sits on the constellation map (viewBox 1000 x 640).
STAR_POS = {"code": (500, 300), "art": (250, 170), "games": (330, 450), "science": (720, 170),
            "robotics": (640, 470), "electricity": (850, 420), "environment": (900, 200), "health": (110, 360)}

PLAIN_REASONS = {  # safety_reasons -> plain words (UI translates the keys)
    "security-tooling", "external-forum", "social-platform", "account-required",
    "unvetted-external-site", "not-kid-oriented-topic", "off-topic", "unclassified",
}


def stop_sort_key(e):
    return (LEVEL_RANK.get(e.get("level"), 1), AGE_RANK.get(e.get("age_group"), 3),
            0 if e["id"].startswith("kids-") else 1, 0 if e.get("safety") == "kid-safe" else 1,
            e["title"]["en"].lower())


def difficulty(e):
    """1-5 dots for the card, from level + youngest age."""
    base = {"Beginner": 1, "Intermediate": 3, "Advanced": 4}.get(e.get("level"), 3)
    if e.get("level") == "Beginner" and AGE_RANK.get(e.get("age_group"), 0) >= 2:
        base = 2
    if e.get("level") == "Advanced" and e.get("age_group") == "teen+":
        base = 5
    return base


def kind(e):
    if e["id"].startswith("kids-"):
        return "kind_unplugged"
    if e["id"].startswith("build-"):
        return "kind_project"
    return "kind_list"


class Universe:
    """Everything the templates need, built once per request from visible entries."""

    def __init__(self, entries, grownup=False):
        self.all = [e for e in entries if gate.tier(e) != gate.ADULT_ONLY]
        self.grownup = grownup
        self.by_id = {e["id"]: e for e in self.all}
        self.galaxies = []
        self.membership = {}  # entry id -> [(galaxy id, system id)]
        for g in GALAXIES:
            systems = []
            for s in g["systems"]:
                everyone = sorted((e for e in self.all if s["match"](e)), key=stop_sort_key)
                visible = [e for e in everyone if self.visible(e)]
                systems.append({"id": s["id"], "look": s["look"], "galaxy": g["id"],
                                "stops": visible, "hidden": len(everyone) - len(visible)})
                for e in everyone:
                    self.membership.setdefault(e["id"], []).append((g["id"], s["id"]))
            total = sum(len(s["stops"]) for s in systems)
            hidden = sum(s["hidden"] for s in systems)
            self.galaxies.append({**{k: g[k] for k in ("id", "icon", "hue")}, "systems": systems,
                                  "count": total, "hidden": hidden, "pos": STAR_POS[g["id"]]})
        self.g = {g["id"]: g for g in self.galaxies}

    def visible(self, e):
        return gate.visible(e, self.grownup)

    def system(self, gid, sid):
        g = self.g.get(gid)
        return next((s for s in g["systems"] if s["id"] == sid), None) if g else None

    def home_of(self, eid):
        m = self.membership.get(eid) or []
        return m[0] if m else (None, None)

    def suggestions(self, n=3, level=None):
        """'Today's suggestions': one stop from n different galaxies, rotating daily."""
        seed = int(hashlib.sha1(datetime.date.today().isoformat().encode()).hexdigest(), 16)
        out = []
        gals = [g for g in self.galaxies if g["count"]]
        for i in range(len(gals)):
            g = gals[(seed + i) % len(gals)]
            pool = [(s, e) for s in g["systems"] for e in s["stops"]
                    if (not level or e["level"] == level)]
            if not pool:
                continue
            pool = [p for p in pool if p[1]["category"] != "Programming Languages"] or pool
            easy = ([p for p in pool if AGE_RANK.get(p[1]["age_group"], 3) <= 1]
                    or [p for p in pool if p[1]["level"] == "Beginner"] or pool)
            s, e = easy[(seed // 7 + i) % len(easy)]
            out.append({"e": e, "galaxy": g["id"], "system": s["id"]})
            if len(out) == n:
                break
        return out

    def row(self, g, level=None, limit=10):
        """Home row for one galaxy: interleave the first stops of each system."""
        lanes = [[(s["id"], e) for e in s["stops"] if not level or e["level"] == level] for s in g["systems"]]
        out, seen, i = [], set(), 0
        while len(out) < limit and any(i < len(l) for l in lanes):
            for lane in lanes:
                if i < len(lane) and lane[i][1]["id"] not in seen and len(out) < limit:
                    seen.add(lane[i][1]["id"])
                    out.append({"e": lane[i][1], "galaxy": g["id"], "system": lane[i][0], "step": i + 1})
            i += 1
        return out

    def orbit_layout(self, g, max_planets=6):
        """Positions for the galaxy page drawing (viewBox 1000 x 720)."""
        cx, cy = 500, 370
        systems = [s for s in g["systems"] if s["stops"] or s["hidden"]]
        n = max(len(systems), 1)
        placed = []
        for i, s in enumerate(systems):
            ang = math.radians(-130 + 360 * i / n)
            sx, sy = cx + 330 * math.cos(ang), cy + 235 * math.sin(ang)
            planets = []
            stops = s["stops"][:max_planets]
            for j, e in enumerate(stops):
                pa = math.radians(-90 + 360 * j / max(len(stops), 1) + i * 25)
                r = 92 + (j % 2) * 18
                planets.append({"e": e, "x": round(sx + r * math.cos(pa), 1),
                                "y": round(sy + r * 0.78 * math.sin(pa), 1), "n": j + 1})
            placed.append({"s": s, "x": round(sx, 1), "y": round(sy, 1), "planets": planets})
        return {"cx": cx, "cy": cy, "systems": placed}

    def neighbours(self, gid, sid, eid):
        """Prev/next on the path and 'suggested' stops for a lesson page."""
        s = self.system(gid, sid)
        stops = s["stops"] if s else []
        idx = next((i for i, e in enumerate(stops) if e["id"] == eid), None)
        nxt = stops[idx + 1] if idx is not None and idx + 1 < len(stops) else None
        suggested = []
        if nxt:
            suggested.append({"e": nxt, "galaxy": gid, "system": sid})
        # a hands-on project from the same system (like "Python F1 project")
        for e in stops[(idx or 0) + 1:]:
            if e["id"].startswith("build-") and e is not nxt:
                suggested.append({"e": e, "galaxy": gid, "system": sid})
                break
        # and the first stop of a sibling system
        g = self.g.get(gid)
        for other in (g["systems"] if g else []):
            if other["id"] != sid and other["stops"] and len(suggested) < 3:
                suggested.append({"e": other["stops"][0], "galaxy": gid, "system": other["id"]})
        return {"index": idx, "stops": stops, "suggested": suggested[:3]}

    def search(self, q="", gid=None, level=None):
        q = (q or "").strip().lower()
        pool = self.all if not gid else [e for s in self.g[gid]["systems"] for e in s["stops"]]
        out, seen = [], set()
        for e in sorted(pool, key=stop_sort_key):
            if e["id"] in seen or not self.visible(e):
                continue
            if level and e["level"] != level:
                continue
            if q and q not in " ".join([_text(e)] + list(e["title"].values()) + list(e["desc"].values())).lower():
                continue
            seen.add(e["id"])
            g, s = self.home_of(e["id"])
            out.append({"e": e, "galaxy": g, "system": s})
        return out
