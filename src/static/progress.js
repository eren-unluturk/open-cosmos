/* Hackcessability: browser-only progress. No accounts, no server, no cookies, no network.
 * Stores ids only in localStorage key "hc_progress_v1": {"v":1,"done":{"<id>":1}}.
 * Works with JavaScript off (the pages are complete without it); this file only adds controls.
 * See docs/PROGRESS_SPEC.md. */
(function (root) {
  'use strict';

  var KEY = 'hc_progress_v1';
  var ID_RE = /^[a-z]+-[0-9a-f]{8}$/;
  var MAX_ITEMS = 2000;
  var MAX_CODE_LENGTH = 60000;
  var B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';

  /* English fallback; the page fills window.HC_PROGRESS_TEXT per language (see the spec). */
  var DEFAULT_TEXT = {
    mark_done: 'Mark as done', done: 'Done',
    marked_done: 'Marked as done', marked_undone: 'Marked as not done', done_label: 'done',
    summary: '{done} of {total} done', steps_summary: '{done} of {total} steps done',
    stars_label: '{stars} of 5 stars',
    panel_title: 'My progress', items_done: '{count} done',
    start_again: 'Start again', start_again_confirm: 'Yes, clear my progress', cancel: 'Cancel', cleared: 'Progress cleared',
    copy_code: 'Copy my progress code', use_code: 'Use a progress code', apply_code: 'Use this code',
    code_label: 'Paste a progress code', copied: 'Progress code copied',
    copy_failed: 'Could not copy. Select the code and copy it by hand.',
    code_ok: 'Progress added', code_bad: "That code didn't work",
    storage_unavailable: "Progress can't be saved in this browser.",
    privacy: 'Your progress is saved only in this browser. Nothing is sent to us.',
    grown_up_note: 'A grown-up can use the progress code to move progress to another device.'
  };

  /* ---------- pure functions (no DOM, no storage unless passed in) ---------- */

  function emptyState() { return { v: 1, done: {} }; }

  function validId(id) { return typeof id === 'string' && ID_RE.test(id); }

  function has(obj, k) { return Object.prototype.hasOwnProperty.call(obj, k); }

  /* Keep only valid ids (values are always 1). Returns null if there are more than MAX_ITEMS ids. */
  function sanitize(obj) {
    var out = emptyState();
    if (!obj || typeof obj !== 'object' || obj.v !== 1 || !obj.done || typeof obj.done !== 'object') return out;
    var n = 0;
    for (var k in obj.done) {
      if (!has(obj.done, k) || !validId(k)) continue;
      n += 1;
      if (n > MAX_ITEMS) return null;
      out.done[k] = 1;
    }
    return out;
  }

  /* Read from a storage-like object ({getItem}). Corrupt or missing data gives an empty state. */
  function load(storage) {
    try {
      var raw = storage.getItem(KEY);
      if (!raw) return emptyState();
      return sanitize(JSON.parse(raw)) || emptyState();
    } catch (e) { return emptyState(); }
  }

  /* Write to a storage-like object ({setItem}). Returns true on success, false if storage is unavailable. */
  function save(storage, state) {
    try {
      storage.setItem(KEY, JSON.stringify({ v: 1, done: state.done }));
      return true;
    } catch (e) { return false; }
  }

  function clear(storage) {
    try { storage.removeItem(KEY); return true; } catch (e) { return false; }
  }

  function setDone(state, id, on) {
    if (!validId(id)) return state;
    if (on) {
      if (!has(state.done, id) && count(state) >= MAX_ITEMS) return state;
      state.done[id] = 1;
    } else { delete state.done[id]; }
    return state;
  }

  function isDone(state, id) { return has(state.done, id); }

  function count(state) {
    var n = 0;
    for (var k in state.done) { if (has(state.done, k)) n += 1; }
    return n;
  }

  function countIn(state, ids) {
    var n = 0;
    for (var i = 0; i < ids.length; i++) { if (isDone(state, ids[i])) n += 1; }
    return n;
  }

  /* One star for every 3 completed items, up to 5. */
  function stars(n) { return Math.max(0, Math.min(5, Math.floor(n / 3))); }

  /* Small ASCII base64 (no btoa/atob needed; the JSON only contains ASCII ids). */
  function b64encode(str) {
    var out = '', i = 0, a, b, c;
    while (i < str.length) {
      a = str.charCodeAt(i++); b = str.charCodeAt(i++); c = str.charCodeAt(i++);
      var hasB = !isNaN(b), hasC = !isNaN(c);
      out += B64.charAt(a >> 2) + B64.charAt(((a & 3) << 4) | ((hasB ? b : 0) >> 4)) +
        (hasB ? B64.charAt(((b & 15) << 2) | ((hasC ? c : 0) >> 6)) : '=') + (hasC ? B64.charAt(c & 63) : '=');
    }
    return out;
  }

  function b64decode(code) {
    if (!/^[A-Za-z0-9+/]*={0,2}$/.test(code) || code.length % 4 !== 0) return null;
    var out = '', i = 0, bits = 0, acc = 0;
    code = code.replace(/=+$/, '');
    for (; i < code.length; i++) {
      acc = (acc << 6) | B64.indexOf(code.charAt(i));
      bits += 6;
      if (bits >= 8) { bits -= 8; out += String.fromCharCode((acc >> bits) & 255); acc &= (1 << bits) - 1; }
    }
    return out;
  }

  function encode(state) { return b64encode(JSON.stringify({ v: 1, done: state.done })); }

  /* Strict import. Returns a clean state, or null if the code is invalid or oversized.
   * Ids that don't match the pattern are ignored. Never evaluates anything. */
  function decode(code) {
    if (typeof code !== 'string') return null;
    code = code.replace(/\s+/g, '');
    if (!code || code.length > MAX_CODE_LENGTH) return null;
    var text = b64decode(code);
    if (text === null) return null;
    var parsed;
    try { parsed = JSON.parse(text); } catch (e) { return null; }
    if (!parsed || typeof parsed !== 'object' || parsed.v !== 1 || !parsed.done || typeof parsed.done !== 'object') return null;
    return sanitize(parsed);
  }

  function merge(a, b) {
    var out = emptyState();
    var k;
    for (k in a.done) { if (has(a.done, k)) out.done[k] = 1; }
    for (k in b.done) { if (has(b.done, k) && count(out) < MAX_ITEMS) out.done[k] = 1; }
    return out;
  }

  function format(template, vars) {
    return String(template).replace(/\{(\w+)\}/g, function (m, k) { return vars && has(vars, k) ? String(vars[k]) : m; });
  }

  var api = {
    KEY: KEY, MAX_ITEMS: MAX_ITEMS, validId: validId, emptyState: emptyState, sanitize: sanitize, load: load,
    save: save, clear: clear, setDone: setDone, isDone: isDone, count: count, countIn: countIn, stars: stars,
    encode: encode, decode: decode, merge: merge, format: format, DEFAULT_TEXT: DEFAULT_TEXT
  };

  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  root.HCProgress = api;
  if (typeof document === 'undefined') { return; }

  /* ---------- browser part: finds data-attributes and adds the controls ---------- */

  var doc = document;
  var storage = null;
  var storageOk = true;
  var state = emptyState();
  var live = null;
  var text = {};
  var renderers = [];

  function t(key, vars) {
    var s = has(text, key) && text[key] ? text[key] : DEFAULT_TEXT[key];
    return format(s === undefined ? key : s, vars);
  }

  function el(tag, cls, content) {
    var e = doc.createElement(tag);
    if (cls) e.className = cls;
    if (content !== undefined) e.textContent = content;
    return e;
  }

  function announce(msg) { if (live) { live.textContent = ''; live.textContent = msg; } }

  function persist() {
    if (!storage) { storageOk = false; } else { storageOk = save(storage, state); }
    rerender();
  }

  function rerender() { for (var i = 0; i < renderers.length; i++) renderers[i](); }

  function readText() {
    var base = root.HC_PROGRESS_TEXT && typeof root.HC_PROGRESS_TEXT === 'object' ? root.HC_PROGRESS_TEXT : {};
    var node = doc.getElementById('hc-progress-text');
    var fromPage = {};
    if (node) { try { fromPage = JSON.parse(node.textContent); } catch (e) { fromPage = {}; } }
    var out = {}, k;
    for (k in base) { if (has(base, k) && typeof base[k] === 'string') out[k] = base[k]; }
    for (k in fromPage) { if (has(fromPage, k) && typeof fromPage[k] === 'string') out[k] = fromPage[k]; }
    return out;
  }

  function idsFrom(value) {
    var ids = (value || '').split(',');
    var out = [];
    for (var i = 0; i < ids.length; i++) { var id = ids[i].replace(/^\s+|\s+$/g, ''); if (validId(id)) out.push(id); }
    return out;
  }

  /* "Mark as done" toggle on an entry or lesson page */
  function setupItem(article) {
    var id = article.getAttribute('data-progress-item');
    if (!validId(id)) return;
    var box = el('div', 'hc-progress');
    var btn = el('button', 'hc-progress-btn');
    btn.type = 'button';
    box.appendChild(btn);
    var note = el('p', 'hc-progress-note');
    note.setAttribute('role', 'status');
    box.appendChild(note);
    article.appendChild(box);
    btn.addEventListener('click', function () {
      var now = !isDone(state, id);
      setDone(state, id, now);
      persist();
      announce(now ? t('marked_done') : t('marked_undone'));
    });
    renderers.push(function () {
      var on = isDone(state, id);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.textContent = '';
      if (on) { var chk = el('span', 'hc-check', '✓'); chk.setAttribute('aria-hidden', 'true'); btn.appendChild(chk); }
      btn.appendChild(doc.createTextNode(on ? t('done') : t('mark_done')));
      btn.classList.toggle('hc-on', on);
      note.textContent = storageOk ? '' : t('storage_unavailable');
    });
  }

  /* A list whose items carry data-progress-id: a check on done items and "3 of 26 done" */
  function setupList(list) {
    var items = list.querySelectorAll('[data-progress-id]');
    var summary = list.querySelector('[data-progress-summary]') ||
      (list.parentNode && list.parentNode.querySelector('[data-progress-summary]'));
    renderers.push(function () {
      var done = 0, total = 0;
      for (var i = 0; i < items.length; i++) {
        var id = items[i].getAttribute('data-progress-id');
        if (!validId(id)) continue;
        total += 1;
        var mark = items[i].querySelector('.hc-listcheck');
        if (isDone(state, id)) {
          done += 1;
          if (!mark) {
            mark = el('span', 'hc-listcheck');
            mark.appendChild(el('span', 'hc-check', '✓')).setAttribute('aria-hidden', 'true');
            mark.appendChild(el('span', 'hc-sr-only', t('done_label')));
            items[i].appendChild(mark);
          }
        } else if (mark) { mark.parentNode.removeChild(mark); }
      }
      if (summary) summary.textContent = format(t('summary'), { done: done, total: total });
    });
  }

  /* A guide or group: data-progress-roadmap="id,id,id" shows "2 of 5 steps done" */
  function setupRoadmap(node) {
    var ids = idsFrom(node.getAttribute('data-progress-roadmap'));
    if (!ids.length) return;
    var p = el('p', 'hc-progress-note');
    node.appendChild(p);
    renderers.push(function () {
      p.textContent = format(t('steps_summary'), { done: countIn(state, ids), total: ids.length });
    });
  }

  function renderStars(node) {
    var n = stars(count(state));
    node.textContent = '';
    node.setAttribute('role', 'img');
    node.setAttribute('aria-label', t('stars_label', { stars: n }));
    node.classList.add('hc-stars');
    for (var i = 0; i < 5; i++) {
      var s = el('span', i < n ? 'hc-star hc-star-on' : 'hc-star', i < n ? '★' : '☆');
      s.setAttribute('aria-hidden', 'true');
      node.appendChild(s);
    }
  }

  function setupStars(node) { renderers.push(function () { renderStars(node); }); }

  /* The "My progress" panel (count, stars, start again, progress code) */
  function setupPanel(panel) {
    panel.textContent = '';
    panel.classList.add('hc-panel');
    var h = el('h2', 'hc-panel-title', t('panel_title'));
    var line = el('p', 'hc-panel-count');
    var starsNode = el('p', '');
    starsNode.setAttribute('data-progress-stars', '');
    var row = el('div', 'hc-row');
    var again = el('button', 'hc-progress-btn', t('start_again')); again.type = 'button';
    var yes = el('button', 'hc-progress-btn hc-danger', t('start_again_confirm')); yes.type = 'button';
    var no = el('button', 'hc-progress-btn', t('cancel')); no.type = 'button';
    yes.hidden = true; no.hidden = true;
    var copy = el('button', 'hc-progress-btn', t('copy_code')); copy.type = 'button';
    var use = el('button', 'hc-progress-btn', t('use_code')); use.type = 'button';
    use.setAttribute('aria-expanded', 'false');
    row.appendChild(again); row.appendChild(yes); row.appendChild(no); row.appendChild(copy); row.appendChild(use);
    var codeBox = el('div', 'hc-codebox'); codeBox.hidden = true;
    var label = el('label', '', t('code_label'));
    var input = el('input', 'hc-input'); input.type = 'text'; input.autocomplete = 'off'; input.spellcheck = false;
    input.id = 'hc-code-input'; label.htmlFor = input.id;
    var apply = el('button', 'hc-progress-btn', t('apply_code')); apply.type = 'button';
    codeBox.appendChild(label); codeBox.appendChild(input); codeBox.appendChild(apply);
    var shown = el('input', 'hc-input'); shown.type = 'text'; shown.readOnly = true; shown.hidden = true;
    shown.setAttribute('aria-label', t('copy_code'));
    var note = el('p', 'hc-progress-note'); note.setAttribute('role', 'status');
    var parent = el('p', 'hc-progress-note', t('grown_up_note'));
    panel.appendChild(h); panel.appendChild(line); panel.appendChild(starsNode); panel.appendChild(row);
    panel.appendChild(shown); panel.appendChild(codeBox); panel.appendChild(note); panel.appendChild(parent);
    setupStars(starsNode);

    function resetConfirm() { again.hidden = false; yes.hidden = true; no.hidden = true; }
    again.addEventListener('click', function () { again.hidden = true; yes.hidden = false; no.hidden = false; yes.focus(); });
    no.addEventListener('click', function () { resetConfirm(); again.focus(); });
    yes.addEventListener('click', function () {
      state = emptyState();
      if (storage) { storageOk = clear(storage); }
      resetConfirm(); rerender(); announce(t('cleared')); again.focus();
    });
    copy.addEventListener('click', function () {
      var code = encode(state);
      shown.value = code; shown.hidden = false;
      var done = function (ok) { note.textContent = ok ? t('copied') : t('copy_failed'); announce(note.textContent); if (!ok) { shown.focus(); shown.select(); } };
      try {
        if (root.navigator && root.navigator.clipboard && root.navigator.clipboard.writeText) {
          root.navigator.clipboard.writeText(code).then(function () { done(true); }, function () { done(false); });
        } else { done(false); }
      } catch (e) { done(false); }
    });
    use.addEventListener('click', function () {
      var open = codeBox.hidden;
      codeBox.hidden = !open; use.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) input.focus();
    });
    apply.addEventListener('click', function () {
      var incoming = decode(input.value);
      if (!incoming) { note.textContent = t('code_bad'); announce(note.textContent); return; }
      state = merge(state, incoming); input.value = '';
      persist(); note.textContent = t('code_ok'); announce(note.textContent);
    });
    renderers.push(function () {
      line.textContent = format(t('items_done'), { count: count(state) });
      if (!storageOk) note.textContent = t('storage_unavailable');
    });
  }

  function fillPrivacy() {
    var nodes = doc.querySelectorAll('[data-progress-privacy]');
    for (var i = 0; i < nodes.length; i++) { if (!nodes[i].textContent.replace(/\s+/g, '')) nodes[i].textContent = t('privacy'); }
  }

  function init() {
    var wanted = doc.querySelectorAll('[data-progress-item],[data-progress-list],[data-progress-roadmap],[data-progress-stars],[data-progress-panel],[data-progress-privacy]');
    if (!wanted.length) return;
    text = readText();
    try { storage = root.localStorage || null; } catch (e) { storage = null; }
    if (!storage) storageOk = false;
    state = storage ? load(storage) : emptyState();
    live = el('div', 'hc-sr-only'); live.id = 'hc-progress-live';
    live.setAttribute('aria-live', 'polite'); live.setAttribute('role', 'status');
    doc.body.appendChild(live);
    var q = function (sel, fn) { var n = doc.querySelectorAll(sel); for (var i = 0; i < n.length; i++) fn(n[i]); };
    q('[data-progress-item]', setupItem);
    q('[data-progress-list]', setupList);
    q('[data-progress-roadmap]', setupRoadmap);
    q('[data-progress-panel]', setupPanel);
    q('[data-progress-stars]:not(.hc-stars)', function (n) { if (!n.closest || !n.closest('[data-progress-panel]')) setupStars(n); });
    fillPrivacy();
    rerender();
  }

  if (doc.readyState === 'loading') { doc.addEventListener('DOMContentLoaded', init); } else { init(); }
})(typeof window !== 'undefined' ? window : this);
