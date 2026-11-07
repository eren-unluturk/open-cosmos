# Hackcessability Project (KTP Hackathon, Nov 7-8 2026)

> One-line pitch: Open-source programming education, made approachable and available in every language. Level-based paths and AI translation for existing open repos. Nothing here is ours; everything links back to its source and license.

## Problem
Great open-source programming resources exist, but they are mostly English-only and hard for beginners to approach: huge lists with no clear starting point.

## Solution
A website (Hackcessability, **Information Access** track) with two sides, built only on open data:
- **Learn**: curated learning lists from [sindresorhus/awesome](https://github.com/sindresorhus/awesome) (CC0)
- **Build**: "build your own X" tutorials from [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) (CC0)

We add AI translation into multiple languages and a Beginner / Intermediate / Advanced path. We claim none of the content as ours. Every entry links to its source and license (see `docs/SOURCES.md`).

## Demo
- Live link: _TBD_
- Video: _TBD_

## Tech Stack
Python (Flask + Jinja2), Tailwind via CDN, Claude API (translation + level tagging), static JSON data, Render. Details in `docs/PLAN.md`.

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
| Eren | **Data lead** | Fetch and parse the two CC0 source READMEs into JSON; decide which entries count as intro-to-programming; keep `docs/SOURCES.md` accurate. | `scripts/fetch.py`, `docs/SOURCES.md` |
| Brian | **AI lead** | Claude prompts for translation and Beginner/Intermediate/Advanced tagging; run and cache the batch; have native speakers spot-check translations. | `scripts/translate.py` |
| Tobi | **Backend lead** | Flask routes, language and level filtering, UI strings, right-to-left support, search, deployment. | `src/app.py`, `requirements.txt` |
| Isabella | **Frontend + pitch lead** | Pages, level badges, language switcher, attribution footer, accessibility; then README, slides, demo video, and submission. | `src/templates/`, `src/static/`, `docs/PITCH.md` |

## Challenges / What We Learned
_Fill in near the end — useful for judging and Devpost._
