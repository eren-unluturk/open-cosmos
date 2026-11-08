// Progress lives only in this browser (localStorage). No accounts, nothing sent anywhere.
(function () {
  var KEY = "openlearn-explored-v1";

  function read() {
    try { return clean(JSON.parse(localStorage.getItem(KEY))); } catch (e) { return {}; }
  }
  function write(d) {
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* private mode: progress just isn't kept */ }
  }
  function each(sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }

  // ---- Kept from Eren's progress.js when we chose one system (issue #26) ----
  var ID_RE = /^[a-z]+-[a-z0-9-]{1,40}$/;   // entry, lesson and problem ids
  var MAX_ITEMS = 2000;
  function safeUrl(u) { return typeof u === "string" && u.charAt(0) === "/" && u.charAt(1) !== "/" ? u : ""; }
  function str(v, max) { return typeof v === "string" ? v.slice(0, max) : ""; }
  function clean(raw) {           // anything read from storage or a pasted code is untrusted
    var out = {}, n = 0;
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return out;
    Object.keys(raw).forEach(function (id) {
      var v = raw[id];
      if (n >= MAX_ITEMS || !ID_RE.test(id) || !v || typeof v !== "object") return;
      out[id] = { t: str(v.t, 200), g: str(v.g, 40), s: str(v.s, 40), u: safeUrl(v.u),
                  at: typeof v.at === "number" ? v.at : 0, solved: v.solved === true };
      n++;
    });
    return out;
  }
  function storageWorks() {
    try { localStorage.setItem(KEY + "-test", "1"); localStorage.removeItem(KEY + "-test"); return true; } catch (e) { return false; }
  }
  // One-time move: items marked with Eren's "Mark as done" button (key hc_progress_v1) become stars here.
  (function migrate() {
    try {
      var old = JSON.parse(localStorage.getItem("hc_progress_v1"));
      if (!old || !old.done) return;
      var d = read();
      Object.keys(old.done).forEach(function (id) { if (ID_RE.test(id) && !d[id]) d[id] = { t: "", g: "", s: "", at: 0 }; });
      write(d);
      localStorage.removeItem("hc_progress_v1");
    } catch (e) { /* nothing to move */ }
  })();
  function fmt(t, vars) { return String(t || "").replace(/\{(\w+)\}/g, function (_, k) { return k in vars ? vars[k] : ""; }); }

  function paint() {
    var d = read();
    var galaxies = {};
    Object.keys(d).forEach(function (id) { if (d[id].g) galaxies[d[id].g] = true; });

    each("[data-id]", function (el) {
      var done = !!d[el.getAttribute("data-id")];
      el.classList.toggle("done", done);
    });
    // "3 of 26 done" under a list: <p data-count-for="#grid" data-text="{done} of {total} done">
    each("[data-count-for]", function (p) {
      var box = document.querySelector(p.getAttribute("data-count-for"));
      if (!box) return;
      var items = box.querySelectorAll("[data-id]"), done = 0;
      Array.prototype.forEach.call(items, function (el) { if (d[el.getAttribute("data-id")]) done++; });
      p.textContent = fmt(p.getAttribute("data-text"), { done: done, total: items.length });
    });
    each("[data-galaxy]", function (el) {
      el.classList.toggle("visited", !!galaxies[el.getAttribute("data-galaxy")]);
    });
    each(".link[data-a]", function (el) {
      el.classList.toggle("lit", !!(galaxies[el.getAttribute("data-a")] && galaxies[el.getAttribute("data-b")]));
    });
    each("[data-explore]", function (btn) {
      var on = !!d[btn.getAttribute("data-explore")];
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      var lab = btn.querySelector(".lab"); if (lab) lab.textContent = on ? btn.getAttribute("data-on") : btn.getAttribute("data-off");
    });

    var log = document.getElementById("log");
    if (log) renderLog(d, galaxies, log);
  }

  function toggle(btn, force) {
    var d = read(), id = btn.getAttribute("data-explore");
    var on = force === undefined ? !d[id] : force;
    if (on) d[id] = { t: btn.getAttribute("data-title"), g: btn.getAttribute("data-g"), s: btn.getAttribute("data-s"), at: Date.now() };
    else delete d[id];
    write(d);
    paint();
  }

  function renderLog(d, galaxies, log) {
    var ids = Object.keys(d).sort(function (a, b) { return d[b].at - d[a].at; });
    var nG = Object.keys(galaxies).length;
    document.getElementById("n-stops").textContent = ids.length;
    document.getElementById("n-gal").textContent = nG;
    var rules = { first: ids.length >= 1, five: ids.length >= 5, hopper: nG >= 3, ten: ids.length >= 10 };
    each(".medal[data-rule]", function (m) { m.classList.toggle("got", !!rules[m.getAttribute("data-rule")]); });
    var lang = log.getAttribute("data-lang");
    log.innerHTML = "";
    ids.forEach(function (id) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = safeUrl(d[id].u) || ("/" + lang + "/entry/" + encodeURIComponent(id) + (d[id].g ? "?g=" + encodeURIComponent(d[id].g) + "&s=" + encodeURIComponent(d[id].s || "") : ""));
      a.textContent = d[id].t || id;
      li.appendChild(a);
      log.appendChild(li);
    });
    document.getElementById("log-empty").hidden = ids.length > 0;
  }

  // Coding problems call this when every test passes (src/static/problem.js).
  window.HackProgress = {
    markSolved: function (id, meta) {
      if (!ID_RE.test(id)) return;
      meta = meta || {};
      var d = read();
      d[id] = { t: str(meta.title, 200) || id, g: str(meta.galaxy, 40) || "code", s: "", u: safeUrl(meta.url), at: Date.now(), solved: true };
      write(d);
      paint();
    }
  };

  // Progress code: move stars to another device (no account). The code is base64 of the store.
  function say(text) { var live = document.getElementById("progress-live"); if (live) live.textContent = text || ""; }
  function makeCode() {
    return btoa(unescape(encodeURIComponent(JSON.stringify(read()))));
  }
  function useCode(code) {
    code = String(code || "").replace(/\s+/g, "");
    if (!code || code.length > 60000 || !/^[A-Za-z0-9+/=]+$/.test(code)) return false;
    var incoming;
    try { incoming = JSON.parse(decodeURIComponent(escape(atob(code)))); } catch (e) { return false; }
    if (!incoming || typeof incoming !== "object" || Object.keys(incoming).length > MAX_ITEMS) return false;
    var d = read(), add = clean(incoming);
    Object.keys(add).forEach(function (id) { if (!d[id] && Object.keys(d).length < MAX_ITEMS) d[id] = add[id]; });
    write(d);
    paint();
    return true;
  }

  document.addEventListener("click", function (ev) {
    var t = ev.target.closest ? ev.target.closest("[data-explore], [data-launch], [data-clear], [data-clear-cancel], [data-copy-code], [data-use-code]") : null;
    if (!t) return;
    if (t.hasAttribute("data-explore")) toggle(t);
    else if (t.hasAttribute("data-launch")) { var b = document.querySelector("[data-explore]"); if (b) toggle(b, true); }
    else if (t.hasAttribute("data-clear")) {
      // Two steps, so a child can't wipe everything with one tap.
      if (t.getAttribute("data-armed") !== "1") {
        t.setAttribute("data-armed", "1");
        t.textContent = t.getAttribute("data-confirm") || t.textContent;
        var c = document.querySelector("[data-clear-cancel]"); if (c) c.hidden = false;
        return;
      }
      write({}); paint(); say(t.getAttribute("data-done"));
      t.removeAttribute("data-armed"); t.textContent = t.getAttribute("data-label") || t.textContent;
      var c2 = document.querySelector("[data-clear-cancel]"); if (c2) c2.hidden = true;
    }
    else if (t.hasAttribute("data-clear-cancel")) {
      var b2 = document.querySelector("[data-clear]");
      if (b2) { b2.removeAttribute("data-armed"); b2.textContent = b2.getAttribute("data-label") || b2.textContent; b2.focus(); }
      t.hidden = true;
    }
    else if (t.hasAttribute("data-copy-code")) {
      var box = document.getElementById("progress-code");
      if (!box) return;
      box.value = makeCode(); box.hidden = false; box.select();
      var ok = false;
      try { ok = document.execCommand && document.execCommand("copy"); } catch (e) { ok = false; }
      say(ok ? t.getAttribute("data-ok") : t.getAttribute("data-fail"));
    }
    else if (t.hasAttribute("data-use-code")) {
      var input = document.getElementById("progress-code-in");
      say(useCode(input && input.value) ? t.getAttribute("data-ok") : t.getAttribute("data-fail"));
    }
  });

  if (!storageWorks()) each("[data-storage-note]", function (n) { n.hidden = false; });


  // ---- Guide slide viewer: one slide at a time, buttons, arrow keys, swipe, aria-live ----
  each("[data-deck]", function (deck) {
    var slides = deck.querySelectorAll("[data-slide]");
    var nav = deck.querySelector("[data-deck-nav]");
    if (!slides.length || !nav) return;
    var rtl = deck.getAttribute("data-rtl") === "1";
    var live = deck.querySelector("[data-live]");
    var pos = nav.querySelector("[data-pos]");
    var dots = nav.querySelectorAll(".deck-dots i");
    var prev = nav.querySelector("[data-prev]"), next = nav.querySelector("[data-next]");
    var i = 0;
    var ofWord = deck.getAttribute("data-of") || "/";
    deck.classList.add("is-deck");
    nav.hidden = false;

    function show(n, focus) {
      i = Math.max(0, Math.min(slides.length - 1, n));
      Array.prototype.forEach.call(slides, function (s, k) { s.classList.toggle("is-active", k === i); });
      Array.prototype.forEach.call(dots, function (d, k) { d.classList.toggle("on", k === i); });
      pos.textContent = (i + 1) + " " + ofWord + " " + slides.length;
      prev.disabled = i === 0;
      next.disabled = i === slides.length - 1;
      if (live) live.textContent = slides[i].getAttribute("aria-label");
      if (focus) { var h = slides[i].querySelector(".slide-title"); if (h) h.focus({ preventScroll: true }); }
    }
    prev.addEventListener("click", function () { show(i - 1, true); });
    next.addEventListener("click", function () { show(i + 1, true); });
    deck.addEventListener("keydown", function (ev) {
      if (ev.target.closest && ev.target.closest("input, textarea, select")) return;
      var fwd = rtl ? "ArrowLeft" : "ArrowRight", back = rtl ? "ArrowRight" : "ArrowLeft";
      if (ev.key === fwd) { show(i + 1, true); ev.preventDefault(); }
      else if (ev.key === back) { show(i - 1, true); ev.preventDefault(); }
    });
    var x0 = null;
    deck.addEventListener("touchstart", function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
    deck.addEventListener("touchend", function (ev) {
      if (x0 === null) return;
      var dx = ev.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) < 50) return;
      var forward = rtl ? dx > 0 : dx < 0;
      show(i + (forward ? 1 : -1), true);
    });
    show(0, false);
  });

  paint();
})();
