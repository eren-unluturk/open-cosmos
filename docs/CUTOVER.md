# Cutover checklist: Render to Vercel

Do not delete anything until every box in "Before" is ticked.

## Before (preconditions)

- [ ] Vercel preview or production URL works: `https://<url>/healthz` returns `{"ok": true}`.
- [ ] `python scripts/smoke_remote.py https://<url>` ends with `PASS` (see the command below).
- [ ] `python scripts/verify_supabase.py` ends with `OK` (skip if you run with `CONTENT_SOURCE=json`).
- [ ] The three demo paths in `docs/DEMO_SLICE.md` work by hand, on a **desktop** browser and on a **phone**:
  - [ ] 1. Child 5-10, lesson-backed (`kids-0d3a63dc` -> lesson `lesson-0d3a63dc`)
  - [ ] 2. Teen, link-only (`build-74d1338b`, with the "leaving our site" notice)
  - [ ] 3. Arabic-ready example (`build-74d1338b` or `kids-0d3a63dc` in Arabic)
- [ ] Arabic is right-to-left everywhere you look: header, lists, a lesson, a problem page, the footer; the name "Open Cosmos" reads correctly inside Arabic text.
- [ ] A JavaScript problem and a Python problem run and pass in the browser (Python needs internet for the first run).
- [ ] The grown-up switch works and stays on while you browse (needs `SECRET_KEY`); feedback sends (if Supabase is on).
- [ ] No keys in the repo; `SUPABASE_SERVICE_KEY` and `ANTHROPIC_API_KEY` are not set on Vercel.

## Edits once the Vercel URL is known

Replace `<url>` with the real production URL (for example `https://open-cosmos.vercel.app`).

- [ ] `README.md`: the Demo section and anywhere it names Render.
- [ ] `docs/PITCH.md`, `docs/PITCH_DATA.md` and slides/demo script: the live link.
- [ ] `docs/ISSUES_TRIAGE.md` / `docs/PLAN.md`: note that hosting moved to Vercel; close or update issue #8 ("Deploy: connect Render") on GitHub.
- [ ] GitHub repo "About" website field: set it to `<url>`.
- [ ] Supabase: if you restrict allowed URLs anywhere, add `<url>` (the site only calls Supabase from the server, so nothing is needed by default).
- [ ] Remove `render.yaml` and, if nothing else needs it, `gunicorn` from `requirements.txt` (in a separate commit, after Render is gone).

## Final step (manual)

- [ ] Delete the Render service in the Render dashboard (Settings > Delete Web Service). Do this last, after the checks above pass on Vercel.

## Run the remote smoke test

```
.venv/bin/python scripts/smoke_remote.py https://<preview-or-production-url>
```

It checks `/healthz`, 18 page types in all five languages, the safety gate, 404 pages, the API, static files, security headers, Arabic right-to-left, the app name in every page title, and response times (over 3 seconds is flagged; the first request is the cold start). Exit code 0 means pass. Add `--delay 0.2` to be gentle on a free tier.
