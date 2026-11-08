// Node tests for the accessibility settings module (run: node --test tests/js/)
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const A = require(path.join(__dirname, "..", "..", "src", "static", "a11y-settings.js"));

function memoryStorage(initial) {
  const data = Object.assign({}, initial);
  return {
    data,
    getItem: (k) => (k in data ? data[k] : null),
    setItem: (k, v) => { data[k] = String(v); },
    removeItem: (k) => { delete data[k]; },
  };
}
const throwing = () => { throw new Error("denied"); };
const mm = (...on) => (q) => ({ matches: on.includes(q) });
const fakeRoot = () => { const attrs = {}; return { attrs, setAttribute: (k, v) => { attrs[k] = v; } }; };

test("defaults when nothing is saved", () => {
  assert.deepEqual(A.load(memoryStorage()), { theme: "auto", size: 100, spacing: "normal", font: "default", motion: "auto" });
});

test("the storage key is hc_a11y_v1 and only settings are stored", () => {
  const s = memoryStorage();
  assert.equal(A.KEY, "hc_a11y_v1");
  assert.equal(A.save(s, { theme: "light", size: 125, spacing: "wide", font: "easy", motion: "reduce", userId: "abc", email: "x@y" }), true);
  assert.deepEqual(Object.keys(s.data), ["hc_a11y_v1"]);
  const stored = JSON.parse(s.data.hc_a11y_v1);
  assert.deepEqual(Object.keys(stored).sort(), ["font", "motion", "size", "spacing", "theme"]);
  assert.deepEqual(A.load(s), { theme: "light", size: 125, spacing: "wide", font: "easy", motion: "reduce" });
});

test("corrupt storage falls back to defaults", () => {
  for (const raw of ["{not json", "null", "42", "\"text\"", "[1,2]", "", "{\"theme\":", "undefined"]) {
    assert.deepEqual(A.load(memoryStorage({ hc_a11y_v1: raw })), A.defaults(), raw);
  }
});

test("invalid values are replaced one field at a time", () => {
  const out = A.load(memoryStorage({ hc_a11y_v1: JSON.stringify({ theme: "neon", size: 999, spacing: "wide", font: 5, motion: "reduce", extra: 1 }) }));
  assert.deepEqual(out, { theme: "auto", size: 100, spacing: "wide", font: "default", motion: "reduce" });
  assert.equal(A.normalize({ size: "125" }).size, 100); // a string is not an allowed number
  assert.equal(A.normalize(undefined).theme, "auto");
});

test("unavailable storage: no crash, defaults, save reports false", () => {
  assert.deepEqual(A.load(null), A.defaults());
  assert.equal(A.save(null, { theme: "light" }), false);
  assert.equal(A.clear(null), false);
  const broken = { getItem: throwing, setItem: throwing, removeItem: throwing };
  assert.deepEqual(A.load(broken), A.defaults());
  assert.equal(A.save(broken, { theme: "light" }), false);
  assert.equal(A.clear(broken), false);
});

test("getStorage survives a throwing localStorage getter (blocked cookies)", () => {
  const win = {};
  Object.defineProperty(win, "localStorage", { get: throwing });
  assert.equal(A.getStorage(win), null);
  assert.equal(A.getStorage(null), null);
  assert.equal(A.getStorage({}), null);
  const s = memoryStorage();
  assert.equal(A.getStorage({ localStorage: s }), s);
});

test("clear removes the key", () => {
  const s = memoryStorage({ hc_a11y_v1: "{}" });
  assert.equal(A.clear(s), true);
  assert.deepEqual(s.data, {});
});

test("auto theme follows the device: contrast, then light, then galaxy", () => {
  assert.equal(A.resolveTheme("auto", mm()), "galaxy");
  assert.equal(A.resolveTheme("auto", mm("(prefers-color-scheme: light)")), "light");
  assert.equal(A.resolveTheme("auto", mm("(prefers-contrast: more)")), "contrast");
  assert.equal(A.resolveTheme("auto", mm("(prefers-contrast: more)", "(prefers-color-scheme: light)")), "contrast");
  assert.equal(A.resolveTheme("auto", null), "galaxy");
  assert.equal(A.resolveTheme("auto", throwing), "galaxy");
  assert.equal(A.resolveTheme("cb", mm("(prefers-contrast: more)")), "cb"); // an explicit choice wins
});

test("motion: explicit choice wins, auto follows prefers-reduced-motion", () => {
  assert.equal(A.resolveMotion("auto", mm("(prefers-reduced-motion: reduce)")), "reduce");
  assert.equal(A.resolveMotion("auto", mm()), "full");
  assert.equal(A.resolveMotion("full", mm("(prefers-reduced-motion: reduce)")), "full");
  assert.equal(A.resolveMotion("reduce", mm()), "reduce");
});

test("apply writes data attributes for CSS", () => {
  const el = fakeRoot();
  A.apply(el, { theme: "contrast", size: 150, spacing: "wide", font: "easy", motion: "reduce" }, mm());
  assert.deepEqual(el.attrs, { "data-theme": "contrast", "data-size": "150", "data-spacing": "wide", "data-font": "easy", "data-motion": "reduce" });
  const el2 = fakeRoot();
  A.apply(el2, undefined, mm("(prefers-color-scheme: light)", "(prefers-reduced-motion: reduce)"));
  assert.deepEqual(el2.attrs, { "data-theme": "light", "data-size": "100", "data-spacing": "normal", "data-font": "default", "data-motion": "reduce" });
});

test("every allowed value is accepted and nothing else", () => {
  for (const [field, values] of Object.entries(A.ALLOWED)) {
    for (const v of values) assert.equal(A.normalize({ [field]: v })[field], v);
    assert.equal(A.normalize({ [field]: "nope" })[field], A.DEFAULTS[field]);
  }
});
