"""Load the JSON catalog once. No Flask here, so tests can import it."""
import json
from pathlib import Path

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
