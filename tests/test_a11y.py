"""Accessibility: markup hooks, statement page and strings in all five languages, theme tokens, fonts, Node tests."""
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
import i18n_a11y  # noqa: E402
from app import LANGS, app  # noqa: E402

STATIC = ROOT / "src" / "static"
TAGS = {"en": "en-US", "es": "es-ES", "ar": "ar-SA", "hi": "hi-IN", "pt": "pt-BR"}


class Strings(unittest.TestCase):
    def test_every_language_has_every_key(self):
        for lang, labels in i18n_a11y.UI.items():
            self.assertEqual(set(labels), set(i18n_a11y.UI_EN), lang)
            self.assertTrue(all(v.strip() for v in labels.values()), lang)

    def test_app_name_stays_in_latin_script(self):
        for lang, labels in i18n_a11y.UI.items():
            for k in ("a11y_intro", "a11y_h_supports", "a11y_page_intro"):
                if "Open" in labels[k] or "Cosmos" in labels[k]:
                    self.assertIn("Open Cosmos", labels[k], (lang, k))
            self.assertIn("Open Cosmos", labels["a11y_intro"], lang)


class Markup(unittest.TestCase):
    def setUp(self):
        self.c = app.test_client()

    def test_head_script_is_external_and_before_paint(self):
        for lang in LANGS:
            html = self.c.get(f"/{lang}/").get_data(as_text=True)
            head = html.split("</head>")[0]
            self.assertIn("a11y-settings.js", head, lang)
            self.assertNotRegex(head, r"<script(?![^>]*\ssrc=)[^>]*>(?!\s*</script>)", lang)  # no inline scripts
            self.assertIn("a11y.css", head)
            self.assertNotIn(" onclick=", html)

    def test_header_button_and_panel_in_every_language(self):
        for lang in LANGS:
            html = self.c.get(f"/{lang}/learn").get_data(as_text=True)
            ui = i18n_a11y.UI_EN if lang == "en" else i18n_a11y.UI[lang]
            self.assertRegex(html, r'<button[^>]*id="a11y-open"[^>]*aria-expanded="false"')
            self.assertIn('aria-haspopup="dialog"', html)
            self.assertRegex(html, r'id="a11y-panel"[^>]*role="dialog"[^>]*aria-modal="true"[^>]*aria-labelledby="a11y-title"')
            self.assertIn(f">{ui['a11y_title']}</h2>", html)
            for group in ("theme", "size", "spacing", "font"):
                self.assertIn(f'name="a11y-{group}"', html)
            self.assertEqual(len(re.findall(r'name="a11y-theme"', html)), 5)
            self.assertIn('id="a11y-motion"', html)
            self.assertIn('role="status" aria-live="polite"', html)  # announcements
            self.assertIn("Open Cosmos", ui["a11y_intro"])

    def test_panel_labels_every_control(self):
        html = self.c.get("/en/").get_data(as_text=True)
        panel = html[html.index('id="a11y-panel"'):]
        self.assertEqual(len(re.findall(r"<input", panel.split("</div>\n<script")[0])), panel.split("</div>\n<script")[0].count("</label>"))
        self.assertEqual(panel.count("<fieldset>"), panel.count("<legend>"))

    def test_rtl_arabic_has_rtl_panel_and_latin_name(self):
        html = self.c.get("/ar/").get_data(as_text=True)
        self.assertIn('<html lang="ar" dir="rtl">', html)
        self.assertIn("Open Cosmos", html)
        self.assertIn('<bdi dir="ltr">Open Cosmos</bdi>', html)

    def test_footer_links_to_the_statement(self):
        for lang in LANGS:
            html = self.c.get(f"/{lang}/").get_data(as_text=True)
            self.assertIn(f'href="/{lang}/accessibility"', html)

    def test_aria_labels_are_translated(self):
        self.assertNotIn('aria-label="Breadcrumb"', self.c.get("/es/lesson/lesson-0d3a63dc").get_data(as_text=True))
        self.assertNotIn('aria-label="Main"', self.c.get("/ar/").get_data(as_text=True))
        self.assertIn(f'aria-label="{i18n_a11y.UI["pt"]["nav_main"]}"', self.c.get("/pt/").get_data(as_text=True))

    def test_listen_widget_on_lessons_entries_and_slides(self):
        for lang in LANGS:
            lesson = self.c.get(f"/{lang}/lesson/lesson-0d3a63dc").get_data(as_text=True)
            self.assertIn(f'data-lang-tag="{TAGS[lang]}"', lesson)
            self.assertRegex(lesson, r'data-listen data-target="#main"[^>]* hidden')  # hidden until speech is supported
            self.assertIn('role="status" aria-live="polite"', lesson)
            entry = self.c.get(f"/{lang}/entry/kids-0d3a63dc").get_data(as_text=True)
            self.assertEqual(entry.count("data-listen "), 2, lang)
            self.assertIn('data-target="#entry-title, #entry-desc"', entry)
            self.assertIn('data-target="#guide .deck"', entry)

    def test_statement_page_in_all_languages(self):
        for lang in LANGS:
            r = self.c.get(f"/{lang}/accessibility")
            self.assertEqual(r.status_code, 200)
            html = r.get_data(as_text=True)
            ui = i18n_a11y.UI_EN if lang == "en" else i18n_a11y.UI[lang]
            self.assertIn("Open Cosmos", html)
            self.assertEqual(html.count("<h1"), 1)
            for key in ("a11y_h_supports", "a11y_h_change", "a11y_h_limits", "a11y_h_report", "a11y_p_voices", "a11y_p_ai", "a11y_p_standard"):
                self.assertIn(ui[key].replace("'", "&#39;").replace('"', "&#34;"), html, (lang, key))
        self.assertEqual(self.c.get("/xx/accessibility").status_code, 404)

    def test_statement_links_to_feedback_only_for_grownups(self):
        for lang in LANGS:
            self.assertNotIn("/feedback", self.c.get(f"/{lang}/accessibility").get_data(as_text=True).split("<footer")[0])
        with self.c.session_transaction() as s:
            s["adult"] = True
        self.assertIn("/es/feedback", self.c.get("/es/accessibility").get_data(as_text=True))

    def test_static_assets_exist_and_are_served(self):
        for name in ("a11y-settings.js", "a11y.js", "listen.js", "a11y.css"):
            self.assertEqual(self.c.get(f"/static/{name}").status_code, 200, name)
        for f in ("AtkinsonHyperlegible-Regular-latin.woff2", "AtkinsonHyperlegible-Bold-latin.woff2", "OFL.txt"):
            self.assertTrue((STATIC / "fonts" / f).exists(), f)
        self.assertIn("SIL Open Font License", (STATIC / "fonts" / "OFL.txt").read_text(encoding="utf-8"))


class Css(unittest.TestCase):
    css = (STATIC / "a11y.css").read_text(encoding="utf-8")

    def test_four_themes_and_size_spacing_font_hooks(self):
        for sel in ('html[data-theme="light"]', 'html[data-theme="contrast"]', 'html[data-theme="cb"]', 'html[data-size="125"]',
                    'html[data-size="150"]', 'html[data-spacing="wide"]', 'html[data-font="easy"]'):
            self.assertIn(sel, self.css, sel)

    def test_font_is_self_hosted_and_loads_only_when_used(self):
        self.assertNotIn("http", re.sub(r"/\*.*?\*/", "", self.css, flags=re.S))
        self.assertEqual(self.css.count("@font-face"), 4)
        galaxy = (STATIC / "galaxy.css").read_text(encoding="utf-8")
        self.assertNotIn("Atkinson", galaxy)  # only the data-font="easy" rule names the family, so nobody downloads it otherwise

    def test_contrast_script_passes(self):
        import check_contrast
        rows, fails = check_contrast.check()
        self.assertGreater(len(rows), 100)
        self.assertEqual(fails, [], fails)

    def test_motion_and_size_work_without_px_fonts(self):
        galaxy = (STATIC / "galaxy.css").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"font-size:\s*\d+px", galaxy))
        self.assertIn('html[data-motion="reduce"]', galaxy)


class NodeSettings(unittest.TestCase):
    def test_settings_module_with_node(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node is not installed")
        files = sorted(str(f) for f in (ROOT / "tests" / "js").glob("*.test.js"))
        out = subprocess.run([node, "--test", *files], capture_output=True, text=True, timeout=120)
        self.assertEqual(out.returncode, 0, out.stdout[-1500:] + out.stderr[-500:])


if __name__ == "__main__":
    unittest.main()
