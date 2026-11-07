# Guide and lesson progress (resume file)

Branch: `guides-lessons`. Fully automatic run; the next session resumes from "NEXT" below.
Auto choices are logged under "Decisions".

## Status
- Phase A (foundation): DONE (reuse flag, fallback guides, helpers, tests, spec).
- Phase B (lessons): DONE: 26 lessons (13 at 5-7, 12 at 8-10, 1 at 11-13) in `src/data/lessons.json`. Integration and programming-challenge entries have no lesson (they keep a go_external slide).
- Phase C (handwritten guides): NOT STARTED, 0 of 65 groups
- Phase D (wrap-up): NOT STARTED

## NEXT
Phase C: handwritten guides, batch 1 (see list below).

## Decisions
- `docs/PITCH_DATA.md` did not exist, so demo-path groups are those with the most kid-safe entries and the best level coverage.
- Guides are keyed by group `<side>:<category>`; each CS Unplugged unit is its own category, so it is its own group.
- Text fields are `{"en": ...}` dicts so translations can be added later.
