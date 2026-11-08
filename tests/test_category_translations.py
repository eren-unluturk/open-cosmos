"""Every category heading has es/ar/hi/pt text, and the listing pages show it."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import store  # noqa: E402
from app import app  # noqa: E402

CATS = {e["category"] for n in ("learn", "build", "kids") for e in json.loads((ROOT / "src/data" / f"{n}.json").read_text(encoding="utf-8"))}
T = json.loads((ROOT / "src/data/categories_translated.json").read_text(encoding="utf-8"))


class Categories(unittest.TestCase):
    def test_all_categories_translated(self):
        self.assertEqual(CATS - set(T), set())
        for name, t in T.items():
            self.assertEqual(set(t), {"es", "ar", "hi", "pt"}, name)
            self.assertTrue(all(v.strip() for v in t.values()), name)

    def test_fallback_to_english(self):
        self.assertEqual(store.category("Books", "en"), "Books")
        self.assertEqual(store.category("Nope", "es"), "Nope")

    def test_listing_uses_translated_heading(self):
        html = app.test_client().get("/ar/build").get_data(as_text=True)
        self.assertNotIn("Build your own Shell", html)


if __name__ == "__main__":
    unittest.main()
