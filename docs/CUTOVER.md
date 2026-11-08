# Cutover: Render to Vercel

Live site: **https://open-cosmos.vercel.app**. Status on Nov 8 2026: running on Vercel; the Render configuration is gone from the repo, and the old Render service still has to be **deleted by hand** (see "Render" below).

## Before (preconditions)

- [x] `https://open-cosmos.vercel.app/healthz` returns `{"ok": true}`.
- [x] `python scripts/smoke_remote.py https://open-cosmos.vercel.app` passed (1,002 checks).
- [x] The live site and the Supabase feedback form were tested by hand.
- [ ] `python scripts/verify_supabase.py` ends with `OK` (re-run any time; the site falls back to the bundled JSON if Supabase is ever unavailable).
- [ ] The three demo paths in `docs/DEMO_SLICE.md` checked by hand on a **phone** as well as desktop.
- [ ] Arabic is right-to-left everywhere (header, lists, a lesson, a problem page, the footer) and "Open Cosmos" reads correctly inside Arabic text.
- [ ] The manual VoiceOver and 200% zoom checklist in `docs/ACCESSIBILITY.md`.
- [x] No keys in the repo (working tree and full git history scanned, `docs/SECURITY.md`). `SUPABASE_SERVICE_KEY` is not deployed; the Vercel variables are only `SECRET_KEY`, `COOKIE_SECURE`, `CONTENT_SOURCE`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`.

## Edits once the Vercel URL was known (done)

- [x] `README.md`, `docs/DEMO_SLICE.md`, `docs/PITCH.md`, `docs/PITCH_DATA.md`: the live link replaces "TBD" and every Render mention.
- [x] `render.yaml` removed, and `gunicorn` removed from `requirements.txt` (nothing else needed it).
- [x] `docs/PLAN.md` and `docs/DEPLOY.md` say hosting is Vercel.
- [x] Old triage and branch-cleanup notes (`docs/ISSUES_TRIAGE.md`, `docs/BRANCH_CLEANUP.md`) removed; they described Render and the old name.

## Still manual

- [ ] GitHub repo "About" website field: set it to https://open-cosmos.vercel.app.
- [ ] Close GitHub issue #8 ("Deploy: connect Render") as obsolete.
- [ ] Rotate the Supabase keys after judging (they were once exposed to an editor session; `docs/SECURITY.md`).

## Render

- [x] `render.yaml` and the Render-only settings are removed from the repo.
- [ ] **Delete the old Render service by hand** (nothing here could do it: no Render login was available). It is safe to delete now that `scripts/smoke_remote.py` passes on the Vercel URL. Render dashboard (dashboard.render.com) > click the web service (`learning-lab`) > **Settings** (left menu) > scroll to the bottom > **Delete Web Service** > type the service name when asked > confirm. Also delete any Render environment group or Blueprint with the same name (Blueprints > the blueprint > Settings > Delete). Nothing in the repo refers to Render any more.

## Run the remote smoke test

```
.venv/bin/python scripts/smoke_remote.py https://open-cosmos.vercel.app --delay 0.2
```

It checks `/healthz`, 18 page types in all five languages, the safety gate, 404 pages, the API, static files, security headers, Arabic right-to-left, the app name in every page title, and response times (over 3 seconds is flagged; the first request is the cold start). Exit code 0 means pass.
