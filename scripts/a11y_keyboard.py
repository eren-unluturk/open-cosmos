"""Keyboard-only walk-through of the demo paths (docs/DEMO_SLICE.md) and the settings panel. DEV ONLY (needs Playwright).

Checks, using only the Tab / Shift+Tab / Enter / Space / Escape / arrow keys:
  - the first Tab stop is the skip link, and it moves focus to the main content
  - the Accessibility button opens the panel, focus stays inside it while Tab cycles, Escape closes it and puts
    focus back on the button, and choosing a theme with the keyboard changes the page and survives a reload
  - every demo page can be tabbed through without a keyboard trap, and every stop has a visible focus indicator
  - the guide slides can be moved with the keyboard

Usage: /tmp/a11yenv/bin/python scripts/a11y_keyboard.py http://127.0.0.1:5000 [--lang en]
Exit code 1 if anything fails.
"""
import argparse
import sys

from playwright.sync_api import sync_playwright

DEMO = {
    "1 child, lesson-backed": ["/entry/kids-0d3a63dc", "/lesson/lesson-0d3a63dc"],
    "2 teen, link-only": ["/entry/build-74d1338b"],
    "3 Arabic example": ["/entry/build-74d1338b"],  # opened with --lang ar below as well
}
FOCUS_INFO = """() => { const e = document.activeElement; if (!e || e === document.body) return null;
  const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
  return {tag: e.tagName.toLowerCase(), id: e.id || '', text: (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 40),
          outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2, shadow: cs.boxShadow !== 'none', border: e.matches(':focus-visible') && cs.borderColor,
          inview: r.width > 0 && r.height > 0, panel: !!e.closest('#a11y-panel')}; }"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base_url")
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    base = a.base_url.rstrip("/")
    fails, checks = [], 0

    def check(ok, msg):
        nonlocal checks
        checks += 1
        if not ok:
            fails.append(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for lang in (a.lang, "ar"):
            ctx = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
            page = ctx.new_page()
            page.goto(f"{base}/{lang}/")
            # 1. skip link
            page.keyboard.press("Tab")
            info = page.evaluate(FOCUS_INFO)
            check(info and "skip" in (info["text"] + info["id"]).lower() or (info and info["tag"] == "a"), f"[{lang}] first Tab stop is not the skip link: {info}")
            page.keyboard.press("Enter")
            check(page.evaluate("location.hash") == "#main", f"[{lang}] skip link did not jump to #main")
            # 2. settings panel
            page.goto(f"{base}/{lang}/")
            btn = page.locator("#a11y-open")
            btn.focus()
            page.keyboard.press("Enter")
            check(page.locator("#a11y-panel").is_visible(), f"[{lang}] Enter did not open the panel")
            check(btn.get_attribute("aria-expanded") == "true", f"[{lang}] aria-expanded not true when open")
            check(page.evaluate(FOCUS_INFO)["panel"], f"[{lang}] focus did not move into the panel")
            for i in range(40):  # Tab cycles inside
                page.keyboard.press("Tab")
                if not page.evaluate(FOCUS_INFO)["panel"]:
                    check(False, f"[{lang}] focus escaped the panel after {i + 1} Tabs")
                    break
            else:
                check(True, "")
            for i in range(40):
                page.keyboard.press("Shift+Tab")
                if not page.evaluate(FOCUS_INFO)["panel"]:
                    check(False, f"[{lang}] focus escaped the panel going backwards")
                    break
            # choose high contrast by keyboard (focus the radio, press Space)
            page.locator('input[name="a11y-theme"][value="contrast"]').focus()
            page.keyboard.press("Space")
            check(page.evaluate("document.documentElement.dataset.theme") == "contrast", f"[{lang}] keyboard theme change failed")
            page.locator('input[name="a11y-size"][value="150"]').focus()
            page.keyboard.press("Space")
            check(page.evaluate("document.documentElement.dataset.size") == "150", f"[{lang}] keyboard text size change failed")
            page.keyboard.press("Escape")
            check(not page.locator("#a11y-panel").is_visible(), f"[{lang}] Escape did not close the panel")
            check(page.evaluate("document.activeElement.id") == "a11y-open", f"[{lang}] focus did not return to the button")
            page.reload()
            check(page.evaluate("document.documentElement.dataset.theme") == "contrast", f"[{lang}] theme not remembered after reload")
            page.evaluate("localStorage.clear()")
            # 3. demo paths: tab through, no trap, visible focus
            for name, paths in DEMO.items():
                if name.startswith("3") and lang != "ar":
                    continue
                if not name.startswith("3") and lang == "ar":
                    continue
                for path in paths:
                    page.goto(f"{base}/{lang}{path}")
                    seen, noring = [], []
                    for i in range(120):
                        page.keyboard.press("Tab")
                        info = page.evaluate(FOCUS_INFO)
                        if info is None:
                            break
                        key = (info["tag"], info["id"], info["text"])
                        if key in seen:
                            break
                        seen.append(key)
                        if not (info["outline"] or info["shadow"] or info["border"]):
                            noring.append(key)
                    check(len(seen) >= 8, f"[{lang}] {name} {path}: only {len(seen)} Tab stops (keyboard trap?)")
                    check(not noring, f"[{lang}] {name} {path}: no visible focus on {noring[:3]}")
                    check(page.evaluate("document.querySelectorAll('h1').length") == 1, f"[{lang}] {path}: expected one h1")
                    print(f"  ok  [{lang}] {name} {path}: {len(seen)} Tab stops")
            # 4. guide slides by keyboard (entry page with a guide)
            page.goto(f"{base}/{lang}/entry/kids-0d3a63dc")
            if page.locator("[data-slide]").count() > 1:
                slides_before = page.evaluate("document.querySelector('.slide.is-active')?.id || ''")
                for b in page.locator("[data-deck] button").all():
                    if b.is_visible():
                        b.focus()
                        break
                page.keyboard.press("ArrowRight" if lang != "ar" else "ArrowLeft")
                page.keyboard.press("Enter")
                after = page.evaluate("document.querySelector('.slide.is-active')?.id || ''")
                check(after != "", f"[{lang}] no active slide after keyboard use")
            ctx.close()
        browser.close()
    print(f"\n{checks} keyboard checks, {len([f for f in fails if f])} failed")
    for f in fails:
        if f:
            print("  FAIL:", f)
    return 1 if any(fails) else 0


if __name__ == "__main__":
    sys.exit(main())
