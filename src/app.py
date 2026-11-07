"""Flask app. Run: flask --app src/app run --debug"""
import json
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, url_for

import guide

load_dotenv()
app = Flask(__name__)
DATA = Path(__file__).parent / "data"
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


def load(side):
    path = DATA / f"{side}.json"
    return json.loads(path.read_text()) if path.exists() else []


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
    if lang not in LANGS or side not in ("learn", "build"):
        abort(404)
    level = request.args.get("level")
    items = [e for e in load(side) if not level or e.get("level") == level]
    groups = {}
    for e in items:
        groups.setdefault(e["category"], []).append(e)
    return render_template("listing.html", side=side, groups=groups, level=level, **ctx(lang))


@app.route("/<lang>/guide")
def guide_page(lang):
    if lang not in LANGS:
        abort(404)
    age, goal, level = (request.args.get(k) for k in ("age", "goal", "level"))
    path = None
    if age in guide.AGES and goal in guide.GOALS and level in LEVELS:
        entries = load("learn") + load("build")
        path = guide.build_path(entries, age, goal, level)
    return render_template("guide.html", path=path, ages=guide.AGES, goals=list(guide.GOALS),
                           age=age, goal=goal, level=level, **ctx(lang))


def ctx(lang):
    return {"lang": lang, "langs": LANGS, "rtl": lang in RTL, "ui": UI[lang], "levels": LEVELS}


if __name__ == "__main__":
    app.run(debug=True)
