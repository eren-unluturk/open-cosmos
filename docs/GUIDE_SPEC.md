# Guides and lessons: spec for Tobi (backend) and Isabella (frontend)

Everything below is already in the repo as data and pure Python. You only wire it into `src/`. No API, no runtime AI.

## Two paths
- **A. Link-only** (every `reuse == "link-only"` entry: all of awesome and build-your-own-x). We have no right to reuse the content. The child sees a short **guide** (slides) with an overview and a recommended timeline. The last slide is "Go to the learning site" with a leaving-our-site notice and a grown-up note.
- **B. Open-content** (`reuse == "open-content"`: CS Unplugged, CC BY-SA 4.0). We adapted some of it into our own **lessons** (`src/data/lessons.json`), shown under a "Lessons" category. The guide's last slide sends the child to OUR lesson page (`go_lesson`).
- **Every visible entry** (kid-safe, and ask-a-grown-up after the gate; never adult-only) always resolves to a guide, because there is a fallback guide for every topic.

## Data model
**Entries** (`learn.json`, `build.json`, `kids.json`) have two new fields:
- `reuse`: `"open-content"` | `"link-only"`
- `reuse_license`: only on open-content (`"CC-BY-SA-4.0"`)

**`src/data/guides.json`**
```
{ "version": 1, "_note": "...",
  "fallback": { "<topic>": <guide>, ... },     // games art web general systems security other
  "groups":   { "<side>:<category>": <guide> } // handwritten; overrides the fallback for that group
}
guide = { id, kind, title:{en}, _note, slides:[slide...], go_lesson_slide? }   // go_lesson_slide only on kids groups
slide = { type, title:{en}, body?:{en}, steps?:[{en}], timeline?:[{when:{en}, minutes:int|"{minutes}", goal:{en}}],
          adult_note?:{en}, estimate?:true, leaving_site?:true, attribution?:true }
types in order: what_is_it, is_it_for_me, how_to_start (3 steps), time, timeline (3-5 items), go_external
```
Placeholders allowed in any text: `{age}`, `{level}`, `{minutes}`, `{sessions}`, `{entry_title}`. Fill them with `guide_helpers.fill(text, entry, age)`. Slide text never contains URLs; the link comes from the entry.

**`src/data/lessons.json`**: a list of lessons (CS Unplugged adaptations).
```
{ id, entry_id,                       // entry_id matches a kids.json id
  title:{en}, summary:{en}, objectives:{en:[...]}, materials:{en:[...]}, steps:{en:[...]},
  talk_about:{en:[...]}, grown_up_note:{en}, age_group, duration_minutes,
  license:"CC-BY-SA-4.0", attribution, source_url, license_url, changes_made }
```
Every text field is `{"en": ...}` so translations can be added as extra language keys later.

## Helpers (`scripts/guide_helpers.py`, pure Python; add `scripts/` to `sys.path` or copy the import)
| Function | Use |
|---|---|
| `group_of(entry)` | key into `guides["groups"]` (`"learn:Front-End Development"`) |
| `guide_for(entry, guides, lessons)` | `{"guide", "source": "group"/"fallback", "slides": [...]}`; the last slide is `go_lesson` only if the entry has a lesson |
| `build_timeline(entry, age)` | `{minutes, sessions, total_minutes, label:"estimate"}`, rule-based by level and age, so each child sees a personalised plan |
| `related_entries(entry, entries, n=4, age=None)` | the "Explore next" strip: kid-safe, age-appropriate, live links only |
| `lesson_for(entry, lessons)` | our lesson for an open-content entry, else `None` |
| `fill(text, entry, age, lang)` | replace placeholders |

## Tobi: tasks
1. `store.py`: load `guides.json` and `lessons.json` (UTF-8, once at startup). Index lessons by `entry_id`. They have no `side`; keep entries' `side` as is.
2. Entry page `/<lang>/entry/<id>`: call `guide_for`, fill placeholders with `fill`, compute `build_timeline` (use the age the child picked, else the entry's) and `related_entries` (only kid-safe, even after the grown-up gate). Pass the slides to the template. Fall back to English text when a language key is missing.
3. Routes `/<lang>/lessons` (list, filter by age) and `/<lang>/lesson/<lesson_id>`.
4. `go_lesson` links to OUR lesson page. `go_external` links to `entry["url"]` with `rel="noopener noreferrer"` (and `target="_blank"` if you like) and shows the leaving-our-site notice before the click. The guide is only shown for visible entries (use `gate.visible`).
5. If `reuse == "link-only"` never show lesson content. Do not add other ways to show linked-page text.

## Isabella: tasks
1. **Slide viewer**: one slide at a time, previous/next buttons, keyboard arrows, swipe on touch, `aria-live` for slide changes, focus management, progress ("2 of 6"). **No-JavaScript fallback**: render all slides stacked in order. Right-to-left layouts for Arabic.
2. **Timeline slide** as a visual strip (Day 1 -> Week 1 -> Week 2) with the minutes; label it "estimate".
3. **go_external slide**: clear "You are leaving our site" notice, the adult note, and a big button. `go_lesson` slide: button to our lesson page plus the attribution text.
4. **Lesson page layout**: title, age, time, materials, numbered steps, "talk about it", the grown-up note, and a **CC BY-SA 4.0 attribution box on every lesson**: show `attribution`, a link to `source_url` ("Original lesson, with pictures"), a link to `license_url`, and the `changes_made` text ("Simplified, shortened and translated by Open Cosmos with AI"). The adapted lesson is itself CC BY-SA 4.0 (ShareAlike).
5. Show "AI-written overview" on guides and an "estimate" tag on all times.

## Translation (done)
Translate only `title`, `body`, `steps`, `when`, `goal`, `adult_note` (guides) and `title`, `summary`, `objectives`, `materials`, `steps`, `talk_about`, `grown_up_note` (lessons), adding `es/ar/hi/pt` keys next to `en`. **Keep the `{placeholders}` exactly as they are.** Lesson translations must keep the CC BY-SA 4.0 attribution. Never translate ids, `type`, URLs or numbers.

## Rebuild (Eren)
`python scripts/mark_reuse.py` -> `python scripts/build_guides.py` -> (lessons) `python scripts/fetch_lessons.py` -> tests. Handwritten guides live in `scripts/guide_content/` and lessons are rebuilt from CS Unplugged; progress is in `docs/GUIDE_PROGRESS.md`.

## Update: guides are translated (Nov 7)
`src/data/guides_translated.json` maps each English guide text to `{es, ar, hi, pt}`. `store.py` merges it at load (`_add_guide_translations`), all or nothing per guide and language, so the existing `tx()`/`localize_slides()` code shows the translation with no change. The English-only notice appears only if a guide has an untranslated text. The last slide also tells the learner that the site may not be in their language and that the browser can translate the page. When `guides.json` changes (new or edited text), new English strings need translations in the overlay; `tests/test_guide_translations.py` fails on stale keys and incomplete entries.
