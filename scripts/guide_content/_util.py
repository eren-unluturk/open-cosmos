"""Compact way to write a guide: G(GUIDES, key, title, what, for_me, steps, timeline, adult=None, time=None)."""
DEFAULT_TIME = "Plan about {minutes} minutes at a time over about {sessions} sessions."


def G(guides, key, title, what, for_me, steps, timeline, adult=None, time=None):
    guides[key] = dict(title=title, what=what, for_me=for_me, steps=steps, time=time or DEFAULT_TIME,
                       timeline=timeline, adult=adult)
