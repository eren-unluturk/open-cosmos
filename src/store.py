"""Load the JSON catalog once. No Flask here, so tests can import it."""
import json
from pathlib import Path

import delivery

DATA = Path(__file__).parent / "data"
SIDES = ("learn", "build", "kids")

_entries = None
_by_id = None


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


# ---------------------------------------------------------------------------
# Lesson text (CS Unplugged, CC BY-SA 4.0). Only for entries with delivery == "hostable".
#   lessons.json             written by scripts/fetch_lessons.py. English, plus the project's own
#                            human translations (Spanish) where they exist.
#   lessons_translated.json  AI translations we added, {entry_id: {lang: markdown}}.
# ---------------------------------------------------------------------------
_lesson_text = None
_lesson_ai = None
_md = None


def _load_lesson_files():
    global _lesson_text, _lesson_ai
    if _lesson_text is None:
        def read(name):
            p = DATA / name
            return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        _lesson_text = {k: v["body"] for k, v in read("lessons.json").items()}
        _lesson_ai = read("lessons_translated.json")


def lesson(entry_id, lang):
    """Lesson text for an entry, or None. Picks the human translation, then the AI one, then English.
    Returns {"markdown", "lang", "ai", "fallback"}."""
    _load_lesson_files()
    human = _lesson_text.get(entry_id)
    if not human:
        return None
    if lang in human:
        return {"markdown": human[lang], "lang": lang, "ai": False, "fallback": False}
    ai = _lesson_ai.get(entry_id, {})
    if lang in ai:
        return {"markdown": ai[lang], "lang": lang, "ai": True, "fallback": False}
    return {"markdown": human["en"], "lang": "en", "ai": False, "fallback": lang != "en"}


def render_markdown(md):
    """Markdown to safe HTML. Raw HTML in the source is escaped; unsafe link schemes are dropped."""
    global _md
    if _md is None:
        from markdown_it import MarkdownIt
        _md = MarkdownIt("commonmark", {"html": False, "linkify": False})
    tokens = _md.parse(md)
    for block in tokens:
        for tok in block.children or []:
            if tok.type == "link_open":
                tok.attrSet("rel", "noopener noreferrer")
    return _md.renderer.render(tokens, _md.options, {})
