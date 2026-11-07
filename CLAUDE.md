# CLAUDE.md

Hackathon project: speed matters more than polish. Working demo > perfect code.

## Ground rules
- Prefer simple, well-known tools; avoid yak-shaving and over-engineering.
- Get an end-to-end happy path working first, then improve.
- Secrets live only in a local `.env` (git-ignored). NEVER commit `.env` or any env file, and never create an `.env.example`.
- Record decisions and TODOs in `docs/PLAN.md`.
- Keep README current: setup/run commands must always work.

## Layout
See README "Project Structure".

## Commands
- Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Data pipeline (run in order): `scripts/fetch.py`, `scripts/fetch_kids.py`, `scripts/categorize.py --no-ai`, then `scripts/coverage.py`, `scripts/check_links.py`
- Test: `.venv/bin/python -m unittest discover -s tests`
- Run the site: `.venv/bin/flask --app src/app run`
- No paid API: do not call the Anthropic API; any AI-style classification or translation is done by hand by Claude Code and committed.
