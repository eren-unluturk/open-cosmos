# Security and privacy: honest answers

Open Cosmos has **no accounts, no passwords, no analytics and no user-generated content shown to anyone**. That removes most risks by design. This page says what is left, with evidence you can re-run.

## 1. "What's the worst thing someone could do with your app?"

There is no user data to steal and nothing a visitor writes is ever shown to another visitor. The realistic worst cases, and what stops them:

| Worst case | What limits it | What is still true |
|---|---|---|
| **Spam the feedback form** | Adults-only page; CSRF token; hidden honeypot field; 5 sends per hour per session; 5 to 1000 characters; control characters stripped; database check constraints and insert-only access. | The Supabase **anon key is public by design** (it is how the database knows who is calling), so someone who finds the project URL could insert rows straight into `feedback`, skipping our form limits. They still cannot read, change or delete anything, and the text is never displayed on the site. Cleaning up means deleting rows in the dashboard. |
| **An unsafe page behind a "kid-safe" tag** | Safety **fails closed**: anything unclear is "ask a grown-up"; the rules can only get stricter; "adult-only" is never shown, even in grown-up mode; non-kid-safe entries are hidden by default; every link is from a CC0 list or CS Unplugged; a person reviewed 70 entries. | We tag **titles, descriptions and hosts, not the linked pages**, and a site can change after we looked. "Kid-safe" means nothing in the listing looks risky. The grown-up switch is a convenience gate, **not security**: anyone can press it. |
| **A bad or hijacked link** | Link-only reuse: we copy no pages. External links appear only on the last guide slide after a "you are leaving our site" notice. `check_links.py` found 7 dead links, removed. | A domain can change hands later. |
| **Cross-site scripting (XSS)** | Jinja autoescape everywhere, no `|safe`, no `Markup`, no `innerHTML` with data (the one use only clears a list), and a Content-Security-Policy with `script-src 'self'` (no inline scripts). Tests fail if a sink appears. | |
| **Prompt injection** | There is **no AI at runtime**. The guide path is picked by plain rules from our own data; translations and tags were written ahead of time and committed. | |
| **Cross-site request forging (flipping the grown-up view from another website)** | Every POST is refused if the browser says it came from another site (`Sec-Fetch-Site` / `Origin`), the session cookie is `SameSite=Lax`, and the feedback form has its own token. | |
| **Tampering with the catalogue** | The anon key can only **read** `content` (verified, see below). The service key lives only on the owner's machine. | If the database were ever empty or malformed, the site falls back to the bundled JSON. |
| **Running hostile code through the coding problems** | Learner code runs in a **Web Worker in the learner's own browser**; it is never sent to or run on our server. | The page stops it after 5 seconds. |

## 2. "Where are your API keys?"

- **There is no AI or paid-API key anywhere.** The website makes no AI calls (`tests/test_security.py` fails if `ANTHROPIC` or `import anthropic` appears in `src/`); translations and tags were done ahead of time by hand and committed.
- **Supabase anon key** (read the catalogue, insert feedback): server-side only, in the Vercel environment (`SUPABASE_ANON_KEY`). The browser never talks to Supabase and never sees it.
- **Supabase service key** (can bypass row-level security): only in the owner's local `.env`, used by `scripts/seed_supabase.py`. **Never deployed.** The website code never reads it (tested).
- **Vercel variables we use:** `SECRET_KEY`, `COOKIE_SECURE`, `CONTENT_SOURCE`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and nothing else. (This list is what the docs and the code require; the owner checks the Vercel dashboard.)
- **Evidence:** `.env` is in `.gitignore` and untracked. A search of the working tree and **all git history, all branches** for key-shaped values (`eyJ...`, `sb_secret_`, `sb_publishable_`, `sk-ant-`, `sk-...`, `AIza...`) found nothing, and none of the three values in the local `.env` appears anywhere in the history. The only `.env.example` that ever existed (added in the first commit, removed shortly after) held blank, commented-out placeholders.
- **Honest note:** the Supabase keys were once exposed to an editor session (an AI coding assistant could read the local `.env`). They are scheduled for **rotation after judging**.

## 3. "How would a screen-reader user log in?"

**There is no login.** There are no accounts, passwords, one-time codes or CAPTCHAs, so nothing to get through. The one gate is the grown-up switch, a normal button that sets a session flag (nothing stored). We made sure it, and the feedback form, work without a mouse or sight:

- Real buttons and labelled form fields with a visible focus ring; every control reachable by keyboard; a skip link; Escape closes the accessibility panel.
- The feedback form has a label on every field, accepts pasted text, has no picture CAPTCHA (a hidden honeypot field instead, which people never see) and shows plain-language messages in a status region ("Thank you", "could not send, try again later", "write between 5 and 1000 characters").
- Checked with axe-core (1,115 page states, 0 violations), a keyboard-only walk-through and a contrast script (`docs/ACCESSIBILITY.md`). A manual VoiceOver pass is on the owner's checklist; we have **not** tested with a real screen reader ourselves.

## Row Level Security: tested with the public key only

There are no per-user records, so the classic "log in as user A and open user B's data" test does not apply. What matters is what the **public anon key** can do. `python scripts/check_rls.py` tests exactly that against the live database (it never prints a key):

| Table | Anon key can | Anon key cannot |
|---|---|---|
| `content` (catalogue) | select | insert, update, delete |
| `feedback` | insert (valid, status `new`) | select, update, delete, insert with another status or a too-short message |

Result on the live project: **11 of 11 checks pass**; the row count of `content` (1,265) was identical before and after the attacks. (The test inserts one clearly-marked feedback row; delete it in the dashboard if you like. The anon key cannot, by design.)

## What we collect

Only when a grown-up sends feedback: **the category, the message, the page path, the language and the time**. No name, email, IP address, account, cookie id or tracking. Everything else stays in the visitor's own browser: learning progress and accessibility settings in `localStorage` (never sent), the grown-up switch and level choice in a signed session cookie (HttpOnly, SameSite=Lax, Secure on the live site). No analytics, no ads, no location, no third-party trackers.

One honest exception: pages load fonts from Google Fonts, and learners who run a Python problem download Python from cdn.jsdelivr.net. Those providers see the visitor's IP address and browser. The easy-to-read font is self-hosted; the main fonts could be too.

## Headers and cookies (checked on the live site)

`Content-Security-Policy` (own scripts only; the code runner gets its own narrower policy), `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Permissions-Policy` (no camera, microphone or location). Session cookie: `HttpOnly`, `SameSite=Lax`, `Secure` when `COOKIE_SECURE=1`.

## How to re-check

```
.venv/bin/python -m unittest tests.test_security     # CSRF, cookies, XSS sinks, secrets, no trackers
.venv/bin/python scripts/check_rls.py                # anon-key access (needs SUPABASE_URL and SUPABASE_ANON_KEY in .env)
git log --all -G'eyJ[A-Za-z0-9_-]{20,}|sb_secret_' --oneline   # nothing should print
```

## Known risks we have not removed

- The anon key is public, so the feedback table can be flooded from outside our form (insert-only, size-limited, never shown).
- The feedback rate limit is in memory per server instance (it resets on restart and is not shared between instances).
- "Kid-safe" is a judgement about listings, not about the linked pages.
- The grown-up switch is not authentication.
- Third-party requests to Google Fonts and cdn.jsdelivr.net (see above); Pyodide is loaded without an integrity check.
- The Supabase keys must be rotated after judging.
