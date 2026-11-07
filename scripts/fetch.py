"""Fetch the two CC0 source READMEs and parse them into English-only JSON.

Output: src/data/learn.json and src/data/build.json following the data contract:
  {id, category, title:{en}, desc:{en}, level, url, source, license}

Usage: python scripts/fetch.py
"""
import json
import re
from pathlib import Path

import requests

DATA = Path(__file__).resolve().parent.parent / "src" / "data"

SOURCES = {
    "learn": {
        "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
        "repo": "https://github.com/sindresorhus/awesome",
        "license": "CC0-1.0",
    },
    "build": {
        "url": "https://raw.githubusercontent.com/codecrafters-io/build-your-own-x/master/README.md",
        "repo": "https://github.com/codecrafters-io/build-your-own-x",
        "license": "CC0-1.0",
    },
}

LINK = re.compile(r"^\s*[*-]\s+(?:\*\*(?P<tag>[^*]+)\*\*:\s*)?\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*(?:[-–]\s*(?P<desc>.*))?$")


def parse(markdown: str, source: str, repo: str, license_: str):
    entries, category = [], "General"
    for line in markdown.splitlines():
        heading = re.match(r"^#{2,4}\s+(.*)", line)
        if heading:
            category = re.sub(r"[*_`]", "", heading.group(1)).strip()
            continue
        m = LINK.match(line)
        if not m or m.group("url").startswith("#"):
            continue  # skip non-links and table-of-contents anchors
        entries.append({
            "id": f"{source}-{len(entries)}",
            "category": category,
            "title": {"en": m.group("title").strip()},
            "desc": {"en": (m.group("desc") or "").strip()},
            "level": None,  # assigned by scripts/translate.py
            "url": m.group("url").strip(),
            "source": repo,
            "license": license_,
        })
    return entries


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    for name, cfg in SOURCES.items():
        text = requests.get(cfg["url"], timeout=30).text
        entries = parse(text, name, cfg["repo"], cfg["license"])
        (DATA / f"{name}.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2))
        print(f"{name}: {len(entries)} entries")


if __name__ == "__main__":
    main()
