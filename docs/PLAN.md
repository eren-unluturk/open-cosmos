# Plan — Open Cosmos (Kappa Theta Pi x CDS StuGov x BUCyS)

Location: CDS, 17th floor, room 1750.

## Chosen track: Information Access
We are submitting to **Information Access**. Project idea below.

## Prompt / Theme
Accessibility. Pick ONE track to submit to on Sunday:
- **Community Access** — software that helps people connect, gather, and participate in their communities
- **Tech Access** — help more people use technology; invent a new way to interact with software, or fix a tool that leaves people out today
- **Information Access** — use open data to build a product that makes complex or hidden information easier to find, understand, or act on

Track details come at opening remarks (Sat 12:30 PM). Judging criteria: _TBD — add after opening remarks_.

## Idea
**Track: Information Access.** A site that makes existing open-source "intro to programming" repos easier to approach and available in many languages. We claim none of the content as ours. Everything is open data, linked to its source repo with its license and attribution.

**What we add (our only contribution):**
1. **Translation** of entry titles and descriptions into multiple languages (code and technical terms kept in English). Done ahead of time with AI help and labeled as AI-generated.
2. **A level-based path** (Beginner / Intermediate / Advanced) plus age and topic tags and a child-safety tier, so newcomers know where to start.
3. **Clear sourcing**: every entry links to the original, its author and license.
4. **Guides and roadmaps**: every entry opens a short slide guide with a recommended timeline (Day 1, Week 1, ...), personalised by age and level with simple rules. Link-only entries end with a "you are leaving our site" slide; CS Unplugged (CC BY-SA 4.0) is adapted into our own lessons. See "Guides, roadmaps and lessons" below.

**Who it's for (details in `docs/PITCH.md`):** (1) a student who needs tutoring and finds GitHub repos unapproachable, and (2) international students who struggle with English-only resources.

**Why it matters:** repos are free but hard to approach and mostly English-only. We lower both barriers.

## Two sides
- **Learn** — sourced from [sindresorhus/awesome](https://github.com/sindresorhus/awesome) (CC0): curated "awesome" lists for learning topics.
- **Build** — sourced from [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) (CC0): "build your own X" tutorials (databases, git, shell, etc.).
- Both are link lists. We translate + level-tag the list entries and link out. Details in `docs/SOURCES.md`.

## Audience update: children just starting to learn
Most kids' coding tutoring is pay-to-use. We now focus on **young beginners (about ages 5-13) and the parents/teachers who help them**, plus non-English speakers.
- **Flagship feature: "What should I learn?" guide** (`/<lang>/guide`, `src/guide.py`). Multiple-choice only (age, goal, level) and it builds an ordered 6-step path from our data, using only existing entries, so it can't invent links. Matching is rule-based on the `kid-safe`, `age_group`, `topic` and `level` fields (no paid API needed). See "Ask the team" for the backfill rules.
- **Child safety:** no accounts, no free-text input, no personal data stored, no ads/tracking. Keep language simple and friendly. Mention that adults should supervise.
- **Kid content:** `awesome` and `build-your-own-x` are written for adult developers and are NOT kid-focused, so we added `uccser/cs-unplugged` (CC BY-SA 4.0 content, verified) as the kid-targeted source and keep the other two as the "older learners" tier. Real kid content for games/art/web at ages 5-10 is still thin; the guide uses backfill rules (see Coverage and Ask the team).
- `scripts/categorize.py` tags every entry with `topic`, `level`, `age_group` and a safety tier (see Decisions).

## Guides, roadmaps and lessons (the system)
- **Two paths per entry.** A. *Link-only* (`reuse = "link-only"`; all awesome and build-your-own-x entries): an AI-written overview guide plus a roadmap, ending in a leaving-our-site slide. B. *Open-content* (`reuse = "open-content"`; CS Unplugged): our own simplified lesson in `src/data/lessons.json`, ending in a slide to our lesson page.
- **Guaranteed coverage.** `src/data/guides.json` has 65 handwritten group guides (one per `side:category`, so 100% of visible entries) plus 7 topic fallbacks as a safety net. `scripts/guide_helpers.py` (`guide_for`, `build_timeline`, `related_entries`, `lesson_for`, `fill`) resolves them with no runtime AI.
- **Roadmap = the timeline slide + `build_timeline`.** The guide gives a 3-5 step plan; the helper turns level and age into minutes per session and number of sessions. All times are labeled estimates.
- **Honest limits.** Guides are written from catalog data only (title, description, category, level, topic), not from the linked pages. Slide text never contains URLs. "Explore next" is computed by the backend, not written by hand.
- **Files:** `docs/GUIDE_SPEC.md` (app tasks), `docs/GUIDE_PROGRESS.md` (coverage), `docs/GUIDE_DECISIONS.md`, `docs/DEMO_SLICE.md`, `docs/PITCH_DATA.md`, `docs/REUSE_CANDIDATES.md`.
- **Rebuild order:** `categorize.py --no-ai` -> `mark_reuse.py` -> `fetch_lessons.py` -> `build_guides.py` -> tests.

## Principles
- Open data only. Only use content under licenses that allow translation/redistribution (CC-BY, MIT, etc.). Record license per source.
- Never present content as ours. Show attribution + "translated from" on every page. Note translations are AI-generated.
- Keep code blocks untouched; translate prose only.

## Tech Stack (Python)
| Layer | Choice | Why |
|-------|--------|-----|
| Language | Python 3.9+ | Whole team can contribute; one language for site and pipeline |
| Web | Flask + Jinja2 (server-rendered) | Simple, fast to build; routes `/<lang>/learn`, `/<lang>/build` |
| Styling | Tailwind via CDN | No build step; `dir="rtl"` for Arabic |
| Categorizing + translating | Rules in `scripts/categorize.py`, plus classification and translation done by hand by Claude Code (no paid API) | No cost, no key; results are committed (`scripts/cache/`, `src/data/`) so anyone can rebuild |
| Data | Static JSON in `src/data/`, generated by `scripts/` | No database, fast, free to host |
| Hosting | Render (or Railway/Fly) | Free tier, deploys from GitHub |

**Pipeline:** `scripts/fetch.py` downloads the two CC0 lists and `scripts/fetch_kids.py` the CS Unplugged lessons -> `scripts/categorize.py --no-ai` tags topic, level, age group and safety (rules + a committed label cache + human overrides) -> translations for es/ar/hi/pt are written into the JSON in `src/data/` and labeled `ai_translated` -> Flask renders it. Everything is done **ahead of time**, so the site runs on static JSON with no API key and no live AI calls.

## Team split (4 people)
1. **Data lead** — `scripts/` data pipeline: fetch + parse the sources into JSON, categorize and safety-tag, reuse flag, guides (`guides.json`) and adapted lessons (`lessons.json`); keep `docs/SOURCES.md` accurate.
2. **AI lead** — translation quality and queue: `scripts/translate.py` (optional, needs an API key nobody has right now), translation batches from `docs/TRANSLATE_QUEUE.md`, native-speaker spot checks; and `src/guide.py` if an AI-assisted path is kept.
3. **Backend lead** — `src/app.py`: Flask routes, language/level filtering, UI strings, RTL, deploy. **Also owns the safety gate and guide filtering:** hide non-`kid-safe` entries by default, add the session-only grown-up gate, and make `src/guide.py` use only `kid-safe` entries that fit the chosen age (entry `age_group` <= chosen age) and goal. Otherwise the guide can show teen+ material to a 6-year-old. Details in "Ask the team".
4. **Frontend + pitch lead** — `src/templates/`, `src/static/`: pages, level badges, language switcher, attribution footer, accessibility; then README, slides, demo video, submission.

**Data contract** (`src/data/learn.json`, `build.json` = CC0; `kids.json` = CC BY-SA 4.0, kept separate; each a list of entries):
`{id, category, tag, title:{en,...}, desc:{en,...}, level, age_group, topic, safety, safety_reasons, url, source, license}` plus optional `ai_translated`
- `id`: `<learn|build|kids>-<8 hex of sha1(url)>`, stable between runs. `tag`: language tag from build-your-own-x (e.g. "Python"), else "".
- `level`: Beginner | Intermediate | Advanced
- `age_group`: youngest suitable age: "5-7" | "8-10" | "11-13" | "teen+". For `kids.json` it comes from the source (CS Unplugged's "11-14" maps to "11-13") and categorize.py never overwrites it.
- `topic`: games | art | web | general | systems | security | other
- `safety`: "kid-safe" | "ask-a-grown-up" | "adult-only"
- `safety_reasons`: short strings, empty only for kid-safe (e.g. "security-tooling", "external-forum", "social-platform", "account-required", "unvetted-external-site", "not-kid-oriented-topic", "off-topic", "unclassified")
- `ai_translated`: list of languages (es, ar, hi, pt) whose `title`/`desc` text was written by AI. The UI must label these as AI-generated.
- `reuse`: "open-content" (content license verified to allow reuse: only CS Unplugged) | "link-only" (everything else); `reuse_license` only on open-content. Set by `scripts/mark_reuse.py`.
- `license`: "CC0-1.0" for learn/build, "CC-BY-SA-4.0" for kids. `source` is the repo URL, `url` the original page (we link out, never copy content).
- Entries are sorted kid-safe first, then Beginner first (translate.py works in file order).

**Pipeline order:** `fetch.py` -> `fetch_kids.py` -> `categorize.py --no-ai` (applies rules, then the committed label cache, then `safety_overrides.json` last) -> `mark_reuse.py` -> `fetch_lessons.py` -> `build_guides.py` -> translations (by hand; `translate.py` is optional and needs a key) -> `coverage.py`, `check_links.py`, `python -m unittest discover -s tests`. **After the data freeze do not re-run `fetch.py`** (it re-downloads the upstream lists; new entries would only get fail-closed rules).

**Git:** branch per person (`data`, `ai`, `backend`, `frontend`), small commits, pull before push, merge to `main` often.

**Languages (start with):** Spanish, Arabic (RTL), Hindi, Portuguese.

## MVP (must ship)
- [x] Source repos picked and licenses recorded in `docs/SOURCES.md` (awesome, build-your-own-x)
- [x] Parser cleaned: language tags split out, markdown stripped, deduped by URL (Data lead)
- [x] `scripts/categorize.py`: topic, level, age_group, safety tier (rules + committed hand-labeled cache, no API key needed)
- [x] Human safety spot-check (`docs/SAFETY_REVIEW.md`, all rows ok) and a human overrides file
- [x] Polite link checker; 7 dead links removed (`scripts/cache/removed_links.json`)
- [x] Data tests, coverage report, link checker (Data lead)
- [x] Translation approach: titles/descriptions translated by hand by Claude Code (no paid API), code and technical terms kept in English, labeled `ai_translated`
- [x] 4 languages started (Spanish, Arabic, Hindi, Portuguese) for 74 entries
- [x] Guide page skeleton (`src/guide.py`, done) — needs kid-friendly data + tagging to shine
- [x] Kid-friendly source added: CS Unplugged (`scripts/fetch_kids.py` -> `src/data/kids.json`, 57 entries: 7 units, 26 lessons, 5 programming-challenge pages, 19 classroom integration activities; CC BY-SA 4.0)
- [x] First translations done: 74 kid-safe Beginner + the first 33 CS Unplugged entries in es/ar/hi/pt (hand-written, labeled `ai_translated`); the 24 newer CS Unplugged entries and all other kid-safe entries are in `docs/TRANSLATE_QUEUE.md`
- [ ] Translate the remaining kid-safe entries (Intermediate) and check translations with native speakers
- [x] Data docs for the pitch: `docs/STATS.md`, `docs/SAFETY_REVIEW.md`, `docs/TRANSLATE_QUEUE.md`
- [x] Guides foundation: `reuse` flag, fallback guides, helpers, tests (`docs/GUIDE_SPEC.md`)
- [x] Lessons from CS Unplugged (`lessons.json`, 26) and handwritten guides (65 of 65 groups, 100% of visible entries; `docs/GUIDE_PROGRESS.md`)
- [x] Browser-only progress (`progress.js`, spec in `docs/PROGRESS_SPEC.md`); Tobi must add the template hooks listed there
- [x] App: guide slide viewer, `/<lang>/lessons` and lesson page with the CC BY-SA attribution box (merged, PR #14)
- [x] List pages: search box and age/topic/level filters, hidden-entry notice (issue #7)
- [ ] Deploy on Render (needs the owner's Render sign-in, issue #8; steps in `docs/ISSUES_TRIAGE.md`)
- [x] Lesson page with language switcher + level tag (`/<lang>/lesson/<id>`)
- [x] Level path / roadmap: the guide slides, timeline strip and "Explore next"
- [x] Attribution/license footer + CC BY-SA attribution box on every lesson and a link to the source on every entry
- [ ] Deployed link + demo video

## Next steps (after the hackathon)
- Optional **parent accounts with child profiles** (opt-in, with consent), to sync progress across devices. Until then progress is browser-only.

## Stretch
- [ ] Low-bandwidth / offline-friendly pages
- [ ] Community translation corrections
- [ ] Search across lessons

## Timeline (official)
**Saturday, Nov 7**
| Time | Event |
|------|-------|
| 12:00 PM | Doors open / sign-in |
| 12:30 PM | Opening remarks (track details) |
| 1:15 PM | **Hacking begins** + team formation |
| 1:30 PM | Chick-fil-A lunch |
| 3:00 & 5:00 PM | Technical workshops |
| 7:00 PM | Anna's Taqueria dinner |
| 7:30 PM | Closing remarks; space closes shortly after |

**Sunday, Nov 8**
| Time | Event |
|------|-------|
| 8:00 AM | Working space reopens |
| **9:00 AM** | **Projects due** + Dunkin' breakfast |
| 9:30 AM | Judging begins |
| ~11:15 AM | Prizes + closing remarks |
| 12:00 PM | Space closes |

## Our working schedule
| When | Goal |
|------|------|
| Sat 12:30-1:15 | Listen to tracks, pick track + idea, form team |
| Sat 1:15-3:00 | Pick stack, scaffold, split tasks, core happy path started |
| Sat 3:00-7:30 | Core feature working end to end |
| Sat night | Wrap up/sleep; plan Sunday fixes |
| Sun 8:00-8:45 | Polish, deploy, README, demo video, submit |
| Sun 9:00 | SUBMITTED (hard deadline) |

## Decisions
- **Categorize, don't filter.** We keep every entry from the two existing CC0 sources and tag each one, so the site serves young learners (5-13) and still offers advanced material. No new sources up front; add one only if coverage results show gaps (`python scripts/coverage.py`). Coverage showed gaps for young ages, so we added `uccser/cs-unplugged` (see below).
- **Safety tiers:** `kid-safe` (nothing risky in the listing), `ask-a-grown-up` (forums/social platforms, accounts or payment, security or network topics, crypto/finance, unvetted sites, or just unclear), `adult-only` (hacking/exploit/malware tooling, adult content).
- **YouTube/Vimeo links are treated as normal (not flagged).** We rely on YouTube's own age restrictions rather than gating every video.
- **Fail closed:** unclear means `ask-a-grown-up`, never `kid-safe`. `kid-safe` also requires a kid topic (games/art/web/general) and a vetted link host. The AI pass can only make an entry stricter, never looser than the rules. We classify titles, descriptions, categories and link hosts only, never the linked pages.
- **Parental gate (design):** by default the site hides `ask-a-grown-up` and `adult-only` entries. An adult can reveal `ask-a-grown-up` entries for the current session only (a simple "I'm a grown-up" confirmation; `adult-only` stays hidden). No accounts, no personal data stored.
- **No paid API.** Nothing in the data pipeline needs an API key. The AI-style classification in `categorize.py` was done by hand (by Claude Code in the Data lead's session): 953 entries the rules could not decide were labeled and stored in `scripts/cache/categorize.json` (same format the script's API pass uses), then `python scripts/categorize.py --no-ai` merges them. The cache is **committed**: it is small, holds only labels for public titles, and lets the whole team and the Sunday rebuild reproduce the data with no API key. New entries not in the cache fall back to fail-closed rules ("unclassified" -> ask-a-grown-up).
- **Vetted hosts:** first tier only: aosabook.org, scratchapixel.com, fullstackpython.com, nand2tetris.org, developer.ibm.com, swtch.com (plus GitHub, MDN, Khan Academy, etc. already in `KNOWN_OK_HOSTS`). Medium family, paywalled, ad-heavy and community sites stay unvetted.
- **CS Unplugged added** (`uccser/cs-unplugged`): content CC BY-SA 4.0 (`LICENCE-CONTENT`), code MIT (`LICENCE`), verified from the repo. Only titles, a short description we wrote, the repo's age group and a link to the lesson page are stored; no lesson text or images. Kept in `kids.json`, separate from the CC0 files. Translations of it must stay CC BY-SA 4.0 with attribution and a "changes were made" note (see `docs/SOURCES.md`).
- **Title keywords can raise safety, too:** Slack/Telegram/Twitter/etc. in a title now add `social-platform` (found when a Slack-bot tutorial slipped through as kid-safe).
- **CS Unplugged activities added** (Nov 7): programming-challenge pages and classroom integration activities, using the same rules (own short description, repo-stated age, link only). Only 5 lessons really have programming challenges; the rest of the site's `/programming/` pages are empty, so they are skipped. Integrations without a stated age are skipped.
- **Link-check policy.** `check_links.py` is polite (1 request/second/host, backoff on 429, one retry) and classifies results as ok / rate_limited / blocked_bot / broken / error. 429 and 403 are NOT treated as broken. It never edits data; confirmed-dead links (404, DNS, bad SSL) are removed by hand and listed in `scripts/cache/removed_links.json`, which `fetch.py` skips. Timeouts and 5xx are rechecked before removal. 7 removed so far; 9 temporary errors remain, all ask-a-grown-up.
- **Guides and lessons (decided).** Link-only entries get an AI-written overview guide (slides + a rule-based timeline) ending in a "leaving our site" slide. Open-content entries (CS Unplugged, CC BY-SA 4.0) are adapted into our own lessons in `src/data/lessons.json`. Every visible entry always resolves to a guide (fallback per topic in `src/data/guides.json`). Guides are written from catalog data only and never claim what is on the linked page. Details: `docs/GUIDE_SPEC.md`; progress: `docs/GUIDE_PROGRESS.md`.
- **Progress is browser-only.** A child can mark entries and lessons as done and see stars; it is stored only in their own browser (`localStorage`, key `hc_progress_v1`, ids only), with a progress code to move it between devices. No accounts, no cookies, no server storage. Spec: `docs/PROGRESS_SPEC.md`; hooks for Tobi are listed there.
- **Site name: Open Cosmos (renamed from "Learning Lab", Nov 8).** The page title, meta tags, footer and generated attribution texts use "Open Cosmos", always in Latin script in every language (in right-to-left text it is wrapped in a bidi isolate or `<bdi>`). It is the `brand` string in `src/ui_strings.py`. The GitHub repo name (`ktp-hackcessability-2026`) and the Render service name (`learning-lab` in `render.yaml`) are unchanged on purpose, so the repo URL and the live service are not recreated. Generated data was rebuilt from the scripts; `build_problems.py --no-node` was used because node is not installed here (text-only change, JavaScript problems not re-checked).
- **List pages (issue #7).** `/<lang>/learn`, `/build` and `/kids` have a search box and age/topic/level filters (`?q=`, `?age=`, `?topic=`, `?level=`), and explain how many entries are hidden until grown-up mode (adult-only is never counted or shown).
- **translate.py (issue #6).** It strips code fences, retries once, runs 5 requests at a time, defaults to `claude-haiku-5-5` (env `ANTHROPIC_MODEL` overrides) and translates only kid-safe entries unless `--all`. It still needs an API key; hand translations go in an overlay file (see below).
- **Guide translations (Nov 7).** All 72 guides (65 groups + 7 fallbacks) are translated into es, ar, hi and pt: 663 unique texts, written by hand by Claude Code (no API), AI-written and not yet checked by native speakers. They live in an overlay, `src/data/guides_translated.json` (English text -> {lang: text}), and `guides.json` stays English-only. `src/store.py` merges it at load, all or nothing per guide and language, so a guide never mixes two languages. Placeholders (`{entry_title}`, `{age}`, `{level}`, `{minutes}`, `{sessions}`) are kept; `{level}` is filled with the English level name. Lessons are translated too (see the next decision).
- **Lessons and interface strings translated (Nov 7).** All 26 lessons (429 unique texts) are translated into es, ar, hi and pt in `src/data/lessons_overlay.json` (English text -> {lang: text}); `lessons.json` stays English-only and `store.py` merges the overlay, all or nothing per lesson and language. About 85 interface strings that were still falling back to English (Arabic 72, Hindi 87, Portuguese 17, Spanish 8: "Materials", "Steps", "Explore next", system names, hidden-link reasons, the CC BY-SA attribution texts and more) are in `src/data/ui_translated.json`. A test fails if any string is missing in any language (names such as Python or the brand may stay English). The titles and descriptions of the last 377 kid-safe entries are translated too (`scripts/translation_content/entries_queue.json`, merged by `scripts/apply_translations.py`), so `docs/TRANSLATE_QUEUE.md` is empty. The 76 coding problems (930 texts: titles, prompts, hints, steps, test names) are translated in `src/data/problems_overlay.json` (code stays English; `problems.json` stays English-only; merged by `store.py`). The titles and descriptions of the 610 grown-up-section (ask-a-grown-up) entries are translated too (`scripts/translation_content/entries_grownup.json`, merged by `scripts/apply_translations.py`). Nothing in the catalogue falls back to English any more, except product names. Native-speaker checks are still needed.
- **Sites that are not in the learner's language.** The last slide of every guide now says the site may not be in their language and that the browser's own "translate this page" button can help (or ask a grown-up). We do not link to Google Translate or any translation proxy: that would send the page a child is visiting to a third party, and we promised not to track. Machine translation can garble code, so code stays in English. Later: link to a human translation when the source has one (CS Unplugged has es, fr, de, it and more).
- **Heuristic caveat:** for the two CC0 sources, `age_group` "11-13" means "Beginner-level web/games/general material", not "written for kids". Only CS Unplugged is actually kid-targeted.

- **Human safety spot-check.** `docs/SAFETY_REVIEW.md` lists 30 random kid-safe, 15 random ask-a-grown-up, all 15 adult-only and 10 youngest/rarest kid-safe entries. Eren reviewed all rows: every one was `ok` (no loosening or tightening needed). Corrections would go in `scripts/cache/safety_overrides.json` (`{"<id>": {"safety": "<tier>", "reason": "..."}}`); `categorize.py` applies it LAST and it may loosen or tighten. The file is currently empty (`{}`). A sample of about 70 of 1,068 entries is a spot-check, not a full review.

## Coverage gaps (for Tobi; run `python scripts/coverage.py`)
26 of 36 age/goal/level combinations have fewer than 6 kid-safe entries. What is real and what is short:
- **Ages 5-7:** only `general` Beginner has real content (24 entries). Games, art and web have 0, and there is no Intermediate or Advanced.
- **Ages 8-10:** `general` Beginner 60; art Beginner 5; games 1; web 0; no Intermediate or Advanced.
- **Ages 11-13:** games, art and web have Beginner and Intermediate (6-9 each); Advanced has 0 everywhere. General is well covered.
- **Rules so the guide never shows an empty or unsafe path:**
  1. Use only `safety == "kid-safe"` entries with `age_group` <= the chosen age.
  2. **Ages 5-10: show only Beginner and only the `general` topic**, whatever goal was chosen (plus the goal's own entries if there are any, e.g. 8-10 art). Don't offer Intermediate/Advanced at these ages.
  3. Backfill A: if the goal has fewer than 6, add `topic == "general"` entries at the same level.
  4. Backfill B: if still short, add entries of the next lower level at the same age.
  5. If a path still ends up under 6, show what exists plus a note ("more coming"), never an empty list, and never an entry that is not `kid-safe`.
  6. Say plainly in the UI that CS Unplugged lessons are for an adult to do with a child.
- These gaps are real (no more open sources are planned), so the pitch should say "growing library" rather than imply full coverage.

## Ask the team (changes needed in files Eren doesn't own)
- **Tobi (`src/app.py`, `src/guide.py`):**
  - Load `kids.json` alongside `learn.json` and `build.json`.
  - Safety gate: hide `safety != "kid-safe"` by default; a session-only "I'm a grown-up" confirmation reveals `ask-a-grown-up`; `adult-only` is never shown. Filter by `safety`, `topic` and `age_group`.
  - Guide: `candidates()` should use only `kid-safe` entries whose `age_group` is <= the chosen age (teen+ never shown to kids) and match the goal's `topic`. **Coverage today:** 26 of 36 age/goal/level combinations have fewer than 6 matching entries (run `python scripts/coverage.py`). Two simple rules fix all of them (simulated against the current data): (A) if the goal has fewer than 6 matches, backfill with `topic == "general"` entries at the same level; (B) if still short, backfill with the next lower level at the same age. For ages 5-10 you may also want to offer only Beginner.
  - Note `topic` also has systems/security/other values.
  - `src/guide.py` still has an optional Claude path (`anthropic`, `ANTHROPIC_API_KEY`). We have no key, so the rule-based path above is the real one: make it the default, and drop the AI path and `anthropic` from `requirements.txt` if nobody will use it (also keeps the deploy simple).
- **Tobi: browser-only progress (read `docs/PROGRESS_SPEC.md`, section "Hooks Tobi must add").** `src/static/progress.js`, `progress.css` and `src/data/progress_text.json` are done and tested; nothing shows until you add these:
  1. `app.py`: load `progress_text.json` and add `"progress_text": {**PT["en"], **PT.get(lang, {})}` to `ctx()` (skip the `_note` key).
  2. `base.html`: the CSS `<link>`, the `<script type="application/json" id="hc-progress-text">{{ progress_text | tojson }}</script>` block, `<script src=".../progress.js" defer>`, and a footer `<p data-progress-privacy>{{ progress_text.privacy }}</p>`.
  3. `entry.html` and the lesson page: `<article data-progress-item="{{ id }}">`.
  4. `/<lang>/lessons`: `<section data-progress-panel></section>`, `<p data-progress-summary></p>`, and `<ul data-progress-list>` with `<li data-progress-id="{{ lesson.id }}">`.
  5. Home page: `<span data-progress-stars></span>`.
  6. No change to the headers: `app.py` sets no CSP today, and the script is CSP-friendly (an external file, no inline script). Nothing is stored on the server and there are no cookies.
- **Tobi and Isabella: guides and lessons.** Full task lists in `docs/GUIDE_SPEC.md` (load `guides.json` and `lessons.json`, entry page uses `guide_for`/`build_timeline`/`related_entries`, `/<lang>/lessons` routes, slide viewer, CC BY-SA attribution box on every lesson).
- **Isabella (`src/templates/`):**
  - Footer/attribution line: "Lessons from CS Unplugged (University of Canterbury CSER Group), licensed CC BY-SA 4.0. Titles and descriptions translated and level-tagged by Open Cosmos with AI; changes were made. Other lists: CC0." Link https://creativecommons.org/licenses/by-sa/4.0/.
  - Show an "AI-translated" badge on any entry whose current language is in `ai_translated`.
  - Safety badges, the grown-up gate UI, and a short "why is this hidden?" text that explains `safety_reasons` in plain language.
  - Show `tag` (programming language) on build entries.
  - CS Unplugged lessons are teacher/parent lesson plans, so say "for an adult to do with a child".
- **Brian (`scripts/translate.py`, and `src/guide.py` / `requirements.txt` with Tobi):**
  - 74 kid-safe Beginner and CS Unplugged entries are already translated in es/ar/hi/pt, so translate.py skips them (it translates only entries missing a language). Remaining kid-safe Intermediate entries are the next batch.
  - **Guide translations are done** (see Decisions): no need to translate guides. Native-speaker checks are still needed. Lesson text is translated too.
  - **Translation queue:** `docs/TRANSLATE_QUEUE.md` lists the 401 kid-safe entries still untranslated (24 CS Unplugged, 258+36 Intermediate, 65+18 Advanced), in priority order, with counts per level and source. Pick row ranges with Eren so nobody edits the same JSON entries.
  - `translate.py` needs an API key and we have none, so translations are done by hand (Claude Code in Eren's session) as overlay modules in `scripts/translation_content/`, merged by `python scripts/apply_translations.py`; the 24 newest CS Unplugged entries are done this way. 377 kid-safe entries remain (`docs/TRANSLATE_QUEUE.md`, regenerate with `python scripts/translate_queue.py`). The script's problems from issue #6 are fixed (code fences, one retry, 5 requests at a time, model `claude-haiku-5-5`); native-speaker checks are still needed.
  - Eren's minimal changes to your file: `kids` is included, `level`/`age_group` set by categorize.py are not overwritten, entries are chosen by missing languages, and `ai_translated` is set. Please keep those.

- **Isabella (`docs/PITCH.md`):** the pitch says the AI picks the path in the guide. Change it to: the guide builds a path from our tagged open data using simple rules and can only pick real entries; AI was used ahead of time to translate and classify (no live AI, no key, no personal data).

## Blockers / Notes
- Bring laptop + charger.

## Frontend decisions (Isabella, Nov 7)
- Galaxy UI on top of the team backend: subjects = galaxies, tracks = systems, entries = stops (`src/tracks.py`). Map in `docs/FRONTEND.md`.
- Guide slides render on `/entry/<id>`; one slide at a time with JS, all stacked without JS. External link only on the last slide, after the leaving notice.
- Card "time" from the sketch is the stop kind (screen-free lesson / build project / resource list); real times only appear as labeled estimates in the guide.
