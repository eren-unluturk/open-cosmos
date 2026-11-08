"""Issue #7: list pages get a search box, age/topic filters, a hidden-entries notice, and the right brand."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from app import LANGS, app  # noqa: E402


class ListingUI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_filter_form_on_every_list_page_and_language(self):
        for lang in LANGS:
            for side in ("learn", "build", "kids"):
                html = self.c.get(f"/{lang}/{side}").get_data(as_text=True)
                self.assertIn('name="q"', html, (lang, side))
                self.assertIn('name="age"', html, (lang, side))
                self.assertIn('name="topic"', html, (lang, side))
                self.assertIn('<label for="list-q"', html, (lang, side))

    def test_filters_work_and_stay_in_the_pills(self):
        html = self.c.get("/en/learn?q=python&age=11-13&topic=general&level=Beginner").get_data(as_text=True)
        self.assertIn('value="python"', html)
        self.assertRegex(html, r'<option value="11-13" selected')
        self.assertRegex(html, r'<option value="general" selected')
        # level pills keep the other filters
        self.assertRegex(html, r'href="/en/learn\?[^"]*q=python')

    def test_hidden_entries_are_explained_until_grown_up_mode(self):
        c = app.test_client()
        html = c.get("/en/learn").get_data(as_text=True)
        self.assertIn("more stops are hidden", html)
        self.assertIn('action="/grownup"', html)
        c.post("/grownup", data={"on": "1", "next": "/en/learn"})
        html = c.get("/en/learn").get_data(as_text=True)
        self.assertNotIn("more stops are hidden", html)

    def test_adult_only_never_listed(self):
        import store
        c = app.test_client()
        c.post("/grownup", data={"on": "1", "next": "/"})
        adult_only = [e for e in store.entries() if e["safety"] == "adult-only"]
        self.assertTrue(adult_only)
        for side in ("learn", "build"):
            html = c.get(f"/en/{side}").get_data(as_text=True)
            for e in adult_only:
                self.assertNotIn(f"/entry/{e['id']}", html)

    def test_bad_filter_values_are_ignored(self):
        r = self.c.get("/en/learn?age=<script>&topic=%27%3E&level=zzz&q=" + "x" * 500)
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("<script>", r.get_data(as_text=True).split("<main")[1])

    def test_brand_is_open_cosmos(self):
        for lang in LANGS:
            html = self.c.get(f"/{lang}/").get_data(as_text=True)
            self.assertRegex(html, r"<title>[^<]*Open Cosmos", lang)
            self.assertNotIn("Open Learn", html)
            self.assertNotIn("Learning Lab", html)


if __name__ == "__main__":
    unittest.main()
