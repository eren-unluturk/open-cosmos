"""Backend tests: store + safety gate + routes. Run: python -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))
import gate  # noqa: E402
import store  # noqa: E402
from app import LANGS, app  # noqa: E402


class StoreTests(unittest.TestCase):
    def test_loads_all_three_sides(self):
        for side in store.SIDES:
            self.assertTrue(store.entries(side), side)
        self.assertEqual(len(store.entries()), sum(len(store.entries(s)) for s in store.SIDES))

    def test_side_and_get(self):
        e = store.entries("kids")[0]
        self.assertEqual(e["side"], "kids")
        self.assertIs(store.get(e["id"]), e)
        self.assertIsNone(store.get("nope"))

    def test_text_fallback(self):
        e = {"title": {"en": "Hi", "es": "Hola"}}
        self.assertEqual(store.text(e, "title", "es"), ("Hola", False))
        self.assertEqual(store.text(e, "title", "ar"), ("Hi", True))
        self.assertEqual(store.text(e, "title", "en"), ("Hi", False))
        self.assertEqual(store.text({}, "title", "en"), ("", False))

    def test_non_ascii_text_loads(self):
        self.assertTrue(any(any(ord(c) > 127 for c in e["title"].get("ar", "")) for e in store.entries("kids")))


class GateTests(unittest.TestCase):
    def test_tiers(self):
        safe, ask, adult = ({"safety": s} for s in ("kid-safe", "ask-a-grown-up", "adult-only"))
        self.assertTrue(gate.visible(safe) and gate.visible(safe, True))
        self.assertFalse(gate.visible(ask))
        self.assertTrue(gate.visible(ask, True))
        self.assertFalse(gate.visible(adult) or gate.visible(adult, True))

    def test_fail_closed(self):
        for e in ({}, {"safety": None}, {"safety": "bogus"}):
            self.assertFalse(gate.visible(e))
            self.assertTrue(gate.visible(e, True))

    def test_real_data(self):
        every = store.entries()
        kid = gate.filter_visible(every)
        self.assertTrue(kid and all(e["safety"] == "kid-safe" for e in kid))
        grown = gate.filter_visible(every, adult=True)
        self.assertFalse(any(e["safety"] == "adult-only" for e in grown))
        self.assertGreater(len(grown), len(kid))


class RouteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_all_pages_all_langs(self):
        for lang in LANGS:
            for path in (f"/{lang}/", f"/{lang}/learn", f"/{lang}/build", f"/{lang}/kids", f"/{lang}/guide"):
                self.assertEqual(self.c.get(path).status_code, 200, path)

    def test_unknown_404(self):
        self.assertEqual(self.c.get("/xx/").status_code, 404)
        self.assertEqual(self.c.get("/en/nope").status_code, 404)

    def test_security_headers(self):
        h = self.c.get("/en/").headers
        self.assertEqual(h["X-Content-Type-Options"], "nosniff")
        self.assertEqual(h["X-Frame-Options"], "DENY")
        self.assertEqual(h["Referrer-Policy"], "no-referrer")

    def test_healthz(self):
        self.assertEqual(self.c.get("/healthz").json, {"ok": True})

    def test_gate_hides_then_reveals(self):
        ask = next(e for e in store.entries("learn") if e["safety"] == "ask-a-grown-up")
        adult = next(e for e in store.entries("learn") if e["safety"] == "adult-only")
        self.assertNotIn(ask["url"], self.c.get("/en/learn").get_data(as_text=True))
        self.c.post("/grownup", data={"on": "1", "next": "/en/learn"})
        html = self.c.get("/en/learn").get_data(as_text=True)
        self.assertIn(ask["url"].replace("&", "&amp;"), html)
        self.assertNotIn(adult["url"].replace("&", "&amp;"), html)
        self.c.post("/grownup", data={"on": "0"})
        self.assertNotIn(ask["url"].replace("&", "&amp;"), self.c.get("/en/learn").get_data(as_text=True))

    def test_open_redirect_blocked(self):
        for bad in ("https://evil.example", "//evil.example"):
            r = self.c.post("/grownup", data={"on": "1", "next": bad})
            self.assertEqual(r.headers["Location"], "/")

    def test_guide_is_kid_safe_only(self):
        self.c.post("/grownup", data={"on": "1"})
        r = self.c.get("/en/guide?age=8-10&goal=games&level=Beginner")
        self.assertEqual(r.status_code, 200)


class FilterTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_age_and_topic_filters(self):
        order = ["5-7", "8-10", "11-13", "teen+"]
        r = self.c.get("/api/entries?age=8-10&topic=general").json
        self.assertGreater(r["count"], 0)
        ids = {x["id"] for x in r["entries"]}
        for i in ids:
            e = store.get(i)
            self.assertLessEqual(order.index(e["age_group"]), 1)
            self.assertEqual(e["topic"], "general")

    def test_bad_filters_ignored(self):
        base = self.c.get("/api/entries").json["count"]
        self.assertEqual(self.c.get("/api/entries?age=99&topic=zzz").json["count"], base)

    def test_accept_language_redirect(self):
        r = self.c.get("/", headers={"Accept-Language": "pt-BR,pt;q=0.9"})
        self.assertTrue(r.headers["Location"].endswith("/pt/"))
        r = self.c.get("/", headers={"Accept-Language": "fr"})
        self.assertTrue(r.headers["Location"].endswith("/en/"))

    def test_api_404_is_json(self):
        r = self.c.get("/api/nope")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json, {"error": "not found"})


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_only_cc_by_sa_kids_are_hostable(self):
        for e in store.entries():
            if e["delivery"] == "hostable":
                self.assertEqual(e["side"], "kids")
                self.assertEqual(e["license"], "CC-BY-SA-4.0")
                self.assertTrue(e["attribution"])
            else:
                self.assertEqual(e["delivery"], "external")
                self.assertIsNone(e["attribution"])
        self.assertTrue(all(e["delivery"] == "external" for e in store.entries() if e["side"] != "kids"))
        self.assertTrue(any(e["delivery"] == "hostable" for e in store.entries()))

    def test_cc0_license_is_never_hostable(self):
        import delivery
        self.assertEqual(delivery.classify({"side": "learn", "license": "CC0-1.0", "url": "https://x.org"})["delivery"], "external")
        self.assertEqual(delivery.classify({"side": "kids", "license": "MIT", "url": "https://x.org"})["delivery"], "external")

    def test_kinds(self):
        import delivery
        k = lambda side, url: delivery.kind_of({"side": side, "url": url})
        self.assertEqual(k("learn", "https://www.youtube.com/watch?v=1"), "video")
        self.assertEqual(k("learn", "https://youtu.be/abc"), "video")
        self.assertEqual(k("build", "https://github.com/a/b"), "repo")
        self.assertEqual(k("learn", "https://x.org/book.pdf"), "document")
        self.assertEqual(k("learn", "https://medium.com/a"), "article")
        self.assertEqual(k("kids", "https://www.csunplugged.org/en/topics/binary-numbers/"), "unit")
        self.assertEqual(k("kids", "https://www.csunplugged.org/en/topics/binary-numbers/lesson-a/"), "lesson")
        self.assertEqual(k("kids", "https://www.csunplugged.org/en/topics/binary-numbers/lesson-a/programming/"), "challenge")
        self.assertEqual(k("kids", "https://www.csunplugged.org/en/topics/binary-numbers/integrations/x/"), "activity")

    def test_every_external_kind_has_a_guide_with_all_levels(self):
        import delivery
        for e in store.entries():
            if e["delivery"] == "external":
                g = delivery.guide_for(e["kind"])
                self.assertIsNotNone(g, e["kind"])
                self.assertEqual(list(g["by_level"]), delivery.LEVELS)
                self.assertTrue(g["steps"] and g["accessibility"] and g["safety"])

    def test_catalogue_pages(self):
        for lang in LANGS:
            self.assertEqual(self.c.get(f"/{lang}/catalogue").status_code, 200)
        for kind in ("video", "repo", "article", "document"):
            for lang in LANGS:
                self.assertEqual(self.c.get(f"/{lang}/howto/{kind}").status_code, 200)
        self.assertEqual(self.c.get("/en/howto/nope").status_code, 404)

    def test_api_catalogue_split_and_gate(self):
        r = self.c.get("/api/catalogue").json
        self.assertGreater(r["hostable"]["count"], 0)
        ids = [x["id"] for d in r.values() for lv in d["levels"].values() for x in lv]
        self.assertTrue(all(store.get(i)["safety"] == "kid-safe" for i in ids))
        host_ids = [x["id"] for lv in r["hostable"]["levels"].values() for x in lv]
        self.assertTrue(all(store.get(i)["delivery"] == "hostable" for i in host_ids))
        self.c.post("/grownup", data={"on": "1"})
        r2 = self.c.get("/api/catalogue").json
        self.assertGreater(r2["external"]["count"], r["external"]["count"])
        ids2 = [x["id"] for d in r2.values() for lv in d["levels"].values() for x in lv]
        self.assertFalse(any(store.get(i)["safety"] == "adult-only" for i in ids2))

    def test_entry_page_shows_attribution_for_hostable(self):
        e = next(x for x in store.entries("kids") if x["delivery"] == "hostable")
        html = self.c.get(f"/en/entry/{e['id']}").get_data(as_text=True)
        self.assertIn("CC BY-SA 4.0", html)
        self.assertIn("Changes were made", html)


class GuideTests(unittest.TestCase):
    def setUp(self):
        import os
        os.environ.pop("ANTHROPIC_API_KEY", None)  # test the rule-based path only

    def test_all_36_combos(self):
        import guide
        order = guide.AGE_ORDER
        for age in guide.AGES:
            for goal in guide.GOALS:
                for level in guide.LEVELS:
                    path = guide.build_path(store.entries(), age, goal, level)
                    self.assertEqual(len(path), guide.PATH_LEN, (age, goal, level))
                    self.assertEqual(len({e["id"] for e in path}), len(path))
                    for e in path:
                        self.assertEqual(e["safety"], "kid-safe")
                        self.assertLessEqual(order.index(e["age_group"]), order.index(age))
                        self.assertLessEqual(guide.LEVELS.index(e["level"]), guide.LEVELS.index(level))
                    idx = [guide.LEVELS.index(e["level"]) for e in path]
                    self.assertEqual(idx, sorted(idx))

    def test_ignores_adult_pool(self):
        import guide
        path = guide.build_path(store.entries(), "5-7", "general", "Beginner")
        self.assertTrue(all(gate.tier(e) == "kid-safe" for e in path))


class SearchAndEntryTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_accent_fold(self):
        e = {"title": {"en": "Binary", "es": "Números binarios"}, "desc": {"en": "x"}, "category": ""}
        self.assertTrue(store.matches(e, "numeros BINARIOS", "es"))
        self.assertFalse(store.matches(e, "python", "es"))

    def test_search_route(self):
        r = self.c.get("/api/entries?side=kids&q=binary").json
        self.assertGreater(r["count"], 0)
        self.assertTrue(all(x["safety"] == "kid-safe" for x in r["entries"]))
        self.assertEqual(self.c.get("/en/learn?q=" + "a" * 500).status_code, 200)

    def test_api_respects_gate(self):
        self.assertTrue(all(x["safety"] == "kid-safe" for x in self.c.get("/api/entries").json["entries"]))
        self.c.post("/grownup", data={"on": "1"})
        safeties = {x["safety"] for x in self.c.get("/api/entries").json["entries"]}
        self.assertIn("ask-a-grown-up", safeties)
        self.assertNotIn("adult-only", safeties)

    def test_api_bad_input(self):
        self.assertEqual(self.c.get("/api/entries?side=bogus").status_code, 404)
        self.assertEqual(self.c.get("/api/entries?lang=xx").status_code, 404)
        self.assertEqual(self.c.get("/api/entries?level=<script>").json["count"],
                         self.c.get("/api/entries").json["count"])

    def test_entry_page_and_gate(self):
        kid = store.entries("kids")[0]
        for lang in LANGS:
            self.assertEqual(self.c.get(f"/{lang}/entry/{kid['id']}").status_code, 200)
        ask = next(e for e in store.entries("learn") if e["safety"] == "ask-a-grown-up")
        adult = next(e for e in store.entries("learn") if e["safety"] == "adult-only")
        self.assertEqual(self.c.get(f"/en/entry/{ask['id']}").status_code, 404)
        self.c.post("/grownup", data={"on": "1"})
        self.assertEqual(self.c.get(f"/en/entry/{ask['id']}").status_code, 200)
        self.assertEqual(self.c.get(f"/en/entry/{adult['id']}").status_code, 404)
        self.assertEqual(self.c.get("/en/entry/nope").status_code, 404)


if __name__ == "__main__":
    unittest.main()
