"""Coding problems adapted from CS Unplugged programming challenges (CC BY-SA 4.0).

Source: the programming challenges in uccser/cs-unplugged (csunplugged/topics/content/en/*/programming-challenges/).
Licence: that content is CC BY-SA 4.0 (LICENCE-CONTENT in the repo). So these adapted problems are ALSO
CC BY-SA 4.0: every one carries the attribution, a link to the original challenge, the licence link and a
"changes were made" note, and the problem page shows them. Keep it that way if you edit this file.

What we changed: the originals ask a program to read input and print a sentence. We rewrote each one in our own
words as a function that returns a value, with our own tests, hints and guided steps, and in Python and JavaScript.
No long passages are copied.

Each entry below makes TWO problems (py-<slug> and js-<slug>) from one shared set of test cases.
Run  python scripts/build_problems.py  after editing: it proves every solution passes and every starter fails.
"""
import json
import re

LICENSE = "CC-BY-SA-4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
REPO = "https://github.com/uccser/cs-unplugged/tree/develop/csunplugged/topics/content/en/{topic}/programming-challenges/{name}"
ATTRIBUTION = ("Adapted from a CS Unplugged programming challenge by the University of Canterbury "
               "Computer Science Education Research Group, licensed CC BY-SA 4.0.")
CHANGES = ("Rewritten in our own words as a function with tests, hints and steps, in Python and JavaScript, "
           "by Hackcessability. This version is also CC BY-SA 4.0.")


def T(s):
    return {"en": s}


def lit(value, language):
    """A value written as code in one language."""
    return repr(value) if language == "python" else json.dumps(value)


def make_tests(language, fn, cases):
    tests = []
    for args, expected in cases:
        call = f"{fn}({', '.join(lit(a, language) for a in args)})"
        exp = lit(expected, language)
        code = f"check({call}, {exp})" if language == "python" else f"assertEqual({call}, {exp})"
        tests.append({"name": T(f"{call} gives {exp}"), "code": code})
    return tests


def starter(language, fn, params, todo):
    if language == "python":
        return f"def {fn}({params}):\n    # {todo}\n    pass\n"
    return f"function {fn}({params}) {{\n  // {todo}\n}}\n"


def py_words(text, language):
    """Python writes True, False and None with capitals."""
    if language != "python":
        return text
    text = text.replace("null (None in Python)", "None")
    for js, py in (("true", "True"), ("false", "False"), ("null", "None")):
        text = re.sub(rf"\b{js}\b", py, text)
    return text


def build(spec):
    """Turn one shared spec into a Python problem and a JavaScript problem."""
    out = []
    for language, prefix in (("python", "py"), ("javascript", "js")):
        side = spec[language]
        fn = side["fn"]
        first = starter(language, fn, side["params"], spec["todo"])
        guided = []
        for i, st in enumerate(spec.get("stages", [])):
            stage = {"goal": T(py_words(st["goal"], language)), "explain": T(py_words(st["explain"], language)),
                     "solution": st[language], "tests": make_tests(language, fn, st["cases"])}
            if i == 0:
                stage["starter"] = first
            guided.append(stage)
        out.append({
            "id": f"{prefix}-{spec['slug']}", "language": language, "level": spec["level"],
            "age_group": spec["age"], "topic": "general",
            "title": T(spec["title"]), "prompt": T(py_words(spec["prompt"].replace("FN", fn), language)),
            "concepts": T(spec["concepts"]), "starter": first,
            "tests": make_tests(language, fn, spec["cases"]) + side.get("extra_tests", []),
            "hints": T([py_words(h, language) for h in (spec[f"hints_{prefix}"] if f"hints_{prefix}" in spec else spec["hints"])]),
            "guided": guided, "solution": side["solution"], "solution_note": T(spec["note"]),
            "license": LICENSE, "source": REPO.format(topic=spec["topic"], name=spec["name"]),
            "attribution": ATTRIBUTION, "license_url": LICENSE_URL, "changes_made": CHANGES,
        })
    return out


SPECS = [
    # ---------------------------------------------------------------- binary numbers
    {
        "slug": "card-values", "topic": "binary-numbers", "name": "dots-right-left",
        "level": "Beginner", "age": "8-10", "title": "Binary card values",
        "prompt": "Binary cards have 1, 2, 4, 8 ... dots. Each card has double the dots of the one before. "
                  "Write a function FN(count) that gives back a list of the dots on the first count cards, smallest first.",
        "concepts": ["lists", "loops", "doubling"], "todo": "give back a list like [1, 2, 4, 8]",
        "cases": [((4,), [1, 2, 4, 8]), ((1,), [1]), ((8,), [1, 2, 4, 8, 16, 32, 64, 128]), ((0,), [])],
        "hints": ["Start with an empty list and a value of 1.",
                  "Repeat count times: add the value to the list.",
                  "After adding it, double the value (value times 2)."],
        "stages": [{"goal": "Add the number 1 to the list count times.",
                    "explain": "Make an empty list. Loop count times and add 1 each time.",
                    "cases": [((3,), [1, 1, 1])],
                    "python": "def card_values(count):\n    cards = []\n    for i in range(count):\n        cards.append(1)\n    return cards\n",
                    "javascript": "function cardValues(count) {\n  const cards = [];\n  for (let i = 0; i < count; i++) {\n    cards.push(1);\n  }\n  return cards;\n}\n"}],
        "note": "Doubling the value each time gives the binary card values: 1, 2, 4, 8, 16 ...",
        "python": {"fn": "card_values", "params": "count",
                   "solution": "def card_values(count):\n    cards = []\n    value = 1\n    for i in range(count):\n        cards.append(value)\n        value = value * 2\n    return cards\n"},
        "javascript": {"fn": "cardValues", "params": "count",
                       "solution": "function cardValues(count) {\n  const cards = [];\n  let value = 1;\n  for (let i = 0; i < count; i++) {\n    cards.push(value);\n    value = value * 2;\n  }\n  return cards;\n}\n"},
    },
    {
        "slug": "cards-from-largest", "topic": "binary-numbers", "name": "left-right-given-largest",
        "level": "Beginner", "age": "8-10", "title": "Cards from the biggest down",
        "prompt": "Write a function FN(largest). It gives back the binary card values from largest down to 1. "
                  "Example: 8 gives [8, 4, 2, 1]. You can trust that largest is 1, 2, 4, 8, 16 and so on.",
        "concepts": ["lists", "while loops", "halving"], "todo": "give back a list like [8, 4, 2, 1]",
        "cases": [((64,), [64, 32, 16, 8, 4, 2, 1]), ((8,), [8, 4, 2, 1]), ((1,), [1]), ((16,), [16, 8, 4, 2, 1])],
        "hints": ["Each card has half the dots of the card before it.",
                  "Keep going while the value is at least 1.",
                  "Add the value to the list, then halve it with whole-number division."],
        "hints_js": ["Each card has half the dots of the card before it.",
                     "Keep going while the value is at least 1.",
                     "Add the value to the list, then halve it with Math.floor(value / 2)."],
        "note": "Halving until you reach 1 lists every card from the biggest down.",
        "python": {"fn": "cards_from_largest", "params": "largest",
                   "solution": "def cards_from_largest(largest):\n    cards = []\n    value = largest\n    while value >= 1:\n        cards.append(value)\n        value = value // 2\n    return cards\n"},
        "javascript": {"fn": "cardsFromLargest", "params": "largest",
                       "solution": "function cardsFromLargest(largest) {\n  const cards = [];\n  let value = largest;\n  while (value >= 1) {\n    cards.push(value);\n    value = Math.floor(value / 2);\n  }\n  return cards;\n}\n"},
    },
    {
        "slug": "bits-needed", "topic": "binary-numbers", "name": "number-bits-representing-number",
        "level": "Beginner", "age": "11-13", "title": "How many cards do I need?",
        "prompt": "Write a function FN(n). It gives back how many binary cards (bits) you need to show the number n. "
                  "n is 1 or more. Example: 5 needs 3 cards (4, 2 and 1).",
        "concepts": ["while loops", "doubling", "counting"], "todo": "give back how many cards are needed",
        "cases": [((5,), 3), ((31,), 5), ((32,), 6), ((1,), 1), ((255,), 8), ((256,), 9)],
        "hints": ["The cards are 1, 2, 4, 8 ... and each new card doubles the biggest one.",
                  "Start with one card worth 1. Count it.",
                  "While the next card (double the biggest) is not more than n, add that card and count it."],
        "note": "You keep adding cards while the next card still fits under n.",
        "python": {"fn": "bits_needed", "params": "n",
                   "solution": "def bits_needed(n):\n    count = 1\n    biggest = 1\n    while biggest * 2 <= n:\n        biggest = biggest * 2\n        count += 1\n    return count\n"},
        "javascript": {"fn": "bitsNeeded", "params": "n",
                       "solution": "function bitsNeeded(n) {\n  let count = 1;\n  let biggest = 1;\n  while (biggest * 2 <= n) {\n    biggest = biggest * 2;\n    count++;\n  }\n  return count;\n}\n"},
    },
    {
        "slug": "binary-cards", "topic": "binary-numbers", "name": "binary-cards-representing-number",
        "level": "Intermediate", "age": "11-13", "title": "Show a number with five cards",
        "prompt": "Five binary cards have 16, 8, 4, 2 and 1 dots. A card is either showing its dots (W, white) or turned over (B, black). "
                  "Write a function FN(n) for a number from 0 to 31. It gives back five letters for the cards, biggest first. "
                  "Example: 11 is 8 + 2 + 1, so it gives \"BWBWW\".",
        "concepts": ["binary numbers", "loops", "if / else", "building text"], "todo": "give back five letters, like BWBWW",
        "cases": [((11,), "BWBWW"), ((31,), "WWWWW"), ((0,), "BBBBB"), ((16,), "WBBBB"), ((1,), "BBBBW"), ((20,), "WBWBB")],
        "hints": ["Look at the cards from the biggest (16) to the smallest (1).",
                  "If what is left of n is at least as big as the card, the card shows (W) and you take its dots away.",
                  "Otherwise the card is turned over (B). Add one letter for every card."],
        "stages": [{"goal": "Look at the 16 card only.",
                    "explain": "Give back \"W\" if n is 16 or more, and \"B\" if not.",
                    "cases": [((20,), "W"), ((3,), "B")],
                    "python": "def binary_cards(n):\n    if n >= 16:\n        return \"W\"\n    return \"B\"\n",
                    "javascript": "function binaryCards(n) {\n  if (n >= 16) return \"W\";\n  return \"B\";\n}\n"}],
        "note": "Going from the biggest card down, each card is used once if it fits. That is binary.",
        "python": {"fn": "binary_cards", "params": "n",
                   "solution": "def binary_cards(n):\n    result = \"\"\n    for card in [16, 8, 4, 2, 1]:\n        if n >= card:\n            result += \"W\"\n            n -= card\n        else:\n            result += \"B\"\n    return result\n"},
        "javascript": {"fn": "binaryCards", "params": "n",
                       "solution": "function binaryCards(n) {\n  let result = \"\";\n  for (const card of [16, 8, 4, 2, 1]) {\n    if (n >= card) {\n      result += \"W\";\n      n -= card;\n    } else {\n      result += \"B\";\n    }\n  }\n  return result;\n}\n"},
    },
    {
        "slug": "count-dots", "topic": "binary-numbers", "name": "count-bw-one-input-using-loop",
        "level": "Intermediate", "age": "11-13", "title": "Count the dots on the cards",
        "prompt": "A row of binary cards is written as letters: W means the card shows its dots, B means it is turned over. "
                  "The last card is worth 1, the one before it 2, then 4, and so on. "
                  "Write a function FN(cards) that gives back the number the row shows. Example: \"WBB\" is 4.",
        "concepts": ["binary to decimal", "loops", "doubling"], "todo": "give back the number the cards show",
        "cases": [(("WBB",), 4), (("W",), 1), (("B",), 0), (("WWWWW",), 31), (("BWBWW",), 11), (("",), 0)],
        "hints": ["Start with a total of 0.",
                  "Go through the letters from left to right. Each step, double the total.",
                  "After doubling, add 1 if the letter is W. B adds nothing."],
        "stages": [{"goal": "Count the W cards.",
                    "explain": "Loop over the letters and add 1 for every W. This is not the final answer yet.",
                    "cases": [(("WBW",), 2)],
                    "python": "def count_dots(cards):\n    total = 0\n    for card in cards:\n        if card == \"W\":\n            total += 1\n    return total\n",
                    "javascript": "function countDots(cards) {\n  let total = 0;\n  for (const card of cards) {\n    if (card === \"W\") total += 1;\n  }\n  return total;\n}\n"}],
        "note": "Doubling before each new card moves every earlier card one place to the left, so it is worth twice as much.",
        "python": {"fn": "count_dots", "params": "cards",
                   "solution": "def count_dots(cards):\n    total = 0\n    for card in cards:\n        total = total * 2\n        if card == \"W\":\n            total += 1\n    return total\n"},
        "javascript": {"fn": "countDots", "params": "cards",
                       "solution": "function countDots(cards) {\n  let total = 0;\n  for (const card of cards) {\n    total = total * 2;\n    if (card === \"W\") total += 1;\n  }\n  return total;\n}\n"},
    },
    # ---------------------------------------------------------------- error detection
    {
        "slug": "parity-row", "topic": "error-detection-and-correction", "name": "detect-parity-error-in-row",
        "level": "Beginner", "age": "11-13", "title": "Spot a parity error in a row",
        "prompt": "In the parity magic trick, every row should have an EVEN number of black cards. "
                  "Write a function FN(row). row is made of B (black) and W (white). "
                  "Give back true if the row has an error (an odd number of B), and false if it is fine.",
        "concepts": ["counting", "remainder (%)", "true and false"], "todo": "give back true if the number of B is odd",
        "cases": [(("WWWBBW",), False), (("WBBWBW",), True), (("WWWWWW",), False), (("B",), True), (("BBBB",), False)],
        "hints": ["Count how many B letters are in the row.",
                  "A number is odd when its remainder after dividing by 2 is 1.",
                  "Give back the result of comparing: count % 2 == 1."],
        "hints_js": ["Count how many B letters are in the row with a loop.",
                     "A number is odd when its remainder after dividing by 2 is 1.",
                     "Give back the result of comparing: count % 2 === 1."],
        "note": "An even number of black cards is the rule, so an odd count means one card was flipped.",
        "python": {"fn": "has_parity_error", "params": "row",
                   "solution": "def has_parity_error(row):\n    return row.count(\"B\") % 2 == 1\n"},
        "javascript": {"fn": "hasParityError", "params": "row",
                       "solution": "function hasParityError(row) {\n  let count = 0;\n  for (const card of row) {\n    if (card === \"B\") count++;\n  }\n  return count % 2 === 1;\n}\n"},
    },
    {
        "slug": "find-flipped-card", "topic": "error-detection-and-correction", "name": "detect-parity-error-in-any-rows-or-columns",
        "level": "Advanced", "age": "teen+", "title": "Find the flipped card",
        "prompt": "A grid of cards is given as a list of rows, like [\"BBW\", \"BWB\", \"WBB\"]. Every row and every column should have an even number of B. "
                  "Someone flipped one card. Write a function FN(rows) that gives back [row, column] of that card, counting from 1. "
                  "If every row and column is fine, give back null (None in Python).",
        "concepts": ["lists of text", "nested loops", "parity", "error correction"], "todo": "give back [row, column] or null",
        "cases": [((["BBW", "BWW", "WBB"],), [2, 3]), ((["WBW", "BWB", "WBB"],), [1, 1]),
                  ((["BBW", "BWB", "WBB"],), None), ((["WWWW", "WWWW", "WBWW", "WWWW"],), [3, 2])],
        "hints": ["First find the row with an odd number of B. Then find the column with an odd number of B.",
                  "To count a column, look at the same position in every row.",
                  "If you found both, give back [row + 1, column + 1]. If not, nothing was flipped."],
        "note": "The flipped card is where the odd row and the odd column cross. That is how the magic trick works.",
        "python": {"fn": "find_flipped_card", "params": "rows",
                   "solution": ("def find_flipped_card(rows):\n    bad_row = None\n    bad_col = None\n"
                                "    for r in range(len(rows)):\n        if rows[r].count(\"B\") % 2 == 1:\n            bad_row = r\n"
                                "    for c in range(len(rows[0])):\n        count = 0\n        for row in rows:\n            if row[c] == \"B\":\n                count += 1\n"
                                "        if count % 2 == 1:\n            bad_col = c\n"
                                "    if bad_row is None or bad_col is None:\n        return None\n    return [bad_row + 1, bad_col + 1]\n")},
        "javascript": {"fn": "findFlippedCard", "params": "rows",
                       "solution": ("function findFlippedCard(rows) {\n  let badRow = -1;\n  let badCol = -1;\n"
                                    "  rows.forEach((row, r) => {\n    let count = 0;\n    for (const card of row) if (card === \"B\") count++;\n    if (count % 2 === 1) badRow = r;\n  });\n"
                                    "  for (let c = 0; c < rows[0].length; c++) {\n    let count = 0;\n    for (const row of rows) if (row[c] === \"B\") count++;\n    if (count % 2 === 1) badCol = c;\n  }\n"
                                    "  if (badRow === -1 || badCol === -1) return null;\n  return [badRow + 1, badCol + 1];\n}\n")},
    },
    {
        "slug": "isbn-check-digit", "topic": "error-detection-and-correction", "name": "calculate-isbn-10-last-digit",
        "level": "Intermediate", "age": "teen+", "title": "Book code: the last digit",
        "prompt": "An ISBN-10 book code has 10 digits. The last one is a check digit. Write a function FN(first9) that gets the first 9 digits as text "
                  "and gives back the check digit as text. How: multiply the digits by 10, 9, 8 ... 2 and add them up. "
                  "The check digit is (11 - total % 11) % 11. If that is 10, give back \"X\".",
        "concepts": ["check digits", "loops", "remainder (%)", "text and numbers"], "todo": "give back the check digit as text",
        "cases": [(("020153082",), "1"), (("014003219",), "3"), (("052135741",), "1"), (("043942089",), "X"), (("000000000",), "0")],
        "hints": ["Go through the 9 digits. The first is multiplied by 10, the next by 9, and so on down to 2.",
                  "Turn each character into a number before you multiply.",
                  "Work out (11 - total % 11) % 11. Give back \"X\" for 10, otherwise the number as text."],
        "stages": [{"goal": "Add up the digits with their weights.",
                    "explain": "Give back the total for now: digit 1 times 10, plus digit 2 times 9, ... plus digit 9 times 2.",
                    "cases": [(("020153082",), 98)],
                    "python": "def isbn10_check_digit(first9):\n    total = 0\n    for i in range(9):\n        total += int(first9[i]) * (10 - i)\n    return total\n",
                    "javascript": "function isbn10CheckDigit(first9) {\n  let total = 0;\n  for (let i = 0; i < 9; i++) {\n    total += Number(first9[i]) * (10 - i);\n  }\n  return total;\n}\n"}],
        "note": "With the check digit added, the weighted total always divides by 11. One wrong digit breaks that.",
        "python": {"fn": "isbn10_check_digit", "params": "first9",
                   "solution": ("def isbn10_check_digit(first9):\n    total = 0\n    for i in range(9):\n        total += int(first9[i]) * (10 - i)\n"
                                "    check = (11 - total % 11) % 11\n    if check == 10:\n        return \"X\"\n    return str(check)\n")},
        "javascript": {"fn": "isbn10CheckDigit", "params": "first9",
                       "solution": ("function isbn10CheckDigit(first9) {\n  let total = 0;\n  for (let i = 0; i < 9; i++) {\n    total += Number(first9[i]) * (10 - i);\n  }\n"
                                    "  const check = (11 - (total % 11)) % 11;\n  return check === 10 ? \"X\" : String(check);\n}\n")},
    },
    {
        "slug": "isbn-valid", "topic": "error-detection-and-correction", "name": "check-valid-isbn-10",
        "level": "Advanced", "age": "teen+", "title": "Is this book code real?",
        "prompt": "Write a function FN(code). code is an ISBN-10 as text. It is valid when it has 10 characters, the first 9 are digits, "
                  "the last is a digit or X (which means 10), and digit 1 times 10 + digit 2 times 9 + ... + digit 10 times 1 divides by 11. "
                  "Give back true or false.",
        "concepts": ["check digits", "validation", "loops", "remainder (%)"], "todo": "give back true or false",
        "cases": [(("0201530821",), True), (("0140032193",), True), (("0521357411",), True), (("043942089X",), True),
                  (("0201530822",), False), (("1234567890",), False), (("12345",), False), (("X201530821",), False)],
        "hints": ["First check the length. Anything but 10 characters is not valid.",
                  "Only the last character may be X, and it counts as 10. Any other letter makes it invalid.",
                  "Multiply each value by 10, 9 ... 1, add them up, and check that total % 11 is 0."],
        "note": "Checking the rules in order (length, letters, total) means a bad code is caught before any maths goes wrong.",
        "python": {"fn": "is_valid_isbn10", "params": "code",
                   "solution": ("def is_valid_isbn10(code):\n    if len(code) != 10:\n        return False\n    total = 0\n"
                                "    for i in range(10):\n        ch = code[i]\n        if ch == \"X\" and i == 9:\n            value = 10\n"
                                "        elif ch.isdigit():\n            value = int(ch)\n        else:\n            return False\n"
                                "        total += value * (10 - i)\n    return total % 11 == 0\n")},
        "javascript": {"fn": "isValidIsbn10", "params": "code",
                       "solution": ("function isValidIsbn10(code) {\n  if (code.length !== 10) return false;\n  let total = 0;\n"
                                    "  for (let i = 0; i < 10; i++) {\n    const ch = code[i];\n    let value;\n"
                                    "    if (ch === \"X\" && i === 9) value = 10;\n    else if (ch >= \"0\" && ch <= \"9\") value = Number(ch);\n    else return false;\n"
                                    "    total += value * (10 - i);\n  }\n  return total % 11 === 0;\n}\n")},
    },
    {
        "slug": "card-check-digit", "topic": "error-detection-and-correction", "name": "calculate-credit-card-last-digit",
        "level": "Advanced", "age": "teen+", "title": "Card number: the last digit",
        "prompt": "Bank card numbers end in a check digit (the Luhn method). Write a function FN(first15) that gets the first 15 digits as text and gives back the last digit as a number. "
                  "How: start from the RIGHT of first15. Double the 1st, 3rd, 5th ... digit from the right; if a doubled value is more than 9, subtract 9. "
                  "Add everything up. The check digit is (10 - total % 10) % 10. (These are made-up test numbers, not real cards.)",
        "concepts": ["check digits", "Luhn method", "loops from the right", "remainder (%)"], "todo": "give back the check digit",
        "cases": [(("510510510510510",), 0), (("411111111111111",), 1), (("555555555555444",), 4), (("000000000000000",), 0)],
        "hints": ["Go through the digits from right to left. Keep track of the position: 0, 1, 2 ...",
                  "At positions 0, 2, 4 ... double the digit. If that gives more than 9, subtract 9.",
                  "Add all the values. The answer is (10 - total % 10) % 10."],
        "note": "Doubling every other digit catches most single mistakes and most swaps of two neighbouring digits.",
        "python": {"fn": "card_check_digit", "params": "first15",
                   "solution": ("def card_check_digit(first15):\n    total = 0\n    for i, ch in enumerate(reversed(first15)):\n        value = int(ch)\n"
                                "        if i % 2 == 0:\n            value *= 2\n            if value > 9:\n                value -= 9\n        total += value\n"
                                "    return (10 - total % 10) % 10\n")},
        "javascript": {"fn": "cardCheckDigit", "params": "first15",
                       "solution": ("function cardCheckDigit(first15) {\n  let total = 0;\n  const digits = first15.split(\"\").reverse();\n"
                                    "  digits.forEach((ch, i) => {\n    let value = Number(ch);\n    if (i % 2 === 0) {\n      value *= 2;\n      if (value > 9) value -= 9;\n    }\n    total += value;\n  });\n"
                                    "  return (10 - (total % 10)) % 10;\n}\n")},
    },
    {
        "slug": "card-valid", "topic": "error-detection-and-correction", "name": "check-valid-credit-card",
        "level": "Advanced", "age": "teen+", "title": "Is this card number possible?",
        "prompt": "Write a function FN(number). number is 16 digits as text. Check it with the Luhn method: from the RIGHT, double every SECOND digit "
                  "(the 2nd, 4th ...), subtract 9 from any doubled value over 9, and add everything up. The number is valid if it has 16 digits and the total divides by 10. "
                  "Give back true or false. (Made-up test numbers only.)",
        "concepts": ["check digits", "Luhn method", "validation"], "todo": "give back true or false",
        "cases": [(("5105105105105100",), True), (("4111111111111111",), True), (("5555555555554444",), True),
                  (("4111111111111112",), False), (("1234567812345678",), False), (("41111111",), False)],
        "hints": ["Check that there are exactly 16 characters and all are digits.",
                  "Go from right to left. Positions 1, 3, 5 ... (counting from 0) are doubled.",
                  "Subtract 9 from doubled values over 9, add everything, and check total % 10 is 0."],
        "note": "This is the same method as the last-digit problem, run over the whole number.",
        "python": {"fn": "is_valid_card", "params": "number",
                   "solution": ("def is_valid_card(number):\n    if len(number) != 16 or not number.isdigit():\n        return False\n    total = 0\n"
                                "    for i, ch in enumerate(reversed(number)):\n        value = int(ch)\n        if i % 2 == 1:\n            value *= 2\n"
                                "            if value > 9:\n                value -= 9\n        total += value\n    return total % 10 == 0\n")},
        "javascript": {"fn": "isValidCard", "params": "number",
                       "solution": ("function isValidCard(number) {\n  if (number.length !== 16 || !/^[0-9]+$/.test(number)) return false;\n  let total = 0;\n"
                                    "  number.split(\"\").reverse().forEach((ch, i) => {\n    let value = Number(ch);\n    if (i % 2 === 1) {\n      value *= 2;\n      if (value > 9) value -= 9;\n    }\n    total += value;\n  });\n"
                                    "  return total % 10 === 0;\n}\n")},
    },
    {
        "slug": "barcode-check-digit", "topic": "error-detection-and-correction", "name": "product-code-13-last-digit-one-line",
        "level": "Intermediate", "age": "11-13", "title": "Barcode: the last digit",
        "prompt": "A 13-digit barcode ends in a check digit. Write a function FN(first12) that gets the first 12 digits as text and gives back the last digit as a number. "
                  "How: add the digits, but multiply every second one (the 2nd, 4th, 6th ...) by 3. The check digit is (10 - total % 10) % 10.",
        "concepts": ["check digits", "loops", "remainder (%)"], "todo": "give back the check digit",
        "cases": [(("941887000085",), 2), (("941527700012",), 6), (("930072885454",), 3), (("932835000371",), 9), (("000000000000",), 0)],
        "hints": ["Go through the 12 digits with their position: 0, 1, 2 ...",
                  "Digits at positions 1, 3, 5 ... are multiplied by 3. The others count once.",
                  "Add them all. The answer is (10 - total % 10) % 10."],
        "stages": [{"goal": "Add up the digits with weights 1 and 3.",
                    "explain": "Give back the total for now. Positions 0, 2, 4 ... count once; positions 1, 3, 5 ... count three times.",
                    "cases": [(("941887000085",), 98)],
                    "python": "def barcode_check_digit(first12):\n    total = 0\n    for i in range(12):\n        weight = 3 if i % 2 == 1 else 1\n        total += int(first12[i]) * weight\n    return total\n",
                    "javascript": "function barcodeCheckDigit(first12) {\n  let total = 0;\n  for (let i = 0; i < 12; i++) {\n    const weight = i % 2 === 1 ? 3 : 1;\n    total += Number(first12[i]) * weight;\n  }\n  return total;\n}\n"}],
        "note": "The check digit makes the weighted total a multiple of 10, so a scanner can spot a misread digit.",
        "python": {"fn": "barcode_check_digit", "params": "first12",
                   "solution": ("def barcode_check_digit(first12):\n    total = 0\n    for i in range(12):\n        weight = 3 if i % 2 == 1 else 1\n"
                                "        total += int(first12[i]) * weight\n    return (10 - total % 10) % 10\n")},
        "javascript": {"fn": "barcodeCheckDigit", "params": "first12",
                       "solution": ("function barcodeCheckDigit(first12) {\n  let total = 0;\n  for (let i = 0; i < 12; i++) {\n    const weight = i % 2 === 1 ? 3 : 1;\n"
                                    "    total += Number(first12[i]) * weight;\n  }\n  return (10 - (total % 10)) % 10;\n}\n")},
    },
    {
        "slug": "barcode-valid", "topic": "error-detection-and-correction", "name": "product-code-check-valid-any-length",
        "level": "Advanced", "age": "teen+", "title": "Check any barcode",
        "prompt": "Barcodes can have 8, 12 or 13 digits. Write a function FN(code) that checks any of them. Start from the RIGHT: the last digit counts once, "
                  "the next one three times, then once, then three times, and so on. The code is valid if the total divides by 10. Give back true or false.",
        "concepts": ["check digits", "loops from the right", "validation"], "todo": "give back true or false",
        "cases": [(("50184385",), True), (("036000241457",), True), (("50174385",), False), (("9330462119318",), True),
                  (("9418870000852",), True), (("9418870000853",), False)],
        "hints": ["Going from the right works for every length, because the last digit always counts once.",
                  "Positions 0, 2, 4 ... from the right count once. Positions 1, 3, 5 ... count three times.",
                  "Give back whether total % 10 is 0."],
        "note": "Counting from the right lines up the weights for 8-, 12- and 13-digit codes alike.",
        "python": {"fn": "is_valid_barcode", "params": "code",
                   "solution": ("def is_valid_barcode(code):\n    total = 0\n    for i, ch in enumerate(reversed(code)):\n"
                                "        weight = 3 if i % 2 == 1 else 1\n        total += int(ch) * weight\n    return total % 10 == 0\n")},
        "javascript": {"fn": "isValidBarcode", "params": "code",
                       "solution": ("function isValidBarcode(code) {\n  let total = 0;\n  code.split(\"\").reverse().forEach((ch, i) => {\n"
                                    "    const weight = i % 2 === 1 ? 3 : 1;\n    total += Number(ch) * weight;\n  });\n  return total % 10 === 0;\n}\n")},
    },
    # ---------------------------------------------------------------- kidbots: number skills
    {
        "slug": "add-in-parts", "topic": "kidbots", "name": "add-in-parts-2-digit-number",
        "level": "Beginner", "age": "11-13", "title": "Add in parts",
        "prompt": "A quick way to add is to make a ten first. Write a function FN(a, b) where a is under 100 and b is under 10. "
                  "If the last digit of a plus b is MORE than 10, split b to make a ten first, like \"(87 + 3) + 4 = 94\". "
                  "Otherwise just write it out, like \"75 + 4 = 79\". Give back the text.",
        "concepts": ["remainder (%)", "if / else", "building text"], "todo": "give back the sum written out",
        "cases": [((87, 7), "(87 + 3) + 4 = 94"), ((54, 9), "(54 + 6) + 3 = 63"), ((75, 4), "75 + 4 = 79"),
                  ((76, 4), "76 + 4 = 80"), ((8, 5), "(8 + 2) + 3 = 13")],
        "hints": ["The last digit of a is a % 10.",
                  "To make a ten you need 10 - a % 10. The rest of b is b minus that.",
                  "Only split when a % 10 + b is more than 10. Put the numbers into the text with spaces exactly as shown."],
        "note": "Making a ten first is a mental-maths trick. The program does the same steps you would do in your head.",
        "python": {"fn": "add_in_parts", "params": "a, b",
                   "solution": ("def add_in_parts(a, b):\n    if a % 10 + b > 10:\n        to_ten = 10 - a % 10\n        rest = b - to_ten\n"
                                "        return f\"({a} + {to_ten}) + {rest} = {a + b}\"\n    return f\"{a} + {b} = {a + b}\"\n")},
        "javascript": {"fn": "addInParts", "params": "a, b",
                       "solution": ("function addInParts(a, b) {\n  if ((a % 10) + b > 10) {\n    const toTen = 10 - (a % 10);\n    const rest = b - toTen;\n"
                                    "    return `(${a} + ${toTen}) + ${rest} = ${a + b}`;\n  }\n  return `${a} + ${b} = ${a + b}`;\n}\n")},
    },
    {
        "slug": "power", "topic": "kidbots", "name": "calculate-exponents",
        "level": "Beginner", "age": "11-13", "title": "Power of a number",
        "prompt": "Write a function FN(base, exponent). It gives back base multiplied by itself exponent times. exponent is 0 or more, and anything to the power 0 is 1. "
                  "Use a loop, not the built-in power operator.",
        "concepts": ["loops", "multiplying", "exponents"], "todo": "give back base to the power exponent",
        "cases": [((3, 5), 243), ((-2, 4), 16), ((2, 0), 1), ((5, 1), 5), ((-3, 3), -27), ((10, 3), 1000)],
        "hints": ["Start with result = 1.",
                  "Repeat exponent times: multiply result by base.",
                  "If exponent is 0 the loop never runs, so the answer stays 1."],
        "note": "Repeated multiplying is exactly what a power means.",
        "python": {"fn": "power", "params": "base, exponent",
                   "solution": "def power(base, exponent):\n    result = 1\n    for i in range(exponent):\n        result *= base\n    return result\n"},
        "javascript": {"fn": "power", "params": "base, exponent",
                       "solution": "function power(base, exponent) {\n  let result = 1;\n  for (let i = 0; i < exponent; i++) {\n    result *= base;\n  }\n  return result;\n}\n",
                       "extra_tests": [{"name": T("It uses a loop, not ** or Math.pow"),
                                        "code": "assert(!power.toString().includes(\"**\") && !power.toString().includes(\"Math.pow\"), \"Please use a loop.\")"}]},
    },
    {
        "slug": "inside-angle", "topic": "kidbots", "name": "calculate-inside-angles-of-regular-polygons",
        "level": "Beginner", "age": "11-13", "title": "Inside angle of a shape",
        "prompt": "In a regular shape all sides and angles are the same. Write a function FN(sides) that gives back the size of each inside angle in degrees. "
                  "The rule is (sides - 2) times 180, divided by sides. Example: a square (4 sides) has 90 degree angles.",
        "concepts": ["maths in code", "functions", "division"], "todo": "give back the inside angle",
        "cases": [((3,), 60), ((4,), 90), ((5,), 108), ((6,), 120), ((10,), 144)],
        "hints": ["You only need the formula from the problem.",
                  "Work out sides - 2 first, then multiply by 180.",
                  "Divide by sides and give back the result."],
        "note": "A shape with n sides can be cut into n - 2 triangles, and each triangle has 180 degrees.",
        "python": {"fn": "inside_angle", "params": "sides",
                   "solution": "def inside_angle(sides):\n    return (sides - 2) * 180 / sides\n"},
        "javascript": {"fn": "insideAngle", "params": "sides",
                       "solution": "function insideAngle(sides) {\n  return (sides - 2) * 180 / sides;\n}\n"},
    },
    {
        "slug": "is-divisor", "topic": "kidbots", "name": "check-if-divisor",
        "level": "Beginner", "age": "8-10", "title": "Does it divide?",
        "prompt": "Write a function FN(number, divisor). Give back true if divisor goes into number with nothing left over, and false if not.",
        "concepts": ["remainder (%)", "true and false"], "todo": "give back true or false",
        "cases": [((20, 4), True), ((20, 6), False), ((7, 7), True), ((9, 1), True), ((10, 3), False)],
        "hints": ["The remainder of number divided by divisor is number % divisor.",
                  "Nothing left over means the remainder is 0.",
                  "Give back the result of comparing the remainder with 0."],
        "note": "% gives what is left over after dividing. Zero left over means it divides exactly.",
        "python": {"fn": "is_divisor", "params": "number, divisor",
                   "solution": "def is_divisor(number, divisor):\n    return number % divisor == 0\n"},
        "javascript": {"fn": "isDivisor", "params": "number, divisor",
                       "solution": "function isDivisor(number, divisor) {\n  return number % divisor === 0;\n}\n"},
    },
    {
        "slug": "factors", "topic": "kidbots", "name": "find-factors",
        "level": "Beginner", "age": "11-13", "title": "All the factors",
        "prompt": "A factor of n is a whole number that divides n exactly. Write a function FN(n) that gives back all the factors of n, smallest first. n is 1 or more.",
        "concepts": ["loops", "remainder (%)", "lists"], "todo": "give back a list of factors",
        "cases": [((12,), [1, 2, 3, 4, 6, 12]), ((61,), [1, 61]), ((1,), [1]), ((16,), [1, 2, 4, 8, 16])],
        "hints": ["Try every number from 1 up to n.",
                  "A number d is a factor when n % d is 0.",
                  "Add each factor to a list, and give back the list at the end."],
        "stages": [{"goal": "Make a list of every number from 1 to n.",
                    "explain": "Loop from 1 to n and add each number to a list. Next you will keep only the factors.",
                    "cases": [((4,), [1, 2, 3, 4])],
                    "python": "def factors(n):\n    result = []\n    for d in range(1, n + 1):\n        result.append(d)\n    return result\n",
                    "javascript": "function factors(n) {\n  const result = [];\n  for (let d = 1; d <= n; d++) {\n    result.push(d);\n  }\n  return result;\n}\n"}],
        "note": "Checking every number from 1 to n is slow for big n, but it is simple and always right.",
        "python": {"fn": "factors", "params": "n",
                   "solution": "def factors(n):\n    result = []\n    for d in range(1, n + 1):\n        if n % d == 0:\n            result.append(d)\n    return result\n"},
        "javascript": {"fn": "factors", "params": "n",
                       "solution": "function factors(n) {\n  const result = [];\n  for (let d = 1; d <= n; d++) {\n    if (n % d === 0) result.push(d);\n  }\n  return result;\n}\n"},
    },
    {
        "slug": "is-prime", "topic": "kidbots", "name": "check-prime",
        "level": "Intermediate", "age": "11-13", "title": "Is it a prime?",
        "prompt": "A prime is a whole number bigger than 1 whose only factors are 1 and itself. Write a function FN(n) that gives back true if n is prime, and false if not.",
        "concepts": ["loops", "remainder (%)", "early return"], "todo": "give back true or false",
        "cases": [((73,), True), ((123,), False), ((1,), False), ((0,), False), ((2,), True), ((97,), True), ((91,), False)],
        "hints": ["Numbers below 2 are never prime.",
                  "Try dividing n by every number from 2 up to n - 1.",
                  "If any of them divides n exactly, give back false straight away. If none do, give back true."],
        "stages": [{"goal": "Handle the small numbers.",
                    "explain": "Give back false if n is less than 2, and true otherwise (for now).",
                    "cases": [((1,), False), ((0,), False), ((7,), True)],
                    "python": "def is_prime(n):\n    if n < 2:\n        return False\n    return True\n",
                    "javascript": "function isPrime(n) {\n  if (n < 2) return false;\n  return true;\n}\n"}],
        "note": "One factor is enough to prove a number is not prime, so the loop can stop early.",
        "python": {"fn": "is_prime", "params": "n",
                   "solution": "def is_prime(n):\n    if n < 2:\n        return False\n    for d in range(2, n):\n        if n % d == 0:\n            return False\n    return True\n"},
        "javascript": {"fn": "isPrime", "params": "n",
                       "solution": "function isPrime(n) {\n  if (n < 2) return false;\n  for (let d = 2; d < n; d++) {\n    if (n % d === 0) return false;\n  }\n  return true;\n}\n"},
    },
    {
        "slug": "prime-factors", "topic": "kidbots", "name": "find-prime-factors",
        "level": "Intermediate", "age": "teen+", "title": "Prime factors",
        "prompt": "Write a function FN(n) that gives back the different prime numbers that divide n, smallest first. Example: 150 = 2 x 3 x 5 x 5, so it gives [2, 3, 5]. "
                  "For n = 1 give back an empty list.",
        "concepts": ["helper functions", "primes", "loops", "lists"], "todo": "give back a list of prime factors",
        "cases": [((26,), [2, 13]), ((150,), [2, 3, 5]), ((7,), [7]), ((64,), [2]), ((1,), []), ((30,), [2, 3, 5])],
        "hints": ["You can write a small helper function that checks if a number is prime.",
                  "Try every d from 2 up to n. Keep d if it divides n AND it is prime.",
                  "Each prime goes in the list once, even if it divides n many times."],
        "note": "Splitting the job into 'is it prime?' and 'does it divide?' keeps each part simple.",
        "python": {"fn": "prime_factors", "params": "n",
                   "solution": ("def prime_factors(n):\n    def is_prime(k):\n        if k < 2:\n            return False\n        for d in range(2, k):\n"
                                "            if k % d == 0:\n                return False\n        return True\n"
                                "    return [d for d in range(2, n + 1) if n % d == 0 and is_prime(d)]\n")},
        "javascript": {"fn": "primeFactors", "params": "n",
                       "solution": ("function primeFactors(n) {\n  const isPrime = (k) => {\n    if (k < 2) return false;\n    for (let d = 2; d < k; d++) if (k % d === 0) return false;\n    return true;\n  };\n"
                                    "  const result = [];\n  for (let d = 2; d <= n; d++) {\n    if (n % d === 0 && isPrime(d)) result.push(d);\n  }\n  return result;\n}\n")},
    },
    # ---------------------------------------------------------------- kidbots: modulo
    {
        "slug": "clock-12", "topic": "kidbots", "name": "modulo-add-hours-12-hour-clock",
        "level": "Intermediate", "age": "11-13", "title": "Add hours on a 12-hour clock",
        "prompt": "On a 12-hour clock, 11 o'clock plus 3 hours is 2 o'clock. Write a function FN(start, hours) that gives back the new hour, from 1 to 12.",
        "concepts": ["remainder (%)", "clock arithmetic", "special cases"], "todo": "give back the new hour (1 to 12)",
        "cases": [((11, 1), 12), ((11, 4), 3), ((11, 12), 11), ((12, 12), 12), ((3, 25), 4)],
        "hints": ["Add the hours, then use % 12 to wrap round the clock.",
                  "% 12 gives a number from 0 to 11.",
                  "A clock has no 0 o'clock: when the answer is 0, give back 12."],
        "stages": [{"goal": "Wrap round with % 12.",
                    "explain": "Give back (start + hours) % 12. This is right except when it gives 0.",
                    "cases": [((11, 4), 3)],
                    "python": "def add_hours_12(start, hours):\n    return (start + hours) % 12\n",
                    "javascript": "function addHours12(start, hours) {\n  return (start + hours) % 12;\n}\n"}],
        "note": "% does the wrapping. The only fix needed is that 0 is written 12 on a clock.",
        "python": {"fn": "add_hours_12", "params": "start, hours",
                   "solution": "def add_hours_12(start, hours):\n    hour = (start + hours) % 12\n    if hour == 0:\n        return 12\n    return hour\n"},
        "javascript": {"fn": "addHours12", "params": "start, hours",
                       "solution": "function addHours12(start, hours) {\n  const hour = (start + hours) % 12;\n  return hour === 0 ? 12 : hour;\n}\n"},
    },
    {
        "slug": "clock-24", "topic": "kidbots", "name": "modulo-add-hours-24-hour-clock",
        "level": "Beginner", "age": "11-13", "title": "Add hours on a 24-hour clock",
        "prompt": "On a 24-hour clock, 22:00 plus 5 hours is 3:00. Write a function FN(start, hours) that gives back the new hour, from 0 to 23.",
        "concepts": ["remainder (%)", "clock arithmetic"], "todo": "give back the new hour (0 to 23)",
        "cases": [((11, 1), 12), ((11, 4), 15), ((11, 12), 23), ((22, 5), 3), ((0, 48), 0)],
        "hints": ["Add the hours together first.",
                  "The clock goes back to 0 after 23.",
                  "% 24 gives the remainder after dividing by 24, which wraps it round."],
        "note": "% 24 keeps only what is left after taking out whole days.",
        "python": {"fn": "add_hours_24", "params": "start, hours",
                   "solution": "def add_hours_24(start, hours):\n    return (start + hours) % 24\n"},
        "javascript": {"fn": "addHours24", "params": "start, hours",
                       "solution": "function addHours24(start, hours) {\n  return (start + hours) % 24;\n}\n"},
    },
    {
        "slug": "month-after", "topic": "kidbots", "name": "modulo-add-months",
        "level": "Intermediate", "age": "11-13", "title": "Months later",
        "prompt": "Write a function FN(month, add). month is 1 (January) to 12 (December). Give back the NAME of the month that is add months later. "
                  "Example: 4 months after October (10) is \"February\".",
        "concepts": ["lists", "indexes", "remainder (%)"], "todo": "give back the month name",
        "cases": [((10, 4), "February"), ((12, 8), "August"), ((1, 6), "July"), ((5, 0), "May"), ((12, 1), "January"), ((3, 24), "March")],
        "hints": ["Make a list of the 12 month names. January is at position 0.",
                  "Turn month into a position with month - 1, then add.",
                  "Use % 12 to wrap round to the start of the year, then look up the name."],
        "note": "Counting from 0 makes % 12 line up with the list positions.",
        "python": {"fn": "month_after", "params": "month, add",
                   "solution": ("def month_after(month, add):\n    names = [\"January\", \"February\", \"March\", \"April\", \"May\", \"June\",\n"
                                "             \"July\", \"August\", \"September\", \"October\", \"November\", \"December\"]\n"
                                "    return names[(month - 1 + add) % 12]\n")},
        "javascript": {"fn": "monthAfter", "params": "month, add",
                       "solution": ("function monthAfter(month, add) {\n  const names = [\"January\", \"February\", \"March\", \"April\", \"May\", \"June\",\n"
                                    "    \"July\", \"August\", \"September\", \"October\", \"November\", \"December\"];\n"
                                    "  return names[(month - 1 + add) % 12];\n}\n")},
    },
    {
        "slug": "add-durations", "topic": "kidbots", "name": "modulo-add-video-timings",
        "level": "Advanced", "age": "teen+", "title": "Add two video lengths",
        "prompt": "Video lengths are written \"hours:minutes:seconds\", like \"0:32:21\". Write a function FN(a, b) that adds two lengths and gives back the total "
                  "in the same form, with no extra zeros. Example: \"0:32:21\" + \"0:33:20\" is \"1:5:41\".",
        "concepts": ["splitting text", "remainder (%)", "whole-number division", "units of time"], "todo": "give back the total, like 1:5:41",
        "cases": [(("0:32:21", "0:33:20"), "1:5:41"), (("3:59:59", "2:13:3"), "6:13:2"), (("4:59:59", "2:59:59"), "7:59:58"),
                  (("0:0:1", "0:0:59"), "0:1:0"), (("0:0:0", "0:0:0"), "0:0:0")],
        "hints": ["Split each text at the \":\" to get hours, minutes and seconds as numbers.",
                  "Turn both lengths into seconds (hours x 3600 + minutes x 60 + seconds) and add them.",
                  "Turn the total back: hours = total // 3600, minutes = (total % 3600) // 60, seconds = total % 60."],
        "hints_js": ["Split each text at the \":\" to get hours, minutes and seconds as numbers.",
                     "Turn both lengths into seconds (hours x 3600 + minutes x 60 + seconds) and add them.",
                     "Turn the total back with Math.floor(total / 3600), Math.floor((total % 3600) / 60) and total % 60."],
        "note": "Working in one unit (seconds) and converting at the end avoids lots of carrying rules.",
        "python": {"fn": "add_durations", "params": "a, b",
                   "solution": ("def add_durations(a, b):\n    def seconds(text):\n        h, m, s = (int(x) for x in text.split(\":\"))\n        return h * 3600 + m * 60 + s\n"
                                "    total = seconds(a) + seconds(b)\n    return f\"{total // 3600}:{total % 3600 // 60}:{total % 60}\"\n")},
        "javascript": {"fn": "addDurations", "params": "a, b",
                       "solution": ("function addDurations(a, b) {\n  const seconds = (text) => {\n    const [h, m, s] = text.split(\":\").map(Number);\n    return h * 3600 + m * 60 + s;\n  };\n"
                                    "  const total = seconds(a) + seconds(b);\n  return `${Math.floor(total / 3600)}:${Math.floor((total % 3600) / 60)}:${total % 60}`;\n}\n")},
    },
    {
        "slug": "leap-year", "topic": "kidbots", "name": "modulo-check-leap-year",
        "level": "Intermediate", "age": "11-13", "title": "Leap years",
        "prompt": "Write a function FN(year) that gives back true for a leap year. The rule: a year that divides by 4 is a leap year, "
                  "EXCEPT years that divide by 100, which are not, EXCEPT years that divide by 400, which are.",
        "concepts": ["remainder (%)", "if / elif / else", "rules with exceptions"], "todo": "give back true or false",
        "cases": [((1600,), True), ((2000,), True), ((2400,), True), ((1700,), False), ((2100,), False), ((2024,), True), ((2023,), False)],
        "hints": ["Check the most special rule first: dividing by 400 means leap year.",
                  "Next: dividing by 100 (but not 400) means NOT a leap year.",
                  "Last: dividing by 4 means leap year. Anything else is not."],
        "note": "Checking the rarest rule first means the exceptions never get missed.",
        "python": {"fn": "is_leap_year", "params": "year",
                   "solution": ("def is_leap_year(year):\n    if year % 400 == 0:\n        return True\n    if year % 100 == 0:\n        return False\n"
                                "    return year % 4 == 0\n")},
        "javascript": {"fn": "isLeapYear", "params": "year",
                       "solution": ("function isLeapYear(year) {\n  if (year % 400 === 0) return true;\n  if (year % 100 === 0) return false;\n  return year % 4 === 0;\n}\n")},
    },
    {
        "slug": "note-name", "topic": "kidbots", "name": "modulo-display-midi-note",
        "level": "Intermediate", "age": "11-13", "title": "Name the music note",
        "prompt": "Music programs number notes from 0 to 127 (60 is middle C). The names repeat every 12 notes: "
                  "C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, B. Write a function FN(number) that gives back the note name.",
        "concepts": ["lists", "remainder (%)", "music and maths"], "todo": "give back the note name",
        "cases": [((60,), "C"), ((34,), "Bb"), ((85,), "C#"), ((127,), "G"), ((0,), "C"), ((69,), "A")],
        "hints": ["Make a list of the 12 note names, starting with C.",
                  "The names repeat every 12 notes, so number % 12 tells you which one.",
                  "Use that remainder as the position in the list."],
        "note": "% 12 throws away whole octaves and keeps only the place inside one octave.",
        "python": {"fn": "note_name", "params": "number",
                   "solution": ("def note_name(number):\n    names = [\"C\", \"C#\", \"D\", \"Eb\", \"E\", \"F\", \"F#\", \"G\", \"Ab\", \"A\", \"Bb\", \"B\"]\n"
                                "    return names[number % 12]\n")},
        "javascript": {"fn": "noteName", "params": "number",
                       "solution": ("function noteName(number) {\n  const names = [\"C\", \"C#\", \"D\", \"Eb\", \"E\", \"F\", \"F#\", \"G\", \"Ab\", \"A\", \"Bb\", \"B\"];\n"
                                    "  return names[number % 12];\n}\n")},
    },
]

PROBLEMS = [p for spec in SPECS for p in build(spec)]
