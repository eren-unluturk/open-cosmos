"""Guide translations overlay (src/data/guides_translated.json): clean, complete per guide, and shown in the app."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import store  # noqa: E402
from app import app  # noqa: E402

OVERLAY = json.loads((ROOT / "src/data/guides_translated.json").read_text(encoding="utf-8"))
RAW = json.loads((ROOT / "src/data/guides.json").read_text(encoding="utf-8"))
LANGS = ("es", "ar", "hi", "pt")
ph = lambda t: sorted(re.findall(r"\{\w+\}", t))  # noqa: E731


class Overlay(unittest.TestCase):
    def test_every_entry_has_four_languages_and_same_placeholders(self):
        for en, t in OVERLAY.items():
            self.assertEqual(set(t), set(LANGS), en)
            for lang, s in t.items():
                self.assertTrue(s.strip(), (en, lang))
                self.assertEqual(ph(s), ph(en), (en, lang))
                self.assertNotRegex(s, r"https?://|www\.", (en, lang))

    def test_no_stale_overlay_keys(self):
        texts = []
        store._text_nodes(RAW, texts)
        english = {n["en"] for n in texts}
        self.assertEqual(set(OVERLAY) - english, set(), "overlay has text that no guide uses any more")

    def test_guides_json_stays_english_only(self):
        texts = []
        store._text_nodes(RAW, texts)
        self.assertTrue(all(set(n) == {"en"} for n in texts))

    def test_all_or_nothing_per_guide(self):
        guides = json.loads(json.dumps(RAW))
        store._add_guide_translations(guides, OVERLAY)
        for g in list(guides["fallback"].values()) + list(guides["groups"].values()):
            nodes = []
            store._text_nodes(g, nodes)
            for lang in LANGS:
                have = [lang in n for n in nodes]
                self.assertTrue(all(have) or not any(have), (g["id"], lang))

    def test_report_coverage(self):
        guides = json.loads(json.dumps(RAW))
        store._add_guide_translations(guides, OVERLAY)
        allg = list(guides["fallback"].values()) + list(guides["groups"].values())
        done = {l: sum(1 for g in allg if all(l in n for n in (lambda o: (store._text_nodes(g, o), o)[1])([]))) for l in LANGS}
        print(f"\n[guide translations] guides fully translated per language: {done} of {len(allg)}")

    def test_translated_guide_is_served_in_the_language(self):
        c = app.test_client()
        lesson = c.get("/es/entry/kids-a93d9654").get_data(as_text=True)  # has a lesson: last slide is go_lesson
        self.assertIn("Empezar la lección", lesson)
        self.assertNotIn("Shown in English", lesson)
        unit = c.get("/es/entry/kids-cff31573").get_data(as_text=True)  # a unit: last slide leaves our site
        self.assertIn("Ir al sitio de aprendizaje", unit)
        self.assertIn("Tu navegador puede traducir la página", unit)
        ar = c.get("/ar/entry/kids-cff31573").get_data(as_text=True)
        self.assertIn("اذهب إلى موقع التعلّم", ar)
        self.assertIn('dir="rtl"', ar)


if __name__ == "__main__":
    unittest.main()
