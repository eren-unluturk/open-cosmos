# Open Cosmos

**Winner, Information Access track, Hackcessability (Nov 2026)**

**Live site: https://open-cosmos.vercel.app** · Track: **Information Access** · KTP Hackathon, Nov 7-8 2026

Open Cosmos, winner of the Information Access track at Hackcessability (Nov 2026), turns the best free programming resources, which are open on GitHub but hard for a beginner to approach and almost all in English, into a safe, space-themed learning map for young beginners (about ages 5-13), the parents and teachers who help them, and anyone who reads English as a second language. Every one of the 1,085 entries is open-licensed, tagged by level, age, topic and **child-safety tier**, translated into Spanish, Arabic, Hindi and Portuguese, and opens a short **guide with a roadmap**. Adults unlock the less kid-friendly material with a session-only **grown-up switch**. We claim none of the content: every entry links to its original and its license.

## What it does
- **Five languages:** English, Spanish, Arabic (right to left), Hindi and Portuguese: titles, descriptions, guides, lessons, coding problems and the interface. All translations are AI-written and **not yet checked by native speakers**; the site labels them.
- **Open data only:** the **Learn** side ([sindresorhus/awesome](https://github.com/sindresorhus/awesome), CC0), the **Build** side ([codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x), CC0) and **CS Unplugged** ([University of Canterbury CSER Group](https://github.com/uccser/cs-unplugged), CC BY-SA 4.0). See `NOTICE.md` and `docs/SOURCES.md`.
- **Safety tiers and the grown-up gate:** each entry is `kid-safe`, `ask-a-grown-up` or `adult-only`. Safety **fails closed** (unclear means ask a grown-up; rules and the AI-written labels can only tighten a tag). Kids see only kid-safe entries; a grown-up can reveal the middle tier for the session; adult-only is never shown.
- **"What should I learn?"** Three multiple-choice questions (age, goal, level) build an ordered path with simple rules. No free text, nothing stored, no AI at runtime.
- **Guides and roadmaps:** every entry has a slide guide (what it is, is it for me, how to start, how much time) and a timeline (Day 1, Week 1...). Link-only entries end with a "you are leaving our site" slide.
- **Adapted lessons:** 26 CS Unplugged lessons rewritten in our own simple words, with a CC BY-SA attribution box and a "changes were made" note.
- **Coding problems:** 76 problems (39 Python, 37 JavaScript) that run **in your browser** (your code never reaches our server), with hints and a guided mode.
- **Browser-only progress:** stars and badges are saved in `localStorage` only. No accounts, no cookies for progress, nothing sent to us.
- **Accessibility:** colour modes (galaxy, light, high contrast, colour-blind-safe), text size and spacing, an easy-to-read font, reduced motion, **read-aloud** with the browser's own voices, and an accessibility statement. See `docs/ACCESSIBILITY.md`.

## 2-minute demo path
1. **Home** at https://open-cosmos.vercel.app: press **"Find my first lesson"** (the yellow button), choose an age (5-7), a goal and a level, then press **"Show my path"** to see a short ordered path.
2. Open **"How binary digits work"** (`/en/entry/kids-0d3a63dc`): swipe the guide and roadmap, press **Listen**, then **Go to the lesson**: our adapted lesson with its CC BY-SA box.
3. Switch the language to **Arabic**: the whole page flips right to left; "Open Cosmos" stays in Latin letters.
4. Open **Accessibility** in the header: try **High contrast** and **150%** text.
5. Open **"2D breakout game using Phaser"** (`/en/entry/build-74d1338b`): a link-only entry with the leaving-our-site notice.
6. Press **"I'm a grown-up, show them"** in the footer: the hidden entries and the **feedback form** appear.
7. Open a **coding problem** (`/en/problem/py-hello`), run and check your code in the browser.

(The specific entries and links: `docs/DEMO_SLICE.md`.)

## Run it locally
```bash
git clone https://github.com/eren-unluturk/open-cosmos.git && cd open-cosmos
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/flask --app src/app run -p 5001      # then open http://127.0.0.1:5001
.venv/bin/python -m unittest discover -s tests # tests
```
No keys, database or account are needed: the site reads the JSON in `src/data/`. Optional features (Supabase catalog and feedback) switch on only if you add `SUPABASE_URL` and `SUPABASE_ANON_KEY` to a local `.env` (never commit it): see `docs/SUPABASE.md`.

## How it is built
- **Flask + Jinja2**, server-rendered, no JavaScript framework and no build step; static files in `public/static/`.
- **Data:** `src/data/*.json`, produced ahead of time by `scripts/` (fetch, categorize, safety-tag, translate, build guides and lessons) and committed. No paid API anywhere.
- **Hosting: Vercel** (`index.py` is the entry point, `vercel.json` sets headers for static files, `src/csp.py` the Content-Security-Policy for pages). Setup: `docs/DEPLOY.md`.
- **Supabase (optional):** a copy of the catalogue (read-only to the public) and the grown-ups' feedback table (insert-only), both behind Row Level Security. **The bundled JSON is always the fallback**: any Supabase error, timeout or empty result and the site just uses the JSON (`CONTENT_SOURCE=auto`).
- **Quality checks:** Python and Node tests, `scripts/check_contrast.py` (WCAG AA colours), `scripts/smoke_remote.py` (1,000+ checks against a running site), axe-core accessibility audits, `scripts/check_rls.py`, `scripts/freeze_check.py`.

More: `docs/PLAN.md` (decisions), `docs/BACKEND.md`, `docs/FRONTEND.md`, `docs/GUIDE_SPEC.md`, `docs/STATS.md`.

## Accessibility
Settings panel (four colour modes, text size and spacing, an easy-to-read font, reduced motion), read-aloud, and a statement page in five languages. **Automated result: 1,115 page states audited with axe-core in all five languages, colour modes and text settings (WCAG 2.0/2.1/2.2 A and AA plus best-practice rules): 0 violations; all four colour modes pass the WCAG AA contrast check; 66 automated keyboard-only and Arabic right-to-left checks pass.** Manual screen-reader (VoiceOver) and 200% zoom testing is still pending, and automated tools catch only some problems. How we tested, the checklist and the limits: [`docs/ACCESSIBILITY.md`](docs/ACCESSIBILITY.md). Barrier reports are welcome (grown-up view, then the feedback form).

## Team
| Name | Role | What they did |
|---|---|---|
| **Eren** | **Data lead** | Led the data pipeline: sourcing the open lists and CS Unplugged, categorizing every entry, safety tagging and the grown-up gate's rules. Designed the guides, lessons and roadmaps. Set up the Supabase catalogue and feedback form, the Vercel deployment and the cutover, and set the direction for the accessibility features. |
| Brian | **AI lead** | Translation quality and queue, native-speaker spot checks. |
| Tobi | **Backend lead** | Flask routes, language and level filtering, UI strings, right-to-left support, search, the safety gate and guide filtering, deployment. |
| Isabella | **Frontend + pitch lead** | Pages, the galaxy theme, level badges, language switcher, attribution footer; README, slides, demo video and submission. |

## Honest limitations
- **Translations are AI-written and not reviewed by native speakers.** Some wording will be unnatural or wrong.
- **"Kid-safe" is a judgement about the listing** (title, description and host), not a review of the linked pages. A person checked 70 entries (`docs/SAFETY_REVIEW.md`). The grown-up switch is a convenience, not security.
- **Kid content is thin** for games, art and web at ages 5-10 (26 of 36 age/goal/level combinations have fewer than 6 kid-safe entries; `docs/STATS.md`). The guide backfills with general beginner material and says so.
- **Guides are written from catalogue data only** (we did not read the linked pages) and time estimates are estimates.
- **We link out, we do not host** most content; the linked sites may not be in the learner's language.
- **Accessibility** was checked with automated audits (axe-core, 0 violations), automated keyboard-only and right-to-left tests and a contrast script. We have had no outside audit and have not tested with a real screen reader ourselves (a VoiceOver checklist is in `docs/ACCESSIBILITY.md`). Read-aloud voices depend on the device.
- Python problems need an internet connection the first time (Python is downloaded to your browser).
- No accounts means progress does not sync between devices (a progress code moves it by hand).

## Privacy
No accounts, no analytics, no ads, no tracking, no location. Learning progress and accessibility settings stay in your browser. The only thing we ever receive is a **grown-up's feedback message** (category, message, page, language, time; no name or email). Details and what is not perfect: `docs/SECURITY.md`.

## Security
There is nothing to log in to and no user data to steal; the keys are server-side only and were never committed; the database is insert-only for feedback and read-only for the catalogue (tested with the public key). Read the short, honest answers in **`docs/SECURITY.md`**.

## What we learned
- **We categorized instead of filtering, and made safety fail closed.** Keeping every entry and tagging it let us serve young learners and still offer advanced material. Rules and the AI-written labels can only make a tag stricter, and a test enforces it. False matches taught us a lot ("from scratch" is not Scratch; a Slack-bot tutorial is not kid-safe).
- **Parsing is never as clean as it looks.** Our first parser silently dropped about 30 build entries; counting lines in the source found it.
- **Free and static beat clever.** No paid API: classification and translation were done ahead of time and committed, so anyone can rebuild with no key, and the site is fast and cheap to host.
- **ShareAlike is a real constraint.** CS Unplugged is CC BY-SA, so we attribute, say "changes were made", keep it apart from the CC0 lists and share our adaptations (and their translations) the same way.
- **Supabase tables need explicit GRANTs and Row Level Security.** A policy alone is not enough when "expose new tables" is off, and we proved the rules by attacking them with the public key.
- **Keep secrets server-side and in `.env`**, and scan the git history, not just the files.
- **Commit often.** A day of Vercel work was nearly lost because it sat uncommitted when we switched branches (it survived in a git stash).
- **A strict Content-Security-Policy breaks things quietly**: our self-hosted font was blocked until `font-src 'self'` was added in both places the policy lives (Flask and `vercel.json`), and a test now keeps the two in step.
- **Accessibility needs real audits** (axe, a contrast script, keyboard walk-throughs), not just good intentions: the audits found missing button names on phones, hard-coded English labels and low-contrast borders that we had not noticed.

## Licensing
Our code: **MIT** (`LICENSE`). Content: CS Unplugged under **CC BY-SA 4.0** (University of Canterbury CSER Group; our adaptations and translations are shared the same way), the two link lists under **CC0**, the easy-to-read font under the **SIL OFL**. Full list in `NOTICE.md` and `docs/SOURCES.md`.
