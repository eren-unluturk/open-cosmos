"""Security checks: cross-site POSTs, cookies, XSS sinks, secrets, data minimisation."""
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from app import app  # noqa: E402


class CrossSitePosts(unittest.TestCase):
    def setUp(self):
        self.c = app.test_client()

    def test_cross_site_posts_are_refused(self):
        for path in ("/grownup", "/en/prefs", "/en/feedback"):
            for headers in ({"Origin": "https://evil.example"}, {"Sec-Fetch-Site": "cross-site"},
                            {"Sec-Fetch-Site": "cross-site", "Origin": "null"}, {"Sec-Fetch-Site": "same-site"},
                            {"Sec-Fetch-Site": "cross-site", "Origin": "http://localhost"}):
                r = self.c.post(path, data={"on": "1"}, headers=headers)
                self.assertEqual(r.status_code, 403, (path, headers))
        with self.c.session_transaction() as s:
            self.assertFalse(s.get("adult"))  # nothing changed

    def test_same_origin_posts_still_work(self):
        r = self.c.post("/grownup", data={"on": "1", "next": "/en/"}, headers={"Origin": "http://localhost", "Sec-Fetch-Site": "same-origin"})
        self.assertEqual(r.status_code, 302)
        with self.c.session_transaction() as s:
            self.assertTrue(s.get("adult"))
        self.assertEqual(self.c.post("/grownup", data={"on": "0"}).status_code, 302)  # no browser headers (curl, tests)

    def test_real_browser_form_posts_work_even_though_origin_is_null(self):
        """With Referrer-Policy: no-referrer, browsers send `Origin: null` on our own same-origin forms (this broke the
        live grown-up button once). Sec-Fetch-Site says same-origin, so it must be accepted."""
        for path, data in (("/grownup", {"on": "1", "next": "/en/"}), ("/en/prefs", {"level": "Beginner", "next": "/en/"})):
            r = self.c.post(path, data=data, headers={"Origin": "null", "Sec-Fetch-Site": "same-origin"})
            self.assertEqual(r.status_code, 302, path)
        r = self.c.post("/es/feedback", data={"message": "x"}, headers={"Origin": "null", "Sec-Fetch-Site": "same-origin"})
        self.assertNotEqual(r.status_code, 403)  # reaches the form's own checks (token), which redirect with a message
        self.assertEqual(self.c.post("/grownup", data={"on": "1"}, headers={"Sec-Fetch-Site": "none"}).status_code, 302)

    def test_session_cookie_flags(self):
        r = self.c.post("/grownup", data={"on": "1"})
        cookie = r.headers["Set-Cookie"]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)
        self.assertTrue(app.config["SESSION_COOKIE_HTTPONLY"])
        self.assertEqual(app.config["SESSION_COOKIE_SAMESITE"], "Lax")

    def test_open_redirect_is_blocked(self):
        for nxt in ("//evil.example", "https://evil.example", "javascript:alert(1)"):
            r = self.c.post("/grownup", data={"on": "1", "next": nxt})
            self.assertTrue(r.headers["Location"].startswith("/") and not r.headers["Location"].startswith("//"), nxt)


class Xss(unittest.TestCase):
    PAYLOAD = '"><script>alert(1)</script><img src=x onerror=alert(2)>'

    def test_search_text_is_escaped_everywhere_it_is_shown(self):
        c = app.test_client()
        for path in ("/en/library", "/en/learn", "/es/problems", "/ar/catalogue", "/hi/kids"):
            html = c.get(path, query_string={"q": self.PAYLOAD}).get_data(as_text=True)
            self.assertNotIn("<script>alert(1)", html, path)
            self.assertNotIn("<img src=x onerror", html, path)

    def test_no_unsafe_template_or_js_sinks(self):
        for path in (ROOT / "src" / "templates").glob("*.html"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"\|\s*safe\b", path.name)
            self.assertNotIn("autoescape false", text, path.name)
        for path in (ROOT / "public" / "static").glob("*.js"):
            text = path.read_text(encoding="utf-8")
            for sink in ("outerHTML", "document.write", "insertAdjacentHTML"):
                self.assertNotIn(sink, text, (path.name, sink))
            for m in re.finditer(r"innerHTML\s*=\s*([^;]*);", text):
                self.assertEqual(m.group(1).strip(), '""', (path.name, m.group(0)))  # only used to clear a list
        for path in (ROOT / "src").glob("*.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("Markup(", text, path.name)
            self.assertNotIn("render_template_string", text, path.name)


class SecretsAndData(unittest.TestCase):
    def test_env_is_ignored_and_untracked(self):
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
        self.assertEqual([f for f in tracked if re.match(r"^\.env", f.split("/")[-1])], [])
        self.assertIn(".env", (ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_no_key_shaped_values_in_tracked_files(self):
        out = subprocess.run(["git", "grep", "-I", "-l", "-E",
                              r"eyJ[A-Za-z0-9_-]{20,}|sb_secret_[A-Za-z0-9_-]{8,}|sk-ant-[A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9]{32,}|AIza[0-9A-Za-z_-]{20,}"],
                             cwd=ROOT, capture_output=True, text=True).stdout.split()
        self.assertEqual(out, [])

    def test_service_key_is_never_read_by_the_website(self):
        for path in list((ROOT / "src").glob("*.py")) + list((ROOT / "public" / "static").glob("*.js")) + list((ROOT / "src" / "templates").glob("*.html")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("SUPABASE_SERVICE_KEY", text, path.name)
            self.assertNotIn("ANTHROPIC", text, path.name)  # the website makes no AI calls and reads no AI key
            self.assertNotIn("import anthropic", text, path.name)

    def test_no_passwords_or_trackers(self):
        for path in (ROOT / "src" / "templates").glob("*.html"):
            text = path.read_text(encoding="utf-8").lower()
            self.assertNotIn('type="password"', text, path.name)
            for tracker in ("google-analytics", "googletagmanager", "gtag(", "plausible", "hotjar", "facebook.net", "segment.com"):
                self.assertNotIn(tracker, text, (path.name, tracker))
        for path in (ROOT / "public" / "static").glob("*.js"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"navigator\.geolocation|document\.cookie\s*=", path.name)


if __name__ == "__main__":
    unittest.main()
