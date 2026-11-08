"""Accessibility audit with axe-core and Playwright. DEV ONLY: not in requirements.txt, run on your own machine.

Setup (once):
  python3 -m venv /tmp/a11yenv && /tmp/a11yenv/bin/pip install playwright
  mkdir -p .cache && curl -sL https://registry.npmjs.org/axe-core/-/axe-core-4.14.0.tgz | tar -xz -O package/axe.min.js > .cache/axe.min.js
  (uses your installed Google Chrome; or run `playwright install chromium` and pass --browser chromium)

Run:  .venv/bin/flask --app src/app run -p 5000 &      then
      /tmp/a11yenv/bin/python scripts/a11y_audit.py http://127.0.0.1:5000 [--langs en,ar] [--json out.json]

Audits the key pages in every colour theme at desktop (1280 px) and phone (390 px) width, plus the settings panel open
and the grown-up pages. Exit code 1 if any violation is found (a documented false positive goes in IGNORE below).
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
AXE = ROOT / ".cache" / "axe.min.js"
# max-text = galaxy + 150% text + roomy spacing + easy font.
# galaxy-flat = galaxy with the star background removed: axe cannot compute contrast over the star/glow gradient
# ("incomplete"), so this run checks the same colours over the flat page colour.
THEMES = ("galaxy", "galaxy-flat", "light", "contrast", "cb", "max-text")
VIEWPORTS = {"desktop": (1280, 900), "phone": (390, 844)}
PAGES = ["/", "/learn", "/kids", "/guide", "/lessons", "/lesson/lesson-0d3a63dc", "/entry/kids-0d3a63dc", "/entry/build-74d1338b",
         "/problems", "/problem/py-hello", "/me", "/library", "/constellation", "/galaxy/code", "/catalogue", "/accessibility"]
GROWNUP_PAGES = ["/feedback", "/entry/learn-1c1ace1d"]
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]
# rule id -> reason, for documented false positives (keep empty unless justified in docs/ACCESSIBILITY.md)
IGNORE = {}


def run_axe(page):
    return page.evaluate("""async (tags) => {
        const r = await axe.run(document, {runOnly: {type: 'tag', values: tags}});
        const pick = n => ({id: n.id, impact: n.impact, help: n.help, nodes: n.nodes.length,
                            targets: n.nodes.slice(0, 3).map(x => x.target.join(' ') + ' :: ' + (x.failureSummary || '').split('\\n').slice(1, 2).join('')) });
        return {violations: r.violations.map(pick), incomplete: r.incomplete.map(pick)};
    }""", TAGS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base_url")
    ap.add_argument("--langs", default="en,ar")
    ap.add_argument("--browser", default="chrome", help="'chrome' (installed Google Chrome) or 'chromium'")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not AXE.exists():
        print("Missing .cache/axe.min.js (see the setup at the top of this file).")
        return 2
    axe_src = AXE.read_text(encoding="utf-8")
    base = a.base_url.rstrip("/")
    results, runs, incomplete = [], 0, Counter()
    with sync_playwright() as p:
        kw = {"channel": "chrome"} if a.browser == "chrome" else {}
        browser = p.chromium.launch(**kw)
        for lang in a.langs.split(","):
            for theme in THEMES:
                for vname, (w, h) in VIEWPORTS.items():
                    ctx = browser.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce")
                    cfg = {"theme": theme, "size": 100, "spacing": "normal", "font": "default", "motion": "reduce"}
                    if theme == "max-text":
                        cfg.update(theme="galaxy", size=150, spacing="wide", font="easy")
                    if theme == "galaxy-flat":
                        cfg["theme"] = "galaxy"
                    ctx.add_init_script("try{localStorage.setItem('hc_a11y_v1', JSON.stringify(%s))}catch(e){}" % json.dumps(cfg))
                    page = ctx.new_page()
                    jobs = [(f"/{lang}{p_}" if p_ != "/" else f"/{lang}/", False) for p_ in PAGES]
                    if theme == "galaxy" or vname == "phone":
                        jobs += [("PANEL", False)]
                    jobs += [(f"/{lang}{p_}", True) for p_ in GROWNUP_PAGES]
                    for path, adult in jobs:
                        try:
                            if adult:  # switch the grown-up view on inside the browser itself, so its cookie is kept
                                page.goto(f"{base}/{lang}/")
                                page.evaluate("fetch('/grownup', {method: 'POST', body: new URLSearchParams({on: '1', next: '/'})})")
                                page.wait_for_timeout(200)
                            if path == "PANEL":
                                page.goto(f"{base}/{lang}/")
                                page.click("#a11y-open")
                                page.wait_for_selector("#a11y-panel:not([hidden])")
                                label = f"/{lang}/ (settings panel open)"
                            else:
                                page.goto(base + path, wait_until="load")
                                label = path
                            page.wait_for_timeout(150)
                            if theme == "galaxy-flat":
                                page.add_style_tag(content="body{background-image:none!important} .bubble{-webkit-text-stroke:0!important}")  # axe reads the decorative outline colour of big titles as the text colour
                            page.add_script_tag(content=axe_src)
                            r = run_axe(page)
                        except Exception as exc:
                            r = {"violations": [{"id": "audit-error", "impact": "critical", "help": str(exc)[:120], "nodes": 1, "targets": []}], "incomplete": []}
                            label = path
                        runs += 1
                        for v in r["incomplete"]:
                            incomplete[v["id"]] += v["nodes"]
                        for v in r["violations"]:
                            if v["id"] in IGNORE:
                                continue
                            results.append({"lang": lang, "theme": theme, "viewport": vname, "page": label, **v})
                        if adult:
                            ctx.clear_cookies()  # back to the default (kid-safe) view for the next page
                    ctx.close()
        browser.close()
    by_rule = Counter()
    for r in results:
        by_rule[r["id"]] += r["nodes"]
    print(f"\nAudited {runs} page states (langs {a.langs}, themes {len(THEMES)}, viewports {len(VIEWPORTS)}).")
    print(f"Violations: {len(results)} page states affected, {sum(by_rule.values())} elements.")
    for rule, n in by_rule.most_common():
        print(f"  {rule}: {n} elements")
    seen = set()
    for r in results:
        key = (r["id"], r["page"].split("/", 2)[-1] if False else r["page"], tuple(r["targets"][:1]))
        if key in seen:
            continue
        seen.add(key)
        if len(seen) <= 40:
            print(f"- [{r['impact']}] {r['id']} on {r['page']} ({r['theme']}, {r['viewport']}): {r['help']}")
            for t in r["targets"][:2]:
                print("    ", t[:200])
    print("Needs manual review (axe 'incomplete', e.g. text on gradients or images): " + (", ".join(f"{k} {n}" for k, n in incomplete.most_common()) or "none"))
    if a.json:
        Path(a.json).write_text(json.dumps({"runs": runs, "violations": results, "incomplete": dict(incomplete)}, indent=1), encoding="utf-8")
    return 1 if results else 0


if __name__ == "__main__":
    sys.exit(main())
