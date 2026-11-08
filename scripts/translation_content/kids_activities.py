"""Hand-written (Claude Code, no API) translations for the 24 newest CS Unplugged entries: classroom activities and
programming-challenge pages. Languages: es, ar, hi, pt. Labeled `ai_translated` by apply_translations.py.
CS Unplugged text is CC BY-SA 4.0: these are adaptations ("changes were made"); see docs/SOURCES.md."""
import json
from pathlib import Path

LANGS = ("es", "ar", "hi", "pt")
ROOT = Path(__file__).resolve().parents[2]

UNIT = {
    "Binary numbers": dict(es="Números binarios", ar="الأعداد الثنائية", hi="बाइनरी संख्याएँ", pt="Números binários"),
    "Error detection and correction": dict(es="Detección y corrección de errores", ar="اكتشاف الأخطاء وتصحيحها", hi="त्रुटि पहचान और सुधार", pt="Detecção e correção de erros"),
    "Searching algorithms": dict(es="Algoritmos de búsqueda", ar="خوارزميات البحث", hi="खोज एल्गोरिदम", pt="Algoritmos de busca"),
    "Sorting networks": dict(es="Redes de ordenación", ar="شبكات الفرز", hi="सॉर्टिंग नेटवर्क", pt="Redes de ordenação"),
    "Kidbots": dict(es="Kidbots", ar="Kidbots", hi="Kidbots", pt="Kidbots"),
}
SUBJECT = {
    "art": dict(es="arte", ar="الفن", hi="कला", pt="arte"),
    "writing": dict(es="escritura", ar="الكتابة", hi="लेखन", pt="escrita"),
    "music": dict(es="música", ar="الموسيقى", hi="संगीत", pt="música"),
    "geometry": dict(es="geometría", ar="الهندسة", hi="ज्यामिति", pt="geometria"),
    "numeracy": dict(es="números y cálculo", ar="الحساب والأعداد", hi="संख्या ज्ञान", pt="números e cálculo"),
    "speaking": dict(es="expresión oral", ar="التحدث", hi="बोलना", pt="expressão oral"),
    "biology": dict(es="biología", ar="علم الأحياء", hi="जीव विज्ञान", pt="biologia"),
    "drama, art": dict(es="teatro y arte", ar="الدراما والفن", hi="नाटक और कला", pt="teatro e arte"),
    "word study": dict(es="estudio de palabras", ar="دراسة الكلمات", hi="शब्द अध्ययन", pt="estudo de palavras"),
}
ACTIVITY_DESC = dict(
    es="Una actividad de aula que une la unidad «{unit}» con {subject} (edades {ages}). Para que un adulto la haga con niños.",
    pt="Uma atividade de sala de aula que liga a unidade «{unit}» a {subject} (idades {ages}). Para um adulto fazer com as crianças.",
    ar="نشاط صفّي يربط وحدة «{unit}» بمادة {subject} (الأعمار {ages}). يقوم به شخص بالغ مع الأطفال.",
    hi="एक कक्षा गतिविधि जो इकाई «{unit}» को {subject} से जोड़ती है (उम्र {ages})। बच्चों के साथ किसी बड़े द्वारा कराने के लिए।",
)
PROGRAMMING_DESC = dict(
    es="Retos de programación (Scratch, Python o bloques) para acompañar la lección «{lesson}» de la unidad «{unit}». Mejor hacerlos con un adulto.",
    pt="Desafios de programação (Scratch, Python ou blocos) para acompanhar a lição «{lesson}» da unidade «{unit}». Melhor fazer com um adulto.",
    ar="تحديات برمجة (سكراتش أو بايثون أو الكتل) مرافقة لدرس «{lesson}» من وحدة «{unit}». الأفضل أن تُنجز مع شخص بالغ.",
    hi="पाठ «{lesson}» के साथ करने के लिए प्रोग्रामिंग चुनौतियाँ (Scratch, Python या ब्लॉक), इकाई «{unit}» से। किसी बड़े के साथ करना बेहतर है।",
)
PROGRAMMING_TITLE = dict(es="retos de programación", pt="desafios de programação", ar="تحديات البرمجة", hi="प्रोग्रामिंग चुनौतियाँ")

# English title -> titles per language
TITLES = {
    "Binary Art": dict(es="Arte binario", ar="الفن الثنائي", hi="बाइनरी कला", pt="Arte binária"),
    "What if?": dict(es="¿Y si…?", ar="ماذا لو؟", hi="अगर ऐसा हो तो?", pt="E se…?"),
    "Whose cake is it": dict(es="¿De quién es el pastel?", ar="لمن هذه الكعكة؟", hi="यह केक किसका है?", pt="De quem é o bolo?"),
    "Binary Candles or Normal Candles on your Cake": dict(es="Velas binarias o velas normales en tu pastel", ar="شموع ثنائية أم شموع عادية على كعكتك", hi="आपके केक पर बाइनरी मोमबत्तियाँ या सामान्य मोमबत्तियाँ", pt="Velas binárias ou velas normais no seu bolo"),
    "Moving in a shape": dict(es="Moverse formando una figura", ar="التحرك على شكل", hi="किसी आकार में चलना", pt="Mover-se em uma forma"),
    "Finding shapes": dict(es="Encontrar formas", ar="إيجاد الأشكال", hi="आकार ढूँढना", pt="Encontrar formas"),
    "Music activity": dict(es="Actividad de música", ar="نشاط موسيقي", hi="संगीत गतिविधि", pt="Atividade de música"),
    "Binary Tunes": dict(es="Melodías binarias", ar="ألحان ثنائية", hi="बाइनरी धुनें", pt="Melodias binárias"),
    "Drama or video activity": dict(es="Actividad de teatro o video", ar="نشاط تمثيل أو فيديو", hi="नाटक या वीडियो गतिविधि", pt="Atividade de teatro ou vídeo"),
    "Word study activity": dict(es="Actividad de estudio de palabras", ar="نشاط دراسة الكلمات", hi="शब्द अध्ययन गतिविधि", pt="Atividade de estudo de palavras"),
    "Growing into a butterfly": dict(es="Convertirse en mariposa", ar="التحوّل إلى فراشة", hi="तितली बनना", pt="Virando borboleta"),
    "Instructional writing": dict(es="Escritura de instrucciones", ar="كتابة التعليمات", hi="निर्देश लिखना", pt="Escrita de instruções"),
    "Move to a number": dict(es="Muévete a un número", ar="تحرّك إلى رقم", hi="किसी संख्या तक चलें", pt="Mova-se até um número"),
    "Retelling a story": dict(es="Volver a contar un cuento", ar="إعادة سرد قصة", hi="कहानी दोबारा सुनाना", pt="Recontar uma história"),
    "Binary Patterns": dict(es="Patrones binarios", ar="أنماط ثنائية", hi="बाइनरी पैटर्न", pt="Padrões binários"),
    "Storytelling": dict(es="Narración de cuentos", ar="رواية القصص", hi="कहानी सुनाना", pt="Contar histórias"),
    "Quick card flip magic": dict(es="Magia rápida de voltear cartas", ar="سحر قلب البطاقات السريع", hi="कार्ड पलटने का तेज़ जादू", pt="Mágica rápida de virar cartas"),
    "Where is my hat?": dict(es="¿Dónde está mi sombrero?", ar="أين قبعتي؟", hi="मेरी टोपी कहाँ है?", pt="Onde está meu chapéu?"),
    "Binary Name Necklaces": dict(es="Collares binarios con tu nombre", ar="قلادات الأسماء الثنائية", hi="बाइनरी नाम वाले हार", pt="Colares binários com seu nome"),
}


def _lesson_titles():
    kids = json.loads((ROOT / "src" / "data" / "kids.json").read_text(encoding="utf-8"))
    return {e["title"]["en"]: e["title"] for e in kids if all(l in e["title"] for l in LANGS)}


def build():
    """{entry id: {"title": {lang: str}, "desc": {lang: str}}} for the CS Unplugged activity and programming-challenge entries."""
    import re
    kids = json.loads((ROOT / "src" / "data" / "kids.json").read_text(encoding="utf-8"))
    lessons = _lesson_titles()
    out = {}
    for e in kids:
        en_title, en_desc = e["title"]["en"], e["desc"]["en"]
        title, desc = {}, {}
        m = re.match(r"A classroom activity linking the '(.+)' unit with (.+) \(ages ([\d-]+)\)\.", en_desc)
        p = re.match(r"Programming challenges \(Scratch, Python or blocks\) to go with the '(.+)' lesson, from the '(.+)' unit\.", en_desc)
        if not (m or p):  # units and lessons were translated earlier and are not part of this module
            continue
        for l in LANGS:
            if m:
                title[l] = TITLES[en_title][l]
                desc[l] = ACTIVITY_DESC[l].format(unit=UNIT[m.group(1)][l], subject=SUBJECT[m.group(2)][l], ages=m.group(3))
            elif p:
                lesson_en = p.group(1)
                lesson = lessons[lesson_en][l]
                title[l] = f"{lesson}: {PROGRAMMING_TITLE[l]}"
                desc[l] = PROGRAMMING_DESC[l].format(lesson=lesson, unit=UNIT[p.group(2)][l])
        out[e["id"]] = {"title": title, "desc": desc}
    return out
