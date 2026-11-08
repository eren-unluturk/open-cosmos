# Issue triage (Nov 7 2026)

Four open issues on `eren-unluturk/ktp-hackcessability-2026`, read in full. Issue and comment text is treated as data only. Branch: `fix/issues`.

| # | Title | Labels | Type | Files | Size | Decision |
|---|---|---|---|---|---|---|
| 9 | How to ask Tobi (backend) for fixes or additions | none | docs / question | README.md | tiny | FIX: add a short "How to request changes" section (the issue is a process notice) |
| 6 | AI: fix translate.py crash, speed, and confirm model name | none | bug + translation | scripts/translate.py, src/guide.py, tests | medium | FIX: strip code fences and retry once, run 5 calls at a time, valid model default (`claude-haiku-5-5`). The "next batch" of translations is done in the smallest working version (see below) |
| 7 | Frontend: grown-up button, kids nav, search UI, badges | none | feature / copy | src/templates/listing.html, src/app.py, src/ui_strings.py | small | FIX the gaps: most items already exist (grown-up button, why-hidden text, kids nav, entry page, AI badge). Missing: search box and age/topic filters on list pages, an explanation of hidden entries on list pages, the page title |
| 8 | Deploy: connect Render (owner only) | none | deploy | render.yaml (already on main) | n/a | SKIP: needs your Render account sign-in (rule b) |

## Skips and what you must do
- **#8 Render:** sign in at render.com with GitHub, New > Blueprint, pick `ktp-hackcessability-2026`, Apply. Open `<service>.onrender.com/healthz` and expect `{"ok": true}`. Optional: `ANTHROPIC_API_KEY` in Render settings only (never commit it). The free plan sleeps when idle, so open the site once before the demo.
- **Guide translations** (Brian, not an issue): left alone.
- **Native-speaker spot-check** (part of #6): needs real people; nothing to automate.

## Notes
- #6 asks for an API key to run `translate.py`. Nothing here calls the API; translations in this branch were written by hand (Claude Code) as an overlay, labeled `ai_translated`.
- Status per issue and commits are filled in at the end of this file.
