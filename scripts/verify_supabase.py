"""Compare the Supabase `content` table with the bundled JSON: row counts and a hash per kind.

Uses SUPABASE_URL and SUPABASE_ANON_KEY (read-only) from the local .env; keys are never printed.
Exit code 0 when everything matches, 1 otherwise.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import content_rows  # noqa: E402
import supabase_client  # noqa: E402


def compare(local_rows, remote_rows):
    """List of difference lines (empty list = identical)."""
    a, b = content_rows.hash_by_kind(local_rows), content_rows.hash_by_kind(remote_rows)
    diffs = []
    for kind in content_rows.KINDS:
        (na, ha), (nb, hb) = a[kind], b[kind]
        if na != nb:
            diffs.append(f"{kind}: local {na} rows, Supabase {nb} rows")
        elif ha != hb:
            lo = {r["id"]: r["data"] for r in local_rows if r["kind"] == kind}
            re_ = {r["id"]: r["data"] for r in remote_rows if r["kind"] == kind}
            changed = sorted(i for i in lo if lo[i] != re_.get(i))
            diffs.append(f"{kind}: same count ({na}) but {len(changed)} differ, e.g. {changed[:3]}")
    only_remote = {(r["kind"], r["id"]) for r in remote_rows} - {(r["kind"], r["id"]) for r in local_rows}
    if only_remote:
        diffs.append(f"{len(only_remote)} rows only in Supabase, e.g. {sorted(only_remote)[:3]}")
    return diffs


def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("Set SUPABASE_URL and SUPABASE_ANON_KEY in your local .env first (see docs/SUPABASE.md).")
        return 1
    local = content_rows.rows_from_files(content_rows.local_files())
    try:
        remote = supabase_client.fetch_rows(url, key)
    except supabase_client.SupabaseError as exc:
        print(f"Could not read Supabase ({exc}).")
        return 1
    for kind, (n, h) in content_rows.hash_by_kind(remote).items():
        print(f"  {kind:<10} {n:>5} rows  {h[:12]}")
    diffs = compare(local, remote)
    if diffs:
        print("DIFFERENT:")
        print("\n".join("  - " + d for d in diffs))
        return 1
    try:
        content_rows.files_from_rows(remote)
    except ValueError as exc:
        print(f"DIFFERENT: rows do not rebuild into valid files ({exc}).")
        return 1
    print("OK: Supabase matches the bundled JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
