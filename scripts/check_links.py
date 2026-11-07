"""Check that entry links still work. Writes a report; NEVER modifies the data.

Polite by design: small thread pool, a delay between requests to the same host, backoff on
429 (honors Retry-After), a generic User-Agent, one retry. Each result gets a class:
  ok            2xx/3xx
  rate_limited  429 (not necessarily broken)
  blocked_bot   401/403/999 (site refuses bots; not necessarily broken)
  broken        404, 410, or DNS failure (real failure)
  error         timeout, SSL, 5xx, refused (real failure, but maybe temporary)

By default only entries that are not already "ok" in the last report are re-checked.

Usage: python scripts/check_links.py [--all] [--limit N] [--workers 6] [--delay 1.0] [--timeout 10]
Report: scripts/cache/link_report.json (git-ignored). Prints real failures, flags kid-safe ones.
"""
import argparse
import collections
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
REPORT = ROOT / "scripts" / "cache" / "link_report.json"
HEADERS = {"User-Agent": "link-checker/1.0 (open-data education project)"}
REAL = ("broken", "error")

_lock = threading.Lock()
_next_ok = collections.defaultdict(float)  # host -> earliest time of the next request


def classify(status, error=None):
    if error == "dns":
        return "broken"
    if error:
        return "error"
    if status < 400:
        return "ok"
    if status == 429:
        return "rate_limited"
    if status in (401, 403, 999):
        return "blocked_bot"
    if status in (404, 410):
        return "broken"
    return "error"


def wait_turn(host, delay):
    with _lock:
        now = time.monotonic()
        when = max(now, _next_ok[host])
        _next_ok[host] = when + delay
    time.sleep(max(0, when - now))


def fetch_once(url, host, delay, timeout):
    wait_turn(host, delay)
    r = requests.head(url, allow_redirects=True, timeout=timeout, headers=HEADERS)
    if r.status_code in (403, 405, 501) or r.status_code >= 500:  # HEAD often unsupported
        wait_turn(host, delay)
        r = requests.get(url, allow_redirects=True, timeout=timeout, headers=HEADERS, stream=True)
        r.close()
    return r


def check(item, delay, timeout):
    url, host = item["url"], urlparse(item["url"]).netloc.lower()
    status, error = None, None
    for attempt in (1, 2):  # one retry
        try:
            r = fetch_once(url, host, delay, timeout)
            status, error = r.status_code, None
            if status == 429 and attempt == 1:
                try:
                    pause = min(float(r.headers.get("Retry-After", 5)), 60)
                except ValueError:
                    pause = 5
                with _lock:  # back off the whole host
                    _next_ok[host] = max(_next_ok[host], time.monotonic() + pause)
                continue
            if status >= 500 and attempt == 1:
                time.sleep(1)
                continue
            break
        except requests.RequestException as ex:
            text = str(ex)
            dns = any(s in text for s in ("NameResolutionError", "nodename nor servname", "Name or service not known"))
            status, error = None, "dns" if dns else type(ex).__name__
            if dns:
                break
    return {"id": item["id"], "url": url, "status": status, "error": error, "class": classify(status, error)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="re-check everything, not just non-ok")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests to one host")
    ap.add_argument("--timeout", type=float, default=10)
    args = ap.parse_args()

    entries = [e for n in ("learn", "build", "kids") if (DATA / f"{n}.json").exists()
               for e in json.loads((DATA / f"{n}.json").read_text())]
    prev = {}
    if REPORT.exists():
        for r in json.loads(REPORT.read_text()):
            if "class" not in r:  # report from the old checker: derive the class
                r["class"] = classify(r["status"] or 0, "x" if r.get("error") else None) if r["status"] else "error"
            prev[r["id"]] = r
    todo = [e for e in entries if args.all or prev.get(e["id"], {}).get("class") != "ok"
            or prev[e["id"]]["url"] != e["url"]][: args.limit]
    print(f"{len(entries)} entries, re-checking {len(todo)} (others were ok last time)")
    with ThreadPoolExecutor(args.workers) as pool:
        for r in pool.map(lambda it: check(it, args.delay, args.timeout), todo):
            prev[r["id"]] = r
    results = [prev[e["id"]] for e in entries if e["id"] in prev]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(results, indent=1))

    counts = collections.Counter(r["class"] for r in results)
    print("Summary:", dict(counts), "| unchecked:", len(entries) - len(results))
    by_id = {e["id"]: e for e in entries}
    real = [r for r in results if r["class"] in REAL]
    print(f"\nREAL failures ({len(real)}), kid-safe ones first:")
    for r in sorted(real, key=lambda r: (by_id[r["id"]]["safety"] != "kid-safe", r["url"])):
        e = by_id[r["id"]]
        print(f"  [{e['safety']}] {r['class']} {r['status'] or r['error']}  {r['id']}  {e['title']['en'][:50]}  {r['url']}")
    print(f"\nNot necessarily broken: {counts['rate_limited']} rate_limited, {counts['blocked_bot']} blocked_bot")
    print(f"Full report: {REPORT}")


if __name__ == "__main__":
    main()
