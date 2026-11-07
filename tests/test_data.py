"""Data-contract tests. Run: python -m unittest discover -s tests -v   (pytest also works)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
sys.path.insert(0, str(ROOT / "scripts"))
import categorize  # noqa: E402

REQUIRED = ["id", "category", "tag", "title", "desc", "level", "age_group", "topic",
            "safety", "safety_reasons", "url", "source", "license"]


def entries():
    return [e for n in ("learn", "build", "kids") if (DATA / f"{n}.json").exists()
            for e in json.loads((DATA / f"{n}.json").read_text())]


def file_entries(name):
    p = DATA / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else []


class DataContract(unittest.TestCase):
    def setUp(self):
        self.entries = entries()

    def test_not_empty(self):
        self.assertGreater(len(self.entries), 0)

    def test_required_fields(self):
        for e in self.entries:
            for f in REQUIRED:
                self.assertIn(f, e, f"{e.get('id')} missing {f}")
            self.assertTrue(e["title"].get("en"), e["id"])
            self.assertIn("en", e["desc"], e["id"])

    def test_enums(self):
        for e in self.entries:
            self.assertIn(e["level"], categorize.LEVELS, e["id"])
            self.assertIn(e["age_group"], categorize.AGES, e["id"])
            self.assertIn(e["topic"], categorize.TOPICS, e["id"])
            self.assertIn(e["safety"], categorize.SAFETY, e["id"])
            self.assertIsInstance(e["safety_reasons"], list, e["id"])

    def test_no_duplicates(self):
        ids = [e["id"] for e in self.entries]
        urls = [e["url"] for e in self.entries]
        self.assertEqual(len(ids), len(set(ids)), "duplicate ids")
        self.assertEqual(len(urls), len(set(urls)), "duplicate urls")

    def test_license_and_source(self):
        for e in self.entries:
            self.assertTrue(e["license"], e["id"])
            self.assertTrue(e["source"].startswith("https://"), e["id"])

    def test_safety_reasons_consistent(self):
        for e in self.entries:
            if e["safety"] == "kid-safe":
                self.assertEqual(e["safety_reasons"], [], e["id"])
            else:
                self.assertTrue(e["safety_reasons"], f"{e['id']} is {e['safety']} with no reasons")

    def test_kid_safe_only_kid_topics(self):  # fail-closed rule
        for e in self.entries:
            if e["safety"] == "kid-safe":
                self.assertIn(e["topic"], categorize.KID_TOPICS, e["id"])

    def test_license_separation(self):  # CC BY-SA entries stay out of the CC0 files
        for name in ("learn", "build"):
            for e in file_entries(name):
                self.assertEqual(e["license"], "CC0-1.0", f"{name}: {e['id']}")
        for e in file_entries("kids"):
            self.assertEqual(e["license"], "CC-BY-SA-4.0", e["id"])
            self.assertEqual(e["source"], "https://github.com/uccser/cs-unplugged", e["id"])
            self.assertTrue(e["url"].startswith("https://www.csunplugged.org/"), e["id"])

    def test_translations_marked_ai(self):  # plan: AI translations must be labeled
        for e in self.entries:
            langs = [l for l in ("es", "ar", "hi", "pt") if l in e["title"]]
            if langs:
                self.assertEqual(sorted(e.get("ai_translated", [])), sorted(langs), e["id"])
                for l in langs:
                    self.assertTrue(e["title"][l].strip(), f"{e['id']} empty {l} title")

    def test_clean_titles(self):
        for e in self.entries:
            self.assertNotRegex(e["title"]["en"], r"[*_`]", e["id"])


class CategorizeUnits(unittest.TestCase):
    def mk(self, title, url="https://github.com/x/y", desc="", category="General"):
        return {"id": "t", "title": {"en": title}, "desc": {"en": desc}, "category": category, "tag": "", "url": url}

    def test_security_is_adult_only(self):
        r = categorize.rule_pass(self.mk("Build your own malware loader"))
        self.assertEqual(categorize.safety_from(r["adult"], r["ask"])[0], "adult-only")

    def test_from_scratch_is_not_scratch(self):
        r = categorize.rule_pass(self.mk("Build a web server from scratch"))
        self.assertNotEqual(r["age_group"], "5-7")

    def test_unknown_host_fails_closed(self):
        r = categorize.rule_pass(self.mk("Learn to make a game", url="https://random-blog.example/post"))
        self.assertNotEqual(categorize.safety_from(r["adult"], r["ask"])[0], "kid-safe")

    def test_validate_rejects_bad_values(self):
        good = {"topic": "web", "level": "Beginner", "age_group": "8-10", "safety": "kid-safe", "safety_reasons": []}
        self.assertIsNotNone(categorize.validate(good))
        self.assertIsNone(categorize.validate({**good, "safety": "safe"}))
        self.assertIsNone(categorize.validate({**good, "topic": "cooking"}))
        self.assertIsNone(categorize.validate("junk"))

    def test_ai_cannot_loosen_safety(self):
        e = self.mk("Hacking tools")
        rules = categorize.rule_pass(e)
        ai = {"topic": "web", "level": "Beginner", "age_group": "8-10", "safety": "kid-safe", "safety_reasons": []}
        categorize.apply(e, rules, ai)
        self.assertEqual(e["safety"], "adult-only")

    def test_human_override_can_loosen_and_tighten(self):
        e = self.mk("Hacking tools")
        categorize.apply(e, categorize.rule_pass(e), None)
        categorize.apply_override(e, {"safety": "ask-a-grown-up", "reason": "reviewed, ok with an adult"})
        self.assertEqual(e["safety"], "ask-a-grown-up")
        self.assertTrue(e["safety_reasons"][0].startswith("human-review"))
        categorize.apply_override(e, {"safety": "kid-safe"})
        self.assertEqual((e["safety"], e["safety_reasons"]), ("kid-safe", []))
        categorize.apply_override(e, {"safety": "adult-only", "reason": "too risky"})
        self.assertEqual(e["safety"], "adult-only")
        with self.assertRaises(ValueError):
            categorize.apply_override(e, {"safety": "nope"})


class OverridesFile(unittest.TestCase):
    def test_overrides_are_applied_and_valid(self):
        p = ROOT / "scripts" / "cache" / "safety_overrides.json"
        ov = json.loads(p.read_text())
        by_id = {e["id"]: e for e in entries()}
        for oid, o in ov.items():
            self.assertIn(oid, by_id, f"override for unknown id {oid}")
            self.assertIn(o["safety"], categorize.SAFETY)
            self.assertEqual(by_id[oid]["safety"], o["safety"], f"override for {oid} not applied; re-run categorize.py")


class RemovedLinks(unittest.TestCase):
    def test_removed_links_stay_out(self):
        removed = json.loads((ROOT / "scripts" / "cache" / "removed_links.json").read_text())
        urls = {e["url"] for e in entries()}
        self.assertFalse(urls & set(removed))


if __name__ == "__main__":
    unittest.main()
