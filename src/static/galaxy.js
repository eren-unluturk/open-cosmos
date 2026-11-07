// Progress lives only in this browser (localStorage). No accounts, nothing sent anywhere.
(function () {
  var KEY = "openlearn-explored-v1";

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function write(d) {
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* private mode: progress just isn't kept */ }
  }
  function each(sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); }

  function paint() {
    var d = read();
    var galaxies = {};
    Object.keys(d).forEach(function (id) { if (d[id].g) galaxies[d[id].g] = true; });

    each("[data-id]", function (el) {
      var done = !!d[el.getAttribute("data-id")];
      el.classList.toggle("done", done);
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

  // Only same-site paths may be used as a link target (the store lives in the browser, so treat it as untrusted).
  function safeUrl(u) { return typeof u === "string" && u.charAt(0) === "/" && u.charAt(1) !== "/" ? u : ""; }

  // Hook for the coding problems (problem.js calls this when every test passes). Same store as "mark explored".
  window.HackProgress = {
    markSolved: function (id, meta) {
      meta = meta || {};
      var d = read();
      d[id] = { t: meta.title || id, g: meta.galaxy || "code", s: "", at: Date.now(), u: safeUrl(meta.url), solved: true };
      write(d);
      paint();
    }
  };

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

  document.addEventListener("click", function (ev) {
    var t = ev.target.closest ? ev.target.closest("[data-explore], [data-launch], [data-clear]") : null;
    if (!t) return;
    if (t.hasAttribute("data-explore")) toggle(t);
    else if (t.hasAttribute("data-launch")) { var b = document.querySelector("[data-explore]"); if (b) toggle(b, true); }
    else if (t.hasAttribute("data-clear")) { write({}); paint(); }
  });


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
