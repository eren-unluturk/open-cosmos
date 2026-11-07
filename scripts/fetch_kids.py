"""Fetch CS Unplugged (kid-friendly, CC BY-SA 4.0) lesson metadata into src/data/kids.json.

We store ONLY: the lesson title, a short description we write ourselves, the age group the
repo states, and a link to the original lesson page. No lesson text or images are copied.
Content license: CC BY-SA 4.0 (LICENCE-CONTENT in the repo). See docs/SOURCES.md.
Run AFTER fetch.py and BEFORE categorize.py.

Usage: python scripts/fetch_kids.py
"""
import json
import re
from pathlib import Path

import requests

from fetch import DATA, entry_id, merge  # same helpers as the CC0 sources

REPO = "https://github.com/uccser/cs-unplugged"
RAW = "https://raw.githubusercontent.com/uccser/cs-unplugged/develop/csunplugged/topics/content"
SITE = "https://www.csunplugged.org/en/topics"
LICENSE = "CC-BY-SA-4.0"
# The repo's age groups are 5-7, 8-10 and 11-14; our contract's top kid group is 11-13.
AGE_MAP = {"5-7": "5-7", "8-10": "8-10", "11-14": "11-13"}
AGE_ORDER = ["5-7", "8-10", "11-13"]


def get(path):
    r = requests.get(f"{RAW}/{path}", timeout=30)
    return r.text if r.status_code == 200 else ""


def first_heading(markdown, fallback):
    m = re.search(r"^#\s+(.+)$", markdown, re.M)
    return re.sub(r"[*_`]", "", m.group(1)).strip() if m else fallback


def parse_age_groups(yaml_text):
    """Minimal parse of the 'age-groups:' block -> {lesson_slug: youngest_age_group}."""
    out, in_block, age = {}, False, None
    for line in yaml_text.splitlines():
        if re.match(r"^age-groups:\s*$", line):
            in_block = True
            continue
        if in_block and re.match(r"^\S", line):
            break  # next top-level key
        if not in_block:
            continue
        m = re.match(r"^  ([\d-]+):\s*$", line)
        if m:
            age = AGE_MAP.get(m.group(1))
            continue
        m = re.match(r"^    ([a-z0-9-]+):\s*$", line)
        if m and age:
            slug = m.group(1)
            if slug not in out or AGE_ORDER.index(age) < AGE_ORDER.index(out[slug]):
                out[slug] = age
    return out


def parse_durations(yaml_text):
    out, slug = {}, None
    for line in yaml_text.splitlines():
        m = re.match(r"^([a-z0-9-]+):\s*$", line)
        if m:
            slug = m.group(1)
            continue
        m = re.match(r"^  duration:\s*(\d+)", line)
        if m and slug:
            out[slug] = int(m.group(1))
    return out


def make(url, title, desc, category, age):
    return {
        "id": entry_id("kids", url), "category": category, "tag": "",
        "title": {"en": title}, "desc": {"en": desc}, "level": None,
        "age_group": age, "url": url, "source": REPO, "license": LICENSE,
    }


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    structure = get("structure/structure.yaml")
    topics = re.findall(r"^  - ([a-z0-9-]+)\s*$", structure.split("age-groups:")[0], re.M)
    entries, seen = [], set()
    for topic in topics:
        topic_yaml = get(f"structure/{topic}/{topic}.yaml")
        ages = parse_age_groups(topic_yaml)
        durations = parse_durations(get(f"structure/{topic}/lessons/lessons.yaml"))
        topic_title = first_heading(get(f"en/{topic}/{topic}.md"), topic.replace("-", " ").title())
        if ages:
            url = f"{SITE}/{topic}/"
            youngest = min(ages.values(), key=AGE_ORDER.index)
            seen.add(url)
            entries.append(make(url, f"{topic_title} (unit)",
                                f"A CS Unplugged unit with several hands-on, screen-free lessons about {topic_title.lower()}.",
                                f"CS Unplugged: {topic_title}", youngest))
        for slug, age in ages.items():
            url = f"{SITE}/{topic}/{slug}/"
            if url in seen:
                continue
            seen.add(url)
            title = first_heading(get(f"en/{topic}/lessons/{slug}.md"), slug.replace("-", " ").title())
            mins = durations.get(slug)
            desc = (f"A hands-on, screen-free CS Unplugged lesson for ages {age}"
                    + (f" (about {mins} minutes)" if mins else "")
                    + f", part of the '{topic_title}' unit.")
            entries.append(make(url, title, desc, f"CS Unplugged: {topic_title}", age))
        print(f"{topic}: {len(ages)} lessons")
    entries.sort(key=lambda e: (e["category"], AGE_ORDER.index(e["age_group"]), e["title"]["en"].lower(), e["id"]))
    path = DATA / "kids.json"
    entries = merge(entries, path)
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
    print(f"kids: {len(entries)} entries")


if __name__ == "__main__":
    main()
