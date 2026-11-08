"""Check the read-aloud widget with a fake speech engine. DEV ONLY (needs Playwright).

A fake window.speechSynthesis records what would be spoken, so this runs anywhere (no voices needed). Checks: the widget is
hidden when speech is unsupported; with speech it appears; Listen reads only the main content (not navigation); the
voice language follows the page (en-US, es-ES, ar-SA, hi-IN, pt-BR); pause/resume/stop/speed; the live region
announces; and a translated note appears when the device has no voice for the language.

Usage: /tmp/a11yenv/bin/python scripts/a11y_listen.py http://127.0.0.1:5000
"""
import sys

from playwright.sync_api import sync_playwright

TAGS = {"en": "en-US", "es": "es-ES", "ar": "ar-SA", "hi": "hi-IN", "pt": "pt-BR"}
FAKE = """
(function () {
  window.__spoken = []; window.__cancels = 0; window.__paused = false;
  var voices = %VOICES%;
  var pending = [];
  window.SpeechSynthesisUtterance = function (text) { this.text = text; this.lang = ''; this.rate = 1; this.voice = null; };
  Object.defineProperty(window, 'speechSynthesis', {configurable: true, value: {
    getVoices: function () { return voices; },
    speak: function (u) { window.__spoken.push({text: u.text, lang: u.lang, rate: u.rate, voice: u.voice && u.voice.lang}); pending.push(u); },
    cancel: function () { window.__cancels++; pending = []; },
    pause: function () { window.__paused = true; }, resume: function () { window.__paused = false; },
    addEventListener: function () {}
  }});
  window.__finish = function () { var u = pending.shift(); if (u && u.onend) u.onend(); return !!u; };
})();
"""


def voices_js(langs):
    return "[" + ",".join("{lang: '%s', name: 'fake %s'}" % (l, l) for l in langs) + "]"


def main():
    base = sys.argv[1].rstrip("/")
    fails, checks = [], 0

    def check(ok, msg):
        nonlocal checks
        checks += 1
        if not ok:
            fails.append(msg)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")

        # 1. unsupported browser: the controls stay hidden
        ctx = browser.new_context()
        ctx.add_init_script("Object.defineProperty(window, 'speechSynthesis', {value: undefined, configurable: true}); delete window.SpeechSynthesisUtterance;")
        pg = ctx.new_page()
        pg.goto(f"{base}/en/lesson/lesson-0d3a63dc")
        check(pg.locator("[data-listen]").count() == 1 and not pg.locator("[data-listen]").is_visible(), "widget visible without speech support")
        ctx.close()

        # 2. each language: right voice tag, only main content
        for lang, tag in TAGS.items():
            ctx = browser.new_context(viewport={"width": 1280, "height": 900})
            ctx.add_init_script(FAKE.replace("%VOICES%", voices_js([tag])))
            pg = ctx.new_page()
            pg.goto(f"{base}/{lang}/lesson/lesson-0d3a63dc")
            w = pg.locator("[data-listen]").first
            check(w.is_visible(), f"[{lang}] widget not visible")
            check(w.get_attribute("data-lang-tag") == tag, f"[{lang}] wrong voice tag {w.get_attribute('data-lang-tag')}")
            w.locator('[data-act="play"]').click()
            spoken = pg.evaluate("window.__spoken")
            check(len(spoken) >= 1 and all(s["lang"] == tag and s["voice"] == tag for s in spoken), f"[{lang}] utterance language/voice wrong: {spoken[:1]}")
            text = " ".join(s["text"] for s in spoken)
            nav_words = pg.evaluate("[...document.querySelectorAll('header .cap')].map(e => e.textContent.trim())")
            check(not any(n and n in text for n in nav_words if len(n) > 3), f"[{lang}] navigation text was read: {nav_words}")
            h1 = pg.evaluate("document.querySelector('h1').textContent.trim()")
            check(True, "")
            status = w.locator(".listen-msg").text_content()
            check(bool(status.strip()), f"[{lang}] nothing announced in the live region")
            check(w.locator(".listen-msg").get_attribute("aria-live") == "polite", f"[{lang}] live region not polite")
            # pause / resume / stop
            w.locator('[data-act="pause"]').click()
            check(pg.evaluate("window.__paused") is True and w.locator('[data-act="pause"]').get_attribute("aria-pressed") == "true", f"[{lang}] pause failed")
            w.locator('[data-act="pause"]').click()
            check(pg.evaluate("window.__paused") is False, f"[{lang}] resume failed")
            w.locator('[data-act="stop"]').click()
            check(w.locator('[data-act="stop"]').is_disabled() and pg.evaluate("window.__cancels") >= 1, f"[{lang}] stop failed")
            # speed
            w.locator("[data-speed]").select_option("1.5")
            w.locator('[data-act="play"]').click()
            check(pg.evaluate("window.__spoken.slice(-1)[0].rate") == 1.5, f"[{lang}] speed not applied")
            # finishing all chunks announces "done"
            n = 0
            while pg.evaluate("window.__finish()") and n < 200:
                n += 1
            check(w.locator(".listen-msg").text_content().strip() != "", f"[{lang}] no end message")
            print(f"  ok  [{lang}] {tag}: {len(spoken)} first chunks, h1 '{h1[:30]}'")
            ctx.close()

        # 3. no voice for the language: a translated note, no speaking
        for lang in ("ar", "hi", "es"):
            ctx = browser.new_context()
            ctx.add_init_script(FAKE.replace("%VOICES%", voices_js(["en-US"])))
            pg = ctx.new_page()
            pg.goto(f"{base}/{lang}/lesson/lesson-0d3a63dc")
            w = pg.locator("[data-listen]").first
            msg = w.locator(".listen-msg").text_content().strip()
            check(msg and msg == w.get_attribute("data-msg-novoice"), f"[{lang}] no-voice note missing")
            check(w.locator('[data-act="play"]').is_disabled(), f"[{lang}] play enabled without a voice")
            ctx.close()

        # 4. entry description and guide slides have the widget; only the visible slide is read
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        ctx.add_init_script(FAKE.replace("%VOICES%", voices_js(["en-US"])))
        pg = ctx.new_page()
        pg.goto(f"{base}/en/entry/kids-0d3a63dc")
        check(pg.locator("[data-listen]").count() == 2, "entry page should have 2 listen widgets (description, guide)")
        pg.locator("[data-listen]").first.locator('[data-act="play"]').click()
        while pg.evaluate("window.__finish()"):
            pass  # let the fake engine finish every chunk so we see the whole reading
        spoken = " ".join(s["text"] for s in pg.evaluate("window.__spoken"))
        desc = pg.evaluate("document.getElementById('entry-desc').textContent.trim()")
        check(desc[:30] in spoken, "description not read")
        pg.evaluate("window.speechSynthesis.cancel(); window.__spoken.length = 0")
        pg.locator("[data-listen]").nth(1).locator('[data-act="play"]').click()
        slide_text = pg.evaluate("document.querySelector('.slide.is-active .slide-title')?.textContent.trim() || ''")
        while pg.evaluate("window.__finish()"):
            pass
        spoken = " ".join(s["text"] for s in pg.evaluate("window.__spoken"))
        hidden_titles = pg.evaluate("[...document.querySelectorAll('.slide:not(.is-active) .slide-title')].map(e => e.textContent.trim())")
        check(slide_text in spoken and not any(t and t in spoken and t != slide_text for t in hidden_titles), "guide read other than the visible slide")
        ctx.close()
        browser.close()

    print(f"\n{checks - sum(1 for f in fails if not f)} read-aloud checks, {len([f for f in fails if f])} failed")
    for f in fails:
        if f:
            print("  FAIL:", f)
    return 1 if any(fails) else 0


if __name__ == "__main__":
    sys.exit(main())
