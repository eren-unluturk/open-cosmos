"""Upload the bundled catalog (src/data/*.json and translation overlays) to the Supabase `content` table.

Idempotent: rows are upserted by (kind, id), so running it twice changes nothing. Reads SUPABASE_URL and
SUPABASE_SERVICE_KEY from the local .env (never printed). The service key bypasses row-level security, so it
must only ever live on your own machine, never on the deployed site.

Usage:
  python scripts/seed_supabase.py --dry-run     counts only, no network
  python scripts/seed_supabase.py               upload
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import content_rows  # noqa: E402
import supabase_client  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print counts only; no network, no keys needed")
    args = ap.parse_args(argv)

    rows = content_rows.rows_from_files(content_rows.local_files())
    counts = {k: v[0] for k, v in content_rows.hash_by_kind(rows).items()}
    print(f"{len(rows)} rows: " + ", ".join(f"{k} {n}" for k, n in counts.items()))
    if args.dry_run:
        print("dry run: nothing was sent.")
        return 0

    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("Set SUPABASE_URL and SUPABASE_SERVICE_KEY in your local .env first (see docs/SUPABASE.md).")
        return 1
    try:
        supabase_client.upsert_rows(url, key, rows)
    except supabase_client.SupabaseError as exc:
        print(f"Upload failed ({exc}). Did you run supabase/schema.sql first?")
        return 1
    print("Uploaded. Now run: python scripts/verify_supabase.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
