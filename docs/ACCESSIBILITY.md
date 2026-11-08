# Accessibility in Open Cosmos

Goal: WCAG 2.2 level AA. No outside audit yet. Everything below runs locally and nothing is sent anywhere.

## Features

| Feature | How it works |
|---|---|
| **Accessibility button** (header, every page) | Opens a settings panel: real `<fieldset>`/radio inputs, 44 px targets, focus moves into the panel and is trapped while it is open (Tab and Shift+Tab cycle), Escape closes it and returns focus to the button, the rest of the page is `inert` while open, changes are announced in a polite live region. |
| **Colours** | Match my device (default), Galaxy, Light, High contrast, Colour-blind friendly (Okabe-Ito accents). "Match my device" uses `prefers-contrast: more`, then `prefers-color-scheme: light`, otherwise Galaxy, and follows changes live. |
| **Text size** | 100%, 125%, 150%: all text is in `rem`, so everything scales. |
| **Line spacing** | "Roomy": WCAG 1.4.12 text spacing (line height 1.9, extra letter/word spacing; never letter spacing on Arabic or Hindi). |
| **Easy-to-read font** | Atkinson Hyperlegible, self-hosted in `src/static/fonts/` (SIL OFL 1.1, licence in `OFL.txt`). The `@font-face` rules only download files when the font is chosen. It covers Latin letters only; Arabic and Hindi keep the device font (said in the panel and on the statement page). |
| **Reduce motion** | Stops the moving stars, spinning maps and transitions. Default follows `prefers-reduced-motion`; choosing "full motion" explicitly overrides the device. |
| **Read aloud (Listen)** | On lessons, guide slides and entry descriptions. Browser `speechSynthesis` only: no network, no cost. Play, pause/resume, stop, speed (slow to faster). Voice language follows the page (`en-US`, `es-ES`, `ar-SA`, `hi-IN`, `pt-BR`). Reads only the main content (navigation, buttons, hidden slides and controls are skipped). Hidden if the browser has no speech synthesis; a translated note appears if the device has no voice for the language. Announced through a polite live region. |
| **Statement page** | `/<lang>/accessibility` in five languages, linked from the footer. |
| **Saved settings** | localStorage key `hc_a11y_v1`, settings only, every access in try/catch (private mode, blocked or corrupt storage fall back to defaults). Applied before first paint by `a11y-settings.js` in `<head>` (external file, no inline scripts, so it works with a strict Content-Security-Policy). |

Right-to-left: the panel, the Listen bar and the statement page work in Arabic; "Open Cosmos" stays in Latin script inside `<bdi dir="ltr">`.

## Tools (all dev-only; nothing here is in requirements.txt)

| Command | What it checks |
|---|---|
| `python scripts/check_contrast.py [--table]` | Contrast of the theme tokens against WCAG AA (needs only Python). Part of the Python tests. |
| `scripts/a11y_audit.py BASE_URL` | axe-core 4.14 over the key pages, in every theme, at desktop (1280) and phone (390) width. |
| `scripts/a11y_keyboard.py BASE_URL` | Keyboard-only walk through the demo paths and the settings panel. |
| `scripts/a11y_listen.py BASE_URL` | Read-aloud with a fake speech engine (voice language, content, pause/stop/speed, no-voice note). |
| `scripts/a11y_reflow.py BASE_URL` | No sideways scrolling at 320 px and 640 px wide, also with the largest text settings. |

One-time setup for the Playwright tools:

```
python3 -m venv /tmp/a11yenv && /tmp/a11yenv/bin/pip install playwright     # uses your installed Google Chrome
mkdir -p .cache && curl -sL https://registry.npmjs.org/axe-core/-/axe-core-4.14.0.tgz | tar -xz -O package/axe.min.js > .cache/axe.min.js
.venv/bin/flask --app src/app run -p 5000 &
/tmp/a11yenv/bin/python scripts/a11y_audit.py http://127.0.0.1:5000 --langs en,ar,hi,es,pt
```

The Node tests (`node --test tests/js/*.test.js`) cover the settings module (defaults, corrupt storage, unavailable storage, theme resolution). `tests/test_a11y.py` runs them when `node` is installed and skips otherwise.

## Audit results (Nov 8, 2026)

| Check | Result |
|---|---|
| axe-core 4.14 (WCAG 2.0/2.1/2.2 A and AA, plus best-practice rules) | **1,115 page states, 0 violations.** 5 languages (en, es, ar, hi, pt) x 6 settings (Galaxy, Galaxy without the star background, Light, High contrast, Colour-blind, and largest text + roomy spacing + easy font) x 2 widths (desktop 1280, phone 390) x the pages below, plus the settings panel open, plus the grown-up feedback page and a grown-up entry |
| Pages audited | Home, Learn, Kids, Guide, Lessons, a lesson, two entries (with guide slides), Problems, a problem, My space log, Library, Constellation, a galaxy map, Catalogue, Accessibility statement |
| Colour contrast of theme tokens | **132 pairs x 4 themes, 0 below AA** (`scripts/check_contrast.py`) |
| Keyboard-only walk-through (`a11y_keyboard.py`) | **36 checks, 0 failed**: skip link, the three demo paths of `docs/DEMO_SLICE.md` (child lesson, teen link-only, Arabic example), 18 to 29 Tab stops per page with no trap and a visible focus on every stop, panel open/trap/Escape/return focus, keyboard theme and size changes, settings survive a reload |
| Read-aloud (`a11y_listen.py`, fake speech engine) | **70 checks, 0 failed**: hidden without speech support, right voice per language, only main content, pause/resume/stop/speed, live-region messages, no-voice note |
| Reflow (`a11y_reflow.py`) | **300 page states at 320 and 640 px, 0 with sideways scrolling**, with default and largest text settings, in en, es, ar, hi, pt |
| Python tests | 225 tests pass (`tests/test_a11y.py`: markup hooks, statement page and strings in all five languages, theme and font CSS, contrast script) |
| Node tests | 11 tests pass (`tests/js/a11y-settings.test.js`: defaults, corrupt storage, unavailable storage, throwing storage getter, theme and motion resolution) |

### What the audit found and we fixed

Existing problems that axe reported on first run, all fixed:

- **Phone header:** the round header buttons (profile, constellation, levels) had no accessible name on phones because their captions were `display: none`. They are now visually hidden but still the name.
- **Language button:** its `aria-label` did not contain its visible text; now it has no override and an extra hidden "(English)".
- **Hard-coded English labels:** "Main" and "Breadcrumb" were English on every page; now translated.
- **Landmarks:** two search forms and two navs had the same name; now unique.
- **Headings:** lesson and problem lists jumped from h1 to h3; a hidden h2 was added.
- **Roles:** the guide carousel had `aria-roledescription` without a role; the stop flow used `role="listitem"` on links.
- **Colour:** the light theme's notice box and big titles with a decorative outline (axe read the outline as the text colour); galaxy muted text was 4.45:1 and is now above 4.5:1; control borders were 2:1 and now use a stronger `--ui-border` token.
- **Map links:** the planet links had a tooltip `<title>` plus an `aria-label`; the tooltip was removed so the accessible name matches the visible number. (Mouse users lose the hover tooltip on those dots; screen reader names are unchanged.)
- **Reflow:** at 320 px the header and some buttons forced sideways scrolling; fixed.

### False positives and things axe cannot decide

- **Text over the star background (Galaxy):** axe cannot compute contrast over gradients, so it reports them as "needs review" (about 30,000 elements across all runs). The same pages are re-run as `galaxy-flat` (stars removed, same colours) with zero violations, and `check_contrast.py` checks every token pair. Stars are decorative dots.
- **Large titles:** `.bubble` titles have a decorative outline; the audit checks the fill colour (outline removed) because axe reads the outline colour as the text colour.
- **`aria-valid-attr-value` / `aria-prohibited-attr` "needs review":** none left after removing `aria-controls` from the Accessibility button and giving the guide carousel a role.

## Contrast table (token pairs, from `check_contrast.py`)

| Pair (text on background) | Needs | galaxy | light | high contrast | colour-blind |
|---|---|---|---|---|---|
| Body text on the page | 4.5:1 | 13.2:1 | 14.9:1 | 21.0:1 | 13.2:1 |
| Text on cards | 4.5:1 | 11.5:1 | 16.0:1 | 21.0:1 | 11.5:1 |
| Muted text on the page | 4.5:1 | 5.6:1 | 7.1:1 | 17.1:1 | 5.6:1 |
| Links on the page | 4.5:1 | 12.1:1 | 7.0:1 | 19.6:1 | 13.2:1 |
| Links on cards | 4.5:1 | 10.5:1 | 7.5:1 | 19.6:1 | 11.4:1 |
| Lilac text on cards | 4.5:1 | 8.4:1 | 11.0:1 | 14.3:1 | 10.0:1 |
| Text on violet buttons | 4.5:1 | 7.1:1 | 9.0:1 | 9.9:1 | 5.2:1 |
| Control borders (UI part) | 3.0:1 | 6.3:1 | 4.1:1 | 21.0:1 | 6.3:1 |
| Text on the gold button (lowest of its gradient) | 4.5:1 | 9.8:1 | 10.0:1 | 14.7:1 | 7.7:1 |

All 132 token pairs pass in all four themes (the script also covers tinted chips, flags, tooltips, code boxes, focus outlines and every stop of the gold button gradient).

## Manual checklist for you (VoiceOver on a Mac, and 200% zoom)

Do these on desktop Safari (best VoiceOver support) and, if you can, on Chrome. Start VoiceOver with **Cmd+F5**; stop it the same way. VO = Control+Option.

**Basics**
- [ ] Home page: VO reads the page title "Open Cosmos ...". The first stop is "Skip to content". Open the rotor (VO+U): Landmarks lists banner, navigation, search, main, footer, each with a distinct name; Headings are in order (one level 1).
- [ ] The header buttons read as buttons with names ("My space log", "Constellation", "Everything", the three level buttons with "pressed" state, "Accessibility", "Language EN (English)").

**Accessibility panel**
- [ ] Activate "Accessibility": VO says it opens a dialog; focus is in the panel; VO+Right reads the controls in order; nothing behind the panel can be reached. Escape closes it and VO is back on the button.
- [ ] Choose "High contrast", then "150%": VO says "Settings updated"; the page changes at once; reload keeps the settings.
- [ ] Switch to Arabic (`/ar/`): the panel and the Listen bar are right-to-left, and "Open Cosmos" is read as English.

**Lesson, guide, entry**
- [ ] Open `/en/lesson/lesson-0d3a63dc`: headings are logical (h1, h2 steps, h2 talk about). Lists are announced as lists (steps are numbered).
- [ ] Press **Listen**. Safari reads aloud with its own voices; Pause says "Paused", Stop says "Stopped", speed changes the pace. VO does not talk over it badly (if it does, that is expected: use either VO or Listen, not both).
- [ ] Open `/en/entry/kids-0d3a63dc` and go through the guide slides: the slide changes are announced ("slide 2 of 6"), "Next" and "Previous" are buttons, the carousel is named.
- [ ] Open a coding problem `/en/problem/py-hello`: the code box is labelled; Run and Check results are announced; hints appear and are announced.
- [ ] Forms: the header search and the filters on `/en/learn` have labels (VO says "Search ... search field").

**Zoom and text size (Chrome or Safari)**
- [ ] Press Cmd and + until the browser zoom shows **200%**, then **400%** (that equals 320 CSS px wide). No page needs sideways scrolling, no text is cut off, the header wraps, and the Accessibility panel scrolls inside itself.
- [ ] At 200% choose Text size 150% and "Roomy": still readable and usable.
- [ ] Turn on the easy-to-read font: Latin text changes; Arabic or Hindi text keeps the device font.

**Colour**
- [ ] Try each colour mode on Home, a lesson and a problem page: all text is readable, links are recognisable (in High contrast they are underlined), the focus outline is visible on every control.
- [ ] macOS Settings > Accessibility > Display: turn on "Increase contrast" and "Reduce motion", reload with "Match my device": the site follows (High contrast, no moving stars).

**Report back** anything that reads wrongly (a name that is missing or in the wrong language, a control you cannot reach, a slide change that is silent).

## Known limits

- Read-aloud voices depend on the device: some have no Arabic or Hindi voice (the page says so).
- The translations (es, ar, hi, pt) are AI-written and not checked by native speakers.
- The easy-to-read font does not cover Arabic or Devanagari.
- We have not had an outside accessibility audit or tested with JAWS, NVDA or TalkBack ourselves.
- When this branch is merged with the Vercel branch: static files move to `public/static/`, and the Content-Security-Policy there needs `font-src 'self' https://fonts.gstatic.com` (the self-hosted font) in `src/csp.py` and `vercel.json`.
