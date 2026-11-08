/* Accessibility settings: the saved choices, and applying them to <html>. Loaded in <head> (a small external script,
   no inline code) so the page is themed before it is first painted.
   Storage: localStorage key "hc_a11y_v1", settings only, no identifiers. Every storage access is in try/catch:
   private mode, blocked storage or corrupt data just gives the defaults. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.HCA11y = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  var KEY = "hc_a11y_v1";
  var ALLOWED = {
    theme: ["auto", "galaxy", "light", "contrast", "cb"],
    size: [100, 125, 150],
    spacing: ["normal", "wide"],
    font: ["default", "easy"],
    motion: ["auto", "reduce", "full"]
  };
  var DEFAULTS = { theme: "auto", size: 100, spacing: "normal", font: "default", motion: "auto" };

  function defaults() { return JSON.parse(JSON.stringify(DEFAULTS)); }

  /* Keep only known fields with allowed values; anything else falls back to the default for that field. */
  function normalize(obj) {
    var out = defaults();
    if (!obj || typeof obj !== "object" || Array.isArray(obj)) return out;
    Object.keys(ALLOWED).forEach(function (k) {
      if (ALLOWED[k].indexOf(obj[k]) !== -1) out[k] = obj[k];
    });
    return out;
  }

  /* The storage object, or null when it is missing or throws (some browsers throw just for reading the property). */
  function getStorage(win) {
    try { return win && win.localStorage ? win.localStorage : null; } catch (e) { return null; }
  }

  function load(storage) {
    if (!storage) return defaults();
    try {
      var raw = storage.getItem(KEY);
      if (raw === null || raw === undefined) return defaults();
      return normalize(JSON.parse(raw));
    } catch (e) { return defaults(); }
  }

  /* Returns true when saved, false when storage is unavailable or full. */
  function save(storage, settings) {
    if (!storage) return false;
    try { storage.setItem(KEY, JSON.stringify(normalize(settings))); return true; } catch (e) { return false; }
  }

  function clear(storage) {
    if (!storage) return false;
    try { storage.removeItem(KEY); return true; } catch (e) { return false; }
  }

  function matches(matchMedia, query) {
    try { return !!(matchMedia && matchMedia(query).matches); } catch (e) { return false; }
  }

  /* "auto" follows the device: more contrast, then light, otherwise the galaxy look. */
  function resolveTheme(theme, matchMedia) {
    if (theme !== "auto") return theme;
    if (matches(matchMedia, "(prefers-contrast: more)")) return "contrast";
    if (matches(matchMedia, "(prefers-color-scheme: light)")) return "light";
    return "galaxy";
  }

  function resolveMotion(motion, matchMedia) {
    if (motion === "reduce" || motion === "full") return motion;
    return matches(matchMedia, "(prefers-reduced-motion: reduce)") ? "reduce" : "full";
  }

  /* Write the settings onto <html> as data attributes. CSS does the rest. */
  function apply(el, settings, matchMedia) {
    var s = normalize(settings);
    el.setAttribute("data-theme", resolveTheme(s.theme, matchMedia));
    el.setAttribute("data-size", String(s.size));
    el.setAttribute("data-spacing", s.spacing);
    el.setAttribute("data-font", s.font);
    el.setAttribute("data-motion", resolveMotion(s.motion, matchMedia));
    return s;
  }

  var api = {
    KEY: KEY, ALLOWED: ALLOWED, DEFAULTS: DEFAULTS,
    defaults: defaults, normalize: normalize, getStorage: getStorage, load: load, save: save, clear: clear,
    resolveTheme: resolveTheme, resolveMotion: resolveMotion, apply: apply
  };

  /* In a browser: apply the saved choices right away, before the page paints. */
  if (typeof document !== "undefined" && document.documentElement && typeof window !== "undefined") {
    try { apply(document.documentElement, load(getStorage(window)), window.matchMedia ? window.matchMedia.bind(window) : null); } catch (e) { /* keep defaults */ }
  }
  return api;
});
