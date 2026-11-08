"""Supabase content store and grown-ups' feedback, with mocked HTTP (no network)."""
import json
import logging
import os
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
import content_rows  # noqa: E402
import feedback  # noqa: E402
import gate  # noqa: E402
import i18n_feedback  # noqa: E402
import store  # noqa: E402
import supabase_client  # noqa: E402
from app import LANGS, app, limiter  # noqa: E402

FILES = content_rows.local_files()
ROWS = json.loads(json.dumps(content_rows.rows_from_files(FILES)))
ENV = {"OPEN_COSMOS_TEST_REMOTE": "1", "SUPABASE_URL": "https://example.supabase.co", "SUPABASE_ANON_KEY": "anon-test-key",
       "CONTENT_SOURCE": "auto"}


class Resp:
    def __init__(self, status=200, body=None):
        self.status_code, self._body = status, body

    def json(self):
        if isinstance(self._body, Exception):
            raise self._body
        return self._body


def serving(rows):
    """A fake requests.get that pages like PostgREST."""
    def fake(url, headers=None, timeout=None, params=None):
        off, lim = params["offset"], params["limit"]
        return Resp(200, rows[off:off + lim])
    return fake


def snapshot():
    return {
        "entries": json.dumps([store.entries(s) for s in store.SIDES], sort_keys=True),
        "guides": json.dumps(store.guides(), sort_keys=True),
        "lessons": json.dumps(store.lessons(), sort_keys=True),
        "problems": json.dumps(store.problems(), sort_keys=True),
        "cat": store.category("Books", "es"),
    }


class Base(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, ENV)
        self.env.start()
        store.reset()

    def tearDown(self):
        self.env.stop()
        store.reset()


class RemoteContent(Base):
    def test_rows_rebuild_the_exact_files(self):
        rebuilt = content_rows.files_from_rows(ROWS)
        for name, data in FILES.items():
            self.assertEqual(rebuilt[name], data, name)

    def test_success_matches_json_exactly(self):
        with mock.patch.dict(os.environ, {"CONTENT_SOURCE": "json"}):
            store.reset()
            from_json = snapshot()
        store.reset()
        with mock.patch("requests.get", side_effect=serving(ROWS)) as g:
            from_remote = snapshot()
        self.assertTrue(g.called)
        self.assertEqual(from_json, from_remote)

    def test_pagination_goes_past_the_page_size(self):
        calls = []

        def fake(url, headers=None, timeout=None, params=None):
            calls.append(params["offset"])
            return serving(ROWS)(url, headers, timeout, params)

        with mock.patch("requests.get", side_effect=fake):
            self.assertEqual(len(store.entries()), len(FILES["learn.json"]) + len(FILES["build.json"]) + len(FILES["kids.json"]))
        self.assertGreater(len(ROWS), supabase_client.PAGE)
        self.assertGreaterEqual(len(calls), 3)

    def test_keys_are_sent_as_headers_only(self):
        seen = {}

        def fake(url, headers=None, timeout=None, params=None):
            seen.update(url=url, headers=headers, timeout=timeout)
            return serving(ROWS)(url, headers, timeout, params)

        with mock.patch("requests.get", side_effect=fake):
            store.entries()
        self.assertNotIn("anon-test-key", seen["url"])
        self.assertEqual(seen["headers"]["apikey"], "anon-test-key")
        self.assertEqual(seen["timeout"], 3)

    def test_cached_for_ten_minutes_then_refetched(self):
        clock = [1000.0]
        with mock.patch("store.time.time", side_effect=lambda: clock[0]), \
                mock.patch("requests.get", side_effect=serving(ROWS)) as g:
            store.entries()
            n = g.call_count
            clock[0] += 599
            store.entries()
            store.problems()
            self.assertEqual(g.call_count, n)
            clock[0] += 5
            store.entries()
            self.assertGreater(g.call_count, n)

    def test_json_mode_never_uses_the_network(self):
        with mock.patch.dict(os.environ, {"CONTENT_SOURCE": "json"}), mock.patch("requests.get") as g:
            store.reset()
            store.entries()
        g.assert_not_called()

    def test_no_keys_means_json_without_network(self):
        with mock.patch.dict(os.environ, {"SUPABASE_URL": ""}), mock.patch("requests.get") as g:
            store.reset()
            self.assertTrue(store.entries())
        g.assert_not_called()


class Fallbacks(Base):
    def check_falls_back(self, patcher):
        with mock.patch.dict(os.environ, {"CONTENT_SOURCE": "json"}):
            store.reset()
            expected = snapshot()
        store.reset()
        with patcher, self.assertLogs("open_cosmos.store", level="WARNING") as logs:
            got = snapshot()
            snapshot()  # a second use must not log again
        self.assertEqual(got, expected)
        self.assertEqual(len(logs.records), 1)
        self.assertNotIn("anon-test-key", logs.output[0])

    def test_timeout(self):
        self.check_falls_back(mock.patch("requests.get", side_effect=requests.Timeout("slow")))

    def test_connection_error(self):
        self.check_falls_back(mock.patch("requests.get", side_effect=requests.ConnectionError("down")))

    def test_http_500(self):
        self.check_falls_back(mock.patch("requests.get", return_value=Resp(500, {"message": "boom"})))

    def test_http_401(self):
        self.check_falls_back(mock.patch("requests.get", return_value=Resp(401, {})))

    def test_invalid_json(self):
        self.check_falls_back(mock.patch("requests.get", return_value=Resp(200, ValueError("not json"))))

    def test_empty_result(self):
        self.check_falls_back(mock.patch("requests.get", return_value=Resp(200, [])))

    def test_not_a_list(self):
        self.check_falls_back(mock.patch("requests.get", return_value=Resp(200, {"message": "hi"})))

    def test_malformed_rows(self):
        bad = [{"kind": "entry", "id": "x"}, {"nope": 1}, "text"]
        self.check_falls_back(mock.patch("requests.get", side_effect=serving(bad)))

    def test_schema_mismatch_missing_kind(self):
        rows = [r for r in ROWS if r["kind"] != "problem"]
        self.check_falls_back(mock.patch("requests.get", side_effect=serving(rows)))

    def test_schema_mismatch_wrong_shape(self):
        rows = json.loads(json.dumps(ROWS))
        rows[0]["data"] = {"item": "not an entry", "pos": 0, "side": "learn"}
        self.check_falls_back(mock.patch("requests.get", side_effect=serving(rows)))

    def test_retries_after_failure_window(self):
        clock = [1000.0]
        calls = iter([requests.Timeout("x"), None])

        def fake(url, headers=None, timeout=None, params=None):
            nxt = next(calls)
            if nxt:
                raise nxt
            return serving(ROWS)(url, headers, timeout, params)

        with mock.patch("store.time.time", side_effect=lambda: clock[0]), mock.patch("requests.get", side_effect=fake):
            self.assertTrue(store.entries())          # failed, bundled JSON
            clock[0] += 130
            self.assertTrue(store.entries())          # retried and succeeded


class SafetyGate(Base):
    def visible(self, adult):
        return sorted(e["id"] for e in gate.filter_visible(store.entries(), adult))

    def test_same_gate_in_both_modes(self):
        with mock.patch.dict(os.environ, {"CONTENT_SOURCE": "json"}):
            store.reset()
            a, b = self.visible(False), self.visible(True)
        store.reset()
        with mock.patch("requests.get", side_effect=serving(ROWS)):
            self.assertEqual(self.visible(False), a)
            self.assertEqual(self.visible(True), b)
            self.assertFalse(any(e["safety"] == "adult-only" for e in gate.filter_visible(store.entries(), True)))
        self.assertLess(len(a), len(b))

    def test_pages_identical_in_both_modes(self):
        paths = ["/es/learn", "/ar/kids", "/hi/problems", "/pt/lessons", "/en/guide"]

        def render():
            c = app.test_client()
            return [c.get(p).get_data(as_text=True) for p in paths]

        with mock.patch.dict(os.environ, {"CONTENT_SOURCE": "json"}):
            store.reset()
            from_json = render()
        store.reset()
        with mock.patch("requests.get", side_effect=serving(ROWS)):
            self.assertEqual(render(), from_json)


class Feedback(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {"SUPABASE_URL": "https://example.supabase.co", "SUPABASE_ANON_KEY": "anon-test-key"})
        self.env.start()
        limiter.hits.clear()
        self.c = app.test_client()

    def tearDown(self):
        self.env.stop()

    def grownup(self):
        with self.c.session_transaction() as s:
            s["adult"] = True

    def token(self, lang="es"):
        html = self.c.get(f"/{lang}/feedback?page=/es/learn").get_data(as_text=True)
        return re.search(r'name="csrf" value="([0-9a-f]+)"', html).group(1)

    def post(self, lang="es", **over):
        data = {"csrf": self.token(lang), "kind": "bug", "message": "The link on this page is broken", "page": "/es/learn", "website": ""}
        data.update(over)
        return self.c.post(f"/{lang}/feedback", data=data)

    # --- access ---
    def test_form_hidden_without_grownup_flag(self):
        for lang in LANGS:
            self.assertEqual(self.c.get(f"/{lang}/feedback").status_code, 404)
            self.assertEqual(self.c.post(f"/{lang}/feedback", data={"message": "hello there"}).status_code, 404)
        self.assertNotIn("/feedback", self.c.get("/es/").get_data(as_text=True))

    def test_form_and_link_appear_with_grownup_flag(self):
        self.grownup()
        self.assertIn("/es/feedback", self.c.get("/es/learn").get_data(as_text=True))
        html = self.c.get("/ar/feedback?page=/ar/learn").get_data(as_text=True)
        self.assertIn('name="csrf"', html)
        self.assertIn("Open Cosmos", html)
        self.assertNotRegex(html, r'name="(name|email)"')
        self.assertIn('dir="rtl"', html)

    # --- sending ---
    def test_valid_feedback_is_inserted_with_anon_key(self):
        self.grownup()
        with mock.patch("requests.post", return_value=Resp(201)) as p:
            r = self.post()
        self.assertEqual(r.status_code, 302)
        self.assertIn("status=sent", r.headers["Location"])
        args, kw = p.call_args
        self.assertTrue(args[0].endswith("/rest/v1/feedback"))
        self.assertEqual(kw["json"], {"kind": "bug", "message": "The link on this page is broken", "page": "/es/learn", "lang": "es"})
        self.assertEqual(kw["headers"]["apikey"], "anon-test-key")
        self.assertEqual(kw["timeout"], 3)

    def test_feedback_is_never_rendered_back(self):
        self.grownup()
        secret = "UNIQUE-SECRET-TEXT-12345"
        with mock.patch("requests.post", return_value=Resp(201)):
            r = self.post(message=f"{secret} please fix")
        for follow in (self.c.get(r.headers["Location"]), self.c.get("/es/feedback"), self.c.get("/es/learn")):
            body = follow.get_data(as_text=True)
            self.assertNotIn(secret, body)
            self.assertNotIn("anon-test-key", body)
        bad = self.post(kind="nope", message=f"{secret} again")  # invalid input is not echoed either
        self.assertNotIn(secret, self.c.get(bad.headers["Location"]).get_data(as_text=True))

    def test_supabase_down_is_friendly(self):
        self.grownup()
        for effect in (requests.Timeout("x"), requests.ConnectionError("x")):
            with mock.patch("requests.post", side_effect=effect):
                r = self.post()
            self.assertIn("status=down", r.headers["Location"])
            page = self.c.get(r.headers["Location"])
            self.assertEqual(page.status_code, 200)
            self.assertIn(i18n_feedback.UI["es"]["fb_down"], page.get_data(as_text=True))
        with mock.patch("requests.post", return_value=Resp(500)):
            self.assertIn("status=down", self.post().headers["Location"])

    def test_not_configured_is_friendly(self):
        self.grownup()
        with mock.patch.dict(os.environ, {"SUPABASE_URL": ""}), mock.patch("requests.post") as p:
            r = self.post()
        p.assert_not_called()
        self.assertIn("status=down", r.headers["Location"])

    # --- protection ---
    def test_honeypot_silently_drops(self):
        self.grownup()
        with mock.patch("requests.post") as p:
            r = self.post(website="http://spam.example")
        p.assert_not_called()
        self.assertIn("status=sent", r.headers["Location"])

    def test_csrf_required_and_tied_to_session(self):
        self.grownup()
        with mock.patch("requests.post") as p:
            self.token()
            for bad in ("", "wrong", "0" * 32):
                r = self.post(csrf=bad)
                self.assertIn("status=expired", r.headers["Location"])
            other = app.test_client()
            with other.session_transaction() as s:
                s["adult"] = True
            tok = re.search(r'name="csrf" value="([0-9a-f]+)"', other.get("/es/feedback").get_data(as_text=True)).group(1)
            r = self.c.post("/es/feedback", data={"csrf": tok, "kind": "bug", "message": "hello there friend", "page": "/"})
            self.assertIn("status=expired", r.headers["Location"])
        p.assert_not_called()

    def test_validation_errors(self):
        self.grownup()
        with mock.patch("requests.post") as p:
            for over in ({"kind": "hack"}, {"message": "hi"}, {"message": "x" * 1001}, {"message": "   \n\t  "}, {"kind": ""}):
                self.assertIn("status=invalid", self.post(**over).headers["Location"], over)
        p.assert_not_called()

    def test_rate_limit_five_per_hour_per_session(self):
        self.grownup()
        with mock.patch("requests.post", return_value=Resp(201)) as p:
            results = [self.post().headers["Location"] for _ in range(7)]
        self.assertEqual(sum("status=sent" in r for r in results), 5)
        self.assertTrue(all("status=rate" in r for r in results[5:]))
        self.assertEqual(p.call_count, 5)
        self.assertIn(i18n_feedback.UI["es"]["fb_rate"], self.c.get(results[6]).get_data(as_text=True))

    # --- pure functions ---
    def test_sanitising(self):
        p, err = feedback.validate("bug", "Hello\x00 wor\x07ld\r\n\tnew‮line", "/es/learn\x00?q=1", "es")
        self.assertIsNone(err)
        self.assertEqual(p["message"], "Hello world newline")
        self.assertNotRegex(p["message"], r"[\x00-\x1f\x7f-\x9f‪-‮]")
        self.assertEqual(p["page"], "/es/learn?q=1")
        self.assertEqual(feedback.clean_page("//evil.example"), "/")
        self.assertEqual(feedback.clean_page("javascript:alert(1)"), "/")
        self.assertEqual(len(feedback.clean_page("/" + "a" * 500)), 200)
        self.assertEqual(feedback.validate("bug", "x" * 1000, "/", "en")[1], None)
        self.assertEqual(feedback.validate("bug", "x" * 1001, "/", "en")[1], "invalid")
        self.assertEqual(feedback.validate("bug", "hello there", "/", "fr")[1], "invalid")

    def test_rate_limiter_window(self):
        t = [0.0]
        rl = feedback.RateLimiter(clock=lambda: t[0])
        self.assertEqual([rl.allow("a") for _ in range(6)], [True] * 5 + [False])
        self.assertTrue(rl.allow("b"))
        t[0] += 3601
        self.assertTrue(rl.allow("a"))

    def test_privacy_note_in_all_five_languages(self):
        self.assertEqual({k for k in i18n_feedback.UI}, {"es", "ar", "hi", "pt"})
        for lang, labels in i18n_feedback.UI.items():
            self.assertEqual(set(labels), set(i18n_feedback.UI_EN), lang)
            self.assertIn("Open Cosmos", labels["fb_privacy"], lang)
        self.grownup()
        for lang in LANGS:
            html = self.c.get(f"/{lang}/feedback").get_data(as_text=True)
            self.assertIn("Open Cosmos", html)
            self.assertIn((i18n_feedback.UI_EN if lang == "en" else i18n_feedback.UI[lang])["fb_privacy"][:40], html)


class Scripts(unittest.TestCase):
    def test_seed_dry_run_prints_counts_and_sends_nothing(self):
        import io
        import seed_supabase
        out = io.StringIO()
        with mock.patch("requests.post") as p, mock.patch("sys.stdout", out):
            self.assertEqual(seed_supabase.main(["--dry-run"]), 0)
        p.assert_not_called()
        self.assertIn("entry 1085", out.getvalue())

    def test_verify_compare(self):
        import verify_supabase
        self.assertEqual(verify_supabase.compare(ROWS, ROWS), [])
        changed = json.loads(json.dumps(ROWS))
        changed[3]["data"]["item"]["title"]["en"] += "!"
        diffs = verify_supabase.compare(ROWS, changed)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(verify_supabase.compare(ROWS, ROWS[:-1])[0].split(":")[0], "ui_overlay")

    def test_upsert_is_idempotent_merge(self):
        with mock.patch("requests.post", return_value=Resp(201)) as p:
            supabase_client.upsert_rows("https://x.supabase.co", "service", ROWS[:250])
        self.assertEqual(p.call_count, 3)
        self.assertEqual(p.call_args.kwargs["params"], {"on_conflict": "kind,id"})
        self.assertIn("merge-duplicates", p.call_args.kwargs["headers"]["Prefer"])


if __name__ == "__main__":
    unittest.main()
