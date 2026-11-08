# Frontend: galaxy theme (Isabella)

Space-themed UI built from Isabella's sketches (home, constellation, galaxy map, lesson page).
Server-rendered Jinja + one CSS file + one small JS file. No build step, no framework, no CDN scripts.

## Where things are
| File | What it is | Tinker here to… |
|------|------------|-----------------|
| `public/static/galaxy.css` | All styles. Colors are the `:root` variables at the top. | Change colors, fonts, spacing, card shapes, button shapes |
| `public/static/a11y.css`, `a11y.js`, `a11y-settings.js`, `listen.js`, `fonts/` | Accessibility: colour themes (tokens only), text size and spacing, the settings panel, the head script that applies saved settings before first paint, read-aloud, and the self-hosted Atkinson Hyperlegible font (SIL OFL). Details: `docs/ACCESSIBILITY.md`. | Add a theme or a setting |
| `public/static/problem.js`, `runner.js`, `problems.css` | Coding problems: editor page logic and the Web Worker that runs learner code in the browser. | Problem page behaviour |
| `public/static/galaxy.js` | Progress stars (localStorage only), the guide slide viewer (buttons, arrow keys, swipe). | Change slide behavior or badges |
| `src/templates/_icons.html` | Every drawn icon (robot, alien, astronaut, book, constellation, flag, subject icons) as SVG symbols. | Redraw an icon |
| `src/templates/macros.html` | Reusable pieces: `card`, `icon`, level buttons, difficulty dots, path strip, grown-up notice. | Change what a card shows |
| `src/templates/base.html` | Header (profile, search, constellation, everything, levels, language), moving subject bar, footer. | Header/footer layout |
| `src/templates/home.html` | Headline, today's suggestions, one subject row, "more galaxies" tiles. | Home page |
| `src/templates/constellation.html` | Star map of all subjects. | Star map |
| `src/templates/galaxy.html` | One subject: center star with orbiting systems (Python = sun, Java = star, Web = spiral…). | Orbit drawing |
| `src/templates/system.html` | One track (e.g. Python): path strip + all stops. | Track page |
| `src/templates/entry.html` | Lesson page for any entry: guide slides, timeline, leaving-our-site slide, path, Explore next. | Lesson page |
| `src/templates/lessons.html`, `lesson.html` | Our adapted CS Unplugged lessons + CC BY-SA attribution box. | Lesson list / lesson layout |
| `src/templates/library.html` | "Everything" search page. | Search results |
| `src/templates/me.html` | "My space log": explored stops and badges (saved only in the browser). | Badges |
| `src/templates/guide.html`, `catalogue.html`, `howto.html`, `listing.html` | Team pages, restyled. | |
| `src/templates/accessibility.html`, `feedback.html`, `problems.html`, `problem.html` | Accessibility statement, grown-ups' feedback form, coding problems. | |
| `src/tracks.py` | Groups entries into **galaxies** (subjects) → **systems** (tracks) → **stops** with regex rules; orbit layout; daily suggestions. | Add a subject or track, move an entry |
| `src/ui_strings.py` | Every UI string in en/es/pt/ar/hi. Missing keys fall back to English. | Wording and translations |
| `tests/test_frontend.py`, `tests/test_a11y.py` | Smoke tests for the galaxy pages; accessibility markup and CSS. | |

## Routes added (backend routes unchanged)
`/<lang>/constellation`, `/<lang>/galaxy/<gid>`, `/<lang>/galaxy/<gid>/<sid>`, `/<lang>/library`, `/<lang>/me`,
`/<lang>/lessons`, `/<lang>/lesson/<id>`, `POST /<lang>/prefs` (level filter, session only), `/<lang>/stop/<id>` (redirects to `/entry/<id>`).
`/<lang>/entry/<id>` now renders the galaxy lesson page with the guide slides from `guides.json` (GUIDE_SPEC tasks 1-5).

## Rules kept
- Safety: everything goes through `gate.visible` and the team's session flag (`POST /grownup`). Hidden entries still 404.
- External links only appear on the last guide slide, after the "You are leaving our site" notice.
- Progress is stored only in the browser (localStorage). No accounts, nothing sent to the server.
- All guides, lessons and problems are translated; if a text is ever missing in a language, the whole page is shown in English and marked "Shown in English" (never a mix).
- No inline scripts and no external scripts: the Content-Security-Policy (`src/csp.py`) only allows our own files. Colours are tokens in `:root` (`galaxy.css`) that the themes in `a11y.css` override; contrast is checked by `scripts/check_contrast.py`.
- The brand name "Open Cosmos" stays in Latin script in every language; in right-to-left text it is wrapped in `<bdi dir="ltr">` or a bidi isolate.
