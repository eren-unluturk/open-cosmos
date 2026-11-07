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
- We only store a title, a short description we wrote ourselves, the age group the repo states, and a link to the original lesson page on csunplugged.org. We do NOT copy lesson text or images.
- **ShareAlike:** any translation or adaptation of CC BY-SA material (including our translated titles/descriptions in `kids.json`) must also be shared under CC BY-SA 4.0, with attribution to the original authors (University of Canterbury CSER Group, CS Unplugged), a link to the license (https://creativecommons.org/licenses/by-sa/4.0/), and a statement that changes were made (translated and level-tagged by Hackcessability, AI-generated).
- **What we list from it:** units, lessons, the lessons' programming-challenge pages (only those that really have challenges) and the cross-curricular "integration" activities that have a repo-stated age (inherited from the lessons they require). Each is a title, a short description we wrote, the repo's age group and a link to the page on csunplugged.org.
- The CS Unplugged project also publishes its own human translations (the repo has `es`, `fr`, `de`, `it`, `zh_Hans`, `mi` content folders). Prefer linking to those language versions where they exist.
- Note: these are teacher/parent lesson plans for hands-on activities, so the audience is the adult helping the child.

## Adapted lessons (`src/data/lessons.json`, CC BY-SA 4.0)
- `lessons.json` holds our own short, simplified adaptations of CS Unplugged lesson plans (26 lessons, ages 5-13). It is **kept in its own file** and is **CC BY-SA 4.0 (ShareAlike)**, like `kids.json`. The CC0 files never contain adapted text.
- We rewrote the ideas in our own short words (no long verbatim passages) and include **no images**; every lesson links to the original lesson page for the pictures and printables.
- Every lesson carries: the license (`CC-BY-SA-4.0`), the attribution (University of Canterbury Computer Science Education Research Group, CS Unplugged), a link to the original lesson, a link to https://creativecommons.org/licenses/by-sa/4.0/ and a "changes were made" statement ("Simplified, shortened and translated by Hackcessability with AI"). The UI must show these on every lesson page.
- Translations of lessons are also CC BY-SA 4.0 and must keep the same attribution and the changes statement.
- Built by `scripts/fetch_lessons.py` from `scripts/lesson_content/` (text written by Claude Code, no paid API). Only `kid-safe`, `open-content` entries get a lesson.
