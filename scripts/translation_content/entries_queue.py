"""Hand-written (Claude Code, no API) translations of the 377 catalogue entries that were still English
(titles and descriptions, es/ar/hi/pt). The text lives in entries_queue.json: {entry id: {"title": {...}, "desc": {...}}}.
Product and language names (Python, Godot, React...) stay as they are. AI-written; not yet checked by native speakers."""
import json
from pathlib import Path

DATA = Path(__file__).with_name("entries_queue.json")


def build():
    return json.loads(DATA.read_text(encoding="utf-8"))
