"""Tiny Supabase REST client (PostgREST). Uses `requests`; no Flask. Never logs or returns keys."""
import time

import requests

TIMEOUT = 3          # seconds per request
PAGE = 500           # rows per request (the API caps a response, so we page)
MAX_SECONDS = 20     # whole catalog download budget
MAX_PAGES = 100


class SupabaseError(Exception):
    pass


def _headers(key, **extra):
    return {"apikey": key, "Authorization": f"Bearer {key}", **extra}


def fetch_rows(url, key, table="content", columns="kind,id,data", timeout=TIMEOUT):
    """All rows of a table, paged. Raises SupabaseError on any HTTP/JSON problem."""
    rows, offset, started = [], 0, time.monotonic()
    for _ in range(MAX_PAGES):
        if time.monotonic() - started > MAX_SECONDS:
            raise SupabaseError("too slow")
        try:
            r = requests.get(f"{url.rstrip('/')}/rest/v1/{table}", headers=_headers(key), timeout=timeout,
                             params={"select": columns, "order": "kind.asc,id.asc", "limit": PAGE, "offset": offset})
            if r.status_code != 200:
                raise SupabaseError(f"HTTP {r.status_code}")
            page = r.json()
        except SupabaseError:
            raise
        except Exception as exc:  # timeout, connection error, invalid JSON
            raise SupabaseError(type(exc).__name__) from None
        if not isinstance(page, list):
            raise SupabaseError("unexpected response")
        rows.extend(page)
        if len(page) < PAGE:
            return rows
        offset += PAGE
    raise SupabaseError("too many pages")


def upsert_rows(url, service_key, rows, table="content", batch=100, timeout=30):
    """Idempotent write (merge on the primary key). Seeding only: needs the service key."""
    for i in range(0, len(rows), batch):
        try:
            r = requests.post(f"{url.rstrip('/')}/rest/v1/{table}", timeout=timeout, json=rows[i:i + batch],
                              params={"on_conflict": "kind,id"},
                              headers=_headers(service_key, **{"Content-Type": "application/json",
                                                               "Prefer": "resolution=merge-duplicates,return=minimal"}))
        except Exception as exc:
            raise SupabaseError(type(exc).__name__) from None
        if r.status_code not in (200, 201, 204):
            raise SupabaseError(f"HTTP {r.status_code}")


def insert_feedback(url, anon_key, payload, timeout=TIMEOUT):
    """Insert one feedback row with the anon key (insert-only by RLS). Returns True on success."""
    try:
        r = requests.post(f"{url.rstrip('/')}/rest/v1/feedback", json=payload, timeout=timeout,
                          headers=_headers(anon_key, **{"Content-Type": "application/json", "Prefer": "return=minimal"}))
    except Exception:
        return False
    return r.status_code in (200, 201, 204)
