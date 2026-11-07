"""Fetch the two CC0 source READMEs and parse them into English-only JSON.

Output: src/data/learn.json and src/data/build.json (see data contract in docs/PLAN.md).
fetch.py only fills the base fields; categorize.py and translate.py add the rest.
Re-running keeps any enrichment already stored for an entry (matched by id), and
ids are derived from the URL so they stay stable between runs.

Usage: python scripts/fetch.py
"""
import hashlib
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

# "* [link text](url) optional trailing text"; link text may be "**Lang**: _Title_"
LINK = re.compile(r"^\s*[*-]\s+\[(?P<text>.+?)\]\((?P<url>[^)\s]+)\)\s*(?P<rest>.*)$")
TAGGED = re.compile(r"^\*\*(?P<tag>[^*]+)\*\*:\s*(?P<title>.+)$")
BASE_FIELDS = ("category", "tag", "url", "source", "license")


def clean(text: str) -> str:
    """Strip markdown emphasis/backticks and collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", text)).strip()


def entry_id(source: str, url: str) -> str:
    return f"{source}-{hashlib.sha1(url.encode()).hexdigest()[:8]}"


def parse(markdown: str, source: str, repo: str, license_: str):
    entries, seen, category = [], set(), "General"
    for line in markdown.splitlines():
        heading = re.match(r"^#{2,4}\s+(.*)", line)
        if heading:
            category = clean(heading.group(1)) or category
            continue
        m = LINK.match(line)
        if not m:
            continue
        url = m.group("url").strip()
        if url.startswith("#") or url in seen:
            continue  # table-of-contents anchor, or duplicate URL (first one wins)
        seen.add(url)
        text, tag = m.group("text").strip(), ""
        t = TAGGED.match(text)
        if t:
            tag, text = clean(t.group("tag")), t.group("title")
        rest = m.group("rest").strip()
        desc = clean(re.sub(r"^[-–]\s*", "", rest)) if re.match(r"^[-–]\s", rest) else ""
        entries.append({
            "id": entry_id(source, url),
            "category": category,
            "tag": tag,
            "title": {"en": clean(text)},
            "desc": {"en": desc},
            "level": None,
            "url": url,
            "source": repo,
            "license": license_,
        })
    return entries


REMOVED = Path(__file__).resolve().parent / "cache" / "removed_links.json"  # url -> reason (dead links)


def drop_removed(entries):
    removed = json.loads(REMOVED.read_text()) if REMOVED.exists() else {}
    return [e for e in entries if e["url"] not in removed]


def merge(new, path: Path):
    """Keep enrichment (level, topic, safety, translations...) from a previous run."""
    if not path.exists():
        return new
    old = {e["id"]: e for e in json.loads(path.read_text())}
    for e in new:
        prev = old.get(e["id"])
        if not prev:
            continue
        for k, v in prev.items():
            if k in BASE_FIELDS or k == "id":
                continue
            if k in ("title", "desc"):
                e[k] = {**v, "en": e[k]["en"]}  # keep translations, refresh English
            else:
                e[k] = v
    return new


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    for name, cfg in SOURCES.items():
        text = requests.get(cfg["url"], timeout=30).text
        entries = parse(text, name, cfg["repo"], cfg["license"])
        path = DATA / f"{name}.json"
        entries = merge(drop_removed(entries), path)
        path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
        print(f"{name}: {len(entries)} entries")


if __name__ == "__main__":
    main()
