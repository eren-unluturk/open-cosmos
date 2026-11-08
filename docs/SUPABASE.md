# Supabase for Open Cosmos

Supabase project name: `open-cosmos`. It does two jobs only:

1. **Holds a copy of the catalog** (entries, guides, lessons, problems and the translation overlays) so content can be fixed without redeploying.
2. **Receives feedback from grown-ups** (a small form that is only reachable after the grown-up session flag is on).

It never holds anything about children, accounts, progress or code that learners write. Progress stays in the browser (`localStorage`).

## Safe by default

The bundled JSON in `src/data` stays the source of truth and always works. `CONTENT_SOURCE` picks where the site reads from:

| Value | Meaning |
|---|---|
| `json` | Never call Supabase. |
| `auto` (default) | Use Supabase when `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set, otherwise JSON. |
| `supabase` | Same as `auto`, but expresses the intent to use Supabase. |

In every mode the site falls back to the bundled JSON on **any** error: timeout (3 s per request), HTTP error, invalid JSON, an empty result, or rows that do not rebuild into valid files (schema mismatch). One short warning is logged (no keys, no URLs). After a failure it retries after 2 minutes; after a success it caches the download in memory for 10 minutes. Because the rows are rebuilt into the *same files* the app already reads, the safety gate, guide matching and language fallbacks behave identically in both modes (tests compare rendered pages byte for byte).

## Tables (`supabase/schema.sql`)

`content(kind, id, data jsonb, updated_at)`, primary key `(kind, id)`. Kinds: `entry`, `guide`, `lesson`, `problem`, `ui_overlay`. `data` wraps the original item with its position so order survives (`{"side", "pos", "item"}`); see `src/content_rows.py`.

| Policy | `content` | `feedback` |
|---|---|---|
| anon SELECT | allowed | denied |
| anon INSERT | denied | allowed (`status` must be `new`) |
| anon UPDATE / DELETE | denied | denied |

`feedback(id, created_at, kind, message, page, lang, status)` has CHECK constraints: kind in bug/translation/content/other, message 5 to 1000 characters, page up to 200, lang one of en/es/ar/hi/pt. There is no name, email, IP or user id column. Read feedback in the Supabase dashboard (Table editor); the website cannot read it.

## Flow

- **Seeding (your machine only):** `scripts/seed_supabase.py` reads `src/data/*.json` and the overlays and upserts them with the service key (idempotent). `--dry-run` prints counts and sends nothing. The JSON files are never edited by it.
- **Reading (the site):** `src/store.py` fetches `content` with the anon key, 500 rows per request, until it has everything, then rebuilds the files.
- **Checking:** `scripts/verify_supabase.py` compares row counts and a hash per kind between Supabase and the local JSON.
- **Feedback:** `GET/POST /<lang>/feedback`, 404 unless the grown-up flag is on. Checks: hidden honeypot field (bots get a fake "sent"), CSRF token tied to the session, kind and length checks, control characters stripped, at most 5 sends per hour per session (in memory, per server process, so it resets on restart). The row is inserted with the anon key over the REST API. If Supabase is down or not configured the visitor sees a friendly message; nothing crashes. Feedback is **untrusted data and is never shown back on any page**, including errors.

## Privacy

Stored per feedback: category, message, the page path, the language and the time. Nothing identifies the sender and the form says so in all five languages (`src/i18n_feedback.py`, key `fb_privacy`), including "do not write personal information". The catalog rows are public data. The site never sends visitor information to Supabase except an adult's feedback message. Server-side only: the browser never talks to Supabase and never sees a key.

## Variables (local `.env`, git-ignored; never commit, no `.env.example`)

| Name | Where | Purpose |
|---|---|---|
| `SUPABASE_URL` | local and deployed | Project URL, like `https://xxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | local and deployed, server-side only | Read `content`, insert `feedback` (RLS limits it) |
| `SUPABASE_SERVICE_KEY` | **local only, never deployed** | Seeding. Bypasses RLS. |
| `CONTENT_SOURCE` | optional | `json`, `supabase` or `auto` (default) |

## What you must do by hand

1. Create a Supabase project named `open-cosmos` (supabase.com, free tier).
2. Open SQL editor, paste `supabase/schema.sql`, run it.
3. In Project settings > API, copy the project URL, the `anon` key and the `service_role` key into your local `.env` as `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`.
4. `python scripts/seed_supabase.py` (try `--dry-run` first).
5. `python scripts/verify_supabase.py` and expect `OK`.
6. On Render, set only `SUPABASE_URL` and `SUPABASE_ANON_KEY` (and optionally `CONTENT_SOURCE`). Do not set the service key there.

To change content later: edit through the normal scripts, then run `seed_supabase.py` again (the site picks it up within 10 minutes). Deleting a row in the dashboard hides it only after the bundled JSON is also updated, since a missing kind makes the site fall back to JSON.
