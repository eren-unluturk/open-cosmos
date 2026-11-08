"""Lessons are translated through an overlay (src/data/lessons_overlay.json); lessons.json stays English-only."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import store  # noqa: E402
from app import LANGS, app  # noqa: E402

OVERLAY = json.loads((ROOT / "src/data/lessons_overlay.json").read_text(encoding="utf-8"))
RAW = json.loads((ROOT / "src/data/lessons.json").read_text(encoding="utf-8"))
LANGS4 = ("es", "ar", "hi", "pt")
FIELDS = store.LESSON_TEXT_FIELDS


def texts(ls):
    out = []
    for f in FIELDS:
        v = ls[f]["en"]
        out += v if isinstance(v, list) else [v]
    return out


class LessonOverlay(unittest.TestCase):
    def test_every_text_has_four_languages(self):
        for en, t in OVERLAY.items():
            self.assertEqual(set(t), set(LANGS4), en)
            for lang, s in t.items():
                self.assertTrue(s.strip(), (en, lang))
                self.assertNotRegex(s, r"https?://|<[a-z]", (en, lang))

    def test_no_stale_keys_and_every_lesson_text_is_translated(self):
        used = {t for ls in RAW for t in texts(ls)}
        self.assertEqual(set(OVERLAY) - used, set(), "overlay has text no lesson uses any more")
        self.assertEqual(used - set(OVERLAY), set(), "lesson text without a translation")

    def test_lessons_json_stays_english_only(self):
        for ls in RAW:
            for f in FIELDS:
                self.assertEqual(set(ls[f]), {"en"})

    def test_loaded_lessons_have_every_language_and_same_shape(self):
        for ls in store.lessons():
            for lang in LANGS4:
                for f in FIELDS:
                    en = ls[f]["en"]
                    self.assertIn(lang, ls[f], (ls["id"], f, lang))
                    self.assertEqual(type(ls[f][lang]), type(en))
                    if isinstance(en, list):
                        self.assertEqual(len(ls[f][lang]), len(en))
                self.assertIn(lang, ls["title"], (ls["id"], lang))

    def test_lesson_pages_are_fully_translated_and_keep_attribution(self):
        c = app.test_client()
        for ls in store.lessons():
            for lang in LANGS4:
                html = c.get(f"/{lang}/lesson/{ls['id']}").get_data(as_text=True)
                self.assertNotIn("english-only", html)
                self.assertIn("CC BY-SA 4.0", html)
                self.assertIn(ls["license_url"], html)
                self.assertNotIn("Simplified, shortened", html, (ls["id"], lang))
                self.assertNotIn("Shown in English", html)
        ar = c.get("/ar/lesson/lesson-a93d9654").get_data(as_text=True)
        self.assertIn('dir="rtl"', ar)
        self.assertRegex(ar, r"[؀-ۿ]{3,}")

    def test_lessons_list_is_translated(self):
        c = app.test_client()
        for lang in LANGS4:
            html = c.get(f"/{lang}/lessons").get_data(as_text=True)
            self.assertNotIn("Children pretend to be tiny switches", html)


if __name__ == "__main__":
    unittest.main()
