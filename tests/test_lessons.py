"""Lesson tests (src/data/lessons.json: CS Unplugged adaptations, CC BY-SA 4.0)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
sys.path.insert(0, str(ROOT / "scripts"))
import guide_helpers as gh  # noqa: E402

LESSONS = json.loads((DATA / "lessons.json").read_text(encoding="utf-8"))
ENTRIES = {e["id"]: e for n in ("learn", "build", "kids") for e in json.loads((DATA / f"{n}.json").read_text(encoding="utf-8"))}
REQ = ["id", "entry_id", "title", "age_group", "duration_minutes", "summary", "objectives", "materials",
       "steps", "talk_about", "grown_up_note", "license", "attribution", "source_url", "license_url", "changes_made"]


class Lessons(unittest.TestCase):
    def test_required_fields_and_attribution(self):
        for ls in LESSONS:
            for k in REQ:
                self.assertIn(k, ls, (ls.get("id"), k))
            self.assertEqual(ls["license"], "CC-BY-SA-4.0")
            self.assertIn("CS Unplugged", ls["attribution"])
            self.assertIn("University of Canterbury", ls["attribution"])
            self.assertEqual(ls["license_url"], "https://creativecommons.org/licenses/by-sa/4.0/")
            self.assertIn("Hackcessability", ls["changes_made"])
            self.assertTrue(ls["source_url"].startswith("https://www.csunplugged.org/"))

    def test_lessons_match_open_content_safe_entries(self):
        ids = [ls["id"] for ls in LESSONS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len({ls["entry_id"] for ls in LESSONS}), len(LESSONS))
        for ls in LESSONS:
            e = ENTRIES[ls["entry_id"]]
            self.assertEqual(e["reuse"], "open-content")
            self.assertEqual(e["safety"], "kid-safe")
            self.assertEqual(e["age_group"], ls["age_group"])
            self.assertEqual(e["url"], ls["source_url"])

    def test_content_shape(self):
        for ls in LESSONS:
            self.assertTrue(ls["title"]["en"])
            self.assertGreaterEqual(len(ls["steps"]["en"]), 2, ls["id"])
            self.assertGreaterEqual(len(ls["objectives"]["en"]), 1, ls["id"])
            self.assertGreater(ls["duration_minutes"], 0)
            blob = json.dumps(ls["steps"]) + json.dumps(ls["summary"])
            self.assertNotIn("<img", blob)
            self.assertNotIn("![", blob)

    def test_lesson_for(self):
        for ls in LESSONS:
            self.assertEqual(gh.lesson_for(ENTRIES[ls["entry_id"]], LESSONS)["id"], ls["id"])
        link_only = next(e for e in ENTRIES.values() if e["reuse"] == "link-only")
        self.assertIsNone(gh.lesson_for(link_only, LESSONS))

    def report(self):
        pass


class Reuse(unittest.TestCase):
    def test_reuse_flag(self):
        for e in ENTRIES.values():
            self.assertIn(e["reuse"], ("open-content", "link-only"), e["id"])
            if e["reuse"] == "open-content":
                self.assertEqual(e["license"], "CC-BY-SA-4.0")
                self.assertEqual(e["reuse_license"], "CC-BY-SA-4.0")
                self.assertTrue(e["id"].startswith("kids-"))
            else:
                self.assertNotIn("reuse_license", e)
                self.assertTrue(e["license"] == "CC0-1.0")


if __name__ == "__main__":
    unittest.main()
