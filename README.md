# Hackcessability Project (KTP Hackathon, Nov 7-8 2026)

> One-line pitch: Open-source programming education, made approachable and available in every language. Level-based, age-aware and safety-tagged paths, with translated titles, built on existing open repos. Nothing here is ours; everything links back to its source and license.

## Problem
Great open-source programming resources exist, but they are mostly English-only and hard for beginners to approach: huge lists with no clear starting point.

## Solution
A website (Hackcessability, **Information Access** track) with two sides, built only on open data:
- **Learn**: curated learning lists from [sindresorhus/awesome](https://github.com/sindresorhus/awesome) (CC0)
- **Build**: "build your own X" tutorials from [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) (CC0)

For young beginners (and the parents and teachers helping them), we add a **"What should I learn?" guide** that builds a short, ordered path from open resources. We also add translated titles and descriptions (Spanish, Arabic, Hindi, Portuguese; AI-generated and labeled as such), a Beginner / Intermediate / Advanced level, an age group, and a child-safety tier on every entry. Kid-targeted lessons come from [CS Unplugged](https://github.com/uccser/cs-unplugged) (CC BY-SA 4.0). We claim none of the content as ours. Every entry links to its source and license (see `docs/SOURCES.md`).

## Demo
- Live link: _TBD_
- Video: _TBD_

## Tech Stack
Python (Flask + Jinja2), Tailwind via CDN, static JSON data produced ahead of time by `scripts/` (no database, no paid API, no key needed to run or rebuild), Render. Details in `docs/PLAN.md`.

## Data Pipeline (run in order)
```bash
python scripts/fetch.py        # download + parse the two CC0 lists
python scripts/fetch_kids.py   # CS Unplugged lessons (CC BY-SA 4.0) -> src/data/kids.json
python scripts/categorize.py --no-ai  # topic, level, age_group, safety (uses the committed cache + human overrides)
python scripts/coverage.py     # stats + guide coverage gaps
python scripts/check_links.py  # polite link report; re-checks only non-ok links (never edits data)
python -m unittest discover -s tests
```
Setup once: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Nothing in the pipeline needs an API key. Translations are written into the JSON ahead of time (see `docs/PLAN.md`); `scripts/translate.py` is an optional API-based alternative nobody is using. If you ever need a secret, keep it in a local `.env` (git-ignored, never committed).

## Project Structure
```
src/      application code
docs/     plan, notes, pitch
assets/   images, logos, demo media
scripts/  setup / seed / helper scripts
tests/    tests
```

## Team & Roles
| Name | Role | Responsibilities | Files |
|------|------|------------------|-------|
| Eren | **Data lead** | Fetch and parse the two CC0 lists and CS Unplugged into JSON; categorize every entry (topic, level, age, safety tier); hand-label what rules can't decide; link checks; stats; keep `docs/SOURCES.md` accurate. | `scripts/` (except `translate.py`), `src/data/`, `docs/SOURCES.md`, `docs/SAFETY_REVIEW.md` |
| Brian | **AI lead** | Translation quality and queue (`docs/TRANSLATE_QUEUE.md`), native-speaker spot checks, and the guide's AI-or-rules path. `translate.py` is optional (needs a key). | `scripts/translate.py`, `src/guide.py` (with Tobi) |
| Tobi | **Backend lead** | Flask routes, language and level filtering, UI strings, right-to-left support, search, deployment. Also the safety gate (hide non-kid-safe by default) and guide filtering by safety, age fit and goal. | `src/app.py`, `requirements.txt` |
| Isabella | **Frontend + pitch lead** | Pages, level badges, language switcher, attribution footer, accessibility; then README, slides, demo video, and submission. | `src/templates/`, `src/static/`, `docs/PITCH.md` |

## Challenges / What We Learned
_Fill in near the end — useful for judging and Devpost._
