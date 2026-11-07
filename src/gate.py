"""Safety gate. Pure functions, no Flask.

kid-safe       -> always shown
ask-a-grown-up -> shown only after the session-only grown-up confirmation
adult-only     -> never shown
Missing or unknown safety counts as ask-a-grown-up (fail closed).
"""
KID_SAFE = "kid-safe"
ASK = "ask-a-grown-up"
ADULT_ONLY = "adult-only"


def tier(entry):
    s = entry.get("safety")
    return s if s in (KID_SAFE, ASK, ADULT_ONLY) else ASK


def visible(entry, adult=False):
    t = tier(entry)
    return t == KID_SAFE or (adult and t == ASK)


def filter_visible(entries, adult=False):
    return [e for e in entries if visible(e, adult)]
