"""Check that entry links still work. Writes a report; NEVER modifies the data.

Usage: python scripts/check_links.py [--limit N] [--workers 20] [--timeout 8]
Report: scripts/cache/link_report.json  (also prints a summary)
"""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
REPORT = ROOT / "scripts" / "cache" / "link_report.json"
HEADERS = {"User-Agent": "hackcessability-link-check/1.0"}


def check(item, timeout):
    url = item["url"]
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout, headers=HEADERS)
        if r.status_code in (403, 405, 501) or r.status_code >= 500:  # HEAD often unsupported
            r = requests.get(url, allow_redirects=True, timeout=timeout, headers=HEADERS, stream=True)
            r.close()
        return {"id": item["id"], "url": url, "status": r.status_code, "ok": r.status_code < 400, "error": None}
    except requests.RequestException as ex:
        return {"id": item["id"], "url": url, "status": None, "ok": False, "error": type(ex).__name__}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--timeout", type=float, default=8)
    args = ap.parse_args()
    items = [e for n in ("learn", "build") for e in json.loads((DATA / f"{n}.json").read_text())][: args.limit]
    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(lambda it: check(it, args.timeout), items))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(results, indent=1))
    bad = [r for r in results if not r["ok"]]
    print(f"Checked {len(results)} links: {len(results) - len(bad)} ok, {len(bad)} broken/unreachable")
    for r in bad[:15]:
        print(f"  {r['status'] or r['error']}  {r['url']}")
    print(f"Full report: {REPORT}")


if __name__ == "__main__":
    main()
