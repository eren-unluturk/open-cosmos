"""Every UI string exists in every language (proper names such as Python or the brand may stay English)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import app  # noqa: E402

NAMES = {"brand", "s_python", "s_java", "s_kidbots", "s_robots", "p_lang_python", "p_lang_javascript"}


class UiStrings(unittest.TestCase):
    def test_no_language_falls_back_to_english(self):
        en = app.UI["en"]
        for code in ("es", "pt", "ar", "hi"):
            missing = sorted(k for k in en if k not in app.UI[code] and k not in NAMES)
            self.assertEqual(missing, [], code)

    def test_placeholders_match(self):
        import re
        ph = lambda s: sorted(re.findall(r"\{\w+\}", str(s)))  # noqa: E731
        for code in ("es", "pt", "ar", "hi"):
            for k, v in app.UI[code].items():
                if k in app.UI["en"] and isinstance(v, str):
                    self.assertEqual(ph(v), ph(app.UI["en"][k]), (code, k))


if __name__ == "__main__":
    unittest.main()
