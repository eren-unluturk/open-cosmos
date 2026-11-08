"""Regression: no raw "{n}"-style placeholder may show in the visible text of the main pages, in any language."""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import app  # noqa: E402

LANGS = ("en", "es", "ar", "hi", "pt")
SKIP = {"script", "style", "template"}


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.depth = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in SKIP and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth:
            self.out.append(data)


def visible_text(html):
    p = Visible()
    p.feed(html)
    return " ".join(p.out)


class NoPlaceholders(unittest.TestCase):
    def test_pages_have_no_raw_placeholders(self):
        c = app.app.test_client()
        entry = re.search(r"/en/entry/([\w-]+)", c.get("/en/library").get_data(as_text=True)).group(1)
        for lang in LANGS:
            paths = [f"/{lang}/", f"/{lang}/library", f"/{lang}/galaxy/code", f"/{lang}/entry/{entry}", f"/{lang}/guide"]
            for path in paths:
                r = c.get(path)
                self.assertEqual(r.status_code, 200, path)
                bad = re.findall(r"\{\w*\}", visible_text(r.get_data(as_text=True)))
                self.assertEqual(bad, [], path)

    def test_library_shows_remaining_count(self):
        html = app.app.test_client().get("/en/library").get_data(as_text=True)
        self.assertRegex(visible_text(html), r"and \d+ more\. Use search")


if __name__ == "__main__":
    unittest.main()
