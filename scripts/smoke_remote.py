"""Smoke test a running Open Cosmos site (local or deployed). Read-only apart from the grown-up toggle on a private session.

Usage:  python scripts/smoke_remote.py BASE_URL [--slow 3.0] [--delay 0]
Example: python scripts/smoke_remote.py https://open-cosmos-git-vercel-yourname.vercel.app

Checks: /healthz; every main page in all five languages (title has the app name, 200, security headers, Arabic is
right-to-left); the safety gate (adult-only never shown, ask-a-grown-up hidden until the grown-up switch); 404 pages;
API endpoints; static files and their headers; response times (anything over --slow seconds is flagged, the first
request counts as the cold start). Exit code 0 only when nothing failed. Slow responses warn, they do not fail.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import content_rows  # noqa: E402

LANGS = ("en", "es", "ar", "hi", "pt")
NAME = "Open Cosmos"
SEC_HEADERS = ("X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Content-Security-Policy")


class Smoke:
    def __init__(self, base, slow, delay):
        self.base, self.slow, self.delay = base.rstrip("/"), slow, delay
        self.s = requests.Session()
        self.fails, self.warns, self.n = [], [], 0
        self.times = []

    def get(self, path, session=None, **kw):
        if self.delay:
            time.sleep(self.delay)
        t = time.monotonic()
        try:
            r = (session or self.s).get(self.base + path, timeout=30, allow_redirects=False, **kw)
        except requests.RequestException as exc:
            self.fail(path, f"request failed: {type(exc).__name__}")
            return None
        dt = time.monotonic() - t
        self.times.append((dt, path))
        if dt > self.slow:
            self.warns.append(f"SLOW {dt:.1f}s  {path}" + ("  (first request: cold start?)" if len(self.times) == 1 else ""))
        return r

    def fail(self, where, msg):
        self.fails.append(f"{where}: {msg}")

    def check(self, where, ok, msg):
        self.n += 1
        if not ok:
            self.fail(where, msg)

    # ---- groups of checks ----
    def health(self):
        r = self.get("/healthz")
        if r is not None:
            self.check("/healthz", r.status_code == 200 and r.json() == {"ok": True}, f"status {r.status_code}, body {r.text[:60]!r}")

    def pages(self, rows):
        lesson = next(r for r in rows if r["kind"] == "lesson")["id"]
        entry = next(r["id"] for r in rows if r["kind"] == "entry" and r["data"]["item"]["safety"] == "kid-safe")
        problem = next(r["id"] for r in rows if r["kind"] == "problem")
        paths = ["/", "/learn", "/build", "/kids", "/guide", "/lessons", f"/lesson/{lesson}", f"/entry/{entry}",
                 "/problems", f"/problem/{problem}", "/me", "/library", "/constellation", "/catalogue", "/howto/video",
                 "/galaxy/code", "/learn?q=python", "/guide?age=8-10&goal=games&level=Beginner"]
        optional = ["/accessibility"]
        for lang in LANGS:
            for p in paths + optional:
                url = f"/{lang}{p}" if p != "/" else f"/{lang}/"
                r = self.get(url)
                if r is None:
                    continue
                if p in optional and r.status_code == 404:
                    continue
                self.check(url, r.status_code == 200, f"status {r.status_code}")
                if r.status_code != 200:
                    continue
                html = r.text
                title = re.search(r"<title>(.*?)</title>", html, re.S)
                self.check(url, bool(title) and NAME in title.group(1), f"title does not contain {NAME!r}: {title.group(1)[:60] if title else None!r}")
                self.check(url, f'<html lang="{lang}"' in html, "wrong html lang")
                for h in SEC_HEADERS:
                    self.check(url, h in r.headers, f"missing header {h}")
                for old in ("Hackcessability", "Learning Lab"):
                    self.check(url, old not in html, f"old app name {old!r} on the page")
                if lang == "ar":
                    self.check(url, 'dir="rtl"' in html, "Arabic page is not right-to-left")
                elif lang != "ar":
                    self.check(url, 'dir="ltr"' in html, "page is not left-to-right")

    def gate(self, rows):
        by = {"adult-only": [], "ask-a-grown-up": [], "kid-safe": []}
        for r in rows:
            if r["kind"] == "entry":
                by[r["data"]["item"]["safety"]].append(r["id"])
        listing = "".join(self.get(f"/en/{side}").text for side in ("learn", "build", "kids")) + self.get("/en/library").text
        for eid in by["adult-only"]:
            self.check("gate", self.get(f"/en/entry/{eid}").status_code == 404, f"adult-only entry {eid} reachable")
        self.check("gate", not any(f"/entry/{e}" in listing for e in by["adult-only"]), "adult-only entry linked in a listing")
        self.check("gate", not any(f"/entry/{e}" in listing for e in by["ask-a-grown-up"]), "ask-a-grown-up entry shown by default")
        for eid in by["ask-a-grown-up"][:5]:
            self.check("gate", self.get(f"/en/entry/{eid}").status_code == 404, f"ask-a-grown-up entry {eid} reachable by default")
        # a private session that switches the grown-up flag on
        s = requests.Session()
        if self.delay:
            time.sleep(self.delay)
        try:
            s.post(self.base + "/grownup", data={"on": "1", "next": "/en/learn"}, timeout=30, allow_redirects=False)
        except requests.RequestException as exc:
            self.fail("gate", f"grown-up toggle failed: {type(exc).__name__}")
            return
        ask = by["ask-a-grown-up"][0]
        self.check("gate", self.get(f"/en/entry/{ask}", session=s).status_code == 200, "ask-a-grown-up entry hidden even for a grown-up")
        self.check("gate", self.get(f"/en/entry/{by['adult-only'][0]}", session=s).status_code == 404, "adult-only entry reachable for a grown-up")
        fb = self.get("/en/feedback", session=s)
        self.check("gate", fb is not None and fb.status_code == 200 and 'name="csrf"' in fb.text, "feedback form missing for a grown-up")
        self.check("gate", self.get("/en/feedback").status_code == 404, "feedback form reachable without the grown-up switch")

    def errors(self):
        for p in ("/en/nope", "/xx/learn", "/en/entry/does-not-exist", "/en/problem/does-not-exist", "/api/nope", "/en/lesson/nope"):
            r = self.get(p)
            if r is not None:
                self.check(p, r.status_code == 404, f"expected 404, got {r.status_code}")
        r = self.get("/api/nope")
        if r is not None and r.status_code == 404:
            self.check("/api/nope", "json" in r.headers.get("Content-Type", ""), "API 404 is not JSON")

    def api(self, rows):
        problem = next(r["id"] for r in rows if r["kind"] == "problem")
        r = self.get("/api/problems?lang=es")
        if r is not None:
            self.check("/api/problems", r.status_code == 200 and r.json()["count"] > 50, f"status {r.status_code}")
        r = self.get(f"/api/problems/{problem}")
        if r is not None:
            body = r.text
            self.check("/api/problems/<id>", r.status_code == 200, f"status {r.status_code}")
            self.check("/api/problems/<id>", '"solution"' not in body, "the solution is in the public problem JSON")
        r = self.get(f"/api/problems/{problem}/hint/1?lang=ar")
        if r is not None:
            self.check("hint", r.status_code == 200 and "hint" in r.json(), f"status {r.status_code}")
        r = self.get("/api/entries?lang=pt&side=kids")
        if r is not None:
            ok = r.status_code == 200
            self.check("/api/entries", ok, f"status {r.status_code}")
            if ok:
                self.check("/api/entries", all(e["safety"] == "kid-safe" for e in r.json()["entries"]), "non kid-safe entry in the default API list")
        r = self.get("/api/catalogue?lang=hi")
        if r is not None:
            self.check("/api/catalogue", r.status_code == 200, f"status {r.status_code}")

    def static(self):
        css = self.get("/static/galaxy.css")
        if css is not None:
            self.check("/static/galaxy.css", css.status_code == 200 and "css" in css.headers.get("Content-Type", ""), f"status {css.status_code}")
            for h in ("X-Content-Type-Options", "Content-Security-Policy"):
                self.check("/static/galaxy.css", h in css.headers, f"missing header {h}")
        for name in ("galaxy.js", "problem.js"):
            r = self.get(f"/static/{name}")
            if r is not None:
                self.check(f"/static/{name}", r.status_code == 200 and "javascript" in r.headers.get("Content-Type", ""), f"status {r.status_code}")
                self.check(f"/static/{name}", "'unsafe-eval'" not in r.headers.get("Content-Security-Policy", ""), "page scripts allowed unsafe-eval")
        run = self.get("/static/runner.js")
        if run is not None:
            csp = run.headers.get("Content-Security-Policy", "")
            self.check("/static/runner.js", run.status_code == 200, f"status {run.status_code}")
            self.check("/static/runner.js", "'unsafe-eval'" in csp and "cdn.jsdelivr.net" in csp, "runner policy cannot run learner code / load Pyodide")
            self.check("/static/runner.js", set(re.findall(r"https://[\w.]+", csp)) <= {"https://cdn.jsdelivr.net"}, "runner policy allows another host")
        page = self.get("/en/problems")
        if page is not None:
            csp = page.headers.get("Content-Security-Policy", "")
            self.check("CSP", "script-src 'self'" in csp and "unsafe-eval" not in csp and "jsdelivr" not in csp, f"page CSP too wide or missing: {csp[:80]}")

    def report(self):
        print(f"\nChecks run: {self.n}   requests: {len(self.times)}")
        if self.times:
            ts = sorted(t for t, _ in self.times)
            print(f"Response time: first {self.times[0][0]:.2f}s, median {ts[len(ts)//2]:.2f}s, slowest {ts[-1]:.2f}s ({max(self.times)[1]})")
        for w in self.warns:
            print("  warn:", w)
        for f in self.fails[:40]:
            print("  FAIL:", f)
        if len(self.fails) > 40:
            print(f"  ... and {len(self.fails) - 40} more")
        print("PASS" if not self.fails else f"FAILED ({len(self.fails)} problems)")
        return 0 if not self.fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("base_url")
    ap.add_argument("--slow", type=float, default=3.0, help="flag responses slower than this many seconds")
    ap.add_argument("--delay", type=float, default=0.0, help="pause between requests (be polite to a free tier)")
    a = ap.parse_args(argv)
    rows = content_rows.rows_from_files(content_rows.local_files())
    sm = Smoke(a.base_url, a.slow, a.delay)
    print(f"Smoke test: {sm.base}")
    sm.health()
    if sm.fails:  # nothing to test if the site does not answer
        print("The site did not answer /healthz correctly; stopping.")
        return sm.report()
    sm.pages(rows)
    sm.gate(rows)
    sm.errors()
    sm.api(rows)
    sm.static()
    return sm.report()


if __name__ == "__main__":
    sys.exit(main())
