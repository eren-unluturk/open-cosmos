"""Deployment config: vercel.json mirrors src/csp.py, the entry point re-exports the app, static files are in public/."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import csp  # noqa: E402
from app import app  # noqa: E402

CONF = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))


def headers(rule):
    return {h["key"]: h["value"] for h in rule["headers"]}


class VercelConfig(unittest.TestCase):
    def test_static_header_rules_match_flask(self):
        by_source = {r["source"]: headers(r) for r in CONF["headers"]}
        runner = by_source["/static/runner.js"]
        other = by_source["/static/((?!runner\\.js).*)"]
        for name, value in csp.headers_for(csp.RUNNER_PATH).items():
            self.assertEqual(runner[name], value, name)
        for name, value in csp.headers_for("/static/galaxy.css").items():
            self.assertEqual(other[name], value, name)
        # the negative lookahead really excludes the runner and nothing else
        pattern = re.compile(r"/static/((?!runner\.js).*)")
        self.assertIsNone(pattern.fullmatch("/static/runner.js"))
        self.assertTrue(pattern.fullmatch("/static/galaxy.css"))

    def test_flask_sends_the_headers_on_pages_and_static(self):
        c = app.test_client()
        page = c.get("/en/").headers
        self.assertEqual(page["Content-Security-Policy"], csp.PAGE_CSP)
        self.assertEqual(c.get("/static/galaxy.css").headers["Content-Security-Policy"], csp.PAGE_CSP)
        self.assertEqual(c.get("/static/runner.js").headers["Content-Security-Policy"], csp.RUNNER_CSP)
        for name in csp.COMMON:
            self.assertIn(name, page)

    def test_csp_allows_our_scripts_and_nothing_external_on_pages(self):
        self.assertIn("script-src 'self';", csp.PAGE_CSP)
        self.assertNotIn("unsafe-eval", csp.PAGE_CSP)
        self.assertNotIn("jsdelivr", csp.PAGE_CSP)
        self.assertIn("worker-src 'self'", csp.PAGE_CSP)
        # the only external hosts allowed on pages are the Google Fonts ones the layout already uses
        self.assertEqual(sorted(set(re.findall(r"https://[\w.]+", csp.PAGE_CSP))), ["https://fonts.googleapis.com", "https://fonts.gstatic.com"])
        # the runner may reach only the CDN that serves Pyodide
        self.assertEqual(set(re.findall(r"https://[\w.]+", csp.RUNNER_CSP)), {"https://cdn.jsdelivr.net"})

    def test_csp_allows_the_self_hosted_font_and_our_own_files(self):
        def directive(policy, name):
            m = re.search(r"(?:^|; )%s ([^;]*)" % name, policy)
            return m.group(1).split() if m else []

        page_rule = next(headers(r) for r in CONF["headers"] if r["source"].startswith("/static/(("))
        for policy in (csp.PAGE_CSP, page_rule["Content-Security-Policy"]):  # Flask (pages) and vercel.json (static files)
            self.assertIn("'self'", directive(policy, "font-src"), "self-hosted Atkinson font would be blocked")
            self.assertIn("https://fonts.gstatic.com", directive(policy, "font-src"))
            self.assertEqual(directive(policy, "script-src"), ["'self'"])  # a11y-settings.js, a11y.js, listen.js, galaxy.js ...
            self.assertIn("'self'", directive(policy, "style-src"))        # galaxy.css, a11y.css, problems.css
        self.assertEqual(csp.PAGE_CSP, page_rule["Content-Security-Policy"])

    def test_accessibility_files_are_under_public_static_and_served(self):
        c = app.test_client()
        for name in ("a11y.css", "a11y.js", "a11y-settings.js", "listen.js", "fonts/AtkinsonHyperlegible-Regular-latin.woff2",
                     "fonts/AtkinsonHyperlegible-Bold-latin-ext.woff2", "fonts/OFL.txt"):
            self.assertTrue((ROOT / "public" / "static" / name).exists(), name)
            r = c.get(f"/static/{name}")
            self.assertEqual(r.status_code, 200, name)
            self.assertIn("Content-Security-Policy", r.headers, name)
        html = c.get("/en/").get_data(as_text=True)
        for ref in ("/static/a11y.css", "/static/a11y-settings.js", "/static/a11y.js", "/static/listen.js", "/static/galaxy.css"):
            self.assertIn(ref, html)
        css = (ROOT / "public" / "static" / "a11y.css").read_text(encoding="utf-8")
        for rel in re.findall(r'url\("([^"]+\.woff2)"\)', css):  # font URLs in the CSS resolve to real files next to it
            self.assertTrue((ROOT / "public" / "static" / rel).exists(), rel)

    def test_templates_have_no_inline_scripts_or_handlers(self):
        for path in (ROOT / "src" / "templates").glob("*.html"):
            html = path.read_text(encoding="utf-8")
            for tag in re.findall(r"<script\b[^>]*>", html):
                self.assertTrue("src=" in tag or "application/json" in tag, (path.name, tag))
            self.assertIsNone(re.search(r"\son[a-z]+\s*=\s*[\"']", html), path.name)

    def test_static_files_live_in_public(self):
        for name in ("galaxy.css", "galaxy.js", "problem.js", "runner.js", "a11y.css", "a11y.js", "a11y-settings.js", "listen.js"):
            self.assertTrue((ROOT / "public" / "static" / name).exists(), name)
        self.assertFalse((ROOT / "src" / "static").exists())
        self.assertEqual(app.test_client().get("/static/galaxy.css").status_code, 200)

    def test_entry_point_reexports_the_same_app(self):
        out = subprocess.run([sys.executable, "-c", "import index, app; print(index.app is app.app)"], cwd=ROOT,
                             capture_output=True, text=True, env={"PATH": "", "PYTHONPATH": str(ROOT / "src")})
        self.assertEqual(out.stdout.strip().splitlines()[-1], "True", out.stderr[-300:])

    def test_requirements_are_minimal_and_pinned_python(self):
        reqs = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
        self.assertNotIn("anthropic", reqs)
        for needed in ("flask", "requests", "python-dotenv"):
            self.assertIn(needed, reqs)
        self.assertEqual((ROOT / ".python-version").read_text().strip(), "3.12")
        self.assertTrue((ROOT / "render.yaml").exists())

    def test_smoke_remote_fails_when_nothing_is_listening(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import io
        from unittest import mock
        import smoke_remote
        with mock.patch("sys.stdout", io.StringIO()):
            self.assertEqual(smoke_remote.main(["http://127.0.0.1:9", "--slow", "3"]), 1)


if __name__ == "__main__":
    unittest.main()
