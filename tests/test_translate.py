"""translate.py helpers (no API calls): fenced JSON, retry, kid-safe-first ordering, 5 workers."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import translate  # noqa: E402

GOOD = '{"level": "Beginner", "age_group": "8-10", "translations": {"es": {"title": "a", "desc": "b"}}}'


class ParseReply(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(translate.parse_json_reply(GOOD)["level"], "Beginner")

    def test_code_fenced_json_does_not_crash(self):
        for wrapped in ("```json\n" + GOOD + "\n```", "```\n" + GOOD + "\n```", "  ```JSON\n" + GOOD + "```  "):
            self.assertEqual(translate.parse_json_reply(wrapped)["age_group"], "8-10")

    def test_prose_around_json(self):
        self.assertEqual(translate.parse_json_reply("Here you go:\n" + GOOD + "\nHope that helps")["level"], "Beginner")

    def test_garbage_raises_valueerror(self):
        for bad in ("", "no json here", "{not json}"):
            with self.assertRaises(ValueError):
                translate.parse_json_reply(bad)


class Retry(unittest.TestCase):
    def test_retries_once_on_a_parse_error(self):
        calls = []

        def ask(entry):
            calls.append(1)
            return "oops" if len(calls) == 1 else GOOD
        out = translate.translate_entry(ask, {"title": {"en": "t"}, "desc": {"en": "d"}})
        self.assertEqual(len(calls), 2)
        self.assertEqual(out["level"], "Beginner")

    def test_gives_up_after_one_retry(self):
        calls = []

        def ask(entry):
            calls.append(1)
            return "oops"
        with self.assertRaises(ValueError):
            translate.translate_entry(ask, {"title": {"en": "t"}, "desc": {"en": "d"}})
        self.assertEqual(len(calls), 2)


class Setup(unittest.TestCase):
    def test_five_workers(self):
        self.assertEqual(translate.WORKERS, 5)

    def test_apply_keeps_level_and_age_and_labels_ai(self):
        e = {"title": {"en": "t"}, "desc": {"en": "d"}, "level": "Advanced", "age_group": "teen+"}
        translate.apply_result(e, translate.parse_json_reply(GOOD))
        self.assertEqual((e["level"], e["age_group"]), ("Advanced", "teen+"))
        self.assertEqual(e["title"]["es"], "a")
        self.assertEqual(e["ai_translated"], ["es"])

    def test_todo_is_kid_safe_first_and_skips_done(self):
        mk = lambda i, safety, level, done=False: {  # noqa: E731
            "id": f"learn-{i}", "safety": safety, "level": level, "age_group": "8-10",
            "title": {"en": "t", **({l: "x" for l in translate.LANGS} if done else {})}}
        es = [mk("a", "ask-a-grown-up", "Beginner"), mk("b", "kid-safe", "Intermediate"),
              mk("c", "kid-safe", "Beginner"), mk("d", "kid-safe", "Beginner", done=True)]
        ids = [e["id"] for e in translate.pick_todo(es)]
        self.assertEqual(ids, ["learn-c", "learn-b"])
        self.assertEqual(len(translate.pick_todo(es, include_all=True)), 3)

    def test_model_name_is_current(self):
        self.assertEqual(translate.MODEL, "claude-haiku-5-5")


if __name__ == "__main__":
    unittest.main()
