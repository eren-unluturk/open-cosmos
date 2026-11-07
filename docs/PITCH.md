# Pitch (2-3 min)

**One line:** Free, open-source programming education that's approachable for beginners and available in your language. Nothing here is ours; everything links back to its source and license.

## 1. Hook
"The best programming resources in the world are free, open, and sitting on GitHub. So why can't most people use them?"

## 2. Problem
- GitHub repos are built by developers for developers: huge lists, no clear starting point, no sense of difficulty.
- Almost everything is in English only.
- Result: the people who most need free education often can't get in the door.

## 3. Who we built this for

**A young learner who needs tutoring.** (and the parent or teacher helping them) Most kids' coding tutoring costs money, and they can't afford it. Friends tell them to "just check GitHub," but they open a list with hundreds of links and no idea where to start. Is a resource for beginners or experts? Which comes first? They give up.
*With us:* they open the site, pick **Beginner**, and see a short, ordered path. Each entry opens a friendly **guide with a roadmap** (what it is, is it for me, how to start, how much time, Day 1 / Week 1 / Week 2), and they can move up to Intermediate and Advanced when ready. For kids' lessons (CS Unplugged) they get a simple **lesson page** they can do together with a grown-up.

**An international student.** They're new to the country and still learning English. The coding resources their class recommends are all in English, and the technical vocabulary on top of that is too much.
*With us:* they switch the site to their language and find titles and descriptions they can understand. Code and key technical terms stay in English, so what they learn still matches their course and the documentation they'll meet later.

## 4. Solution / Demo (walk through live)
1. Start at **"What should I learn?"**: pick an age, a goal (games, art, web), and a level, and get an ordered 6-step path.
2. Open a **child lesson** (CS Unplugged, e.g. "How binary digits work", age 5-7): swipe through the guide, then open our adapted lesson page with its CC BY-SA attribution box.
3. Open a **teen resource** (e.g. a 2D breakout game tutorial): read its guide and roadmap, then see the "you are leaving our site" slide before going to the original.
4. Switch to Spanish, then Arabic (watch it flip right-to-left). Titles and descriptions are translated; guides and lessons are English for now.
5. Filter by **Beginner / Intermediate / Advanced**; browse **Learn** (`sindresorhus/awesome`) and **Build** (`codecrafters-io/build-your-own-x`).
6. Open the grown-up gate to show how non-kid-safe entries stay hidden by default.
(Specific entry ids and URLs: `docs/DEMO_SLICE.md`.)

## 5. How it works (tech)
Python + Flask with static JSON. Kids answer only multiple-choice questions, so we collect no personal data; the guide builds a path from our tagged open data with simple rules and can only pick real entries. A pipeline fetches the open sources (two CC0 lists plus CS Unplugged under CC BY-SA 4.0), tags every entry with topic, level, age group and a child-safety tier, and flags whether its content may be reused. AI (Claude Code) was used **ahead of time** to classify entries, translate titles and descriptions into Spanish, Arabic, Hindi and Portuguese (keeping code and technical terms), write 65 group guides with roadmaps, and adapt 26 CS Unplugged lessons. Everything is stored as JSON, so there is no live AI, no API key and no cost, and the site is fast.

## 6. Honesty & open data (say this out loud)
- We use **only open data** (two CC0 lists and CS Unplugged under CC BY-SA 4.0). We claim none of the content.
- We add: **translation**, a **level-, age- and safety-tagged path**, and **guides with roadmaps**. For link-only content we only describe it and link out; we never copy it.
- **CS Unplugged lessons are adapted** (simplified in our own words, no images) under CC BY-SA 4.0, with attribution and a "changes were made" statement.
- Guides are AI-written from catalog data only (we did not read the linked pages), and **time estimates are estimates**. Translations are AI-generated, labeled as such, and not yet checked by native speakers.
- 'Kid-safe' means nothing in the listing looks risky, not that we reviewed the page. A grown-up gate hides everything else by default.

## 7. Impact / Next steps
- More languages, with community corrections from native speakers.
- More source repos (each license-checked), so more content can become adapted lessons instead of link-only.
- Translate the guides and lessons (placeholders are kept intact), with native-speaker review.
- Offline/low-bandwidth mode for places with poor connectivity.
- Learner progress tracking and richer "next step" suggestions (today: computed "Explore next").

## Submission checklist
- [ ] Repo access set up for judges (repo is currently private; make public or share if required)
- [ ] README complete
- [ ] Demo video
- [ ] Deployed link works
- [ ] Devpost/submission form filled
- [ ] Slides

## Event notes
- Submit to **Information Access** by Sun 9:00 AM; judging starts 9:30 AM.
- Emphasize accessibility impact: who is left out today, and how this fixes it.
