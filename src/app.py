"""Flask app. Run: flask --app src/app run --debug"""
import os
import secrets

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, session, url_for

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
    return redirect(url_for("home", lang="en"))


@app.route("/<lang>/")
def home(lang):
    if lang not in LANGS:
        abort(404)
    return render_template("home.html", **ctx(lang))


@app.route("/<lang>/<side>")
def listing(lang, side):
    if lang not in LANGS or side not in SIDES:
        abort(404)
    level, q = filters()
    items = select(lang, side, level, q)
    groups = {}
    for e in items:
        groups.setdefault(e["category"], []).append(e)
    return render_template("listing.html", side=side, groups=groups, level=level, q=q, **ctx(lang))


def filters():
    """Validated query values. Anything not on the allow-list is dropped."""
    level = request.args.get("level")
    level = level if level in LEVELS else None
    q = (request.args.get("q") or "").strip()[:80]
    return level, q


def select(lang, side, level, q):
    items = gate.filter_visible(store.entries(side), is_adult())
    if level:
        items = [e for e in items if e.get("level") == level]
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
                           is_ai=lang in e.get("ai_translated", []), **ctx(lang))


@app.get("/api/entries")
def api_entries():
    lang = request.args.get("lang", "en")
    side = request.args.get("side")
    if lang not in LANGS or (side and side not in SIDES):
        abort(404)
    level, q = filters()
    items = select(lang, side, level, q)
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
    return {"lang": lang, "langs": LANGS, "rtl": lang in RTL, "ui": UI[lang], "levels": LEVELS, "adult": is_adult()}


if __name__ == "__main__":
    app.run(debug=True)
