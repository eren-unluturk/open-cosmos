"""WCAG AA contrast check of the colour themes (galaxy, light, contrast, cb) from the CSS tokens.

Reads :root in public/static/galaxy.css (the galaxy theme) and the html[data-theme=...] blocks in a11y.css, then
checks the text/background pairs the site actually uses: 4.5:1 for normal text, 3:1 for large text and UI parts.
Semi-transparent colours are blended over the page background first. Exit code 1 if any pair fails.
Real pages are checked separately with axe (scripts/a11y_audit.py).

Usage: python scripts/check_contrast.py [--table]   (--table prints a Markdown table for docs/ACCESSIBILITY.md)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "src" / "static"
THEMES = ("galaxy", "light", "contrast", "cb")


def parse_tokens(block):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"--([\w-]+):\s*([^;]+);", block)}


def load_themes():
    galaxy_css = (STATIC / "galaxy.css").read_text(encoding="utf-8")
    root = parse_tokens(re.search(r":root\s*\{(.*?)\n\}", galaxy_css, re.S).group(1))
    a11y_css = (STATIC / "a11y.css").read_text(encoding="utf-8")
    themes = {"galaxy": dict(root)}
    for name in THEMES[1:]:
        m = re.search(r'html\[data-theme="%s"\]\s*\{(.*?)\n\}' % name, a11y_css, re.S)
        themes[name] = {**root, **parse_tokens(m.group(1))}
    return themes


def parse_color(value, tokens, depth=0):
    """-> (r, g, b, a) with a in 0..1. Understands #hex, rgb()/rgba() and var(--x)."""
    value = value.strip()
    m = re.fullmatch(r"var\(--([\w-]+)\)", value)
    if m and depth < 6:
        return parse_color(tokens[m.group(1)], tokens, depth + 1)
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0
    m = re.fullmatch(r"rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\s*\)", value)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4) or 1)
    raise ValueError(f"cannot parse colour {value!r}")


def blend(top, bottom):
    r, g, b, a = top
    return tuple(round(a * t + (1 - a) * u) for t, u in zip((r, g, b), bottom[:3])) + (1.0,)


def luminance(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# (foreground, background, minimum ratio, where it is used). A background written "x@N over y" is token x at N% alpha over y.
PAIRS = [
    ("moon", "night", 4.5, "body text on the page"),
    ("moon", "navy", 4.5, "text on cards and panels"),
    ("moon", "card", 4.5, "text on translucent cards (over the page)"),
    ("mist", "night", 4.5, "muted text on the page"),
    ("mist", "navy", 4.5, "muted text on cards"),
    ("soft", "night", 4.5, "lead paragraphs"),
    ("soft", "navy", 4.5, "lead paragraphs on cards"),
    ("gold", "night", 4.5, "links and accents on the page"),
    ("gold", "navy", 4.5, "links and accents on cards"),
    ("sun", "night", 4.5, "link hover on the page"),
    ("lilac", "navy", 4.5, "lilac text on cards"),
    ("teal", "navy", 4.5, "teal chips on cards"),
    ("pink", "navy", 4.5, "pink chips on cards"),
    ("gold", "gold@8 over navy", 4.5, "gold chip"),
    ("gold", "gold@16 over navy", 4.5, "warning flag"),
    ("lilac", "purple@25 over navy", 4.5, "AI-translated flag"),
    ("moon", "mist@18 over navy", 4.5, "plain flag"),
    ("moon", "purple@18 over navy", 4.5, "talk-about bubbles"),
    ("on-violet", "violet", 4.5, "text on violet buttons"),
    ("on-violet", "nebula", 4.5, "grown-up bar (dark end)"),
    ("on-violet", "violet", 4.5, "grown-up bar (light end)"),
    ("night", "moon", 4.5, "tooltips and skip-link style surfaces"),
    ("moon", "code-bg", 4.5, "code boxes"),
    ("sun", "disc-a", 4.5, "icon discs"),
    ("gold", "gold@14 over night", 3.0, "icon on tinted disc (UI part)"),
    # UI parts and large text: 3:1
    ("gold", "night", 3.0, "focus outline on the page"),
    ("gold", "navy", 3.0, "focus outline on cards"),
    ("ui-border", "night", 3.0, "borders that identify a control (buttons, inputs, code box)"),
    ("ui-border", "navy", 3.0, "control borders on cards"),
    ("mist", "night", 3.0, "icons"),
]
BUTTONS = [  # the gold button is a gradient: check its text against every stop
    ("on-gold", "sun"), ("on-gold", "gold"), ("on-gold", "amber"),
]
LIGHT_BTN = ("#231600", "#FFE08A", "#F4B942")  # light theme overrides .btn-gold with a fixed light gradient


def resolve(spec, tokens, night):
    if " over " in spec:
        top, over = spec.split(" over ")
        name, alpha = top.split("@")
        c = parse_color(f"var(--{name})", tokens)
        under = parse_color(f"var(--{over})", tokens)
        under = blend(under, parse_color(f"var(--night)", tokens)) if under[3] < 1 else under
        return blend((c[0], c[1], c[2], int(alpha) / 100), under)
    c = parse_color(f"var(--{spec})", tokens)
    if c[3] < 1:
        c = blend(c, parse_color("var(--night)", tokens))
    return c


def check():
    rows, fails = [], []
    for theme, tokens in load_themes().items():
        for fg, bg, need, where in PAIRS:
            f = resolve(fg, tokens, None)
            b = resolve(bg, tokens, None)
            r = ratio(f, b)
            ok = r >= need
            rows.append((theme, fg, bg, need, r, ok, where))
            if not ok:
                fails.append(rows[-1])
        stops = [(fg, bg) for fg, bg in BUTTONS]
        for fg, bg in stops:
            if theme == "light":
                f = parse_color(LIGHT_BTN[0], tokens)
                b = parse_color(LIGHT_BTN[1 if bg == "sun" else 2], tokens)
            else:
                f, b = resolve(fg, tokens, None), resolve(bg, tokens, None)
            r = ratio(f, b)
            rows.append((theme, fg, f"btn-gold {bg}", 4.5, r, r >= 4.5, "gold button text"))
            if r < 4.5:
                fails.append(rows[-1])
    return rows, fails


def main():
    rows, fails = check()
    if "--table" in sys.argv:
        print("| Theme | Text / UI part | On | Needs | Ratio | Where |\n|---|---|---|---|---|---|")
        for theme, fg, bg, need, r, ok, where in rows:
            print(f"| {theme} | {fg} | {bg} | {need}:1 | {r:.2f}:1 {'ok' if ok else 'FAIL'} | {where} |")
    for theme, fg, bg, need, r, ok, where in fails:
        print(f"FAIL {theme}: {fg} on {bg} = {r:.2f}:1 (needs {need}:1) - {where}")
    print(f"{len(rows)} pairs checked, {len(fails)} below WCAG AA")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
