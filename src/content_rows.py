"""Turn the bundled JSON catalog into Supabase `content` rows and back. No Flask, no network.

One source of truth for the row format, used by store.py (reading), scripts/seed_supabase.py (writing) and
scripts/verify_supabase.py (comparing). Rebuilding the files from the rows must give exactly the bundled JSON,
so the site behaves the same whichever source it loads from.

Row: {"kind": ..., "id": ..., "data": {...}}. `data` wraps the original item so order survives the database:
  entry      {"side": "learn|build|kids", "pos": n, "item": <entry>}
  guide      {"pos": n, "item": <guide>}   id is "fallback/<key>", "groups/<key>" or "meta" (version, _note)
  lesson     {"pos": n, "item": <lesson>}
  problem    {"pos": n, "item": <problem>}
  ui_overlay {"item": <whole overlay file>}  id is the file name without .json
"""
import hashlib
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"
SIDES = ("learn", "build", "kids")
KINDS = ("entry", "guide", "lesson", "problem", "ui_overlay")
OVERLAYS = ("guides_translated", "lessons_overlay", "problems_overlay", "ui_translated", "categories_translated")
FILES = tuple(f"{s}.json" for s in SIDES) + ("guides.json", "lessons.json", "problems.json") + tuple(f"{o}.json" for o in OVERLAYS)


def _default(name):
    if name == "guides.json":
        return {"fallback": {}, "groups": {}}
    return {} if name.endswith("_translated.json") or name.endswith("_overlay.json") else []


def local_files():
    """{file name: parsed JSON} for every file the catalog is built from."""
    out = {}
    for name in FILES:
        path = DATA / name
        out[name] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else _default(name)
    return out


def rows_from_files(files):
    rows = []
    for side in SIDES:
        for pos, e in enumerate(files[f"{side}.json"]):
            rows.append({"kind": "entry", "id": e["id"], "data": {"side": side, "pos": pos, "item": e}})
    meta = {k: v for k, v in files["guides.json"].items() if k not in ("fallback", "groups")}
    rows.append({"kind": "guide", "id": "meta", "data": {"pos": -1, "item": meta}})  # version, _note
    pos = 0
    for section in ("fallback", "groups"):
        for key, g in files["guides.json"][section].items():
            rows.append({"kind": "guide", "id": f"{section}/{key}", "data": {"pos": pos, "item": g}})
            pos += 1
    for pos, ls in enumerate(files["lessons.json"]):
        rows.append({"kind": "lesson", "id": ls["id"], "data": {"pos": pos, "item": ls}})
    for pos, p in enumerate(files["problems.json"]):
        rows.append({"kind": "problem", "id": p["id"], "data": {"pos": pos, "item": p}})
    for name in OVERLAYS:
        rows.append({"kind": "ui_overlay", "id": name, "data": {"item": files[f"{name}.json"]}})
    return rows


def files_from_rows(rows):
    """Rebuild the JSON files from rows. Raises ValueError on anything unexpected (the caller falls back to JSON)."""
    if not isinstance(rows, list) or not rows:
        raise ValueError("no rows")
    by_kind = {k: [] for k in KINDS}
    seen = set()
    for r in rows:
        if not isinstance(r, dict) or r.get("kind") not in KINDS or not isinstance(r.get("id"), str) or not r["id"]:
            raise ValueError("bad row")
        d = r.get("data")
        if not isinstance(d, dict) or "item" not in d:
            raise ValueError("bad data")
        key = (r["kind"], r["id"])
        if key in seen:
            raise ValueError("duplicate row")
        seen.add(key)
        if r["kind"] != "ui_overlay" and not isinstance(d.get("pos"), int):
            raise ValueError("missing pos")
        by_kind[r["kind"]].append(r)
    if any(not v for v in by_kind.values()):
        raise ValueError("a kind is empty")

    files = {f"{s}.json": [] for s in SIDES}
    for r in sorted(by_kind["entry"], key=lambda r: r["data"]["pos"]):
        side, e = r["data"].get("side"), r["data"]["item"]
        if side not in SIDES or not isinstance(e, dict) or e.get("id") != r["id"] \
                or not isinstance(e.get("title"), dict) or not isinstance(e.get("desc"), dict):
            raise ValueError("bad entry")
        files[f"{side}.json"].append(e)

    guides = {"fallback": {}, "groups": {}}
    for r in sorted(by_kind["guide"], key=lambda r: r["data"]["pos"]):
        if r["id"] == "meta":
            if not isinstance(r["data"]["item"], dict):
                raise ValueError("bad guide meta")
            guides.update(r["data"]["item"])
            continue
        section, _, key = r["id"].partition("/")
        if section not in ("fallback", "groups") or not key or not isinstance(r["data"]["item"], dict):
            raise ValueError("bad guide")
        guides[section][key] = r["data"]["item"]
    files["guides.json"] = guides

    files["lessons.json"] = []
    for r in sorted(by_kind["lesson"], key=lambda r: r["data"]["pos"]):
        ls = r["data"]["item"]
        if not isinstance(ls, dict) or ls.get("id") != r["id"] or "entry_id" not in ls or not isinstance(ls.get("title"), dict):
            raise ValueError("bad lesson")
        files["lessons.json"].append(ls)

    files["problems.json"] = []
    for r in sorted(by_kind["problem"], key=lambda r: r["data"]["pos"]):
        p = r["data"]["item"]
        if not isinstance(p, dict) or p.get("id") != r["id"] or not isinstance(p.get("title"), dict):
            raise ValueError("bad problem")
        files["problems.json"].append(p)

    overlays = {r["id"]: r["data"]["item"] for r in by_kind["ui_overlay"]}
    for name in OVERLAYS:
        if not isinstance(overlays.get(name), dict):
            raise ValueError(f"missing overlay {name}")
        files[f"{name}.json"] = overlays[name]
    return files


def hash_by_kind(rows):
    """{kind: (count, sha256 of the canonical JSON of its rows sorted by id)}. Compares content, not order of arrival."""
    out = {}
    for kind in KINDS:
        mine = sorted((r for r in rows if r.get("kind") == kind), key=lambda r: r["id"])
        blob = json.dumps([[r["id"], r["data"]] for r in mine], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        out[kind] = (len(mine), hashlib.sha256(blob.encode("utf-8")).hexdigest())
    return out
