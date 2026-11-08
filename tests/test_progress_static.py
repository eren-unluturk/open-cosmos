"""Static checks for src/static/progress.js (browser-only progress). Nothing may be sent anywhere."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "src" / "static" / "progress.js"
CSS = ROOT / "src" / "static" / "progress.css"
TEXT = ROOT / "src" / "data" / "progress_text.json"


class ProgressStatic(unittest.TestCase):
    def setUp(self):
        self.js = JS.read_text(encoding="utf-8")

    def test_files_exist(self):
        self.assertTrue(JS.exists() and CSS.exists() and TEXT.exists())

    def test_no_dangerous_apis(self):
        for bad in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function", "fetch(",
                    "XMLHttpRequest", "sendBeacon", "WebSocket", "document.cookie", "sessionStorage", "indexedDB",
                    "window.open", "location."):
            self.assertNotIn(bad, self.js, bad)

    def test_no_urls_or_external_hosts(self):
        self.assertNotRegex(self.js, r"https?://")

    def test_storage_key_exact(self):
        self.assertEqual(self.js.count("hc_progress_v1"), 2)  # the constant + the header comment
        self.assertIn("var KEY = 'hc_progress_v1';", self.js)
        self.assertEqual(self.js.count("root.localStorage"), 1)  # touched in exactly one place

    def test_storage_access_is_guarded(self):
        self.assertIn("try { storage = root.localStorage || null; } catch (e) { storage = null; }", self.js)

    def test_strings_cover_every_language(self):
        data = json.loads(TEXT.read_text(encoding="utf-8"))
        en = set(data["en"])
        for lang in ("en", "es", "ar", "hi", "pt"):
            self.assertEqual(set(data[lang]), en, lang)
            self.assertTrue(data[lang]["privacy"].strip())
        for key in re.findall(r"t\('(\w+)'", self.js):
            self.assertIn(key, en, key)

    def test_css_uses_logical_properties(self):
        css = CSS.read_text(encoding="utf-8")
        for physical in ("margin-left", "margin-right", "padding-left", "padding-right", "text-align: left", "text-align: right"):
            self.assertNotIn(physical, css, physical)
        self.assertIn("min-block-size: 44px", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_node_unit_tests(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node is not installed: skipping tests/progress.test.js (install Node to run the JS unit tests)")
        r = subprocess.run([node, str(ROOT / "tests" / "progress.test.js")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
