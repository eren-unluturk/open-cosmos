# Translation queue (kid-safe entries not yet translated into es/ar/hi/pt)

Regenerate with `python scripts/translate_queue.py`. **0 entries** still need es, ar, hi and pt for `title` and `desc`. Priority: CS Unplugged first, then Beginner, then Intermediate, then Advanced.

## Counts

| Source | Beginner | Intermediate | Advanced | Total |
|---|---|---|---|---|
| awesome | 0 | 0 | 0 | 0 |
| build-your-own-x | 0 | 0 | 0 | 0 |
| CS Unplugged | 0 | 0 | 0 | 0 |
| **All** | 0 | 0 | 0 | 0 |

## How to work through it
- **By hand (no API key):** add a module in `scripts/translation_content/` with `build()` returning `{entry id: {"title": {lang: ...}, "desc": {lang: ...}}}` for es, ar, hi, pt (see `kids_activities.py`), then run `python scripts/apply_translations.py` and the tests. Keep code and technical terms in English. They are labeled `ai_translated`.
- **With an API key:** `python scripts/translate.py --limit N` (kid-safe only, priority order, 5 requests at a time; add `--all` for everything).
- Still needs native-speaker checks for all four languages.

## Queue

| # | id | source | level | age | topic | title (en) |
|---|---|---|---|---|---|---|
