"""Guide tests. Handwritten coverage is REPORTED (it grows over time), never a failure."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
sys.path.insert(0, str(ROOT / "scripts"))
import guide_helpers as gh  # noqa: E402

GUIDES = json.loads((DATA / "guides.json").read_text(encoding="utf-8"))
LESSONS = json.loads((DATA / "lessons.json").read_text(encoding="utf-8"))
ENTRIES = [e for n in ("learn", "build", "kids") for e in json.loads((DATA / f"{n}.json").read_text(encoding="utf-8"))]
VISIBLE = [e for e in ENTRIES if e["safety"] != "adult-only"]
REQUIRED = ["what_is_it", "is_it_for_me", "how_to_start", "time", "timeline"]
ALL_GUIDES = list(GUIDES["fallback"].values()) + list(GUIDES["groups"].values())


def texts(slide):
    for k in ("title", "body", "adult_note"):
        if k in slide:
            yield slide[k]["en"]
    for s in slide.get("steps", []):
        yield s["en"]
    for t in slide.get("timeline", []):
        yield t["when"]["en"]
        yield t["goal"]["en"]


class Guides(unittest.TestCase):
    def test_every_visible_entry_resolves(self):
        for e in VISIBLE:
            r = gh.guide_for(e, GUIDES, LESSONS)
            self.assertTrue(r["slides"], e["id"])

    def test_fallback_for_every_topic(self):
        self.assertEqual(set(GUIDES["fallback"]), set(gh.TOPICS))

    def test_required_slides_with_english_text(self):
        for g in ALL_GUIDES:
            kinds = [s["type"] for s in g["slides"]]
            self.assertEqual(kinds[:5], REQUIRED, g["id"])
            self.assertIn(kinds[-1], ("go_external",), g["id"])
            self.assertEqual(len(g["slides"][2]["steps"]), 3, g["id"])
            self.assertTrue(3 <= len(g["slides"][4]["timeline"]) <= 5, g["id"])
            for s in g["slides"]:
                for t in texts(s):
                    self.assertTrue(t.strip(), (g["id"], s["type"]))
            self.assertIn("AI-written", g["_note"])

    def test_placeholders_allowed(self):
        for g in ALL_GUIDES + [x for x in ALL_GUIDES if x.get("go_lesson_slide")]:
            slides = g["slides"] + ([g["go_lesson_slide"]] if g.get("go_lesson_slide") else [])
            for s in slides:
                for t in texts(s):
                    for ph in re.findall(r"\{(\w+)\}", t):
                        self.assertIn(ph, gh.PLACEHOLDERS, (g["id"], ph))
                for t in s.get("timeline", []):
                    if isinstance(t["minutes"], str):
                        self.assertEqual(t["minutes"], "{minutes}")

    def test_no_urls_in_slide_text(self):
        for g in ALL_GUIDES:
            for s in g["slides"] + ([g["go_lesson_slide"]] if g.get("go_lesson_slide") else []):
                for t in texts(s):
                    self.assertNotRegex(t, r"https?://|www\.|\.com\b|\.org\b", (g["id"], t))

    def test_external_slide_wording(self):
        for g in ALL_GUIDES:
            last = g["slides"][-1]
            body = last["body"]["en"]
            self.assertIn("We don't control that site", body)
            self.assertIn("Ask a grown-up before you go", body)
            self.assertIn("Check the original for details", body)
            self.assertTrue(last.get("leaving_site"))

    def test_go_lesson_only_with_a_lesson(self):
        for e in VISIBLE:
            r = gh.guide_for(e, GUIDES, LESSONS)
            if r["slides"][-1]["type"] == "go_lesson":
                self.assertIsNotNone(gh.lesson_for(e, LESSONS), e["id"])
                self.assertEqual(e["reuse"], "open-content")
        for g in ALL_GUIDES:
            if g.get("go_lesson_slide"):
                a = g["go_lesson_slide"]["adult_note"]["en"]
                self.assertIn("CC BY-SA 4.0", a)
                self.assertIn("Changes were made", a)

    def test_related_entries_are_safe_and_live(self):
        removed = set(json.loads((ROOT / "scripts/cache/removed_links.json").read_text()))
        for e in VISIBLE[::7]:
            for r in gh.related_entries(e, ENTRIES, 4):
                self.assertEqual(r["safety"], "kid-safe")
                self.assertNotIn(r["url"], removed)
                self.assertNotEqual(r["id"], e["id"])
                self.assertLessEqual(gh.AGES.index(r["age_group"]), gh.AGES.index(e["age_group"]))

    def test_related_excludes_removed_and_too_old(self):
        kid = next(e for e in ENTRIES if e["safety"] == "kid-safe" and e["age_group"] == "8-10" and e["id"].startswith("kids-"))
        rel = gh.related_entries(kid, ENTRIES, 50)
        self.assertTrue(all(r["age_group"] in ("5-7", "8-10") for r in rel))
        rel2 = gh.related_entries(kid, ENTRIES, 50, removed={r["url"] for r in rel})
        self.assertEqual(rel2, [])

    def test_timeline_rules(self):
        e = ENTRIES[0]
        t = gh.build_timeline(e, "5-7")
        self.assertLess(t["minutes"], gh.build_timeline(e, "teen+")["minutes"])
        self.assertEqual(t["label"], "estimate")

    def test_report_handwritten_coverage(self):
        groups = {gh.group_of(e) for e in VISIBLE}
        done = groups & set(GUIDES["groups"])
        covered = sum(1 for e in VISIBLE if gh.group_of(e) in GUIDES["groups"])
        print(f"\n[guides] handwritten groups {len(done)}/{len(groups)}; entries covered {covered}/{len(VISIBLE)} "
              f"({covered / len(VISIBLE):.0%}); the rest use topic fallbacks")


if __name__ == "__main__":
    unittest.main()
