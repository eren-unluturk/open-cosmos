"""Build src/data/guides.json: one fallback guide per topic + handwritten group guides.

Handwritten guides live in scripts/guide_content/*.py as GUIDES = {group_key: {...}} (written by
Claude Code from catalog data only; no API). This script turns them into the slide format and
adds the standard final slide (go_external / go_lesson). Deterministic; safe to re-run.

Usage: python scripts/build_guides.py
"""
import importlib
import json
import pkgutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import guide_helpers as gh  # noqa: E402

OUT = ROOT / "src" / "data" / "guides.json"
NOTE = ("AI-written (Claude Code) from catalog data only (titles, descriptions, categories, levels, topics). "
        "We have not read the linked pages. Time estimates are estimates.")


def T(s):
    return {"en": s}


def slide(kind, title, body=None, **kw):
    s = {"type": kind, "title": T(title)}
    if body:
        s["body"] = T(body)
    if "steps" in kw:
        s["steps"] = [T(x) for x in kw.pop("steps")]
    if "timeline" in kw:
        s["timeline"] = [{"when": T(w), "minutes": m, "goal": T(g)} for w, m, g in kw.pop("timeline")]
    if kw.get("adult_note"):
        s["adult_note"] = T(kw.pop("adult_note"))
    if kw.pop("estimate", False):
        s["estimate"] = True
    s.update(kw)
    return s


def external_slide():
    return slide("go_external", "Go to the learning site",
                 "You are about to leave our site to visit {entry_title} on another website. " + gh.LEAVING + " " + gh.LANGUAGE_TIP,
                 adult_note="Grown-ups: this link goes to a site we do not control and have not reviewed beyond its listing. Please look at it first.",
                 leaving_site=True)


def lesson_slide():
    return slide("go_lesson", "Start the lesson",
                 "Open our lesson page for {entry_title}. It is a short, simple version of an open lesson you can do together.",
                 adult_note=("Adapted from CS Unplugged by the University of Canterbury Computer Science Education Research Group, "
                             "licensed CC BY-SA 4.0. Changes were made: simplified, shortened and translated by Open Cosmos with AI."),
                 attribution=True)


def make_guide(gid, title, what, for_me, steps, time, timeline, adult=None, kind="group", lesson=False):
    assert len(steps) == 3 and 3 <= len(timeline) <= 5, gid
    slides = [
        slide("what_is_it", "What is it?", what),
        slide("is_it_for_me", "Is it for me?", for_me, adult_note=adult),
        slide("how_to_start", "How to start", steps=steps),
        slide("time", "How much time?", time + " (estimate)", estimate=True),
        slide("timeline", "A plan you can follow", timeline=timeline, estimate=True),
        external_slide(),
    ]
    g = {"id": gid, "kind": kind, "title": T(title), "slides": slides, "_note": NOTE}
    if lesson:
        g["go_lesson_slide"] = lesson_slide()
    return g


# ---- topic fallbacks: usable by ANY entry of that topic (placeholders are filled per entry)
TL = [("Day 1", "{minutes}", "Look around and pick one thing to try."),
      ("Week 1", "{minutes}", "Try it again and write down one thing you learned."),
      ("Week 2", "{minutes}", "Make something small of your own with a grown-up or friend.")]
FALLBACKS = {
    "games": ("Games", "{entry_title} is about learning programming through games or game ideas.",
              "It is for anyone who likes games and wants to see how they are made. We marked it {level}, for about age {age}."),
    "art": ("Art and creative coding", "{entry_title} is about making art, drawings, music or pictures with code.",
            "It is for anyone who likes to draw, design or make things look cool. We marked it {level}, for about age {age}."),
    "web": ("Websites", "{entry_title} is about building websites and web pages.",
            "It is for anyone who wants to make a page that shows up in a browser. We marked it {level}, for about age {age}."),
    "general": ("Learning to code", "{entry_title} is about learning how to program or how computers think.",
                "It is for anyone starting out or looking for the next step. We marked it {level}, for about age {age}."),
    "systems": ("How computers work", "{entry_title} is about how computers and programs work inside.",
                "It is for people who like to look under the hood. We marked it {level}, for about age {age}; these topics are often harder."),
    "security": ("Computer safety topics", "{entry_title} is about computer security.",
                 "Security topics are for grown-ups or older learners with a grown-up nearby. We marked it {level}, for about age {age}."),
    "other": ("More to explore", "{entry_title} is a computing resource that does not fit our main topics.",
              "It might still be useful. We marked it {level}, for about age {age}; ask a grown-up if you are not sure."),
}


def fallback_guides():
    out = {}
    for topic, (title, what, for_me) in FALLBACKS.items():
        out[topic] = make_guide(
            f"fallback-{topic}", title, what, for_me,
            ["Open the link with a grown-up if you are under 13.",
             "Look for a part that matches what you already know. Skip the hard parts for now.",
             "Try one small thing, then stop and tell someone what you tried."],
            "Plan for about {minutes} minutes at a time, over about {sessions} sessions.",
            TL, adult="Grown-ups: please look at the page before your child does and sit nearby for the first session.",
            kind="fallback")
    return out


def load_content():
    groups = {}
    pkg = ROOT / "scripts" / "guide_content"
    sys.path.insert(0, str(ROOT / "scripts"))
    for m in sorted(pkgutil.iter_modules([str(pkg)]), key=lambda m: m.name):
        if m.name.startswith("_"):
            continue
        mod = importlib.import_module(f"guide_content.{m.name}")
        for key, g in mod.GUIDES.items():
            assert key not in groups, f"duplicate guide {key}"
            groups[key] = make_guide("group-" + key.replace(" ", "-").lower(), g["title"], g["what"], g["for_me"],
                                     g["steps"], g["time"], g["timeline"], adult=g.get("adult"),
                                     lesson=key.startswith("kids:"))
    return groups


def main():
    (ROOT / "scripts" / "guide_content" / "__init__.py").touch()
    data = {"version": 1, "_note": NOTE, "fallback": fallback_guides(), "groups": load_content()}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"guides.json: {len(data['fallback'])} fallback, {len(data['groups'])} handwritten group guides")


if __name__ == "__main__":
    main()
