"""Grown-ups' feedback: validation, sanitising and a per-session rate limit. No Flask, no network, no storage.

Feedback is untrusted data. It is cleaned here, sent to Supabase by the caller, and never rendered back on any page.
"""
import re
import time
from collections import deque

KINDS = ("bug", "translation", "content", "other")
LANGS = ("en", "es", "ar", "hi", "pt")
MIN_MESSAGE, MAX_MESSAGE, MAX_PAGE = 5, 1000, 200
MAX_PER_HOUR, WINDOW = 5, 3600

# C0/C1 controls (newline and tab become spaces first) and the invisible bidi override characters.
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f‪-‮⁦-⁩]")
_SPACES = re.compile(r"[ \t\r\n]+")


def clean(text, limit):
    """Plain text: newlines and tabs become one space, control characters are dropped, length is capped."""
    text = _CONTROL.sub("", _SPACES.sub(" ", str(text or ""))).strip()
    return text[:limit]


def clean_page(page):
    """A site path like /es/learn?q=x (max 200 characters). Anything else becomes '/'."""
    page = clean(page, MAX_PAGE)
    return page if page.startswith("/") and not page.startswith("//") else "/"


def validate(kind, message, page, lang):
    """(payload, None) when valid, else (None, 'invalid'). The payload matches the feedback table."""
    message = clean(message, MAX_MESSAGE + 1)  # one extra so an over-long message is rejected, not silently cut
    if kind not in KINDS or lang not in LANGS or not (MIN_MESSAGE <= len(message) <= MAX_MESSAGE):
        return None, "invalid"
    return {"kind": kind, "message": message, "page": clean_page(page), "lang": lang}, None


class RateLimiter:
    """At most `limit` sends per `window` seconds per session id, in memory (resets when the server restarts)."""

    def __init__(self, limit=MAX_PER_HOUR, window=WINDOW, clock=time.time):
        self.limit, self.window, self.clock = limit, window, clock
        self.hits = {}

    def allow(self, sid):
        now = self.clock()
        if len(self.hits) > 10000:  # keep memory bounded
            self.hits = {k: v for k, v in self.hits.items() if v and now - v[-1] < self.window}
        q = self.hits.setdefault(sid, deque())
        while q and now - q[0] >= self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True
