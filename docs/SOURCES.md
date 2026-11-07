# Sources & Licenses

We use only open-licensed content. Add every source here BEFORE using it.

| Repo / Source | Side | Author | License | Link |
|---------------|------|--------|---------|------|
| awesome | Learning | Sindre Sorhus & contributors | CC0 1.0 (GitHub license metadata) | https://github.com/sindresorhus/awesome |
| build-your-own-x | Building | CodeCrafters & contributors | CC0 1.0 (stated in README "Origins & License"; no LICENSE file) | https://github.com/codecrafters-io/build-your-own-x |
| CS Unplugged | Learning (kids) | University of Canterbury Computer Science Education Research Group (CSER), as named in the repo's LICENCE | **Content: CC BY-SA 4.0** (`LICENCE-CONTENT`: markdown in `csunplugged/topics/content/` and images in `csunplugged/static/img/`). **Code: MIT** (`LICENCE`). Verified from the repo on the `develop` branch. | https://github.com/uccser/cs-unplugged |

## IMPORTANT: what CC0 covers
Both repos are **curated lists of links**. CC0 covers the lists themselves (titles, categories, descriptions), NOT the external articles/tutorials they point to (blogs, Medium, YouTube, etc. have their own copyright).

So we:
- DO translate/organize the list entries (titles, descriptions, categories) and add our level tags.
- DO link out to the original resource, never copy its content.
- DO NOT copy or translate linked articles unless that specific article has an open license (record it here per resource).

## CS Unplugged (CC BY-SA 4.0) — extra rules
- Lives in its own file, `src/data/kids.json`, never mixed into the CC0 files (`learn.json`, `build.json`).
- `kids.json` still holds only a title, a short description we wrote ourselves, the age group the repo states, and a link to the original lesson page.
- **Lesson text (added):** the license lets us host it, so units and lessons also have their markdown in `src/data/lessons.json` (written by `scripts/fetch_lessons.py`, markdown under `csunplugged/topics/content/` only). English always; Spanish only where the CS Unplugged project made its own human translation. AI translations (ar, hi, pt, and es for units without a human one) are in `src/data/lessons_translated.json`. Each lesson page shows the credit line, the license link and "changes were made". **Images are NOT copied yet** (an alt-text description stands in); video links stay external. Programming-challenge and classroom-activity pages are still link-only.
- **ShareAlike:** any translation or adaptation of CC BY-SA material (including our translated titles/descriptions in `kids.json`) must also be shared under CC BY-SA 4.0, with attribution to the original authors (University of Canterbury CSER Group, CS Unplugged), a link to the license (https://creativecommons.org/licenses/by-sa/4.0/), and a statement that changes were made (translated and level-tagged by Hackcessability, AI-generated).
- **What we list from it:** units, lessons, the lessons' programming-challenge pages (only those that really have challenges) and the cross-curricular "integration" activities that have a repo-stated age (inherited from the lessons they require). Each is a title, a short description we wrote, the repo's age group and a link to the page on csunplugged.org.
- The CS Unplugged project also publishes its own human translations (the repo has `es`, `fr`, `de`, `it`, `zh_Hans`, `mi` content folders). Prefer linking to those language versions where they exist.
- Note: these are teacher/parent lesson plans for hands-on activities, so the audience is the adult helping the child.
