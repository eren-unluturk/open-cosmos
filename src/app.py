"""Flask app. Run: flask --app src/app run --debug"""
import hmac
import json
import os
import secrets
import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, session, url_for

import delivery
import gate
import guide
import i18n_guides
import i18n_lessons
import i18n_problems
import feedback
import i18n_a11y
import i18n_feedback
import supabase_client
import problems as problem_kit
import store
import tracks
from ui_strings import UI as GALAXY_UI

# The data lead owns scripts/guide_helpers.py (pure Python). We import it as is.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import guide_helpers  # noqa: E402

load_dotenv()
app = Flask(__name__)
# Set SECRET_KEY in .env for production. A random fallback only resets sessions on restart.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                  SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1")  # on in production (HTTPS)
SIDES = store.SIDES
TOPICS = ("games", "art", "web", "general", "systems", "security", "other")
LANGS = {"en": "English", "es": "Español", "ar": "العربية", "hi": "हिन्दी", "pt": "Português"}
RTL = {"ar"}
LEVELS = ["Beginner", "Intermediate", "Advanced"]

# UI strings: galaxy frontend strings live in ui_strings.py; guide/lesson labels in i18n_*.py are layered on top.
UI = GALAXY_UI


KIDS_LABEL = {"en": "For kids", "es": "Para niños", "ar": "للأطفال", "hi": "बच्चों के लिए", "pt": "Para crianças"}
for _code, _label in KIDS_LABEL.items():
    UI[_code].setdefault("kids", _label)
UI["en"].update(i18n_guides.UI_EN)
UI["en"].update(i18n_lessons.UI_EN)
UI["en"].update(i18n_problems.UI_EN)
UI["en"].update(i18n_feedback.UI_EN)
UI["en"].update(i18n_a11y.UI_EN)
for _code, _extra in i18n_guides.UI.items():
    UI[_code].update(_extra)
for _code, _extra in i18n_lessons.UI.items():
    UI[_code].update(_extra)
for _code, _extra in i18n_problems.UI.items():
    UI[_code].update(_extra)
for _code, _extra in i18n_feedback.UI.items():
    UI[_code].update(_extra)
for _code, _extra in i18n_a11y.UI.items():
    UI[_code].update(_extra)


def is_adult():
    return bool(session.get("adult"))


@app.route("/")
def index():
    # Pick the best supported language from the browser, default English.
    lang = request.accept_languages.best_match(list(LANGS)) or "en"
    return redirect(url_for("home", lang=lang))


@app.route("/<lang>/")
def home(lang):
    if lang not in LANGS:
        abort(404)
    u, lv = universe(), level_pref()
    rows = [(g, u.row(g, lv)) for g in u.galaxies]
    return render_template("home.html", suggestions=u.suggestions(3, lv), rows=rows,
                           lesson_count=len(store.lessons()), **ctx(lang))


@app.route("/<lang>/<side>")
def listing(lang, side):
    if lang not in LANGS or side not in SIDES:
        abort(404)
    level, q, age, topic = filters()
    items = select(lang, side, level, q, age, topic)
    groups = {}
    for e in items:
        groups.setdefault(e["category"], []).append(e)
    hidden = 0
    if not is_adult():  # entries a grown-up could reveal (adult-only is never counted or shown)
        hidden = len(select(lang, side, level, q, age, topic, adult=True)) - len(items)
    return render_template("listing.html", side=side, groups=groups, level=level, q=q,
                           age=age, topic=topic, ages=guide.AGES, topics=TOPICS, hidden=hidden, **ctx(lang))


def filters():
    """Validated query values. Anything not on the allow-list is dropped."""
    level = request.args.get("level")
    level = level if level in LEVELS else None
    q = (request.args.get("q") or "").strip()[:80]
    age = request.args.get("age")
    age = age if age in guide.AGES else None
    topic = request.args.get("topic")
    topic = topic if topic in TOPICS else None
    return level, q, age, topic


def select(lang, side, level, q, age=None, topic=None, adult=None):
    items = gate.filter_visible(store.entries(side), is_adult() if adult is None else adult)
    if level:
        items = [e for e in items if e.get("level") == level]
    if age:  # entries suited to this age or younger
        items = [e for e in items if guide.age_fits(e, age)]
    if topic:
        items = [e for e in items if e.get("topic") == topic]
    if q:
        items = [e for e in items if store.matches(e, q, lang)]
    return items


def tx(value, lang):
    """Text from a {"en": ..., "es": ...} dict. Returns (text, fell_back_to_english)."""
    if not isinstance(value, dict):
        return value, False
    if value.get(lang):
        return value[lang], False
    return value.get("en", ""), lang != "en"


def localize_slides(slides, entry, age, lang):
    """Guide slides with text picked for lang and {placeholders} filled. Also says if English was used."""
    timeline = guide_helpers.build_timeline(entry, age)
    english = False

    def pick(value):
        nonlocal english
        text, fell = tx(value, lang)
        english = english or fell
        return guide_helpers.fill(text, entry, age, lang)

    out = []
    for s in slides:
        item = {"type": s["type"], "title": pick(s["title"]), "estimate": bool(s.get("estimate")),
                "leaving_site": bool(s.get("leaving_site")), "attribution": bool(s.get("attribution"))}
        if s.get("body"):
            item["body"] = pick(s["body"])
        if s.get("steps"):
            item["steps"] = [pick(x) for x in s["steps"]]
        if s.get("adult_note"):
            item["adult_note"] = pick(s["adult_note"])
        if s.get("timeline"):
            item["timeline"] = [{"when": pick(x["when"]), "goal": pick(x["goal"]),
                                 "minutes": timeline["minutes"] if x["minutes"] == "{minutes}" else x["minutes"]}
                                for x in s["timeline"]]
        out.append(item)
    return out, english, timeline


@app.route("/<lang>/entry/<entry_id>")
def entry_page(lang, entry_id):
    e = store.get(entry_id)
    if lang not in LANGS or e is None or not gate.visible(e, is_adult()):
        abort(404)
    title, fb_title = store.text(e, "title", lang)
    desc, fb_desc = store.text(e, "desc", lang)
    age = request.args.get("age")
    age = age if age in guide_helpers.AGES else None
    resolved = guide_helpers.guide_for(e, store.guides(), store.lessons())
    slides, english_only, timeline = localize_slides(resolved["slides"], e, age, lang)
    visible_entries = [x for x in store.entries() if x.get("safety") == "kid-safe"]  # never the grown-up tier
    related = guide_helpers.related_entries(e, visible_entries, age=age)
    # where this entry sits on the galaxy map (breadcrumbs + path strip)
    u = universe()
    gid, sid = request.args.get("g"), request.args.get("s")
    if (gid, sid) not in u.membership.get(entry_id, []):
        gid, sid = u.home_of(entry_id)
    nb = u.neighbours(gid, sid, entry_id) if gid else {"index": None, "stops": [], "suggested": []}
    return render_template("entry.html", e=e, title=title, desc=desc, fell_back=fb_title or fb_desc,
                           gid=gid, sid=sid, nb=nb,
                           guide=delivery.guide_for(e["kind"], lang), slides=slides, timeline=timeline,
                           guide_english_only=english_only and lang != "en", related=related, age=age,
                           lesson=store.lesson_for_entry(e["id"]) if e.get("reuse") == "open-content" else None,
                           is_ai=lang in e.get("ai_translated", []), **ctx(lang))


@app.route("/<lang>/stop/<entry_id>")
def stop_redirect(lang, entry_id):
    """Old galaxy URL; kept so saved progress links keep working."""
    return redirect(url_for("entry_page", lang=lang, entry_id=entry_id, **request.args))


@app.route("/<lang>/lessons")
def lessons_page(lang):
    if lang not in LANGS:
        abort(404)
    _, _, age, _ = filters()
    items = []
    for ls in store.lessons():
        entry = store.get(ls["entry_id"])
        if entry is None or entry.get("reuse") != "open-content" or not gate.visible(entry, is_adult()):
            continue
        if age and not guide.age_fits(ls, age):
            continue
        items.append(ls)
    order = {a: i for i, a in enumerate(guide.AGE_ORDER)}
    items.sort(key=lambda x: (order.get(x["age_group"], 9), x["title"]["en"].lower()))
    return render_template("lessons.html", lessons=items, age=age, ages=guide.AGES, **ctx(lang))


@app.route("/<lang>/lesson/<lesson_id>")
def lesson_page(lang, lesson_id):
    ls = store.lesson_by_id(lesson_id)
    entry = store.get(ls["entry_id"]) if ls else None
    # Only open-content entries have lessons, and only visible entries are shown.
    if lang not in LANGS or ls is None or entry is None or entry.get("reuse") != "open-content" \
            or not gate.visible(entry, is_adult()):
        abort(404)
    english = False
    def pick(field):
        nonlocal english
        value, fell = tx(ls.get(field), lang)
        english = english or fell
        return value
    view = {f: pick(f) for f in ("title", "summary", "objectives", "materials", "steps", "talk_about", "grown_up_note")}
    return render_template("lesson.html", ls=ls, v=view, entry=entry, english_only=english and lang != "en", **ctx(lang))

# --- Coding problems. The learner's code runs in their browser (static/runner.js). We never run it. ---

LANGUAGES = problem_kit.LANGUAGES


def problem_text(p, field, lang):
    return tx(p.get(field), lang)


def localize_tests(tests, lang):
    return [{"name": tx(t["name"], lang)[0], "code": t["code"]} for t in tests]


@app.route("/<lang>/problems")
def problems_page(lang):
    if lang not in LANGS:
        abort(404)
    level, q, age, _ = filters()
    language = request.args.get("language")
    language = language if language in LANGUAGES else None
    items = []
    for p in store.problems():
        if level and p["level"] != level:
            continue
        if language and p["language"] != language:
            continue
        if age and not guide.age_fits(p, age):
            continue
        if q and not store.matches({"title": p["title"], "desc": p["prompt"], "category": " ".join(p["concepts"]["en"]), "tag": p["language"]}, q, lang):
            continue
        items.append(p)
    order = {l: i for i, l in enumerate(problem_kit.LEVELS)}
    ages = {a: i for i, a in enumerate(guide.AGE_ORDER)}
    items.sort(key=lambda p: (order[p["level"]], ages[p["age_group"]], p["title"]["en"].lower()))
    return render_template("problems.html", problems=items, level=level, language=language, age=age, q=q,
                           languages=LANGUAGES, ages=guide.AGES, **ctx(lang))


@app.route("/<lang>/problem/<problem_id>")
def problem_page(lang, problem_id):
    p = store.problem(problem_id)
    if lang not in LANGS or p is None:
        abort(404)
    title, fb1 = problem_text(p, "title", lang)
    prompt, fb2 = problem_text(p, "prompt", lang)
    concepts, fb3 = problem_text(p, "concepts", lang)
    fell_back = fb1 or fb2 or fb3
    stages = []
    for s in p.get("guided", []):
        goal, g1 = tx(s["goal"], lang)
        explain, g2 = tx(s["explain"], lang)
        fell_back = fell_back or g1 or g2
        stages.append({"goal": goal, "explain": explain, "starter": s.get("starter", ""),
                       "tests": localize_tests(s["tests"], lang)})
    config = {
        "id": p["id"], "language": p["language"], "lang": lang, "starter": p["starter"],
        "preamble": p.get("preamble", ""),
        "prelude": problem_kit.PRELUDE_PY if p["language"] == "python" else problem_kit.PRELUDE_JS,
        "tests": localize_tests(p["tests"], lang), "stages": stages, "hint_count": len(p["hints"]["en"]),
        "max_code": problem_kit.MAX_CODE, "title": title, "galaxy": "code",
        "url": url_for("problem_page", lang=lang, problem_id=p["id"]),
        "ui": {k: v for k, v in ctx(lang)["ui"].items() if k.startswith("p_")},
    }
    return render_template("problem.html", p=p, title=title, prompt=prompt, concepts=concepts, config=config,
                           english_only=fell_back and lang != "en", **ctx(lang))


def api_problem_or_404(problem_id):
    p = store.problem(problem_id)
    if p is None:
        abort(404)
    return p


@app.get("/api/problems")
def api_problems():
    lang = request.args.get("lang", "en")
    if lang not in LANGS:
        abort(404)
    return {"count": len(store.problems()), "problems": [
        {"id": p["id"], "language": p["language"], "level": p["level"], "age_group": p["age_group"],
         "topic": p["topic"], "title": tx(p["title"], lang)[0], "concepts": tx(p["concepts"], lang)[0]}
        for p in store.problems()]}


@app.get("/api/problems/<problem_id>")
def api_problem(problem_id):
    return problem_kit.public_view(api_problem_or_404(problem_id))


@app.get("/api/problems/<problem_id>/hint/<int:n>")
def api_problem_hint(problem_id, n):
    """Hints are handed out one at a time (n starts at 1) so they are not in the page from the start."""
    p = api_problem_or_404(problem_id)
    lang = request.args.get("lang", "en")
    hints = tx(p["hints"], lang if lang in LANGS else "en")[0]
    if n < 1 or n > len(hints):
        abort(404)
    return {"index": n, "total": len(hints), "hint": hints[n - 1]}


@app.get("/api/problems/<problem_id>/solution")
def api_problem_solution(problem_id):
    """The reference answer. ?stage=3 gives the example for guided step 3 (1-based)."""
    p = api_problem_or_404(problem_id)
    lang = request.args.get("lang", "en")
    lang = lang if lang in LANGS else "en"
    stage = request.args.get("stage")
    if stage:
        if not stage.isdigit() or not 1 <= int(stage) <= len(p.get("guided", [])):
            abort(404)
        s = p["guided"][int(stage) - 1]
        return {"stage": int(stage), "solution": s["solution"], "note": tx(s["explain"], lang)[0]}
    return {"solution": p["solution"], "note": tx(p.get("solution_note", {"en": ""}), lang)[0]}


@app.route("/<lang>/catalogue")
def catalogue(lang):
    if lang not in LANGS:
        abort(404)
    level, q, age, topic = filters()
    groups = split_catalogue(select(lang, None, level, q, age, topic))
    return render_template("catalogue.html", groups=groups, level=level, q=q, age=age, topic=topic,
                           kinds=delivery.GUIDES, **ctx(lang))


@app.route("/<lang>/howto/<kind>")
def howto(lang, kind):
    g = delivery.guide_for(kind, lang)
    if lang not in LANGS or g is None:
        abort(404)
    return render_template("howto.html", g=g, kind=kind, kinds=delivery.GUIDES, **ctx(lang))


def split_catalogue(items):
    """{"hostable": {level: [...]}, "external": {level: [...]}}, easier levels first, empty levels dropped."""
    out = {d: {l: [] for l in LEVELS} for d in ("hostable", "external")}
    for e in items:
        if e.get("level") in LEVELS:
            out[e["delivery"]][e["level"]].append(e)
    return {d: {l: es for l, es in by.items() if es} for d, by in out.items()}


@app.get("/api/catalogue")
def api_catalogue():
    lang = request.args.get("lang", "en")
    if lang not in LANGS:
        abort(404)
    level, q, age, topic = filters()
    groups = split_catalogue(select(lang, None, level, q, age, topic))

    def brief(e):
        return {"id": e["id"], "side": e["side"], "kind": e["kind"], "level": e["level"],
                "age_group": e.get("age_group"), "topic": e.get("topic"),
                "title": store.text(e, "title", lang)[0], "url": e["url"], "license": e["license"]}

    return {d: {"count": sum(len(es) for es in by.values()),
                "levels": {l: [brief(e) for e in es] for l, es in by.items()}}
            for d, by in groups.items()}


@app.get("/api/entries")
def api_entries():
    lang = request.args.get("lang", "en")
    side = request.args.get("side")
    if lang not in LANGS or (side and side not in SIDES):
        abort(404)
    level, q, age, topic = filters()
    items = select(lang, side, level, q, age, topic)
    return {"count": len(items), "entries": [
        {"id": e["id"], "side": e["side"], "title": store.text(e, "title", lang)[0],
         "desc": store.text(e, "desc", lang)[0], "level": e.get("level"), "age_group": e.get("age_group"),
         "topic": e.get("topic"), "safety": e.get("safety"), "url": e["url"], "license": e["license"]}
        for e in items]}


@app.route("/<lang>/guide")
def guide_page(lang):
    if lang not in LANGS:
        abort(404)
    age, goal, level = (request.args.get(k) for k in ("age", "goal", "level"))
    path = None
    if age in guide.AGES and goal in guide.GOALS and level in LEVELS:
        entries = gate.filter_visible(store.entries())
        path = guide.build_path(entries, age, goal, level)
    short = path is not None and len(path) < guide.PATH_LEN  # tell the child more is coming
    return render_template("guide.html", path=path, short=short, ages=guide.AGES, goals=list(guide.GOALS),
                           age=age, goal=goal, level=level, **ctx(lang))


# --- galaxy pages (frontend, docs/FRONTEND.md) ---
@lru_cache(maxsize=2)
def _universe(adult):
    return tracks.Universe(store.entries(), adult)


def universe():
    return _universe(is_adult())


def level_pref():
    lv = request.args.get("level") or session.get("level")
    return lv if lv in LEVELS else None


@app.route("/<lang>/constellation")
def constellation(lang):
    if lang not in LANGS:
        abort(404)
    return render_template("constellation.html", links=tracks.LINKS, **ctx(lang))


@app.route("/<lang>/galaxy/<gid>")
def galaxy(lang, gid):
    u = universe()
    g = u.g.get(gid)
    if lang not in LANGS or g is None:
        abort(404)
    return render_template("galaxy.html", g=g, layout=u.orbit_layout(g), **ctx(lang))


@app.route("/<lang>/galaxy/<gid>/<sid>")
def system(lang, gid, sid):
    u = universe()
    s = u.system(gid, sid)
    if lang not in LANGS or s is None:
        abort(404)
    return render_template("system.html", g=u.g[gid], s=s, **ctx(lang))


@app.route("/<lang>/library")
def library(lang):
    if lang not in LANGS:
        abort(404)
    u = universe()
    q = (request.args.get("q") or "").strip()[:80]
    gid = request.args.get("g")
    gid = gid if gid in u.g else None
    lv = level_pref()
    where = request.args.get("where")
    where = where if where in WHERE else None
    pool = u.all if not gid else [e for s in u.g[gid]["systems"] for e in s["stops"]]
    seen, matched = set(), []
    for e in sorted(pool, key=tracks.stop_sort_key):
        if e["id"] in seen or not u.visible(e) or (lv and e.get("level") != lv) or (q and not store.matches(e, q, lang)):
            continue
        seen.add(e["id"])
        g, s = u.home_of(e["id"])
        matched.append({"e": e, "galaxy": g, "system": s, "where": where_of(e)})
    probs = problem_hits(lang, q, lv) if (not gid or gid == PROBLEM_GALAXY) else []
    counts = {"site": len(probs) + sum(1 for r in matched if r["where"] == "site"),
              "external": sum(1 for r in matched if r["where"] == "external")}
    results = [r for r in matched if not where or r["where"] == where]
    if where == "external":
        probs = []
    page = max(1, request.args.get("page", 1, type=int))
    hidden = 0 if (q or gid or is_adult()) else len([e for e in u.all if not u.visible(e)])
    return render_template("library.html", q=q, gid=gid, where=where, counts=counts, problems=probs,
                           results=results[: page * 48], total=len(results) + len(probs),
                           page=page, hidden=hidden, **ctx(lang))


# "Where do you do it?" filter on the Everything page.
#   site      you can do it here: our coding problems, and entries that have one of our adapted lessons
#   external  a link to another site (the lesson is done there)
WHERE = ("site", "external")
PROBLEM_GALAXY = "code"  # coding problems live in the "code" galaxy


def where_of(entry):
    return "site" if entry.get("lesson_id") else "external"


def problem_hits(lang, q, level):
    """Coding problems that match the search box and level filter."""
    out = []
    for p in store.problems():
        if level and p["level"] != level:
            continue
        if q and not store.matches({"title": p["title"], "desc": p["prompt"], "category": " ".join(p["concepts"]["en"]),
                                    "tag": p["language"]}, q, lang):
            continue
        out.append(p)
    order = {l: i for i, l in enumerate(problem_kit.LEVELS)}
    return sorted(out, key=lambda p: (order[p["level"]], p["title"]["en"].lower()))


@app.route("/<lang>/me")
def me(lang):
    if lang not in LANGS:
        abort(404)
    return render_template("me.html", **ctx(lang))


@app.post("/<lang>/prefs")
def prefs(lang):
    """Level filter (Beginner robot / Intermediate alien / Advanced astronaut). Session only."""
    if lang not in LANGS:
        abort(404)
    lv = request.form.get("level", "")
    if lv in LEVELS:
        session["level"] = lv
    else:
        session.pop("level", None)
    nxt = request.form.get("next") or url_for("home", lang=lang)
    if not nxt.startswith("/") or nxt.startswith("//"):  # block open redirects
        nxt = "/"
    return redirect(nxt)


@app.post("/grownup")
def grownup():
    # Session-only flag. No account, nothing stored on the server.
    if request.form.get("on") == "1":
        session["adult"] = True
    else:
        session.pop("adult", None)
    nxt = request.form.get("next", "/")
    if not nxt.startswith("/") or nxt.startswith("//"):  # block open redirects
        nxt = "/"
    return redirect(nxt)


# ---- Grown-ups' feedback (adults only). Stored in Supabase, never shown back on any page. ----
limiter = feedback.RateLimiter()


def _csrf_token():
    if not session.get("csrf"):
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]


@app.route("/<lang>/feedback", methods=["GET", "POST"])
def feedback_page(lang):
    if lang not in LANGS or not is_adult():
        abort(404)  # the form does not exist until the grown-up session is on
    status = request.args.get("status") if request.method == "GET" else None
    if status not in ("sent", "down", "invalid", "rate", "expired"):
        status = None
    if request.method == "POST":
        sent = request.form
        if sent.get("website"):  # honeypot: bots fill hidden fields; pretend it worked, store nothing
            return redirect(url_for("feedback_page", lang=lang, status="sent"))
        token = session.get("csrf") or ""
        if not token or not hmac.compare_digest(token, str(sent.get("csrf", ""))):
            return redirect(url_for("feedback_page", lang=lang, status="expired"))
        payload, err = feedback.validate(sent.get("kind"), sent.get("message"), sent.get("page"), lang)
        if err:
            return redirect(url_for("feedback_page", lang=lang, status="invalid"))
        if not session.get("sid"):
            session["sid"] = secrets.token_hex(8)
        if not limiter.allow(session["sid"]):
            return redirect(url_for("feedback_page", lang=lang, status="rate"))
        url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_ANON_KEY")
        ok = bool(url and key) and supabase_client.insert_feedback(url, key, payload)
        return redirect(url_for("feedback_page", lang=lang, status="sent" if ok else "down"))
    page = feedback.clean_page(request.args.get("page", "/"))
    return render_template("feedback.html", status=status, page=page, csrf=_csrf_token(),
                           kinds=feedback.KINDS, **ctx(lang))


@app.route("/<lang>/accessibility")
def accessibility(lang):
    if lang not in LANGS:
        abort(404)
    return render_template("accessibility.html", **ctx(lang))


@app.errorhandler(404)
def not_found(_):
    if request.path.startswith("/api/"):
        return {"error": "not found"}, 404
    return "Not found", 404


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.after_request
def security_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    return resp


# Progress strings (privacy line, counts, progress code). Used by galaxy.js, the one progress system (issue #26). "_note" is for humans.
PROGRESS_TEXT = {k: v for k, v in json.loads((Path(__file__).parent / "data" / "progress_text.json")
                                             .read_text(encoding="utf-8")).items() if k != "_note"}


def ctx(lang):
    u = universe()
    return {"lang": lang, "langs": LANGS, "rtl": lang in RTL, "ui": UI[lang], "levels": LEVELS, "adult": is_adult(),
            "grownup": is_adult(), "u": u, "galaxies": u.galaxies, "cur_level": level_pref(),
            "difficulty": tracks.difficulty, "kind_of": tracks.kind, "level_icon": tracks.LEVEL_ICON,
            "progress_text": {**PROGRESS_TEXT["en"], **PROGRESS_TEXT.get(lang, {})}}


# Voice language for read-aloud (the page language decides the voice)
app.jinja_env.globals["listen_tags"] = {"en": "en-US", "es": "es-ES", "ar": "ar-SA", "hi": "hi-IN", "pt": "pt-BR"}
app.jinja_env.globals["category_label"] = lambda name, lang: store.category(name, lang)


@app.context_processor
def helpers():
    def switch_lang(code):
        path = request.path
        if request.view_args and "lang" in request.view_args:
            path = path.replace("/" + request.view_args["lang"], "/" + code, 1)
        qs = request.query_string.decode()
        return path + ("?" + qs if qs else "")

    def tr(field, lang):
        if not isinstance(field, dict):
            return field or ""
        return field.get(lang) or field.get("en", "")

    return {"switch_lang": switch_lang, "tr": tr}


if __name__ == "__main__":
    app.run(debug=True)
