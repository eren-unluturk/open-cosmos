"""Coding problems are translated through an overlay (src/data/problems_overlay.json); problems.json stays English-only."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import store  # noqa: E402

OVERLAY = json.loads((ROOT / "src/data/problems_overlay.json").read_text(encoding="utf-8"))
RAW = json.loads((ROOT / "src/data/problems.json").read_text(encoding="utf-8"))
LANGS4 = ("es", "ar", "hi", "pt")


def english_texts():
    out = set()
    for p in RAW:
        nodes = []
        store._problem_nodes(p, nodes)
        for n in nodes:
            out.update(n["en"] if isinstance(n["en"], list) else [n["en"]])
    return out


class ProblemOverlay(unittest.TestCase):
    def test_every_text_has_four_languages(self):
        for en, t in OVERLAY.items():
            self.assertEqual(set(t), set(LANGS4), en)
            for s in t.values():
                self.assertTrue(s.strip(), en)

    def test_no_stale_keys_and_nothing_missing(self):
        used = english_texts()
        self.assertEqual(set(OVERLAY) - used, set())
        self.assertEqual(used - set(OVERLAY), set())

    def test_same_shape_in_every_language(self):
        for p in store.problems():
            nodes = []
            store._problem_nodes(p, nodes)
            for n in nodes:
                for lang in LANGS4:
                    self.assertIn(lang, n, (p["id"], lang))
                    self.assertEqual(type(n[lang]), type(n["en"]))
                    if isinstance(n["en"], list):
                        self.assertEqual(len(n[lang]), len(n["en"]))


if __name__ == "__main__":
    unittest.main()
