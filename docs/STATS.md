# Stats for the pitch (Nov 8 2026)

Generated from `src/data/*.json`, `scripts/cache/link_report.json` and `python scripts/coverage.py`; translation, guide and problem counts were recounted on Nov 8 for the final submission. Numbers feed the slides; rerun after any data change.

## Headline
- **1,085 open-licensed entries** from 3 sources, each linking out to the original with its license.
- **475 kid-safe** entries (44%); 595 ask-a-grown-up; 15 adult-only (never shown).
- **57 kid-targeted** CS Unplugged entries (ages 5-13), **26 adapted lessons** and **76 coding problems** (24 ours, 52 adapted from CS Unplugged).
- **1,078 of 1,085 links** respond (OK or bot-blocked); 1,048 confirmed OK; 7 unreachable right now (all ask-a-grown-up); 7 dead links removed earlier.
- **Translated (title + description): all 1,085 entries in Spanish, Arabic, Hindi and Portuguese** (475 kid-safe and 610 behind the grown-up gate), plus all 72 guides, 26 lessons, 76 coding problems and the interface. AI-written, labelled, not checked by native speakers.

## By source

| Source | Entries |
|---|---|
| awesome (CC0) | 676 |
| build-your-own-x (CC0) | 352 |
| CS Unplugged (CC BY-SA 4.0) | 57 |

## By level

| Level | Entries |
|---|---|
| Beginner | 136 |
| Intermediate | 693 |
| Advanced | 256 |

## By topic

| Topic | Entries |
|---|---|
| general | 314 |
| systems | 237 |
| web | 214 |
| other | 169 |
| games | 70 |
| art | 46 |
| security | 35 |

## By age group (suggested youngest age)

| Age group | Entries |
|---|---|
| 5-7 | 24 |
| 8-10 | 37 |
| 11-13 | 109 |
| teen+ | 915 |

## By safety tier

| Safety | Entries |
|---|---|
| kid-safe | 475 |
| ask-a-grown-up | 595 |
| adult-only | 15 |

## Kid-safe entries per age group

| Age group | Entries |
|---|---|
| 5-7 | 24 |
| 8-10 | 36 |
| 11-13 | 77 |
| teen+ | 338 |

Kid-safe ages 5-10 are almost entirely CS Unplugged: 5-7: 24 of 24 are CS Unplugged, 8-10: 31 of 36 are CS Unplugged, 11-13: 2 of 77 are CS Unplugged.

## Translation status

| Language | Entries fully translated (title + description) | Of them kid-safe | Guides (72) | Lessons (26) | Coding problems (76) |
|---|---|---|---|---|---|
| Spanish | 1,085 of 1,085 | 475 of 475 | 72 | 26 | 76 |
| Arabic | 1,085 of 1,085 | 475 of 475 | 72 | 26 | 76 |
| Hindi | 1,085 of 1,085 | 475 of 475 | 72 | 26 | 76 |
| Portuguese | 1,085 of 1,085 | 475 of 475 | 72 | 26 | 76 |

All translations are AI-generated, written by hand by Claude Code (no paid API) and labelled with `ai_translated`; **none has had a native-speaker check yet**. A page is shown in a language only when everything on it is translated, so pages never mix two languages.

## Link verification

| Result | Links |
|---|---|
| OK | 1048 |
| Bot-blocked (403, usually Medium; probably fine) | 30 |
| Unreachable now (timeouts, SSL, 5xx; rechecked Nov 8) | 7 |
| Removed as dead (404/DNS/SSL) | 7 |

All 57 CS Unplugged links are OK. Checked politely (one request per second per host, backoff on 429).

## How we keep it safe

Every entry gets one of three tiers: **kid-safe** (nothing risky in the listing), **ask-a-grown-up** (forums and social platforms, accounts or payments, security or networking topics, crypto and finance, sites we have not vetted, or anything unclear) and **adult-only** (hacking, malware and exploit tooling, adult content). The system **fails closed**: when a rule is unsure, the entry goes to ask-a-grown-up, never kid-safe, and kid-safe also needs a kid-friendly topic (games, art, web, general) and a vetted link host. The site hides everything but kid-safe by default; an adult can reveal ask-a-grown-up entries for the current session, and adult-only entries are never shown. There are no accounts, no free-text input and no personal data. Rules did the first pass, the leftover entries were labeled by hand with the same fail-closed rule, and a person spot-checked 70 entries (30 kid-safe, 15 ask-a-grown-up, all 15 adult-only, 10 youngest-age kid-safe): all were fine, and a human-overrides file can tighten or loosen any label. **Limits:** we classify titles, descriptions, categories and link hosts only. We do not read the linked pages, so "kid-safe" means "nothing in the listing looks risky", not "we reviewed the page", and linked sites can change. A grown-up should still supervise, and YouTube links follow YouTube's own age restrictions.

## Honesty caveats
- For the two CC0 lists, age group "11-13" means **beginner-level web, games or general material**, not material written for kids. Only **CS Unplugged** is kid-targeted, and its lessons are plans for an adult to do with a child.
- Real kid content for games, art and web at ages 5-10 is thin (see `docs/PLAN.md` "Coverage gaps"); the guide backfills with general beginner material.
- The CC0 licenses cover the lists, not the pages they link to. We copy no page content and always link out.
- Translations are AI-generated and unreviewed by native speakers; the UI labels them.

## Guides and lessons
- **65 handwritten group guides** + 7 topic fallbacks: 100% of the 1,070 visible entries resolve to a guide (1,044 end in "go to the learning site", 26 end in "go to our lesson").
- **26 adapted lessons** (CS Unplugged, CC BY-SA 4.0): ages 5-7: 12, 8-10: 13, 11-13: 1.
- **Reuse flag:** 1,028 link-only entries, 57 open-content entries.
- Guides, lessons, coding problems and the interface are available in all five languages (AI-written, not checked by native speakers). Guides are written from catalogue data only and time estimates are estimates. More in `docs/PITCH_DATA.md`.
- **Guide translations:** all 72 guides are translated into Spanish, Arabic, Hindi and Portuguese (AI-written, not yet checked by native speakers). All 26 lessons are translated too.
