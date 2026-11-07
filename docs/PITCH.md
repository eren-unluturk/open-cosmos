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
*With us:* they open the site, pick **Beginner**, and see a short, ordered path. Each entry has a plain-language description, and they can move up to Intermediate and Advanced when ready.

**An international student.** They're new to the country and still learning English. The coding resources their class recommends are all in English, and the technical vocabulary on top of that is too much.
*With us:* they switch the site to their language and find titles and descriptions they can understand. Code and key technical terms stay in English, so what they learn still matches their course and the documentation they'll meet later.

## 4. Solution / Demo (walk through live)
1. Start at **"What should I learn?"**: pick an age, a goal (games, art, web), and a level, and get an ordered 6-step path.
2. Open the site in English, then switch to Spanish, then Arabic (watch it flip right-to-left).
3. **Learn** side: curated lists from `sindresorhus/awesome`. **Build** side: "build your own X" projects from `codecrafters-io/build-your-own-x`.
4. Filter by **Beginner / Intermediate / Advanced**.
5. Click through to the original resource, with source repo and license shown on every entry.

## 5. How it works (tech)
Python + Flask. Kids answer only multiple-choice questions, so we collect no personal data; the AI picks a path from our open data and can only choose real entries. A pipeline fetches the two open (CC0) source lists. Claude translates each entry into Spanish, Arabic, Hindi, and Portuguese, keeping code and technical terms, and assigns a level. Translations are generated ahead of time and stored as JSON, so the site is fast and the API key is never exposed.

## 6. Honesty & open data (say this out loud)
- We use **only open data** (CC0). We claim none of the content.
- We add two things: **translation** and a **level-based path**.
- Every entry credits and links to its source and license. Translations are AI-generated and labeled as such.

## 7. Impact / Next steps
- More languages, with community corrections from native speakers.
- More source repos (each license-checked).
- Offline/low-bandwidth mode for places with poor connectivity.
- Learner progress tracking and guided "next step" suggestions.

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
