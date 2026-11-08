"""Reflow check (WCAG 1.4.10): no horizontal page scroll at 320 CSS px wide (400% zoom) and 640 px (200% zoom on a
1280 px screen), with default settings and with the largest text + roomy spacing + easy font. DEV ONLY (Playwright).

Usage: /tmp/a11yenv/bin/python scripts/a11y_reflow.py http://127.0.0.1:5000 [--langs en,ar]
"""
import argparse
import json
import sys

from playwright.sync_api import sync_playwright

PAGES = ["/", "/learn", "/kids", "/guide", "/lessons", "/lesson/lesson-0d3a63dc", "/entry/kids-0d3a63dc", "/problems",
         "/problem/py-hello", "/me", "/library", "/constellation", "/galaxy/code", "/catalogue", "/accessibility"]
CONFIGS = {"default": {"theme": "galaxy", "size": 100, "spacing": "normal", "font": "default", "motion": "reduce"},
           "max-text": {"theme": "galaxy", "size": 150, "spacing": "wide", "font": "easy", "motion": "reduce"}}
WIDTHS = (640, 320)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base_url")
    ap.add_argument("--langs", default="en,ar")
    a = ap.parse_args()
    base, bad, n = a.base_url.rstrip("/"), [], 0
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for lang in a.langs.split(","):
            for cname, cfg in CONFIGS.items():
                for w in WIDTHS:
                    ctx = browser.new_context(viewport={"width": w, "height": 800})
                    ctx.add_init_script("localStorage.setItem('hc_a11y_v1', JSON.stringify(%s))" % json.dumps(cfg))
                    page = ctx.new_page()
                    for path in PAGES:
                        url = f"{base}/{lang}{path}" if path != "/" else f"{base}/{lang}/"
                        page.goto(url)
                        page.wait_for_timeout(100)
                        over = page.evaluate("""() => { const d = document.documentElement; const sw = d.scrollWidth, cw = d.clientWidth;
                          if (sw <= cw + 1) return null;
                          const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > cw + 1 && !e.closest('.flow, .marquee, pre, .ide, .map, svg, .tl, table'))
                              .slice(0, 3).map(e => e.tagName.toLowerCase() + '.' + (e.className && e.className.baseVal === undefined ? e.className : '')).filter(Boolean);
                          return {sw, cw, wide}; }""")
                        n += 1
                        if over and over["wide"]:
                            bad.append((lang, cname, w, path, over))
                    ctx.close()
        browser.close()
    print(f"{n} page states at 320/640 px, {len(bad)} with horizontal scroll caused by page content")
    for b in bad[:30]:
        print("  OVERFLOW", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
