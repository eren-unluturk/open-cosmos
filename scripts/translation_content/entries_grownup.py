"""Hand-written (Claude Code, no API) translations of the titles and descriptions of the grown-up-section entries
(es/ar/hi/pt). Text lives in entries_grownup.json: {entry id: {"title": {...}, "desc": {...}}}.
Product and language names stay as they are. AI-written; not yet checked by native speakers."""
import json
from pathlib import Path

DATA = Path(__file__).with_name("entries_grownup.json")


def build():
    return json.loads(DATA.read_text(encoding="utf-8"))
