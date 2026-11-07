"""Coverage of the 'What should I learn?' guide + stats summary.

For each of the 36 guide combinations (3 ages x 4 goals x 3 levels) count the
kid-safe entries that fit: safety == kid-safe, level matches, topic matches the goal
("general" accepts any kid topic), and the entry's youngest-suitable age <= chosen age.
Combinations with fewer than 6 entries are flagged (the guide shows a 6-step path).

Usage: python scripts/coverage.py
"""
import json
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "src" / "data"
AGES = ["5-7", "8-10", "11-13"]
ALL_AGES = AGES + ["teen+"]
GOALS = ["games", "art", "web", "general"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
NEEDED = 6


def load():
    return [e for n in ("learn", "build") for e in json.loads((DATA / f"{n}.json").read_text())]


def fits(e, age, goal, level):
    return (e["safety"] == "kid-safe" and e["level"] == level
            and (goal == "general" or e["topic"] == goal)
            and ALL_AGES.index(e["age_group"]) <= ALL_AGES.index(age))


def main():
    entries = load()
    print(f"Total entries: {len(entries)}\n")
    for label, key in [("level", "level"), ("topic", "topic"), ("age_group", "age_group"), ("safety", "safety")]:
        print(f"By {label}: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(e[key] for e in entries).items())))
    print("By source: " + ", ".join(f"{k.split('github.com/')[-1]}={v}"
                                    for k, v in sorted(Counter(e['source'] for e in entries).items())))
    reasons = Counter(r for e in entries for r in e["safety_reasons"])
    print("Top safety reasons: " + ", ".join(f"{k}={v}" for k, v in reasons.most_common(8)))
    only_unvetted = sum(e["safety_reasons"] == ["unvetted-external-site"] for e in entries)
    print(f"Entries held back ONLY because the host is unvetted: {only_unvetted}\n")

    print(f"Guide coverage (kid-safe entries per combination; need >= {NEEDED}):")
    print(f"{'age':6}{'goal':9}" + "".join(f"{l:>14}" for l in LEVELS))
    gaps = 0
    for age in AGES:
        for goal in GOALS:
            counts = [sum(fits(e, age, goal, lv) for e in entries) for lv in LEVELS]
            gaps += sum(c < NEEDED for c in counts)
            print(f"{age:6}{goal:9}" + "".join(f"{str(c) + (' !' if c < NEEDED else ''):>14}" for c in counts))
    print(f"\nCombinations below {NEEDED}: {gaps} of 36")


if __name__ == "__main__":
    main()
