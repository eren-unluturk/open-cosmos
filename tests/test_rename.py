"""The app is called "Open Cosmos" (Latin script in every language); the old names must not appear in rendered pages."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from app import LANGS, app  # noqa: E402
import store  # noqa: E402

OLD = ("Hackcessability", "Learning Lab", "Open Learn", "learning-lab")
LESSON = json.loads((ROOT / "src/data/lessons.json").read_text(encoding="utf-8"))[0]
KID = next(e for e in store.entries() if e["safety"] == "kid-safe")
PAGES = ["/", "/learn", "/build", "/kids", "/guide", "/lessons", f"/lesson/{LESSON['id']}", f"/entry/{KID['id']}",
         f"/entry/{LESSON['entry_id']}", "/problems", "/problem/py-hello", "/problem/py-card-values", "/me", "/library",
         "/constellation", "/galaxy/code", "/galaxy/code/python", "/catalogue", "/howto/video"]


class Rename(unittest.TestCase):
    def test_every_page_every_language(self):
        c = app.test_client()
        for lang in LANGS:
            for p in PAGES:
                r = c.get(f"/{lang}{p}" if p != "/" else f"/{lang}/")
                self.assertEqual(r.status_code, 200, (lang, p))
                html = r.get_data(as_text=True)
                self.assertIn("Open Cosmos", html, (lang, p))
                for old in OLD:
                    self.assertNotIn(old, html, (lang, p, old))

    def test_meta_tags_and_rtl_footer(self):
        html = app.test_client().get("/ar/").get_data(as_text=True)
        self.assertIn('<meta name="application-name" content="Open Cosmos">', html)
        self.assertIn('<meta property="og:site_name" content="Open Cosmos">', html)
        self.assertIn('<bdi dir="ltr">Open Cosmos</bdi>', html)

    def test_generated_attribution_uses_new_name(self):
        for ls in json.loads((ROOT / "src/data/lessons.json").read_text(encoding="utf-8")):
            self.assertIn("Open Cosmos", ls["changes_made"]["en"] if isinstance(ls["changes_made"], dict) else ls["changes_made"])


if __name__ == "__main__":
    unittest.main()
