/* Read aloud with the browser's built-in speech synthesis. No network, no cost, no data leaves the device.
   Each widget is <div data-listen data-target="#id" data-lang-tag="es-ES" hidden>. It stays hidden when the browser
   has no speech synthesis. Only the target's main content is read: navigation, buttons, hidden parts and other
   controls are skipped. Messages are announced through the widget's polite live region. */
(function () {
  "use strict";
  var synth = window.speechSynthesis;
  if (!synth || typeof window.SpeechSynthesisUtterance === "undefined") return; // unsupported: the buttons stay hidden

  var widgets = document.querySelectorAll("[data-listen]");
  if (!widgets.length) return;
  var current = null; // the widget that is reading now (only one at a time)

  var SKIP = "nav, button, select, input, textarea, script, style, svg, noscript, iframe, form, [aria-hidden='true'], [hidden], [inert], .listen, .sr-only, [data-no-listen]";
  var BLOCK = /^(P|LI|H[1-6]|DIV|SECTION|ARTICLE|TR|DD|DT|BLOCKQUOTE|PRE|FIGCAPTION|SUMMARY|OL|UL|ASIDE|HEADER|FOOTER|MAIN)$/;

  function visible(el) {
    var cs = window.getComputedStyle(el);
    return cs.display !== "none" && cs.visibility !== "hidden";
  }

  /* The text to read, as a list of paragraphs. */
  function paragraphs(root) {
    var out = [], buf = "";
    function flush() { var t = buf.replace(/\s+/g, " ").trim(); if (t) out.push(t); buf = ""; }
    function walk(node) {
      if (node.nodeType === 3) { buf += node.nodeValue; return; }
      if (node.nodeType !== 1) return;
      if (node !== root && (node.matches(SKIP) || !visible(node))) return;
      var block = BLOCK.test(node.tagName);
      var heading = /^H[1-6]$/.test(node.tagName);
      if (block) flush();
      for (var c = node.firstChild; c; c = c.nextSibling) walk(c);
      if (block) {
        if (heading && buf && !/[.!?؟।]$/.test(buf.trim())) buf += ".";
        flush();
      }
    }
    walk(root);
    flush();
    return out;
  }

  /* Short chunks: some browsers cut off long utterances after ~15 seconds. */
  function chunks(paras) {
    var out = [];
    paras.forEach(function (p) {
      var sentences = p.match(/[^.!?؟।]+[.!?؟।]*\s*/g) || [p], cur = "";
      sentences.forEach(function (s) {
        if ((cur + s).length > 200 && cur) { out.push(cur.trim()); cur = ""; }
        cur += s;
      });
      if (cur.trim()) out.push(cur.trim());
    });
    return out;
  }

  function pickVoice(tag) {
    var voices = synth.getVoices ? synth.getVoices() : [];
    var want = tag.toLowerCase().replace("_", "-"), base = want.split("-")[0], exact = null, near = null;
    voices.forEach(function (v) {
      var l = (v.lang || "").toLowerCase().replace("_", "-");
      if (!exact && l === want) exact = v;
      if (!near && l.split("-")[0] === base) near = v;
    });
    return { voice: exact || near, known: voices.length > 0 };
  }

  function setup(w) {
    var tag = w.getAttribute("data-lang-tag") || "en-US";
    var btnPlay = w.querySelector('[data-act="play"]');
    var btnPause = w.querySelector('[data-act="pause"]');
    var btnStop = w.querySelector('[data-act="stop"]');
    var speed = w.querySelector("[data-speed]");
    var msg = w.querySelector(".listen-msg");
    var T = function (k) { return w.getAttribute("data-msg-" + k) || ""; };
    var queue = [], idx = 0, state = "idle", paused = false;

    function say(text) { if (msg) msg.textContent = text; }
    function ui() {
      btnPlay.disabled = (state === "playing") || w.hasAttribute("data-novoice");
      btnPause.disabled = state === "idle";
      btnStop.disabled = state === "idle";
      btnPause.textContent = paused ? T("resume") : T("pause");
      btnPause.setAttribute("aria-pressed", paused ? "true" : "false");
    }
    function stop(silent) {
      try { synth.cancel(); } catch (e) { /* ignore */ }
      state = "idle"; paused = false; queue = []; idx = 0;
      if (current === w) current = null;
      ui();
      if (!silent) say(T("stopped"));
    }
    function noVoice() {
      w.setAttribute("data-novoice", "");
      state = "idle"; paused = false;
      say(T("novoice")); ui();
    }
    function speakFrom(i) {
      if (i >= queue.length) { state = "idle"; paused = false; if (current === w) current = null; ui(); say(T("done")); return; }
      idx = i;
      var u = new window.SpeechSynthesisUtterance(queue[i]);
      var pv = pickVoice(tag);
      u.lang = tag;
      if (pv.voice) u.voice = pv.voice;
      u.rate = parseFloat(speed ? speed.value : "1") || 1;
      u.onend = function () { if (state === "playing" && idx === i) speakFrom(i + 1); };
      u.onerror = function (e) {
        if (e && (e.error === "canceled" || e.error === "interrupted")) return;
        if (e && (e.error === "language-unavailable" || e.error === "voice-unavailable" || e.error === "synthesis-unavailable")) noVoice();
        else { state = "idle"; ui(); }
      };
      try { synth.speak(u); } catch (e) { state = "idle"; paused = false; if (current === w) current = null; ui(); }
    }
    function play() {
      if (current && current !== w) current.stop(true);
      var pv = pickVoice(tag);
      if (pv.known && !pv.voice) { noVoice(); return; }
      var roots = document.querySelectorAll(w.getAttribute("data-target")); // a selector list reads each match in page order
      var paras = [];
      Array.prototype.forEach.call(roots, function (r) { paras = paras.concat(paragraphs(r)); });
      queue = chunks(paras);
      if (!queue.length) { say(T("nothing")); return; }
      try { synth.cancel(); } catch (e) { /* ignore */ }
      state = "playing"; paused = false; current = w; ui();
      say(T("playing"));
      speakFrom(0);
    }

    btnPlay.addEventListener("click", play);
    btnPause.addEventListener("click", function () {
      if (state === "idle") return;
      if (paused) { synth.resume(); paused = false; state = "playing"; say(T("playing")); }
      else { synth.pause(); paused = true; say(T("paused")); }
      ui();
    });
    btnStop.addEventListener("click", function () { stop(false); });
    if (speed) speed.addEventListener("change", function () {
      if (state === "playing" && !paused) { try { synth.cancel(); } catch (e) { /* ignore */ } var i = idx; window.setTimeout(function () { speakFrom(i); }, 60); }
    });

    /* leaving the slide or page stops the reading (the target changes under us) */
    var target = document.querySelector(w.getAttribute("data-target").split(",").pop().trim());
    if (target) target.addEventListener("click", function (e) { if (w.contains(e.target)) return; if (state !== "idle" && e.target.closest && e.target.closest("button, a")) stop(true); });
    document.addEventListener("keydown", function (e) { if (state !== "idle" && (e.key === "ArrowLeft" || e.key === "ArrowRight") && target && target.contains(document.activeElement)) stop(true); });

    w.stop = stop;
    w.hidden = false;
    ui();

    /* voices can arrive late: tell the visitor early if this language has none */
    function checkVoices() {
      var pv = pickVoice(tag);
      if (pv.known && !pv.voice) noVoice(); else if (pv.voice && w.hasAttribute("data-novoice")) { w.removeAttribute("data-novoice"); say(""); ui(); }
    }
    checkVoices();
    if (synth.addEventListener) synth.addEventListener("voiceschanged", checkVoices);
  }

  Array.prototype.forEach.call(widgets, setup);
  window.addEventListener("pagehide", function () { try { synth.cancel(); } catch (e) { /* ignore */ } });
})();
