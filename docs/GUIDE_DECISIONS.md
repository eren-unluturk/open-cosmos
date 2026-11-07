# Guide and lesson decisions (made automatically; nobody was asked)
- `docs/PITCH_DATA.md` did not exist, so the demo-path groups are the ones with the most kid-safe entries and the best level coverage (CS Unplugged units first, then Gaming, Platforms, Learn, Front-End Development).
- Guides are keyed by group `<side>:<category>`. Each CS Unplugged unit is its own category, so it is its own group.
- Every text field is a `{"en": ...}` dict so translations can be added later; slide text never contains URLs.
- The final slide is always `go_external` in `slides`; kids groups also carry `go_lesson_slide`, which `guide_helpers.guide_for` swaps in only when the entry has a lesson.
- CS Unplugged units, programming-challenge pages and classroom integration activities do not get their own lesson (only the 26 lessons do); they keep the external slide, which links to the original CS Unplugged page.
- Lessons were rewritten from the CS Unplugged plans in simple English, no pictures, no long passages. The original page is linked for printables and images.
- Time estimates are labeled `estimate` everywhere. Guides never describe what is on a linked page; they describe the group, the level and the age only.
- For the 11-13 and teen+ groups the tone is slightly more independent, but the grown-up note stays for anything that needs an account or hardware.
- Ask-a-grown-up groups get a guide whose adult note says a grown-up should check the site first.
