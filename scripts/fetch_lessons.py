"""Fetch lesson text for the hostable CS Unplugged lessons into src/data/lessons.json.

Why we may: CS Unplugged content is CC BY-SA 4.0 (LICENCE-CONTENT: markdown under
csunplugged/topics/content/). We keep it in its own file, show the credit line on every page,
and share translations under the same license. See docs/SOURCES.md.

What we store per lesson: the markdown, lightly cleaned. English always; Spanish when the
CS Unplugged project has its own human translation of that lesson (preferred over AI).
Images are NOT copied yet; the image's alt text stays in the page as a description.
Videos stay external links.

Run after fetch_kids.py:  python scripts/fetch_lessons.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
RAW = "https://raw.githubusercontent.com/uccser/cs-unplugged/develop/csunplugged/topics/content"
HUMAN_LANGS = {"es": "es"}  # site language -> CS Unplugged content folder (human translations only)
LICENSE = "CC-BY-SA-4.0"


def source_path(url, lang):
    """csunplugged.org page URL -> markdown path in the repo, or None (we only host units and lessons)."""
    parts = [p for p in urlparse(url).path.split("/") if p]  # ['en','topics',topic,(lesson)]
    if len(parts) < 3 or parts[1] != "topics":
        return None
    if len(parts) == 3:
        return f"{lang}/{parts[2]}/{parts[2]}.md"
    if len(parts) == 4 and parts[3] not in ("programming", "integrations"):
        return f"{lang}/{parts[2]}/lessons/{parts[3]}.md"
    return None


TAG_LINE = re.compile(r"^[ \t]*\{[a-z-]+[^}\n]*\}[ \t]*$")


def clean(md):
    """Turn CS Unplugged's template tags into plain markdown. Safe to render with HTML disabled."""
    out, prev_panel = [], False
    md = md.replace("\r\n", "\n")
    # A few image tags wrap their alt text over several lines. Put each tag on one line first.
    md = re.sub(r"\{(?:image|video|button-link)[^}]*\}", lambda m: re.sub(r"\s*\n\s*", " ", m.group(0)), md)
    for line in md.split("\n"):
        stripped = line.strip()
        if stripped.startswith("{panel ") and stripped != "{panel end}":
            prev_panel = True
            continue
        if stripped == "{panel end}":
            continue
        if prev_panel and stripped.startswith("#"):
            indent = line[: len(line) - len(line.lstrip())]
            out.append(f"{indent}**{stripped.lstrip('#').strip()}**")
            prev_panel = False
            continue
        if stripped:
            prev_panel = False
        m = re.match(r"^(\s*)\{video url=\"([^\"]+)\"[^}]*\}\s*$", line)
        if m:
            out.append(f"{m.group(1)}[Watch the video (opens another site)]({m.group(2)})")
            continue
        m = re.match(r"^(\s*)\{image [^}]*alt=\"([^\"]*)\"[^}]*\}\s*$", line)
        if m:
            alt = m.group(2).strip()
            out.append(f"{m.group(1)}*(Picture: {alt})*" if alt else "")
            continue
        m = re.match(r"^(\s*)\{button-link link=\"([^\"]+)\" text=\"([^\"]+)\"[^}]*\}\s*$", line)
        if m:
            out.append(f"{m.group(1)}[{m.group(3)}]({m.group(2)})")
            continue
        if TAG_LINE.match(line):  # any other whole-line tag (resources, comments, interactives)
            continue
        # Links that point inside the CS Unplugged site framework (not real web addresses): keep the words only.
        line = re.sub(r"\[([^\]]+)\]\((?!https?://|mailto:|#)[^)]*\)", r"\1", line)
        line = re.sub(r"\{glossary-link [^}]*\}(.*?)\{glossary-link end\}", r"\1", line)
        line = re.sub(r"\{(?:math|filename|noprint)[^}]*\}", "", line)
        out.append(line)
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def get(path):
    r = requests.get(f"{RAW}/{path}", timeout=30)
    return r.text if r.status_code == 200 else None


def main():
    sys.path.insert(0, str(ROOT / "src"))
    import store  # noqa: E402  (reads kids.json, adds the delivery fields)
    lessons, missing = {}, []
    for e in store.entries("kids"):
        if e["delivery"] != "hostable" or e["kind"] not in ("unit", "lesson"):
            continue
        en_path = source_path(e["url"], "en")
        body_en = get(en_path) if en_path else None
        if not body_en:
            missing.append(e["url"])
            continue
        body = {"en": clean(body_en)}
        for site_lang, folder in HUMAN_LANGS.items():
            text = get(source_path(e["url"], folder))
            if text:
                body[site_lang] = clean(text)
        lessons[e["id"]] = {"path": en_path, "license": LICENSE, "body": body}
        print(f"{e['kind']:6} {en_path}  langs={','.join(body)}  chars={len(body['en'])}")
    out = DATA / "lessons.json"
    out.write_text(json.dumps(lessons, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\n{len(lessons)} lessons written. Missing source: {missing or 'none'}")


if __name__ == "__main__":
    main()
