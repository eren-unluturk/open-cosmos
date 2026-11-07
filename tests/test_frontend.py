"""Galaxy frontend smoke tests. Run: python -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from app import LANGS, app  # noqa: E402
import store  # noqa: E402


class GalaxyPages(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_galaxy_pages_all_langs(self):
        ls = store.lessons()[0]
        for lang in LANGS:
            for path in ("/", "constellation", "galaxy/code", "galaxy/code/python", "library", "library?q=python",
                         "me", "lessons", f"lesson/{ls['id']}", "catalogue"):
                url = f"/{lang}/" if path == "/" else f"/{lang}/{path}"
                self.assertEqual(self.c.get(url).status_code, 200, url)

    def test_entry_has_slides_and_leaving_notice(self):
        e = next(e for e in store.entries("build") if e["safety"] == "kid-safe")
        html = self.c.get(f"/en/entry/{e['id']}").get_data(as_text=True)
        self.assertEqual(html.count("data-slide-type="), 6)
        self.assertIn("You are leaving our site", html)
        self.assertIn('rel="noopener noreferrer"', html)

    def test_lesson_entry_links_to_our_lesson_with_attribution(self):
        ls = store.lessons()[0]
        html = self.c.get(f"/en/entry/{ls['entry_id']}").get_data(as_text=True)
        self.assertIn(f"/en/lesson/{ls['id']}", html)
        page = self.c.get(f"/en/lesson/{ls['id']}").get_data(as_text=True)
        self.assertIn("CC BY-SA 4.0", page)
        self.assertIn(ls["source_url"], page)

    def test_level_filter_is_session_only(self):
        self.c.post("/en/prefs", data={"level": "Advanced", "next": "/en/"})
        html = self.c.get("/en/library").get_data(as_text=True)
        self.assertIn('class="navbtn lvl lvl-astronaut on"', html)
        r = self.c.post("/en/prefs", data={"level": "", "next": "//evil.example"})
        self.assertEqual(r.headers["Location"], "/")

    def test_galaxy_hides_grown_up_stops_by_default(self):
        u_html = self.c.get("/en/galaxy/robotics").get_data(as_text=True)
        self.assertIn("I&#39;m a grown-up", u_html)


if __name__ == "__main__":
    unittest.main()
