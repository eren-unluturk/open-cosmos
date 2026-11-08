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

    def test_covers_the_24_cs_unplugged_activity_entries(self):
        self.assertEqual(len(self.tr), 24)
        self.assertTrue(all(i.startswith("kids-") for i in self.tr))

    def test_every_language_title_and_desc_present_and_clean(self):
        for eid, t in self.tr.items():
            for lang in at.LANGS:
                for field in ("title", "desc"):
                    s = t[field][lang]
                    self.assertTrue(s.strip(), (eid, lang, field))
                    self.assertNotRegex(s, r"[{}]", (eid, lang))  # no unfilled placeholders
                    self.assertNotIn("http", s)

    def test_data_contains_them_and_labels_ai(self):
        for eid, t in self.tr.items():
            e = ENTRIES[eid]
            for lang in at.LANGS:
                self.assertEqual(e["title"][lang], t["title"][lang], eid)
                self.assertEqual(e["desc"][lang], t["desc"][lang], eid)
            self.assertTrue(set(at.LANGS) <= set(e["ai_translated"]), eid)
            self.assertEqual(e["license"], "CC-BY-SA-4.0")

    def test_arabic_keeps_arabic_script(self):
        for eid, t in self.tr.items():
            self.assertTrue(re.search(r"[؀-ۿ]", t["desc"]["ar"]), eid)

    def test_queue_shrinks(self):
        import translate
        left = [e for e in translate.pick_todo(list(ENTRIES.values())) if e["id"].startswith("kids-")]
        self.assertEqual(left, [])


if __name__ == "__main__":
    unittest.main()
