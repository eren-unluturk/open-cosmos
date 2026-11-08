"""Load the JSON catalog once. No Flask here, so tests can import it."""
import json
from pathlib import Path

import delivery

DATA = Path(__file__).parent / "data"
SIDES = ("learn", "build", "kids")

_entries = None
_by_id = None
_guides = None
_lessons = None
_lesson_by_id = None
_lesson_by_entry = None


def _read_json(name, default):
    path = DATA / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def _text_nodes(node, out):
    """Collect every {"en": ...} text dict inside a guide."""
    if isinstance(node, dict):
        if isinstance(node.get("en"), str) and all(len(k) == 2 for k in node):
            out.append(node)
            return
        for v in node.values():
            _text_nodes(v, out)
    elif isinstance(node, list):
        for v in node:
            _text_nodes(v, out)


def _add_guide_translations(guides, overlay):
    """guides.json text is {"en": ...}. Add other languages from guides_translated.json (English text -> {lang: text}).

    All or nothing per guide and language: a guide is shown in a language only when every one of its texts
    is translated, so a half-translated guide never mixes two languages. guides.json itself stays English-only.
    """
    for guide in list(guides.get("fallback", {}).values()) + list(guides.get("groups", {}).values()):
        nodes = []
        _text_nodes(guide, nodes)
        for lang in ("es", "ar", "hi", "pt"):
            if nodes and all(lang in overlay.get(n["en"], {}) for n in nodes):
                for n in nodes:
                    n.setdefault(lang, overlay[n["en"]][lang])


def _load_lessons():
    """guides.json and lessons.json are written by the data lead (scripts/build_guides.py, fetch_lessons.py)."""
    global _guides, _lessons, _lesson_by_id, _lesson_by_entry
    if _lessons is None:
        _guides = _read_json("guides.json", {"fallback": {}, "groups": {}})
        _add_guide_translations(_guides, _read_json("guides_translated.json", {}))
        _lessons = _read_json("lessons.json", [])
        _lesson_by_id = {x["id"]: x for x in _lessons}
        _lesson_by_entry = {x["entry_id"]: x for x in _lessons}


def _read(side):
    path = DATA / f"{side}.json"
    if not path.exists():
        return []
    entries = json.loads(path.read_text(encoding="utf-8"))
    for e in entries:
        e["side"] = side
        e.update(delivery.classify(e))  # adds delivery, kind, attribution (never saved to disk)
    return entries


def _load():
    global _entries, _by_id
    if _entries is None:
        _entries = {side: _read(side) for side in SIDES}
        _by_id = {e["id"]: e for es in _entries.values() for e in es}
        _load_lessons()
        for e in _by_id.values():  # which entries have a lesson on this site
            lesson = _lesson_by_entry.get(e["id"])
            e["lesson_id"] = lesson["id"] if lesson else None


def entries(side=None):
    """All entries, or just one side (learn | build | kids)."""
    _load()
    if side is None:
        return [e for side in SIDES for e in _entries[side]]
    return _entries.get(side, [])


def get(entry_id):
    _load()
    return _by_id.get(entry_id)


def text(entry, field, lang):
    """Return (text, fell_back). Falls back to English when the language is missing."""
    value = entry.get(field) or {}
    if value.get(lang):
        return value[lang], False
    return value.get("en", ""), lang != "en"


def _fold(s):
    """Lowercase and strip accents so 'Numeros' finds 'Números'."""
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def matches(entry, q, lang):
    """True if every word in q appears in the title, desc or category (shown language + English)."""
    haystack = _fold(" ".join([
        entry.get("category", ""),
        entry.get("tag", ""),
        text(entry, "title", lang)[0], entry["title"].get("en", ""),
        text(entry, "desc", lang)[0], entry["desc"].get("en", ""),
    ]))
    return all(word in haystack for word in _fold(q).split())


def guides():
    """The guides.json document: {"fallback": {...}, "groups": {...}}."""
    _load_lessons()
    return _guides


def lessons():
    """All adapted lessons (a list, in file order)."""
    _load_lessons()
    return _lessons


def lesson_by_id(lesson_id):
    _load_lessons()
    return _lesson_by_id.get(lesson_id)


def lesson_for_entry(entry_id):
    _load_lessons()
    return _lesson_by_entry.get(entry_id)

_problems = None
_problem_by_id = None


def _load_problems():
    global _problems, _problem_by_id
    if _problems is None:
        _problems = _read_json("problems.json", [])
        _problem_by_id = {p["id"]: p for p in _problems}


def problems():
    """All coding problems (src/data/problems.json, built by scripts/build_problems.py)."""
    _load_problems()
    return _problems


def problem(problem_id):
    _load_problems()
    return _problem_by_id.get(problem_id)
