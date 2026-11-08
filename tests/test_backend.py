"""Backend tests: store + safety gate + routes. Run: python -m unittest discover -s tests -v"""
import sys
import json
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


class GuidesAndLessonsTests(unittest.TestCase):
    """docs/GUIDE_SPEC.md, Tobi tasks 1-5."""

    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def lesson_entry(self):
        return store.get(store.lessons()[0]["entry_id"])

    def link_only(self, safety="kid-safe"):
        return next(e for e in store.entries("build") if e["safety"] == safety and e.get("reuse") == "link-only")

    def test_store_loads_guides_and_lessons(self):
        self.assertEqual(len(store.lessons()), 26)
        self.assertIn("fallback", store.guides())
        ids = {e["id"] for e in store.entries("kids")}
        for ls in store.lessons():
            self.assertIn(ls["entry_id"], ids)
            self.assertIs(store.lesson_by_id(ls["id"]), ls)
            self.assertEqual(store.get(ls["entry_id"])["lesson_id"], ls["id"])
        self.assertIsNone(self.link_only()["lesson_id"])

    def test_every_visible_entry_resolves_to_a_guide(self):
        import guide_helpers
        for e in store.entries():
            if e["safety"] in ("kid-safe", "ask-a-grown-up"):
                r = guide_helpers.guide_for(e, store.guides(), store.lessons())
                self.assertTrue(r["slides"], e["id"])

    def test_entry_page_with_lesson_in_every_language(self):
        e = self.lesson_entry()
        for lang in LANGS:
            r = self.c.get(f"/{lang}/entry/{e['id']}")
            self.assertEqual(r.status_code, 200, lang)
            html = r.get_data(as_text=True)
            self.assertIn(f"/{lang}/lesson/{e['lesson_id']}", html)
            self.assertIn('data-slide-type="what_is_it"', html)
            self.assertNotIn("{entry_title}", html)  # placeholders are filled
            self.assertNotIn("{age}", html)

    def test_link_only_entry_leaves_the_site_with_a_notice(self):
        e = self.link_only()
        html = self.c.get(f"/en/entry/{e['id']}").get_data(as_text=True)
        self.assertIn('data-slide-type="go_external"', html)
        self.assertIn("You are leaving our site", html)
        self.assertIn('rel="noopener noreferrer"', html)
        self.assertNotIn("/lesson/", html)

    def test_translated_ui_for_slide_page(self):
        e = self.link_only()
        html = self.c.get(f"/es/entry/{e['id']}").get_data(as_text=True)
        self.assertIn("Vas a salir de nuestro sitio", html)
        # Guides are translated through an overlay: the notice appears only for a guide that is not translated yet.
        from app import localize_slides
        import guide_helpers
        resolved = guide_helpers.guide_for(e, {"fallback": {}, "groups": {guide_helpers.group_of(e): {
            "slides": [{"type": "what_is_it", "title": {"en": "What is it?"}, "body": {"en": "x"}}]}}}, [])
        _, english_only, _ = localize_slides(resolved["slides"], e, None, "es")
        self.assertTrue(english_only)
        self.assertNotIn("Por ahora este texto está en inglés", html)  # this entry's guide is translated

    def test_hidden_entries_have_no_guide_page(self):
        ask = next(e for e in store.entries("build") if e["safety"] == "ask-a-grown-up")
        self.assertEqual(self.c.get(f"/en/entry/{ask['id']}").status_code, 404)
        self.c.post("/grownup", data={"on": "1"})
        r = self.c.get(f"/en/entry/{ask['id']}")
        self.assertEqual(r.status_code, 200)
        self.assertIn('data-slide-type="go_external"', r.get_data(as_text=True))

    def test_related_is_kid_safe_even_after_the_gate(self):
        self.c.post("/grownup", data={"on": "1"})
        ask = next(e for e in store.entries("build") if e["safety"] == "ask-a-grown-up")
        html = self.c.get(f"/en/entry/{ask['id']}").get_data(as_text=True)
        for e in store.entries():
            if e["safety"] != "kid-safe" and e["id"] != ask["id"]:
                self.assertNotIn(f"/entry/{e['id']}\"", html)

    def test_lessons_list_and_age_filter(self):
        r = self.c.get("/en/lessons")
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        for ls in store.lessons():
            self.assertIn(f"/en/lesson/{ls['id']}", html)
        young = self.c.get("/en/lessons?age=5-7").get_data(as_text=True)
        self.assertIn("5-7", young)
        self.assertNotIn(f"/en/lesson/{next(x for x in store.lessons() if x['age_group'] == '11-13')['id']}", young)
        for lang in LANGS:
            self.assertEqual(self.c.get(f"/{lang}/lessons").status_code, 200)

    def test_every_lesson_page_has_the_attribution_box(self):
        for ls in store.lessons():
            r = self.c.get(f"/en/lesson/{ls['id']}")
            self.assertEqual(r.status_code, 200, ls["id"])
            html = r.get_data(as_text=True)
            self.assertIn("CC BY-SA 4.0", html)
            self.assertIn(ls["source_url"], html)
            self.assertIn(ls["license_url"], html)
            self.assertIn(ls["changes_made"], html)
            self.assertIn("Original lesson, with pictures", html)

    def test_lesson_pages_in_every_language(self):
        ls = store.lessons()[0]
        for lang in LANGS:
            r = self.c.get(f"/{lang}/lesson/{ls['id']}")
            self.assertEqual(r.status_code, 200, lang)
        html = self.c.get(f"/es/lesson/{ls['id']}").get_data(as_text=True)
        self.assertNotIn("Por ahora este texto está en inglés", html)  # lessons are translated (lessons_overlay.json)
        self.assertIn("Pasos", html)

    def test_lesson_404s(self):
        self.assertEqual(self.c.get("/en/lesson/nope").status_code, 404)
        self.assertEqual(self.c.get("/xx/lesson/" + store.lessons()[0]["id"]).status_code, 404)

    def test_link_only_never_serves_lesson_content(self):
        import json
        fake = {"id": "lesson-fake", "entry_id": self.link_only()["id"], "title": {"en": "x"}, "age_group": "5-7",
                "duration_minutes": 5, "summary": {"en": "s"}, "objectives": {"en": []}, "materials": {"en": []},
                "steps": {"en": []}, "talk_about": {"en": []}, "grown_up_note": {"en": "g"}}
        store.lessons().append(fake)
        store._lesson_by_id["lesson-fake"] = fake
        try:
            self.assertEqual(self.c.get("/en/lesson/lesson-fake").status_code, 404)
            self.assertNotIn("lesson-fake", self.c.get("/en/lessons").get_data(as_text=True))
        finally:
            store.lessons().remove(fake)
            del store._lesson_by_id["lesson-fake"]

    def test_lessons_follow_the_gate(self):
        entry = self.lesson_entry()
        original = entry["safety"]
        entry["safety"] = "ask-a-grown-up"
        try:
            ls = store.lessons()[0]
            self.assertEqual(self.c.get(f"/en/lesson/{ls['id']}").status_code, 404)
            self.assertNotIn(f"/en/lesson/{ls['id']}", self.c.get("/en/lessons").get_data(as_text=True))
        finally:
            entry["safety"] = original

    def test_guide_page_says_more_is_coming_when_short(self):
        import guide
        short = None
        for age in guide.AGES:
            for goal in guide.GOALS:
                path = guide.build_path(gate_visible(), age, goal, "Beginner")
                if len(path) < guide.PATH_LEN:
                    short = (age, goal)
        if short:
            html = self.c.get(f"/en/guide?age={short[0]}&goal={short[1]}&level=Beginner").get_data(as_text=True)
            self.assertIn("More is coming", html)


def gate_visible():
    return gate.filter_visible(store.entries())


class ProblemTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def test_data_is_valid(self):
        import problems as kit
        self.assertGreaterEqual(len(store.problems()), 12)
        ids = [p["id"] for p in store.problems()]
        self.assertEqual(len(ids), len(set(ids)))
        for p in store.problems():
            self.assertEqual(kit.validate(p), [], p["id"])

    def test_reference_solutions_pass_and_starters_fail(self):
        import problems as kit
        for p in store.problems():
            if p["language"] == "javascript" and not kit.node_available():
                continue
            self.assertEqual(kit.verify(p), [], p["id"])

    def test_every_level_and_both_languages_exist(self):
        self.assertEqual({p["level"] for p in store.problems()}, {"Beginner", "Intermediate", "Advanced"})
        self.assertEqual({p["language"] for p in store.problems()}, {"python", "javascript"})

    def test_pages_in_every_language(self):
        for lang in LANGS:
            self.assertEqual(self.c.get(f"/{lang}/problems").status_code, 200, lang)
            for p in store.problems():
                self.assertEqual(self.c.get(f"/{lang}/problem/{p['id']}").status_code, 200, (lang, p["id"]))

    def test_filters(self):
        html = self.c.get("/en/problems?language=python&level=Beginner").get_data(as_text=True)
        for p in store.problems():
            shown = f"/problem/{p['id']}\"" in html
            self.assertEqual(shown, p["language"] == "python" and p["level"] == "Beginner", p["id"])
        young = self.c.get("/en/problems?age=8-10").get_data(as_text=True)
        self.assertNotIn("/problem/js-binary-search\"", young)
        self.assertEqual(self.c.get("/en/problems?language=<script>&level=zzz").status_code, 200)
        self.assertIn("/problem/py-hello\"", self.c.get("/en/problems?q=hello").get_data(as_text=True))

    def test_404s(self):
        self.assertEqual(self.c.get("/en/problem/nope").status_code, 404)
        self.assertEqual(self.c.get("/xx/problem/py-hello").status_code, 404)
        self.assertEqual(self.c.get("/api/problems/nope").status_code, 404)

    def test_page_does_not_carry_hints_or_answers(self):
        import html as htmllib
        for p in store.problems():
            page = htmllib.unescape(self.c.get(f"/en/problem/{p['id']}").get_data(as_text=True))
            for hint in p["hints"]["en"]:
                self.assertNotIn(hint, page, p["id"])
            self.assertNotIn(p["solution"].strip(), page, p["id"])
        self.assertNotIn("return n * 2", self.c.get("/en/problem/py-double").get_data(as_text=True))
    def test_api_public_view_hides_answers(self):
        r = self.c.get("/api/problems/py-evens").json
        self.assertNotIn("solution", r)
        self.assertNotIn("hints", r)
        self.assertEqual(r["hint_count"], 3)
        self.assertTrue(all("solution" not in s for s in r["guided"]))
        self.assertEqual(self.c.get("/api/problems?lang=es").json["count"], len(store.problems()))

    def test_hints_come_one_at_a_time(self):
        for n in (1, 2, 3):
            r = self.c.get(f"/api/problems/py-double/hint/{n}").json
            self.assertEqual((r["index"], r["total"]), (n, 3))
            self.assertTrue(r["hint"])
        self.assertEqual(self.c.get("/api/problems/py-double/hint/0").status_code, 404)
        self.assertEqual(self.c.get("/api/problems/py-double/hint/4").status_code, 404)

    def test_solution_and_stage_examples(self):
        r = self.c.get("/api/problems/py-double/solution").json
        self.assertIn("return n * 2", r["solution"])
        s = self.c.get("/api/problems/py-evens/solution?stage=3").json
        self.assertIn("n % 2 == 0", s["solution"])
        self.assertEqual(self.c.get("/api/problems/py-double/solution?stage=9").status_code, 404)
        self.assertEqual(self.c.get("/api/problems/py-double/solution?stage=x").status_code, 404)

    def test_config_has_what_the_runner_needs(self):
        import json, re
        html = self.c.get("/es/problem/py-double").get_data(as_text=True)
        cfg = json.loads(re.search(r'id="problem-data">(.*?)</script>', html, re.S).group(1))
        self.assertEqual((cfg["language"], cfg["lang"]), ("python", "es"))
        self.assertIn("def check", cfg["prelude"])
        self.assertTrue(cfg["tests"] and cfg["stages"])
        self.assertEqual(cfg["ui"]["p_run"], "Ejecutar")
        self.assertTrue(all(k.startswith("p_") for k in cfg["ui"]))
        self.assertNotIn("solution", cfg)

    def test_blocked_builtin_preamble(self):
        import problems as kit
        p = store.problem("py-to-binary")
        self.assertIn("def bin", p["preamble"])
        err = kit.run_reference(p, "def to_binary(n):\n    return bin(n)[2:]\n", 'check(to_binary(5), "101")')
        self.assertIn("do not use bin", err)

    def test_static_files_are_served(self):
        for name in ("runner.js", "problem.js"):
            r = self.c.get(f"/static/{name}")
            self.assertEqual(r.status_code, 200, name)
            r.close()

    def test_problem_labels_complete(self):
        import i18n_problems
        for lang, labels in i18n_problems.UI.items():
            self.assertEqual(set(labels), set(i18n_problems.UI_EN), lang)
        self.assertIn("{n}", i18n_problems.UI["hi"]["p_failed"])
        self.assertIn("{i}", i18n_problems.UI["ar"]["p_hint_n"])


class StarProgressTests(unittest.TestCase):
    """One progress system: Isabella's stars in galaxy.js (issue #26). Eren's extras kept inside it."""

    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def page(self, path):
        r = self.c.get(path)
        self.assertEqual(r.status_code, 200, path)
        return r.get_data(as_text=True)

    def test_old_system_is_gone(self):
        for path in ("/en/", "/en/lessons", "/en/me", "/en/guide?age=8-10&goal=games&level=Beginner"):
            html = self.page(path)
            self.assertNotIn("progress.js", html)
            self.assertNotIn("data-progress-", html)
        ls = store.lessons()[0]
        self.assertNotIn("data-progress-item", self.page(f"/en/lesson/{ls['id']}"))
        self.assertFalse((Path(SRC).parent / "public" / "static" / "progress.js").exists())

    def test_star_button_still_on_lesson_page(self):
        ls = store.lessons()[0]
        self.assertIn("data-explore=", self.page(f"/en/lesson/{ls['id']}"))

    def test_privacy_line_in_every_language(self):
        import json
        text = json.loads((Path(SRC) / "data" / "progress_text.json").read_text(encoding="utf-8"))
        for lang in LANGS:
            self.assertIn(text[lang]["privacy"], self.page(f"/{lang}/"))

    def test_counts_on_lessons_and_guide(self):
        html = self.page("/en/lessons")
        self.assertIn('data-count-for="#lesson-grid"', html)
        self.assertIn('id="lesson-grid"', html)
        g = self.page("/en/guide?age=8-10&goal=games&level=Beginner")
        self.assertIn('data-count-for="#route"', g)
        self.assertIn('<li data-id="', g)

    def test_me_page_has_code_storage_note_and_safe_clear(self):
        html = self.page("/es/me")
        for hook in ("data-copy-code", "data-use-code", 'id="progress-code-in"', "data-storage-note",
                     "data-clear-cancel", "data-confirm=", 'id="progress-live"'):
            self.assertIn(hook, html)

    def test_galaxy_js_has_the_kept_features(self):
        js = (Path(SRC).parent / "public" / "static" / "galaxy.js").read_text(encoding="utf-8")
        for needle in ("window.HackProgress", "markSolved", "function safeUrl", "function clean",
                       "hc_progress_v1", "MAX_ITEMS", "data-count-for"):
            self.assertIn(needle, js)
        self.assertNotIn("eval(", js)
        self.assertNotIn("fetch(", js)
class AdaptedProblemTests(unittest.TestCase):
    """Problems adapted from CS Unplugged must carry and show the CC BY-SA 4.0 credit."""

    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def adapted(self):
        return [p for p in store.problems() if p["license"] == "CC-BY-SA-4.0"]

    def test_there_are_many_and_both_languages(self):
        ids = {p["id"] for p in self.adapted()}
        self.assertGreaterEqual(len(ids), 50)
        for p in self.adapted():
            twin = ("js-" if p["language"] == "python" else "py-") + p["id"].split("-", 1)[1]
            self.assertIn(twin, ids)

    def test_every_adapted_problem_has_full_credit(self):
        for p in self.adapted():
            self.assertIn("CS Unplugged", p["attribution"], p["id"])
            self.assertTrue(p["source"].startswith("https://github.com/uccser/cs-unplugged/"), p["id"])
            self.assertEqual(p["license_url"], "https://creativecommons.org/licenses/by-sa/4.0/")
            self.assertIn("CC BY-SA 4.0", p["changes_made"])

    def test_page_shows_the_credit_box(self):
        p = self.adapted()[0]
        html = self.c.get(f"/en/problem/{p['id']}").get_data(as_text=True)
        self.assertIn('class="panel cc-box"', html)
        self.assertIn(p["source"], html)
        self.assertIn(p["license_url"], html)
        self.assertNotIn('class="panel cc-box"', self.c.get("/en/problem/py-hello").get_data(as_text=True))

    def test_python_text_uses_python_words(self):
        import re
        for p in self.adapted():
            if p["language"] == "python":
                text = p["prompt"]["en"] + " ".join(p["hints"]["en"])
                self.assertIsNone(re.search(r"\b(true|false|null)\b", text), p["id"])


class WhereFilterTests(unittest.TestCase):
    """Everything page: split "do it here" (coding problems + our lessons) from "on other sites"."""

    def setUp(self):
        app.config["TESTING"] = True
        self.c = app.test_client()

    def page(self, path):
        r = self.c.get(path)
        self.assertEqual(r.status_code, 200, path)
        return r.get_data(as_text=True)

    def test_site_shows_problems_and_lesson_entries_only(self):
        import re
        html = self.page("/en/library?where=site")
        for p in store.problems():
            self.assertIn(f"/en/problem/{p['id']}", html)
        for eid in re.findall(r'/en/entry/([a-z]+-[0-9a-f]{8})', html):
            self.assertTrue(store.get(eid)["lesson_id"], eid)

    def test_external_has_no_problems_and_no_lesson_entries(self):
        import re
        html = self.page("/en/library?where=external")
        self.assertNotIn("/en/problem/", html)
        ids = re.findall(r'/en/entry/([a-z]+-[0-9a-f]{8})', html)
        self.assertTrue(ids)
        for eid in ids:
            self.assertIsNone(store.get(eid)["lesson_id"], eid)

    def test_counts_add_up(self):
        import re
        html = self.page("/en/library")
        site = int(re.search(r"Do it here \((\d+)\)", html).group(1))
        ext = int(re.search(r"On other sites \((\d+)\)", html).group(1))
        visible_lessons = sum(1 for ls in store.lessons() if store.get(ls["entry_id"])["safety"] == "kid-safe")
        self.assertEqual(site, len(store.problems()) + visible_lessons)
        self.assertGreater(ext, 0)

    def test_search_works_inside_each_group(self):
        html = self.page("/en/library?where=site&q=binary")
        self.assertIn("/en/problem/py-to-binary", html)
        self.assertIn("/en/problem/js-binary-search", html)
        self.assertNotIn("/en/problem/py-hello", html)

    def test_bad_value_and_every_language(self):
        self.assertIn("/en/problem/", self.page("/en/library?where=<script>"))
        for lang in LANGS:
            self.page(f"/{lang}/library?where=site")
            self.page(f"/{lang}/library?where=external")

    def test_other_galaxy_hides_problems(self):
        self.assertNotIn("/en/problem/", self.page("/en/library?g=art"))


class TranslationParityTests(unittest.TestCase):
    def test_ui_labels_complete(self):
        import i18n_guides
        import i18n_lessons
        for mod in (i18n_guides, i18n_lessons):
            for lang, labels in mod.UI.items():
                self.assertEqual(set(labels), set(mod.UI_EN), (mod.__name__, lang))
        self.assertIn("{n}", i18n_guides.UI["ar"]["more"])
        self.assertIn("{n}", i18n_lessons.UI["hi"]["lesson_minutes"])
        self.assertIn("{i}", i18n_lessons.UI["pt"]["slide_n"])

    def test_guides_match_english_shape(self):
        import delivery
        for kind in delivery.GUIDES:
            en = delivery.guide_for(kind, "en")
            for lang in ("es", "ar", "hi", "pt"):
                g = delivery.guide_for(kind, lang)
                self.assertTrue(g["translated"], (kind, lang))
                for field in ("steps", "accessibility", "safety"):
                    self.assertEqual(len(g[field]), len(en[field]), (kind, lang, field))
                self.assertEqual(list(g["by_level"]), list(en["by_level"]))
                for lvl in en["by_level"]:
                    self.assertEqual(len(g["by_level"][lvl]), len(en["by_level"][lvl]), (kind, lang, lvl))

    def test_unknown_language_falls_back_to_english(self):
        import delivery
        g = delivery.guide_for("video", "xx")
        self.assertFalse(g["translated"])
        self.assertEqual(g["title"], delivery.GUIDES["video"]["title"])

    def test_howto_pages_in_every_language(self):
        c = app.test_client()
        for lang in LANGS:
            for kind in ("video", "repo", "article", "document"):
                self.assertIn(f'lang="{lang}"', c.get(f"/{lang}/howto/{kind}").get_data(as_text=True))
        self.assertIn("IA", c.get("/es/howto/video").get_data(as_text=True))

    def test_youtube_shortcut_is_right(self):
        import delivery
        steps = " ".join(delivery.GUIDES["video"]["steps"])
        self.assertIn("J to go back 10 seconds", steps)


class GuideTests(unittest.TestCase):
    def setUp(self):
        import os

    def test_all_36_combos(self):
        import guide
        order = guide.AGE_ORDER
        for age in guide.AGES:
            for goal in guide.GOALS:
                for level in guide.LEVELS:
                    path = guide.build_path(store.entries(), age, goal, level)
                    self.assertGreater(len(path), 0, (age, goal, level))  # never empty
                    self.assertLessEqual(len(path), guide.PATH_LEN, (age, goal, level))
                    if order.index(age) <= 1:  # ages 5-10: Beginner only
                        self.assertTrue(all(e["level"] == "Beginner" for e in path), (age, goal, level))
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
