"""Flask app. Run: flask --app src/app run --debug"""
import os
import secrets

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, session, url_for

import delivery
import gate
import guide
import store

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

# UI strings per language. Backend/frontend leads: extend as pages grow.
UI = {
    "en": {"guide": "What should I learn?", "start": "Show my path", "learn": "Learn", "build": "Build", "all": "All levels", "source": "Source", "license": "License",
           "tagline": "Open-source programming resources, in your language."},
    "es": {"guide": "¿Qué debo aprender?", "start": "Mostrar mi ruta", "learn": "Aprender", "build": "Construir", "all": "Todos los niveles", "source": "Fuente", "license": "Licencia",
           "tagline": "Recursos de programación de código abierto, en tu idioma."},
    "ar": {"guide": "ماذا أتعلّم؟", "start": "اعرض مساري", "learn": "تعلّم", "build": "ابنِ", "all": "كل المستويات", "source": "المصدر", "license": "الرخصة",
           "tagline": "موارد برمجة مفتوحة المصدر بلغتك."},
    "hi": {"guide": "मुझे क्या सीखना चाहिए?", "start": "मेरा रास्ता दिखाएँ", "learn": "सीखें", "build": "बनाएँ", "all": "सभी स्तर", "source": "स्रोत", "license": "लाइसेंस",
           "tagline": "ओपन-सोर्स प्रोग्रामिंग संसाधन, आपकी भाषा में।"},
    "pt": {"guide": "O que devo aprender?", "start": "Mostrar meu caminho", "learn": "Aprender", "build": "Construir", "all": "Todos os níveis", "source": "Fonte", "license": "Licença",
           "tagline": "Recursos de programação open source, no seu idioma."},
}


KIDS_LABEL = {"en": "For kids", "es": "Para niños", "ar": "للأطفال", "hi": "बच्चों के लिए", "pt": "Para crianças"}
for _code, _label in KIDS_LABEL.items():
    UI[_code].setdefault("kids", _label)


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
    return render_template("home.html", **ctx(lang))


@app.route("/<lang>/<side>")
def listing(lang, side):
    if lang not in LANGS or side not in SIDES:
        abort(404)
    level, q, age, topic = filters()
    items = select(lang, side, level, q, age, topic)
    groups = {}
    for e in items:
        groups.setdefault(e["category"], []).append(e)
    return render_template("listing.html", side=side, groups=groups, level=level, q=q,
                           age=age, topic=topic, **ctx(lang))


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


def select(lang, side, level, q, age=None, topic=None):
    items = gate.filter_visible(store.entries(side), is_adult())
    if level:
        items = [e for e in items if e.get("level") == level]
    if age:  # entries suited to this age or younger
        items = [e for e in items if guide.age_fits(e, age)]
    if topic:
        items = [e for e in items if e.get("topic") == topic]
    if q:
        items = [e for e in items if store.matches(e, q, lang)]
    return items


@app.route("/<lang>/entry/<entry_id>")
def entry_page(lang, entry_id):
    e = store.get(entry_id)
    if lang not in LANGS or e is None or not gate.visible(e, is_adult()):
        abort(404)
    title, fb_title = store.text(e, "title", lang)
    desc, fb_desc = store.text(e, "desc", lang)
    return render_template("entry.html", e=e, title=title, desc=desc, fell_back=fb_title or fb_desc,
                           guide=delivery.guide_for(e["kind"]),
                           is_ai=lang in e.get("ai_translated", []), **ctx(lang))


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
    g = delivery.guide_for(kind)
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
    return render_template("guide.html", path=path, ages=guide.AGES, goals=list(guide.GOALS),
                           age=age, goal=goal, level=level, **ctx(lang))


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


def ctx(lang):
    return {"lang": lang, "langs": LANGS, "rtl": lang in RTL, "ui": {**UI["en"], **UI[lang]}, "levels": LEVELS, "adult": is_adult()}


if __name__ == "__main__":
    app.run(debug=True)
