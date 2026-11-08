"""Row Level Security check with the ANON key only (the key the website uses). Never prints keys.

There are no user accounts, so there is no "user A reads user B's data" case; what matters is what the public key can do:
  content  : anon can read; anon cannot insert, update or delete
  feedback : anon can insert (status must be 'new'); anon cannot read, update or delete
Reads SUPABASE_URL and SUPABASE_ANON_KEY from the local .env. Inserts ONE feedback row marked as an automated test
(delete it in the Supabase dashboard if you like: the anon key cannot delete it, by design).

Usage: python scripts/check_rls.py [--no-insert]
"""
import argparse
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
URL, KEY = os.environ.get("SUPABASE_URL", "").rstrip("/"), os.environ.get("SUPABASE_ANON_KEY", "")
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))


def call(method, path, **kw):
    return requests.request(method, f"{URL}/rest/v1/{path}", headers={**H, **kw.pop("headers", {})}, timeout=15, **kw)


def count(table):
    r = call("GET", f"{table}?select=id", headers={"Prefer": "count=exact", "Range": "0-0"})
    return r.status_code, r.headers.get("Content-Range", "")


def blocked(r):
    """Denied, or accepted but matching no rows (RLS filtered everything out)."""
    if r.status_code in (401, 403):
        return True
    return r.status_code in (200, 204) and r.text.strip() in ("", "[]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-insert", action="store_true")
    a = ap.parse_args()
    if not URL or not KEY:
        print("Set SUPABASE_URL and SUPABASE_ANON_KEY in your local .env first.")
        return 2
    print("Anon-key checks (keys are never printed)")
    status, before = count("content")
    check("anon can SELECT content", status in (200, 206) and "/" in before and not before.endswith("/0"), f"HTTP {status}, rows {before.split('/')[-1]}")
    row = call("GET", "content?select=kind,id&limit=1").json()[0]
    sel = f"kind=eq.{row['kind']}&id=eq.{row['id']}"
    r = call("POST", "content", json={"kind": "entry", "id": "rls-test-should-not-exist", "data": {"item": {}}}, headers={"Prefer": "return=minimal"})
    check("anon cannot INSERT into content", r.status_code in (401, 403), f"HTTP {r.status_code}")
    r = call("PATCH", f"content?{sel}", json={"updated_at": "2000-01-01T00:00:00Z"}, headers={"Prefer": "return=representation"})
    check("anon cannot UPDATE content", blocked(r), f"HTTP {r.status_code}")
    r = call("DELETE", "content?id=eq.rls-test-should-not-exist", headers={"Prefer": "return=representation"})
    check("anon cannot DELETE content", blocked(r), f"HTTP {r.status_code}")
    status, after = count("content")
    check("content is unchanged after the attempts", after == before, f"{before.split('/')[-1]} rows before, {after.split('/')[-1]} after")

    r = call("GET", "feedback?select=id&limit=1")
    check("anon cannot SELECT feedback", r.status_code in (401, 403) or (r.status_code == 200 and r.text.strip() == "[]"), f"HTTP {r.status_code}")
    r = call("PATCH", "feedback?status=eq.new", json={"status": "handled"}, headers={"Prefer": "return=representation"})
    check("anon cannot UPDATE feedback", blocked(r), f"HTTP {r.status_code}")
    r = call("DELETE", "feedback?status=eq.new", headers={"Prefer": "return=representation"})
    check("anon cannot DELETE feedback", blocked(r), f"HTTP {r.status_code}")
    r = call("POST", "feedback", json={"kind": "bug", "message": "automated RLS test with a status that is not new", "page": "/", "lang": "en", "status": "handled"},
             headers={"Prefer": "return=minimal"})
    check("anon cannot insert feedback with a non-'new' status", r.status_code in (401, 403), f"HTTP {r.status_code}")
    r = call("POST", "feedback", json={"kind": "bug", "message": "x", "page": "/", "lang": "en"}, headers={"Prefer": "return=minimal"})
    check("feedback rules reject a too-short message", r.status_code in (400, 401, 403), f"HTTP {r.status_code}")
    if not a.no_insert:
        r = call("POST", "feedback", json={"kind": "other", "message": "Automated RLS test, please ignore and delete this row.", "page": "/en/", "lang": "en"},
                 headers={"Prefer": "return=minimal"})
        check("anon CAN insert a valid feedback row", r.status_code in (200, 201, 204), f"HTTP {r.status_code}")
    print("RESULT:", "PASS" if all(results) else "FAIL", f"({sum(results)}/{len(results)})")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
