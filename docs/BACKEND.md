# Backend design (Tobi)

Scope: `src/app.py`, `src/guide.py`, `requirements.txt`. Hackathon rule: simple, no database, no accounts.

## What the data really is
There are no lesson bodies. `src/data/*.json` is a catalog of 1,068 entries that link out to the source.

| File | Entries | License | Notes |
|------|---------|---------|-------|
| learn.json | 676 | CC0 | awesome lists |
| build.json | 359 | CC0 | build-your-own-x |
| kids.json | 33 | CC BY-SA 4.0 | CS Unplugged, truly kid-targeted |

Only 452 are `kid-safe` (learn 354, build 65, kids 33). By level: Beginner 72, Intermediate 297, Advanced 83.
"Lesson page" in the plan = an entry detail page (title, desc, level, age, safety, source, license, link out).

## Gaps in the current backend
1. `load()` ignores `kids.json`.
2. No safety gate. Everything is shown, including `adult-only`.
3. `read_text()` has no `encoding="utf-8"`. It breaks ar/hi text on Windows.
4. Guide ignores `safety`, `age_group` and `topic`. A 6-year-old can get teen+ links.
5. Guide fallback returns fewer than 6 items for most combos (27 of 36).
6. `listing` reads and parses JSON on every request.
7. Missing language falls back to nothing: `e["title"][lang]` is not used at all yet.
8. `MODEL = "claude-haiku-5-5"` is unverified. Make it an env var.

## Module layout
```
src/
  app.py        routes only
  store.py      load + index data once at startup
  gate.py       safety rules + grown-up session flag
  guide.py      path builder (pure function, no Flask)
  i18n.py       UI strings, RTL, text fallback
```
`guide.py` and `gate.py` stay pure so `tests/` can call them with no server.

## store.py
Load all three files once (UTF-8) into a list plus a dict by id.
Add `side` (`learn|build|kids`) to each entry at load time.
Helper `text(entry, field, lang)` returns `entry[field][lang]`, else `en`, and says if it fell back.

## Safety gate (gate.py)
- Default view: `safety == "kid-safe"` only.
- "I'm a grown-up" sets `session["adult"] = True` (signed cookie, session only, no data stored).
  It reveals `ask-a-grown-up`. `adult-only` is never shown, even with the flag.
- Unknown or missing `safety` counts as `ask-a-grown-up` (fail closed).
- The guide ignores the flag. It always uses `kid-safe`.
- Needs `app.secret_key` from env `SECRET_KEY`. Dev fallback only when `FLASK_DEBUG`.

```python
def visible(entry, adult): 
    s = entry.get("safety", "ask-a-grown-up")
    return s == "kid-safe" or (adult and s == "ask-a-grown-up")
```

## Routes
| Route | Purpose |
|-------|---------|
| `GET /` | redirect to `/en/` (later: use Accept-Language) |
| `GET /<lang>/` | home |
| `GET /<lang>/<side>` | `side` in learn, build, kids. Filters: `level`, `age`, `topic`, `q` |
| `GET /<lang>/entry/<id>` | detail page, attribution, AI-translated flag |
| `GET /<lang>/guide` | multiple-choice guide |
| `POST /grownup` | set or clear the session flag, redirect back |
| `GET /api/entries` | JSON, same filters, same gate (frontend / tests) |
| `GET /healthz` | for Render |

Rules: 404 on unknown lang or side. Validate every query value against an allow-list. No free text reaches the model or the data.
Search `q`: case-insensitive substring over the shown-language title, desc and `en` title. Stretch: fold accents. Cap `q` at 80 chars.
Entry `ai_translated` lists the languages written by AI. Pass `is_ai = lang in e["ai_translated"]` to the template.

## Guide algorithm (guide.py)
Input: `age` (5-7, 8-10, 11-13), `goal`, `level`.
1. Pool = `kid-safe` entries only.
2. Age fit: `age_group` order `5-7 < 8-10 < 11-13 < teen+`. Keep entries with `age_group <= age`.
3. Score: `+3` if `topic == goal`, `+1` if `topic == "general"`, `+1` if `side == "kids"` when age <= 10.
4. Level: take chosen level first. Backfill with the next lower level if the pool has fewer than 6 (rule B from PLAN).
5. Backfill with `topic == "general"` at the same level (rule A).
6. Order: easier level first, then score. Take 6.
7. Optional AI re-order: send only ids and titles. Keep only returned ids that are in the pool. On any error, use the order from step 6.
Ages 5-10: offer Beginner only (UI hint, backend still accepts any).
Unit test: all 36 combos return at least 3 entries, none above the chosen age, all `kid-safe`.

## Languages
`es ar hi pt en`. RTL for `ar`. UI strings move to `i18n.py` (or `ui.json`).
Missing UI key falls back to `en`. Missing entry text falls back to `en`, and the template shows "shown in English".

## Config (env only, never committed)
`SECRET_KEY`, `ANTHROPIC_API_KEY` (optional), `ANTHROPIC_MODEL` (default set once verified).

## Deploy (Render)
`gunicorn --chdir src app:app`, add `gunicorn` to `requirements.txt` (pinned). Health check `/healthz`.
Set `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`.
Add response headers: `X-Content-Type-Options: nosniff`, a basic CSP (Tailwind CDN allowed), `Referrer-Policy: no-referrer`.

## Build order
1. `store.py`: UTF-8 load, kids included, `side` field.
2. `gate.py` + `/grownup` + filter in `listing`.
3. `guide.py` rewrite + tests.
4. `/entry/<id>`, `/api/entries`, search.
5. Headers, `/healthz`, gunicorn, deploy.
6. Tests: gate hides adult-only, guide age fit, every route returns 200 for all 5 langs.

## Open questions
- Does Isabella want `/api/entries`, or are server-rendered pages enough?
- Is `kids` its own tab, or merged into Learn? (License text differs, so a separate label is safer.)
- Which model name is valid for the guide? Check before demo.

## Lesson catalogue (hosted vs external)
Rule lives in `src/delivery.py`. `store.py` adds `delivery`, `kind` and `attribution` to every entry at load time. Nothing is written to the JSON files.

| delivery | What | Why |
|----------|------|-----|
| `hostable` | CS Unplugged (`kids.json`, CC BY-SA 4.0) | License lets us show the lesson on our pages with credit, license link, a "changes were made" note, and the same license. |
| `external` | `learn.json`, `build.json` | CC0 covers only the list. The linked pages belong to their owners, so we link out. |

`kind`: hostable = unit, lesson, challenge, activity. External = video, repo, article, document.
Hosted units and lessons (33) have their text in `src/data/lessons.json`; challenges and activities (24) are still link-only. `store.lesson(id, lang)` picks a human translation, then an AI one from `lessons_translated.json`, then English (`fallback: true`). `store.render_markdown` renders with raw HTML disabled and `rel="noopener noreferrer"` on links. Images are not copied yet.

Translations: `src/i18n_guides.py` holds the how-to guides and catalogue labels in es, ar, hi, pt (AI-written, not native-checked). Tests check that every translated list has the same length as the English one.

Routes: `/<lang>/catalogue` (two sections, grouped Beginner, Intermediate, Advanced), `/<lang>/howto/<kind>` (steps, accessibility tips, per-level tips, safety), `/api/catalogue`. The safety gate and the age, topic and level filters apply to all of them.
