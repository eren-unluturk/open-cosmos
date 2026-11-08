"""Hand-written entry translations (issue #6 'next batch'): complete, labeled, and merged into the data."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import apply_translations as at  # noqa: E402

DATA = ROOT / "src" / "data"
ENTRIES = {e["id"]: e for n in ("learn", "build", "kids") for e in json.loads((DATA / f"{n}.json").read_text(encoding="utf-8"))}


class Overlay(unittest.TestCase):
    def setUp(self):
        self.tr = at.collect()

    def test_covers_the_24_activities_and_the_377_queued_entries(self):
        self.assertEqual(len(self.tr), 24 + 377)
        self.assertEqual(sum(1 for i in self.tr if i.startswith("kids-")), 24)

    def test_every_language_title_and_desc_present_and_clean(self):
        for eid, t in self.tr.items():
            for lang in at.LANGS:
                for field in ("title", "desc"):
                    s = t[field][lang]
                    if field == "desc" and not ENTRIES[eid]["desc"]["en"]:
                        self.assertEqual(s, "", (eid, lang))  # nothing to translate
                        continue
                    self.assertTrue(s.strip(), (eid, lang, field))
                    self.assertNotRegex(s, r"[{}]", (eid, lang))  # no unfilled placeholders
                    self.assertNotRegex(s, r"https?://|www\.")

    def test_data_contains_them_and_labels_ai(self):
        for eid, t in self.tr.items():
            e = ENTRIES[eid]
            for lang in at.LANGS:
                self.assertEqual(e["title"][lang], t["title"][lang], eid)
                self.assertEqual(e["desc"][lang], t["desc"][lang], eid)
            self.assertTrue(set(at.LANGS) <= set(e["ai_translated"]), eid)
            if eid.startswith("kids-"):
                self.assertEqual(e["license"], "CC-BY-SA-4.0")

    def test_arabic_keeps_arabic_script(self):
        for eid, t in self.tr.items():
            if ENTRIES[eid]["desc"]["en"]:
                self.assertTrue(re.search("[\u0600-\u06FF]", t["desc"]["ar"]), eid)

    def test_the_kid_safe_queue_is_empty(self):
        import translate
        self.assertEqual(translate.pick_todo(list(ENTRIES.values())), [])

    def test_empty_descriptions_stay_empty(self):
        for eid, t in self.tr.items():
            if not ENTRIES[eid]["desc"]["en"]:
                for lang in at.LANGS:
                    self.assertEqual(ENTRIES[eid]["desc"][lang], "", (eid, lang))


if __name__ == "__main__":
    unittest.main()
