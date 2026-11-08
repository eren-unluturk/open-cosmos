# Open Cosmos Project (KTP Hackathon, Nov 7-8 2026)

> One-line pitch: Open-source programming education, made approachable and available in every language. Level-based, age-aware and safety-tagged paths, with translated titles, built on existing open repos. Nothing here is ours; everything links back to its source and license.

## Problem
Great open-source programming resources exist, but they are mostly English-only and hard for beginners to approach: huge lists with no clear starting point.

## Solution
A website (Open Cosmos, **Information Access** track) with two sides, built only on open data:
- **Learn**: curated learning lists from [sindresorhus/awesome](https://github.com/sindresorhus/awesome) (CC0)
- **Build**: "build your own X" tutorials from [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) (CC0)

For young beginners (and the parents and teachers helping them), we add a **"What should I learn?" guide** that builds a short, ordered path from open resources. We also add translated titles and descriptions (Spanish, Arabic, Hindi, Portuguese; AI-generated and labeled as such), a Beginner / Intermediate / Advanced level, an age group, and a child-safety tier on every entry. Kid-targeted lessons come from [CS Unplugged](https://github.com/uccser/cs-unplugged) (CC BY-SA 4.0). 

**Guides, roadmaps and lessons (our contribution on top of the lists):**
- Every entry opens a short slide **guide**: what it is, is it for me, how to start, how much time, and a recommended **roadmap** (e.g. Day 1, Week 1, Week 2) that adapts to the child's age and level. Guides are AI-written ahead of time from the catalog data and are labeled as such.
- For link-only content (almost everything) the last slide says **"you are leaving our site"** with a grown-up note and sends the learner to the original, so we never copy it.
- For CS Unplugged (CC BY-SA 4.0) we go further: **26 adapted lessons** in our own simple words, shown on our own lesson pages with attribution and a "changes were made" note.
- Each guide ends with **Explore next**, a computed list of related kid-safe entries.

We claim none of the content as ours. Every entry links to its source and license (see `docs/SOURCES.md`).

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
python scripts/apply_translations.py # hand-written es/ar/hi/pt translations from scripts/translation_content/ (no API key)
python scripts/mark_reuse.py   # reuse flag: open-content (CS Unplugged) vs link-only
python scripts/fetch_lessons.py # src/data/lessons.json (26 adapted CS Unplugged lessons)
python scripts/build_guides.py # src/data/guides.json (7 fallbacks + 65 handwritten group guides)
python scripts/coverage.py     # stats + guide coverage gaps
python scripts/guide_progress.py # docs/GUIDE_PROGRESS.md (guide coverage)
python scripts/freeze_check.py  # final checks before submitting
python scripts/check_links.py  # polite link report; re-checks only non-ok links (never edits data)
# After the data freeze, do NOT re-run fetch.py (new upstream entries would only get fail-closed rules).
python -m unittest discover -s tests
```
Setup once: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Nothing in the pipeline needs an API key. Translations are written into the JSON ahead of time (see `docs/PLAN.md`); `scripts/translate.py` is an optional API-based alternative nobody is using. If you ever need a secret, keep it in a local `.env` (git-ignored, never committed).

## Guides and lessons
Every learning entry has a short slide **guide** with a recommended roadmap/timeline (`src/data/guides.json`: 65 handwritten group guides plus 7 topic fallbacks, so every visible entry has one; written ahead of time, no live AI). Link-only entries end with a "leaving our site" slide; CS Unplugged lessons (CC BY-SA 4.0) are adapted into our own lessons in `src/data/lessons.json` (26 lessons). Spec for the app: `docs/GUIDE_SPEC.md`. Demo items: `docs/DEMO_SLICE.md`. Numbers for slides: `docs/PITCH_DATA.md`.

## Frontend (galaxy theme)
Space-themed UI: palette `#0D1B2A #1B263B #415A77 #778DA9 #E0E1DD` plus galaxy yellows and purples. Map of every file and where to change things: `docs/FRONTEND.md`.

## Project Structure
```
src/      application code
docs/     plan, notes, pitch
assets/   images, logos, demo media
scripts/  setup / seed / helper scripts
tests/    tests
```

## How to request changes
- Open a GitHub issue and assign it to the person who owns the file (see the roles table below), or mention them in an issue or PR.
- Say what you need and which URL, file or data field it touches.
- Backend files: `src/app.py`, `src/store.py`, `src/gate.py`, `src/guide.py`. Pull `main` before you start and run `python -m unittest discover -s tests`.
- Never commit `.env` or any secret.

## Team & Roles
| Name | Role | Responsibilities | Files |
|------|------|------------------|-------|
| Eren | **Data lead** | Fetch and parse the two CC0 lists and CS Unplugged into JSON; categorize every entry (topic, level, age, safety tier); hand-label what rules can't decide; link checks; stats; keep `docs/SOURCES.md` accurate. | `scripts/` (except `translate.py`), `src/data/`, `docs/SOURCES.md`, `docs/SAFETY_REVIEW.md` |
| Brian | **AI lead** | Translation quality and queue (`docs/TRANSLATE_QUEUE.md`), native-speaker spot checks, and the guide's AI-or-rules path. `translate.py` is optional (needs a key). | `scripts/translate.py`, `src/guide.py` (with Tobi) |
| Tobi | **Backend lead** | Flask routes, language and level filtering, UI strings, right-to-left support, search, deployment. Also the safety gate (hide non-kid-safe by default) and guide filtering by safety, age fit and goal. | `src/app.py`, `requirements.txt` |
| Isabella | **Frontend + pitch lead** | Pages, level badges, language switcher, attribution footer, accessibility; then README, slides, demo video, and submission. | `src/templates/`, `src/static/`, `docs/PITCH.md` |

## Challenges / What We Learned
**Data**
- *Parsing is never as clean as it looks.* The two lists are hand-edited Markdown: language tags in bold (`**Python**: title`), `[video]` and `[pdf]` markers, `#` anchors and duplicate links. Our first parser silently dropped about 30 build entries; we found it by counting lines in the source.
- *Safety fails closed.* Every entry is `kid-safe`, `ask-a-grown-up` or `adult-only`; anything unclear is ask-a-grown-up. Rules were only ever allowed to get stricter (a test enforces it), and false matches taught us a lot ("from scratch" is not Scratch, "child process" is not a child, a Slack-bot tutorial is not kid-safe).
- *No paid API, so no API in the pipeline.* Classification and translation are done ahead of time by hand with Claude Code and committed (`scripts/cache/`, `src/data/`), so anyone can rebuild with no key.
- *ShareAlike is a constraint.* CS Unplugged is CC BY-SA 4.0 and the lists are CC0, so they live in separate files, we copy no lesson text, and translations carry attribution and a "changes were made" note.
- *Hand-labeling has limits.* We label titles, descriptions and hosts, never the linked pages, and a person spot-checked only 70 entries. "Kid-safe" means nothing in the listing looks risky. Real kid content for games, art and web at ages 5-10 is thin, so the guide backfills and we say so (see `docs/STATS.md`).
