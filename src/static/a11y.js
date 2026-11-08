/* Accessibility settings panel. The panel markup is in every page (translated by the server); this script opens it,
   traps focus while it is open, closes on Escape, applies and saves the choices (see a11y-settings.js).
   No network, no cookies, nothing leaves the browser. */
(function () {
  "use strict";
  var A = window.HCA11y;
  var openBtn = document.getElementById("a11y-open");
  var panel = document.getElementById("a11y-panel");
  var backdrop = document.getElementById("a11y-backdrop");
  if (!A || !openBtn || !panel || !backdrop) return;

  var storage = A.getStorage(window);
  var mm = window.matchMedia ? window.matchMedia.bind(window) : null;
  var settings = A.load(storage);
  var live = document.getElementById("a11y-status");
  var lastFocus = null;
  var msgApplied = panel.getAttribute("data-msg-applied") || "";
  var msgReset = panel.getAttribute("data-msg-reset") || "";

  function say(text) {
    if (!live) return;
    live.textContent = "";
    window.setTimeout(function () { live.textContent = text; }, 30); // a change is what screen readers announce
  }

  function fieldValue(name) {
    var el = panel.querySelector('input[name="a11y-' + name + '"]:checked');
    return el ? el.value : null;
  }

  /* Show the saved choices in the form. The motion checkbox shows what is in effect (device preference counts). */
  function sync() {
    ["theme", "size", "spacing", "font"].forEach(function (name) {
      var el = panel.querySelector('input[name="a11y-' + name + '"][value="' + String(settings[name]) + '"]');
      if (el) el.checked = true;
    });
    var motion = panel.querySelector("#a11y-motion");
    if (motion) motion.checked = A.resolveMotion(settings.motion, mm) === "reduce";
  }

  function commit(message) {
    settings = A.normalize(settings);
    A.apply(document.documentElement, settings, mm);
    A.save(storage, settings);
    say(message);
  }

  panel.addEventListener("change", function (e) {
    var t = e.target;
    if (!t || !t.name) return;
    if (t.id === "a11y-motion") settings.motion = t.checked ? "reduce" : "full";
    else if (t.name === "a11y-size") settings.size = parseInt(t.value, 10);
    else if (t.name.indexOf("a11y-") === 0) settings[t.name.slice(5)] = t.value;
    commit(msgApplied);
  });

  var resetBtn = document.getElementById("a11y-reset");
  if (resetBtn) resetBtn.addEventListener("click", function () {
    settings = A.defaults();
    A.clear(storage);
    A.apply(document.documentElement, settings, mm);
    sync();
    say(msgReset);
  });

  /* ---- open / close with a focus trap ---- */
  function backgroundParts() {
    return Array.prototype.filter.call(document.body.children, function (el) {
      return el !== panel && el !== backdrop && el.tagName !== "SCRIPT";
    });
  }

  function focusables() {
    return Array.prototype.filter.call(
      panel.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'),
      function (el) { return el.offsetParent !== null || el === document.activeElement; });
  }

  function open() {
    lastFocus = document.activeElement;
    sync();
    panel.hidden = false;
    backdrop.hidden = false;
    openBtn.setAttribute("aria-expanded", "true");
    document.body.classList.add("a11y-locked");
    backgroundParts().forEach(function (el) { el.setAttribute("inert", ""); });
    var first = panel.querySelector("input:checked") || focusables()[0];
    (first || panel).focus();
  }

  function close() {
    panel.hidden = true;
    backdrop.hidden = true;
    openBtn.setAttribute("aria-expanded", "false");
    document.body.classList.remove("a11y-locked");
    backgroundParts().forEach(function (el) { el.removeAttribute("inert"); });
    if (lastFocus && lastFocus.focus) lastFocus.focus(); else openBtn.focus();
  }

  openBtn.addEventListener("click", function () { if (panel.hidden) open(); else close(); });
  backdrop.addEventListener("click", close);
  var closeBtn = document.getElementById("a11y-close");
  if (closeBtn) closeBtn.addEventListener("click", close);

  panel.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key !== "Tab") return;
    var items = focusables();
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && (document.activeElement === first || document.activeElement === panel)) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* "Match my device" follows the device when it changes (dark/light, contrast, reduced motion). */
  ["(prefers-color-scheme: light)", "(prefers-contrast: more)", "(prefers-reduced-motion: reduce)"].forEach(function (q) {
    try {
      var list = mm && mm(q);
      var handler = function () { A.apply(document.documentElement, settings, mm); if (!panel.hidden) sync(); };
      if (list && list.addEventListener) list.addEventListener("change", handler);
      else if (list && list.addListener) list.addListener(handler);
    } catch (e) { /* older browsers: no live updates */ }
  });
})();
