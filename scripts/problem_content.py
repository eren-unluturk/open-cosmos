"""Our own coding problems (original text and code, written for this project).

Edit here, then run:  python scripts/build_problems.py   (checks every solution, writes src/data/problems.json)

Rules for authors:
- The starter must FAIL the tests. Every solution must PASS them. The build script checks both.
- Tests run after the learner's code, in the same scope. Python: check(actual, expected) or assert.
  JavaScript: assertEqual(actual, expected) or assert(condition, message). Both can read `output`.
- Hints go from a nudge to almost the answer. Never put the full answer in a hint.
- Keep sentences short. These are read by children (ages 8 and up) and by people reading in a second language.
- Guided stages are small steps. The learner's code carries over from stage to stage.
"""


def T(s):
    return {"en": s}


def test(name, code):
    return {"name": T(name), "code": code}


def stage(goal, explain, solution, tests, starter=None):
    s = {"goal": T(goal), "explain": T(explain), "solution": solution, "tests": tests}
    if starter is not None:
        s["starter"] = starter
    return s


COMMON = {"license": "original", "source": "Hackcessability"}

PROBLEMS = [
    # ------------------------------------------------------------------ Python
    {
        "id": "py-hello", "language": "python", "level": "Beginner", "age_group": "8-10", "topic": "general",
        "title": T("Say hello"),
        "prompt": T("Make the computer say hello. Use print to show the words Hello, world! on the screen."),
        "concepts": T(["print", "text in quote marks"]),
        "starter": "# Write your code here.\n",
        "tests": [
            test("It prints exactly Hello, world!", 'check(output.strip(), "Hello, world!")'),
            test("It prints one line", 'check(len(output.strip().splitlines()), 1)'),
        ],
        "hints": T([
            "Use the print function to show something on the screen.",
            "Text goes inside quote marks, inside the brackets: print(\"...\").",
            "Type the words exactly: capital H, a comma, and an exclamation mark at the end.",
        ]),
        "guided": [
            stage("Print any word.",
                  "print(...) shows what is inside the brackets. Words must be inside quote marks, like \"hi\".",
                  'print("hi")',
                  [test("Something is printed", 'check(len(output.strip()) > 0, True)')],
                  starter='# Try printing the word hi.\n'),
        ],
        "solution": 'print("Hello, world!")\n',
        "solution_note": T("print shows text. The words are inside quote marks so Python knows they are text."),
        **COMMON,
    },
    {
        "id": "py-double", "language": "python", "level": "Beginner", "age_group": "8-10", "topic": "general",
        "title": T("Double it"),
        "prompt": T("Write a function called double. It takes a number n and gives back n times 2."),
        "concepts": T(["functions", "return", "multiplying"]),
        "starter": "def double(n):\n    # give back n times 2\n    pass\n",
        "tests": [
            test("double(4) is 8", "check(double(4), 8)"),
            test("double(0) is 0", "check(double(0), 0)"),
            test("double(-3) is -6", "check(double(-3), -6)"),
            test("double(2.5) is 5.0", "check(double(2.5), 5.0)"),
        ],
        "hints": T([
            "A function gives a value back with the word return.",
            "In Python, the * sign multiplies.",
            "The body of your function is one line: return, then n times 2.",
        ]),
        "guided": [
            stage("Give a value back.",
                  "return sends a value out of the function. For now, just give back n itself.",
                  "def double(n):\n    return n\n",
                  [test("It gives back its input", "check(double(7), 7)")],
                  starter="def double(n):\n    pass\n"),
            stage("Multiply by 2.",
                  "Change what you return. In Python, * means times.",
                  "def double(n):\n    return n * 2\n",
                  [test("double(4) is 8", "check(double(4), 8)")]),
        ],
        "solution": "def double(n):\n    return n * 2\n",
        "solution_note": T("return n * 2 hands back the answer to whoever called the function."),
        **COMMON,
    },
    {
        "id": "py-evens", "language": "python", "level": "Beginner", "age_group": "11-13", "topic": "general",
        "title": T("Count the even numbers"),
        "prompt": T("Write a function count_evens(numbers). It gets a list of whole numbers and gives back how many of them are even."),
        "concepts": T(["lists", "loops", "if", "remainder (%)"]),
        "starter": "def count_evens(numbers):\n    # count the even numbers in the list\n    pass\n",
        "tests": [
            test("[1, 2, 3, 4] has 2 even numbers", "check(count_evens([1, 2, 3, 4]), 2)"),
            test("An empty list has 0", "check(count_evens([]), 0)"),
            test("[2, 4, 6] has 3", "check(count_evens([2, 4, 6]), 3)"),
            test("[1, 3] has 0", "check(count_evens([1, 3]), 0)"),
            test("0 and -2 are even", "check(count_evens([0, -2, 5]), 2)"),
        ],
        "hints": T([
            "An even number has no remainder when you divide it by 2.",
            "The % sign gives the remainder. 7 % 2 is 1, and 8 % 2 is 0.",
            "Keep a counter. Loop over the list. If n % 2 == 0, add 1 to the counter. Return the counter.",
        ]),
        "guided": [
            stage("Make a counter and give it back.",
                  "A counter is a variable that starts at 0. Return it at the end.",
                  "def count_evens(numbers):\n    count = 0\n    return count\n",
                  [test("An empty list gives 0", "check(count_evens([]), 0)")],
                  starter="def count_evens(numbers):\n    pass\n"),
            stage("Loop over the list and count every number.",
                  "for n in numbers: runs the lines below it once for each number. Add 1 to count each time.",
                  "def count_evens(numbers):\n    count = 0\n    for n in numbers:\n        count += 1\n    return count\n",
                  [test("It counts every item (all of these are even)", "check(count_evens([2, 4, 6]), 3)")]),
            stage("Count only the even ones.",
                  "Put the counting line inside an if. The test n % 2 == 0 is true for even numbers.",
                  "def count_evens(numbers):\n    count = 0\n    for n in numbers:\n        if n % 2 == 0:\n            count += 1\n    return count\n",
                  [test("[1, 2, 3, 4] has 2 even numbers", "check(count_evens([1, 2, 3, 4]), 2)")]),
        ],
        "solution": "def count_evens(numbers):\n    count = 0\n    for n in numbers:\n        if n % 2 == 0:\n            count += 1\n    return count\n",
        "solution_note": T("n % 2 == 0 is true when n divides by 2 with nothing left over. The counter goes up only then."),
        **COMMON,
    },
    {
        "id": "py-reverse-words", "language": "python", "level": "Intermediate", "age_group": "11-13", "topic": "general",
        "title": T("Reverse the words"),
        "prompt": T("Write a function reverse_words(sentence). It gives back the same words in the opposite order, joined by single spaces. "
                    "Example: \"one two three\" becomes \"three two one\". Extra spaces at the ends or in the middle are ignored."),
        "concepts": T(["strings", "split and join", "slicing"]),
        "starter": "def reverse_words(sentence):\n    # return the words in the opposite order\n    pass\n",
        "tests": [
            test("\"one two three\" becomes \"three two one\"", 'check(reverse_words("one two three"), "three two one")'),
            test("One word stays the same", 'check(reverse_words("hello"), "hello")'),
            test("An empty sentence gives an empty string", 'check(reverse_words(""), "")'),
            test("Extra spaces are ignored", 'check(reverse_words("  a   b "), "b a")'),
        ],
        "hints": T([
            "Start by splitting the sentence into a list of words with .split().",
            "A list can be turned around with words[::-1].",
            "Put the words back together with \" \".join(your_list).",
        ]),
        "guided": [
            stage("Split the sentence into words.",
                  ".split() turns \"a b\" into the list [\"a\", \"b\"]. It also ignores extra spaces.",
                  "def reverse_words(sentence):\n    words = sentence.split()\n    return words\n",
                  [test("It gives a list of words", 'check(reverse_words("a b"), ["a", "b"])')],
                  starter="def reverse_words(sentence):\n    pass\n"),
            stage("Turn the list around.",
                  "words[::-1] gives the list in reverse order.",
                  "def reverse_words(sentence):\n    words = sentence.split()\n    return words[::-1]\n",
                  [test("The list is reversed", 'check(reverse_words("a b c"), ["c", "b", "a"])')]),
        ],
        "solution": "def reverse_words(sentence):\n    words = sentence.split()\n    return \" \".join(words[::-1])\n",
        "solution_note": T("split makes a list, [::-1] reverses it, and join glues the words back into one string."),
        **COMMON,
    },
    {
        "id": "py-fizzbuzz", "language": "python", "level": "Intermediate", "age_group": "11-13", "topic": "general",
        "title": T("Fizz and Buzz"),
        "prompt": T("Write a function fizzbuzz(n). It gives back a list for the numbers 1 to n. For each number, put in the text \"Fizz\" if it divides by 3, "
                    "\"Buzz\" if it divides by 5, and \"FizzBuzz\" if it divides by both. Otherwise put the number as text, like \"7\"."),
        "concepts": T(["loops", "range", "if / elif", "remainder (%)", "lists"]),
        "starter": "def fizzbuzz(n):\n    # return a list of text, one item for each number from 1 to n\n    pass\n",
        "tests": [
            test("fizzbuzz(5) is the right list", 'check(fizzbuzz(5), ["1", "2", "Fizz", "4", "Buzz"])'),
            test("15 is FizzBuzz", 'check(fizzbuzz(15)[-1], "FizzBuzz")'),
            test("fizzbuzz(0) is an empty list", "check(fizzbuzz(0), [])"),
            test("3 is Fizz", 'check(fizzbuzz(3)[2], "Fizz")'),
            test("10 is Buzz", 'check(fizzbuzz(10)[9], "Buzz")'),
        ],
        "hints": T([
            "range(1, n + 1) gives the numbers from 1 up to n.",
            "i % 3 == 0 means i divides by 3 with nothing left over.",
            "Check for both 3 and 5 first (divides by 15). If you check 3 first, you never reach FizzBuzz.",
        ]),
        "guided": [
            stage("Make a list of the numbers as text.",
                  "str(5) turns the number 5 into the text \"5\". result.append(x) adds x to the end of a list.",
                  "def fizzbuzz(n):\n    result = []\n    for i in range(1, n + 1):\n        result.append(str(i))\n    return result\n",
                  [test("fizzbuzz(3) is [\"1\", \"2\", \"3\"] for now", 'check(fizzbuzz(2), ["1", "2"])')],
                  starter="def fizzbuzz(n):\n    pass\n"),
            stage("Say Fizz for multiples of 3.",
                  "Inside the loop, use if i % 3 == 0: to add \"Fizz\" instead of the number.",
                  "def fizzbuzz(n):\n    result = []\n    for i in range(1, n + 1):\n        if i % 3 == 0:\n            result.append(\"Fizz\")\n        else:\n            result.append(str(i))\n    return result\n",
                  [test("3 is Fizz", 'check(fizzbuzz(3)[2], "Fizz")')]),
        ],
        "solution": ("def fizzbuzz(n):\n    result = []\n    for i in range(1, n + 1):\n"
                     "        if i % 15 == 0:\n            result.append(\"FizzBuzz\")\n"
                     "        elif i % 3 == 0:\n            result.append(\"Fizz\")\n"
                     "        elif i % 5 == 0:\n            result.append(\"Buzz\")\n"
                     "        else:\n            result.append(str(i))\n    return result\n"),
        "solution_note": T("A number that divides by both 3 and 5 divides by 15, so that check comes first."),
        **COMMON,
    },
    {
        "id": "py-to-binary", "language": "python", "level": "Advanced", "age_group": "teen+", "topic": "general",
        "title": T("Write a number in binary"),
        "prompt": T("Write a function to_binary(n). It gives back the binary digits of a whole number n (0 or more) as text. "
                    "Example: 5 becomes \"101\". Do not use the built-in bin() function."),
        "concepts": T(["binary numbers", "while loops", "remainder (%) and whole-number division (//)", "building text"]),
        "starter": "def to_binary(n):\n    # return the binary digits of n as text\n    pass\n",
        "preamble": "def bin(*args, **kwargs):\n    raise NameError('Please do not use bin().')\n",
        "tests": [
            test("5 is 101", 'check(to_binary(5), "101")'),
            test("0 is 0", 'check(to_binary(0), "0")'),
            test("8 is 1000", 'check(to_binary(8), "1000")'),
            test("10 is 1010", 'check(to_binary(10), "1010")'),
            test("255 is 11111111", 'check(to_binary(255), "11111111")'),
        ],
        "hints": T([
            "The last binary digit of n is n % 2. Then divide n by 2 with // and repeat until n is 0.",
            "The digits come out last-first. Put each new digit at the front of the text, not the end.",
            "Zero is a special case: its answer is \"0\", but the loop would give an empty text.",
        ]),
        "guided": [
            stage("Find the last binary digit.",
                  "A number's last binary digit is its remainder when you divide by 2. n % 2 is 0 or 1. Give it back as text.",
                  "def to_binary(n):\n    return str(n % 2)\n",
                  [test("6 ends in 0", 'check(to_binary(6), "0")'), test("7 ends in 1", 'check(to_binary(7), "1")')],
                  starter="def to_binary(n):\n    pass\n"),
            stage("Collect every digit, even if they come out backwards.",
                  "Repeat while n > 0: add the last digit, then do n = n // 2 to drop it. The digits will be in reverse order for now.",
                  "def to_binary(n):\n    digits = \"\"\n    while n > 0:\n        digits += str(n % 2)\n        n = n // 2\n    return digits\n",
                  [test("6 comes out backwards as 011", 'check(to_binary(6), "011")')]),
        ],
        "solution": ("def to_binary(n):\n    if n == 0:\n        return \"0\"\n    digits = \"\"\n    while n > 0:\n"
                     "        digits = str(n % 2) + digits\n        n = n // 2\n    return digits\n"),
        "solution_note": T("Each step peels off the last binary digit. Putting new digits at the front fixes the order."),
        **COMMON,
    },
    # -------------------------------------------------------------- JavaScript
    {
        "id": "js-hello", "language": "javascript", "level": "Beginner", "age_group": "8-10", "topic": "general",
        "title": T("Say hello"),
        "prompt": T("Make the computer say hello. Use console.log to show the words Hello, world! on the screen."),
        "concepts": T(["console.log", "text in quote marks"]),
        "starter": "// Write your code here.\n",
        "tests": [
            test("It prints exactly Hello, world!", 'assertEqual(output.trim(), "Hello, world!")'),
            test("It prints one line", 'assertEqual(output.trim().split("\\n").length, 1)'),
        ],
        "hints": T([
            "Use console.log to show something on the screen.",
            "Text goes inside quote marks, inside the brackets: console.log(\"...\");",
            "Type the words exactly: capital H, a comma, and an exclamation mark at the end.",
        ]),
        "guided": [
            stage("Print any word.",
                  "console.log(...) shows what is inside the brackets. Words must be inside quote marks, like \"hi\".",
                  'console.log("hi");\n',
                  [test("Something is printed", "assert(output.trim().length > 0, \"Nothing was printed yet.\")")],
                  starter="// Try printing the word hi.\n"),
        ],
        "solution": 'console.log("Hello, world!");\n',
        "solution_note": T("console.log shows text. The words are inside quote marks so JavaScript knows they are text."),
        **COMMON,
    },
    {
        "id": "js-add", "language": "javascript", "level": "Beginner", "age_group": "11-13", "topic": "general",
        "title": T("Add two numbers"),
        "prompt": T("Write a function called add. It takes two numbers, a and b, and gives back their sum."),
        "concepts": T(["functions", "return", "adding"]),
        "starter": "function add(a, b) {\n  // give back a plus b\n}\n",
        "tests": [
            test("add(2, 3) is 5", "assertEqual(add(2, 3), 5)"),
            test("add(-1, 1) is 0", "assertEqual(add(-1, 1), 0)"),
            test("add(0.5, 0.25) is 0.75", "assertEqual(add(0.5, 0.25), 0.75)"),
            test("add(10, 0) is 10", "assertEqual(add(10, 0), 10)"),
        ],
        "hints": T([
            "A function gives a value back with the word return.",
            "In JavaScript, the + sign adds two numbers.",
            "The body is one line: return, then a plus b, then a semicolon.",
        ]),
        "guided": [
            stage("Give a value back.",
                  "return sends a value out of the function. For now, just give back a.",
                  "function add(a, b) {\n  return a;\n}\n",
                  [test("It gives back a", "assertEqual(add(7, 0), 7)")],
                  starter="function add(a, b) {\n}\n"),
        ],
        "solution": "function add(a, b) {\n  return a + b;\n}\n",
        "solution_note": T("return a + b; hands the sum back to whoever called the function."),
        **COMMON,
    },
    {
        "id": "js-find-max", "language": "javascript", "level": "Beginner", "age_group": "11-13", "topic": "general",
        "title": T("Find the biggest number"),
        "prompt": T("Write a function findMax(numbers). It gives back the biggest number in the list. If the list is empty, give back null. "
                    "Do not use Math.max."),
        "concepts": T(["arrays", "loops", "if", "comparing numbers"]),
        "starter": "function findMax(numbers) {\n  // give back the biggest number\n}\n",
        "tests": [
            test("The biggest of [3, 9, 2] is 9", "assertEqual(findMax([3, 9, 2]), 9)"),
            test("Negative numbers work", "assertEqual(findMax([-5, -2, -9]), -2)"),
            test("One number is its own biggest", "assertEqual(findMax([7]), 7)"),
            test("An empty list gives null", "assertEqual(findMax([]), null)"),
            test("It does not use Math.max", 'assert(!findMax.toString().includes("Math.max"), "Please do not use Math.max.")'),
        ],
        "hints": T([
            "Keep a variable for the biggest number you have seen so far.",
            "Start it as the first item. Then look at the other items one by one.",
            "If an item is bigger than your variable, put that item in the variable. Handle the empty list first.",
        ]),
        "guided": [
            stage("Handle the empty list.",
                  "numbers.length is how many items there are. If it is 0, return null.",
                  "function findMax(numbers) {\n  if (numbers.length === 0) return null;\n  return numbers[0];\n}\n",
                  [test("An empty list gives null", "assertEqual(findMax([]), null)")],
                  starter="function findMax(numbers) {\n}\n"),
            stage("Start with the first number as the biggest.",
                  "numbers[0] is the first item. Keep it in a variable called biggest and return that.",
                  "function findMax(numbers) {\n  if (numbers.length === 0) return null;\n  let biggest = numbers[0];\n  return biggest;\n}\n",
                  [test("One number is its own biggest", "assertEqual(findMax([7]), 7)")]),
            stage("Look at every number.",
                  "Use for (const n of numbers) { ... }. If n is bigger than biggest, set biggest = n.",
                  "function findMax(numbers) {\n  if (numbers.length === 0) return null;\n  let biggest = numbers[0];\n  for (const n of numbers) {\n    if (n > biggest) biggest = n;\n  }\n  return biggest;\n}\n",
                  [test("The biggest of [3, 9, 2] is 9", "assertEqual(findMax([3, 9, 2]), 9)")]),
        ],
        "solution": "function findMax(numbers) {\n  if (numbers.length === 0) return null;\n  let biggest = numbers[0];\n  for (const n of numbers) {\n    if (n > biggest) biggest = n;\n  }\n  return biggest;\n}\n",
        "solution_note": T("The variable biggest always holds the largest number seen so far."),
        **COMMON,
    },
    {
        "id": "js-count-vowels", "language": "javascript", "level": "Intermediate", "age_group": "11-13", "topic": "general",
        "title": T("Count the vowels"),
        "prompt": T("Write a function countVowels(text). It gives back how many vowels (a, e, i, o, u) are in the text. Capital letters count too."),
        "concepts": T(["strings", "loops", "includes", "lower case"]),
        "starter": "function countVowels(text) {\n  // count a, e, i, o and u\n}\n",
        "tests": [
            test("hello has 2 vowels", 'assertEqual(countVowels("hello"), 2)'),
            test("Capital letters count", 'assertEqual(countVowels("AEIOU"), 5)'),
            test("Empty text has 0", 'assertEqual(countVowels(""), 0)'),
            test("rhythm has 0", 'assertEqual(countVowels("rhythm"), 0)'),
            test("A whole sentence", 'assertEqual(countVowels("Programming is fun"), 5)'),
        ],
        "hints": T([
            "You can loop over the letters of a text with for (const ch of text).",
            "\"aeiou\".includes(ch) is true when ch is a vowel.",
            "Capital letters are not in \"aeiou\". Make the text lower case first with text.toLowerCase().",
        ]),
        "guided": [
            stage("Count every letter.",
                  "for (const ch of text) goes through the text one letter at a time. Add 1 to count each time.",
                  "function countVowels(text) {\n  let count = 0;\n  for (const ch of text) {\n    count++;\n  }\n  return count;\n}\n",
                  [test("It counts every letter for now", 'assertEqual(countVowels("abc"), 3)')],
                  starter="function countVowels(text) {\n}\n"),
            stage("Count only the vowels.",
                  "Add an if: \"aeiou\".includes(ch) is true when ch is a vowel. Only then add 1.",
                  "function countVowels(text) {\n  let count = 0;\n  for (const ch of text) {\n    if (\"aeiou\".includes(ch)) count++;\n  }\n  return count;\n}\n",
                  [test("hello has 2 vowels", 'assertEqual(countVowels("hello"), 2)')]),
        ],
        "solution": "function countVowels(text) {\n  let count = 0;\n  for (const ch of text.toLowerCase()) {\n    if (\"aeiou\".includes(ch)) count++;\n  }\n  return count;\n}\n",
        "solution_note": T("toLowerCase makes A and a the same, so one check finds both."),
        **COMMON,
    },
    {
        "id": "js-sort-numbers", "language": "javascript", "level": "Intermediate", "age_group": "teen+", "topic": "general",
        "title": T("Sort a list by hand"),
        "prompt": T("Write a function sortNumbers(numbers). It gives back a NEW list with the same numbers from smallest to biggest. "
                    "Do not change the list you were given, and do not use .sort()."),
        "concepts": T(["arrays", "nested loops", "swapping", "sorting"]),
        "starter": "function sortNumbers(numbers) {\n  // give back a new, sorted list\n}\n",
        "tests": [
            test("[3, 1, 2] becomes [1, 2, 3]", "assertEqual(sortNumbers([3, 1, 2]), [1, 2, 3])"),
            test("A sorted list stays sorted", "assertEqual(sortNumbers([1, 2, 3]), [1, 2, 3])"),
            test("A backwards list", "assertEqual(sortNumbers([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])"),
            test("An empty list", "assertEqual(sortNumbers([]), [])"),
            test("Repeated numbers", "assertEqual(sortNumbers([2, 2, 1]), [1, 2, 2])"),
            test("The original list is not changed", "const a = [3, 1, 2]; sortNumbers(a); assertEqual(a, [3, 1, 2])"),
            test("It does not use .sort()", 'assert(!sortNumbers.toString().includes(".sort("), "Please do not use .sort().")'),
        ],
        "hints": T([
            "Make a copy first: const result = [...numbers]; Then change only the copy.",
            "Compare each item with the one next to it. If they are the wrong way round, swap them.",
            "One pass along the list is not enough for every list. Repeat the passes (a loop inside a loop).",
        ]),
        "guided": [
            stage("Make a copy and return it.",
                  "[...numbers] makes a new list with the same items. Changing the copy leaves the original alone.",
                  "function sortNumbers(numbers) {\n  const result = [...numbers];\n  return result;\n}\n",
                  [test("It returns a new list", "const a = [2, 1]; const r = sortNumbers(a); assert(Array.isArray(r) && r !== a, \"Return a new list, not the same one.\")")],
                  starter="function sortNumbers(numbers) {\n}\n"),
            stage("Make one pass: swap neighbours that are the wrong way round.",
                  "Loop i from 0 to length - 2. If result[i] > result[i + 1], swap them using a temporary variable.",
                  "function sortNumbers(numbers) {\n  const result = [...numbers];\n  for (let i = 0; i < result.length - 1; i++) {\n    if (result[i] > result[i + 1]) {\n      const temp = result[i];\n      result[i] = result[i + 1];\n      result[i + 1] = temp;\n    }\n  }\n  return result;\n}\n",
                  [test("[2, 1] becomes [1, 2]", "assertEqual(sortNumbers([2, 1]), [1, 2])"),
                   test("[1, 3, 2] becomes [1, 2, 3]", "assertEqual(sortNumbers([1, 3, 2]), [1, 2, 3])")]),
        ],
        "solution": ("function sortNumbers(numbers) {\n  const result = [...numbers];\n"
                     "  for (let pass = 0; pass < result.length; pass++) {\n"
                     "    for (let i = 0; i < result.length - 1 - pass; i++) {\n"
                     "      if (result[i] > result[i + 1]) {\n"
                     "        const temp = result[i];\n        result[i] = result[i + 1];\n        result[i + 1] = temp;\n"
                     "      }\n    }\n  }\n  return result;\n}\n"),
        "solution_note": T("Each pass pushes the biggest remaining number to the end. This is called bubble sort."),
        **COMMON,
    },
    {
        "id": "js-binary-search", "language": "javascript", "level": "Advanced", "age_group": "teen+", "topic": "general",
        "title": T("Binary search"),
        "prompt": T("Write a function binarySearch(sorted, target). The list is sorted from smallest to biggest. "
                    "Give back the position (index) of target, or -1 if it is not there. Do it by halving the part you search each time."),
        "concepts": T(["binary search", "divide and conquer", "while loops", "indexes"]),
        "starter": "function binarySearch(sorted, target) {\n  // give back the index of target, or -1\n}\n",
        "tests": [
            test("7 is at position 3", "assertEqual(binarySearch([1, 3, 5, 7, 9], 7), 3)"),
            test("The first item", "assertEqual(binarySearch([1, 3, 5, 7, 9], 1), 0)"),
            test("The last item", "assertEqual(binarySearch([1, 3, 5, 7, 9], 9), 4)"),
            test("A missing number gives -1", "assertEqual(binarySearch([1, 3, 5, 7, 9], 4), -1)"),
            test("An empty list gives -1", "assertEqual(binarySearch([], 1), -1)"),
            test("A list with one item", "assertEqual(binarySearch([2], 2), 0)"),
            test("A big list", "const big = Array.from({ length: 1000 }, (_, i) => i * 2); assertEqual(binarySearch(big, 998), 499); assertEqual(binarySearch(big, 999), -1)"),
        ],
        "hints": T([
            "Keep two positions, low and high. The target can only be between them.",
            "Look at the middle item: mid = Math.floor((low + high) / 2). Is it the target, too small, or too big?",
            "If the middle is too small, the target is on the right: set low = mid + 1. If too big, set high = mid - 1. Stop when low is more than high.",
        ]),
        "guided": [
            stage("Check the middle item.",
                  "Math.floor(sorted.length / 2) is the middle position. If that item is the target, return its position. Otherwise return -1 for now.",
                  "function binarySearch(sorted, target) {\n  const mid = Math.floor(sorted.length / 2);\n  if (sorted[mid] === target) return mid;\n  return -1;\n}\n",
                  [test("The middle of [1, 3, 5] is found", "assertEqual(binarySearch([1, 3, 5], 3), 1)"),
                   test("4 is not in [1, 3, 5]", "assertEqual(binarySearch([1, 3, 5], 4), -1)")],
                  starter="function binarySearch(sorted, target) {\n}\n"),
            stage("Search the right half when the middle is too small.",
                  "Use low and high and a while (low <= high) loop. When sorted[mid] < target, set low = mid + 1. For now, if the middle is too big, just return -1.",
                  "function binarySearch(sorted, target) {\n  let low = 0;\n  let high = sorted.length - 1;\n  while (low <= high) {\n    const mid = Math.floor((low + high) / 2);\n    if (sorted[mid] === target) return mid;\n    if (sorted[mid] < target) low = mid + 1;\n    else return -1;\n  }\n  return -1;\n}\n",
                  [test("9 is found on the right", "assertEqual(binarySearch([1, 3, 5, 7, 9], 9), 4)"),
                   test("7 is found on the right", "assertEqual(binarySearch([1, 3, 5, 7, 9], 7), 3)")]),
        ],
        "solution": ("function binarySearch(sorted, target) {\n  let low = 0;\n  let high = sorted.length - 1;\n"
                     "  while (low <= high) {\n    const mid = Math.floor((low + high) / 2);\n"
                     "    if (sorted[mid] === target) return mid;\n"
                     "    if (sorted[mid] < target) low = mid + 1;\n    else high = mid - 1;\n  }\n  return -1;\n}\n"),
        "solution_note": T("Each step throws away half of the list, so 1000 items need only about 10 looks."),
        **COMMON,
    },
]
