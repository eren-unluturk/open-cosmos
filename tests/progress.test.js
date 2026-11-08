// Node test for src/static/progress.js (no packages). Run: node tests/progress.test.js
'use strict';
const assert = require('node:assert');
const P = require('../src/static/progress.js');

let failed = 0;
function test(name, fn) {
  try { fn(); console.log('ok   - ' + name); } catch (e) { failed += 1; console.log('FAIL - ' + name + '\n       ' + (e && e.message)); }
}
function memoryStorage(initial) {
  const data = {};
  if (initial !== undefined) data[P.KEY] = initial;
  return { getItem: (k) => (k in data ? data[k] : null), setItem: (k, v) => { data[k] = String(v); }, removeItem: (k) => { delete data[k]; }, data };
}
const broken = { getItem() { throw new Error('blocked'); }, setItem() { throw new Error('blocked'); }, removeItem() { throw new Error('blocked'); } };
const ID = (n) => 'kids-' + ('00000000' + n.toString(16)).slice(-8);
const b64 = (s) => Buffer.from(s, 'utf8').toString('base64');

test('the storage key is exactly hc_progress_v1', () => assert.strictEqual(P.KEY, 'hc_progress_v1'));

test('add and remove an item', () => {
  const s = P.emptyState();
  P.setDone(s, 'kids-0d3a63dc', true);
  P.setDone(s, 'lesson-0d3a63dc', true);
  assert.strictEqual(P.count(s), 2);
  assert.ok(P.isDone(s, 'kids-0d3a63dc'));
  P.setDone(s, 'kids-0d3a63dc', false);
  assert.ok(!P.isDone(s, 'kids-0d3a63dc'));
  assert.strictEqual(P.count(s), 1);
});

test('invalid ids are never added', () => {
  const s = P.emptyState();
  for (const bad of ['', 'kids-xyz', 'KIDS-0d3a63dc', 'kids-0d3a63d', 'https://evil.example', '__proto__', 'a-0d3a63dcx', null, 5]) P.setDone(s, bad, true);
  assert.strictEqual(P.count(s), 0);
});

test('save then load round trip stores ids only', () => {
  const st = memoryStorage();
  const s = P.emptyState();
  P.setDone(s, 'learn-1c1ace1d', true);
  assert.strictEqual(P.save(st, s), true);
  assert.deepStrictEqual(JSON.parse(st.data[P.KEY]), { v: 1, done: { 'learn-1c1ace1d': 1 } });
  assert.ok(P.isDone(P.load(st), 'learn-1c1ace1d'));
});

test('corrupt JSON in storage is ignored', () => {
  for (const raw of ['not json', '{"v":2,"done":{}}', '[]', 'null', '{"v":1,"done":5}', '{"v":1}', '']) {
    const s = P.load(memoryStorage(raw));
    assert.strictEqual(P.count(s), 0, raw);
  }
});

test('invalid ids inside stored data are dropped, valid ones kept', () => {
  const s = P.load(memoryStorage(JSON.stringify({ v: 1, done: { 'kids-0d3a63dc': 1, 'javascript:alert(1)': 1, '__proto__': 1 } })));
  assert.deepStrictEqual(Object.keys(s.done), ['kids-0d3a63dc']);
});

test('unavailable storage does not throw', () => {
  assert.doesNotThrow(() => P.load(broken));
  assert.strictEqual(P.count(P.load(broken)), 0);
  assert.strictEqual(P.save(broken, P.emptyState()), false);
  assert.strictEqual(P.clear(broken), false);
  assert.strictEqual(P.save(null, P.emptyState()), false);
  assert.strictEqual(P.count(P.load(null)), 0);
});

test('count and star calculations (1 star per 3 items, max 5)', () => {
  assert.deepStrictEqual([0, 1, 2, 3, 5, 6, 14, 15, 16, 100].map(P.stars), [0, 0, 0, 1, 1, 2, 4, 5, 5, 5]);
  const s = P.emptyState();
  for (let i = 0; i < 7; i++) P.setDone(s, ID(i), true);
  assert.strictEqual(P.count(s), 7);
  assert.strictEqual(P.stars(P.count(s)), 2);
  assert.strictEqual(P.countIn(s, [ID(0), ID(1), ID(99)]), 2);
});

test('progress code round trip', () => {
  const s = P.emptyState();
  P.setDone(s, 'kids-0d3a63dc', true); P.setDone(s, 'lesson-c04ee384', true);
  const code = P.encode(s);
  assert.strictEqual(code, b64(JSON.stringify({ v: 1, done: s.done })));
  assert.deepStrictEqual(P.decode(code).done, s.done);
  assert.deepStrictEqual(P.decode('  ' + code.slice(0, 8) + '\n' + code.slice(8) + ' ').done, s.done);
});

test('import rejects garbage', () => {
  for (const bad of ['', 'not base64!', '@@@@', 'abc', b64('not json'), b64('[]'), b64('{"v":2,"done":{}}'), b64('{"v":1,"done":null}'), null, undefined, 42]) {
    assert.strictEqual(P.decode(bad), null, String(bad));
  }
});

test('import ignores invalid ids but keeps valid ones', () => {
  const code = b64(JSON.stringify({ v: 1, done: { 'kids-0d3a63dc': 1, 'bad id': 1, 'http://x.example/a': 1, '__proto__': 1, 'learn-ZZZZZZZZ': 1 } }));
  assert.deepStrictEqual(Object.keys(P.decode(code).done), ['kids-0d3a63dc']);
});

test('import rejects oversized input', () => {
  const tooLong = 'A'.repeat(60004);
  assert.strictEqual(P.decode(tooLong), null);
  const many = {};
  for (let i = 0; i < 2001; i++) many[ID(i)] = 1;
  assert.strictEqual(P.decode(b64(JSON.stringify({ v: 1, done: many }))), null);
  const ok = {};
  for (let i = 0; i < 2000; i++) ok[ID(i)] = 1;
  assert.strictEqual(P.count(P.decode(b64(JSON.stringify({ v: 1, done: ok })))), 2000);
});

test('the total is capped at 2000 when adding or merging', () => {
  const a = P.emptyState(); const b = P.emptyState();
  for (let i = 0; i < 2000; i++) P.setDone(a, ID(i), true);
  P.setDone(a, ID(5000), true);
  assert.strictEqual(P.count(a), 2000);
  for (let i = 1000; i < 3000; i++) P.setDone(b, ID(i), true);
  assert.ok(P.count(P.merge(a, b)) <= 2000);
});

test('format fills placeholders and leaves unknown ones', () => {
  assert.strictEqual(P.format('{done} of {total} done', { done: 3, total: 26 }), '3 of 26 done');
  assert.strictEqual(P.format('{x} {y}', { x: 1 }), '1 {y}');
});

if (failed) { console.log('\n' + failed + ' test(s) failed'); process.exit(1); }
console.log('\nall progress tests passed');
