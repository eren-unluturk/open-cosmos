"""Load the catalog. No Flask here, so tests can import it.

Source: bundled JSON in src/data (always works) or Supabase (CONTENT_SOURCE=auto|supabase). With Supabase the rows
are fetched server-side with the anon key, cached for 10 minutes, and rebuilt into exactly the same files; on ANY
error, timeout, empty result or schema mismatch we log one short warning and use the bundled JSON.
"""
import copy
import json
import logging
import os
import sys
import time
from pathlib import Path

import content_rows
import delivery

DATA = Path(__file__).parent / "data"
SIDES = ("learn", "build", "kids")

_entries = None
_by_id = None
_guides = None
_lessons = None
_lesson_by_id = None
_lesson_by_entry = None


log = logging.getLogger("open_cosmos.store")
CACHE_SECONDS = 600       # a good Supabase download is reused for 10 minutes
RETRY_SECONDS = 120       # after a failed download we stay on JSON this long before trying again

_remote = None            # (fetched_at, files or None) once we have tried
_warned = False


def content_source():
    value = (os.environ.get("CONTENT_SOURCE") or "auto").strip().lower()
    return value if value in ("json", "supabase", "auto") else "auto"


def _remote_enabled():
    if content_source() == "json":
        return False
    if "unittest" in sys.modules and not os.environ.get("OPEN_COSMOS_TEST_REMOTE"):
        return False  # tests never touch the network unless a test turns this on
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_ANON_KEY"))


def _fetch_remote():
    import supabase_client
    return content_rows.files_from_rows(
        supabase_client.fetch_rows(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"]))


def _remote_files():
    """The catalog files from Supabase, or None (use the bundled JSON)."""
    global _remote, _warned
    if not _remote_enabled():
        return None
    if _remote is None:
        try:
            _remote = (time.time(), _fetch_remote())
            _warned = False
        except Exception as exc:  # network, HTTP, JSON, schema: all the same to the visitor
            if not _warned:
                log.warning("Supabase content unavailable (%s); using the bundled JSON.", type(exc).__name__)
                _warned = True
            _remote = (time.time(), None)
    return _remote[1]


def _expire():
    """Forget everything loaded once the cache is old, so the next request reloads (and retries Supabase)."""
    global _remote, _entries, _by_id, _guides, _lessons, _lesson_by_id, _lesson_by_entry, _problems, _problem_by_id, _categories
    if _remote is None:
        return
    ttl = CACHE_SECONDS if _remote[1] is not None else RETRY_SECONDS
    if time.time() - _remote[0] > ttl:
        _remote = None
        _entries = _by_id = _guides = _lessons = _lesson_by_id = _lesson_by_entry = None
        _problems = _problem_by_id = _categories = None


def reset():
    """Drop all caches (used by tests)."""
    global _remote, _warned
    _remote, _warned = None, False
    _expire_all()


def _expire_all():
    global _entries, _by_id, _guides, _lessons, _lesson_by_id, _lesson_by_entry, _problems, _problem_by_id, _categories
    _entries = _by_id = _guides = _lessons = _lesson_by_id = _lesson_by_entry = None
    _problems = _problem_by_id = _categories = None


def _read_json(name, default):
    remote = _remote_files()
    if remote is not None and name in remote:
        return copy.deepcopy(remote[name])
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


LESSON_TEXT_FIELDS = ("summary", "grown_up_note", "objectives", "materials", "steps", "talk_about")


def _add_lesson_translations(lessons, overlay):
    """lessons.json text is {"en": ...}. Add other languages from lessons_overlay.json (English text -> {lang: text}).

    All or nothing per lesson and language, so a lesson page never mixes two languages.
    """
    def pieces(value):
        return value if isinstance(value, list) else [value]

    for ls in lessons:
        for lang in ("es", "ar", "hi", "pt"):
            ok = all(lang in overlay.get(t, {}) for f in LESSON_TEXT_FIELDS for t in pieces(ls[f]["en"]))
            if not ok:
                continue
            for f in LESSON_TEXT_FIELDS:
                en = ls[f]["en"]
                ls[f].setdefault(lang, [overlay[t][lang] for t in en] if isinstance(en, list) else overlay[en][lang])


def _load_lessons():
    """guides.json and lessons.json are written by the data lead (scripts/build_guides.py, fetch_lessons.py)."""
    global _guides, _lessons, _lesson_by_id, _lesson_by_entry
    _expire()
    if _lessons is None:
        _guides = _read_json("guides.json", {"fallback": {}, "groups": {}})
        _add_guide_translations(_guides, _read_json("guides_translated.json", {}))
        _lessons = _read_json("lessons.json", [])
        _add_lesson_translations(_lessons, _read_json("lessons_overlay.json", {}))
        kid_titles = {e["id"]: e["title"] for e in _read_json("kids.json", [])}
        for ls in _lessons:  # the lesson title is the entry title, which is already translated
            for lang, text in kid_titles.get(ls["entry_id"], {}).items():
                ls["title"].setdefault(lang, text)
        _lesson_by_id = {x["id"]: x for x in _lessons}
        _lesson_by_entry = {x["entry_id"]: x for x in _lessons}


def _read(side):
    entries = _read_json(f"{side}.json", [])
    for e in entries:
        e["side"] = side
        e.update(delivery.classify(e))  # adds delivery, kind, attribution (never saved to disk)
    return entries


def _load():
    global _entries, _by_id
    _expire()
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
    _expire()
    if _problems is None:
        _problems = _read_json("problems.json", [])
        _add_problem_translations(_problems, _read_json("problems_overlay.json", {}))
        _problem_by_id = {p["id"]: p for p in _problems}


def _problem_nodes(node, out):
    """Every {"en": text-or-list} dict inside a problem (prompt, hints, steps, test names...)."""
    if isinstance(node, dict):
        en = node.get("en")
        if isinstance(en, (str, list)) and all(len(k) == 2 for k in node):
            out.append(node)
            return
        for v in node.values():
            _problem_nodes(v, out)
    elif isinstance(node, list):
        for v in node:
            _problem_nodes(v, out)


def _add_problem_translations(problems, overlay):
    """problems.json is English-only. Add other languages from problems_overlay.json (English text -> {lang: text}).

    All or nothing per problem and language, so a problem page never mixes two languages. Code stays untouched.
    """
    for p in problems:
        nodes = []
        _problem_nodes(p, nodes)
        for lang in ("es", "ar", "hi", "pt"):
            pieces = [t for n in nodes for t in (n["en"] if isinstance(n["en"], list) else [n["en"]])]
            if not pieces or not all(lang in overlay.get(t, {}) for t in pieces):
                continue
            for n in nodes:
                en = n["en"]
                n.setdefault(lang, [overlay[t][lang] for t in en] if isinstance(en, list) else overlay[en][lang])


def problems():
    """All coding problems (src/data/problems.json, built by scripts/build_problems.py)."""
    _load_problems()
    return _problems


def problem(problem_id):
    _load_problems()
    return _problem_by_id.get(problem_id)


_categories = None


def category(name, lang):
    """Heading for a category: translated when we have it, else the English name."""
    global _categories
    if _categories is None:
        _categories = _read_json("categories_translated.json", {})
    return _categories.get(name, {}).get(lang) or name
