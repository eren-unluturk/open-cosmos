"""Final smoke test: every page in all five languages, the safety gate, and 404s."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from app import LANGS, app  # noqa: E402
import store  # noqa: E402

LESSON = json.loads((ROOT / "src/data/lessons.json").read_text(encoding="utf-8"))[0]
ENTRIES = store.entries()
KID = next(e for e in ENTRIES if e["safety"] == "kid-safe" and e["id"].startswith("build-"))
ASK = next(e for e in ENTRIES if e["safety"] == "ask-a-grown-up")
ADULT = [e for e in ENTRIES if e["safety"] == "adult-only"]
PAGES = ["/", "/learn", "/build", "/kids", "/guide", "/guide?age=8-10&goal=games&level=Beginner", "/lessons",
         f"/lesson/{LESSON['id']}", f"/entry/{KID['id']}", f"/entry/{LESSON['entry_id']}", "/problems", "/problem/py-hello",
         "/me", "/library", "/library?q=python", "/constellation", "/galaxy/code", "/galaxy/code/python", "/catalogue",
         "/howto/video", "/learn?q=python&age=11-13&topic=general&level=Beginner"]


class Smoke(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True

    def test_every_page_every_language_returns_200(self):
        c = app.test_client()
        bad = []
        for lang in LANGS:
            for p in PAGES:
                r = c.get(f"/{lang}{p}" if p != "/" else f"/{lang}/")
                if r.status_code != 200:
                    bad.append((lang, p, r.status_code))
        self.assertEqual(bad, [])

    def test_health_and_api(self):
        c = app.test_client()
        self.assertEqual(c.get("/healthz").get_json(), {"ok": True})
        self.assertEqual(c.get("/api/entries").status_code, 200)

    def test_gate_default_hides_ask_and_adult_only(self):
        c = app.test_client()
        self.assertEqual(c.get(f"/en/entry/{ASK['id']}").status_code, 404)
        for e in ADULT:
            self.assertEqual(c.get(f"/en/entry/{e['id']}").status_code, 404, e["id"])
        self.assertNotIn(f"/entry/{ASK['id']}", c.get("/en/learn").get_data(as_text=True))
        ids = {e["id"] for e in c.get("/api/entries").get_json()} if isinstance(c.get("/api/entries").get_json(), list) else set()
        self.assertFalse(ids & {e["id"] for e in ADULT})

    def test_grown_up_flag_reveals_ask_but_never_adult_only(self):
        c = app.test_client()
        c.post("/grownup", data={"on": "1", "next": "/en/learn"})
        self.assertEqual(c.get(f"/en/entry/{ASK['id']}").status_code, 200)
        for e in ADULT:
            self.assertEqual(c.get(f"/en/entry/{e['id']}").status_code, 404, e["id"])
        c.post("/grownup", data={"on": "0", "next": "/en/learn"})
        self.assertEqual(c.get(f"/en/entry/{ASK['id']}").status_code, 404)

    def test_unknown_pages_404(self):
        c = app.test_client()
        for p in ("/en/nope", "/xx/", "/en/entry/zzz-00000000", "/en/lesson/lesson-ffffffff", "/en/galaxy/nope",
                  "/en/problem/does-not-exist", "/en/howto/zzz", "/nothing-here"):
            self.assertEqual(c.get(p, follow_redirects=True).status_code, 404, p)

    def test_rtl_and_english_fallback(self):
        c = app.test_client()
        html = c.get("/ar/learn").get_data(as_text=True)
        self.assertIn('dir="rtl"', html)
        self.assertIn('dir="ltr"', c.get("/en/learn").get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
