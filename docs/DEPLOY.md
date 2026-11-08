# Deploying Open Cosmos on Vercel

Vercel project name: `open-cosmos`. Render stays in place (`render.yaml`) until the cutover in `docs/CUTOVER.md`.

## How the repo is set up for Vercel

Based on Vercel's current docs for Flask ([Deploy a Flask app on Vercel](https://vercel.com/docs/frameworks/backend/flask), [Python runtime](https://vercel.com/docs/functions/runtimes/python)):

| Need | What we did |
|---|---|
| Entry point | Vercel detects Flask from `requirements.txt` and looks for a module-level `app` in `index.py`, `app.py`, `server.py`, ... (root, `src/` or `app/`). `index.py` at the root re-exports `src/app.py`'s `app` unchanged. `src/app.py` also puts its own folder on `sys.path`, so it works whichever file Vercel picks. No `builds` or `routes` in `vercel.json` (that is the old way). |
| Static files | Vercel ignores Flask's static folder and serves `public/` from its CDN. Our files (including the accessibility CSS/JS and `fonts/`) moved from `src/static` to `public/static`, so `/static/galaxy.css` is the same URL. Flask is configured to serve the same folder locally. |
| Python | `.python-version` pins 3.12 (Vercel supports 3.12, 3.13, 3.14; 3.12 is the default). |
| Dependencies | `requirements.txt` has only `flask`, `requests`, `python-dotenv` and `gunicorn` (kept only because `render.yaml` still uses it). `anthropic` was removed: nothing at runtime needs it and we call no paid API. |
| Data files | `src/data/*.json` are read with paths relative to the code (`Path(__file__)`), and Python functions bundle all project files by default. Nothing is written at runtime (no database, no files; sessions are signed cookies; progress is in the browser; the rate limiter and caches are in memory). |
| Headers | Flask sets the security headers and the Content-Security-Policy on dynamic pages (`src/csp.py`). `vercel.json` sets the same headers for static files under `/static/` (the CDN does not run Flask). A test (`tests/test_vercel_config.py`) fails if the two drift apart. |

### The Content-Security-Policy

- **Pages:** scripts only from our own origin (`script-src 'self'`, no inline scripts, no `eval`; this includes the accessibility scripts `a11y-settings.js`, `a11y.js` and `listen.js`), styles from us plus inline style attributes plus the Google Fonts stylesheet, fonts from our own origin (the self-hosted Atkinson Hyperlegible, `font-src 'self'`) and `fonts.gstatic.com`, images from us and `data:`, connections to us only, workers from us only, no frames, no plugins.
- **The code runner** (`/static/runner.js`) runs learner code in a Web Worker. A worker's policy comes from the response that served the worker script, so that one file gets its own wider policy: `unsafe-eval` (learner JavaScript uses `new Function`), `wasm-unsafe-eval` (Python via Pyodide) and `https://cdn.jsdelivr.net` (where Pyodide is downloaded from). Nothing else external is allowed there either.
- Checked in a real browser: a JavaScript problem and a Python problem both run and pass; six pages in four languages produced no policy violations.

## Environment variables (names only; set them in the Vercel dashboard)

| Name | Value | Notes |
|---|---|---|
| `SECRET_KEY` | a long random string | Signs the session cookie (grown-up switch, feedback token). Without it each server instance makes its own random key, so a visitor can lose the grown-up switch between requests. **Required on Vercel.** Make one with `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `COOKIE_SECURE` | `1` | Cookies only over HTTPS. |
| `CONTENT_SOURCE` | `auto` (or `json`) | `json` = never use Supabase. |
| `SUPABASE_URL` | `https://xxxx.supabase.co` | Optional. |
| `SUPABASE_ANON_KEY` | the anon key | Optional, server-side only. |

**Never deploy `SUPABASE_SERVICE_KEY`.** It is for seeding from your own machine only. Do not set `ANTHROPIC_API_KEY` either.

## Manual steps

1. Make sure the code is on GitHub (branch `vercel` merged, or deploy the branch as a preview first).
2. On vercel.com: **Add New > Project > Import Git Repository**, pick this repo.
3. **Project name: `open-cosmos`.** Framework preset: Flask (it should be detected). Leave build and output settings empty.
4. Add the environment variables above (Production and Preview).
5. **Deploy.** Open the deployment URL and check `/healthz` returns `{"ok": true}`.
6. **Settings > Git > Production Branch:** set it to `main`.
7. Run the remote smoke test against the preview URL (command at the bottom of `docs/CUTOVER.md`), then follow `docs/CUTOVER.md`.

## Troubleshooting

- **Build fails on dependencies:** check `requirements.txt` installs on Python 3.12 (`pip install -r requirements.txt` in a fresh 3.12 venv).
- **"No flask entrypoint found" or the home page is Vercel's 404:** the entry file must define a top-level `app`. We use `index.py`. Check the deployment's Functions tab to see which file was picked.
- **`ModuleNotFoundError: No module named 'delivery'` (or another file in `src/`):** the path fix in `index.py` / `src/app.py` did not run; confirm both files are in the deployment.
- **CSS and JavaScript return 404:** static files must be in `public/static/`. If `src/static` came back after a merge, move it again.
- **Page looks unstyled and the console shows "Refused to load ... Content Security Policy":** a template started using an inline script or a new external host. Fix the template (preferred) or extend `src/csp.py` **and** `vercel.json` together.
- **The code runner never finishes:** the browser could not load Pyodide from `cdn.jsdelivr.net` (offline, blocked, or the runner's policy changed). JavaScript problems work without the CDN.
- **Grown-up switch keeps turning off:** `SECRET_KEY` is not set, or `COOKIE_SECURE=1` while testing on plain `http://`.
- **Everything is English / content looks old:** with Supabase on, content is cached for 10 minutes; check `python scripts/verify_supabase.py`. To rule Supabase out, set `CONTENT_SOURCE=json` and redeploy.
- **First request is slow (cold start):** `scripts/smoke_remote.py` flags anything over 3 seconds; the first request counts as the cold start. Warm requests should be well under a second.
- **Changed an env var and nothing happened:** variables only apply to new deployments. Redeploy.
- **Feedback form says "could not send":** Supabase is not configured or schema.sql was not run (`docs/SUPABASE.md`). It never crashes the page.
