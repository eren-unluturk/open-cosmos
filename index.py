"""Vercel entry point. Vercel looks for a module-level Flask `app` in index.py (or app.py, server.py ... or the same
names in src/). The real app is src/app.py; this file only makes `src` importable and re-exports it unchanged."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from app import app  # noqa: E402,F401
