// Checks that the edge function (functions/panchang/[slug].js) fills a city page exactly as panchang.js renders it.
//
// For every English city page and a set of instants (ordinary days, the days the clocks change in North America,
// Europe and Australia, and moments just before and after a city's midnight), it runs the real /panchang.js in a
// small fake page under Node, with the clock set to that instant, and compares every box it draws with what the
// function writes. Run from the repo root after the panchang build:
//
//     node tools/check_edge.mjs
//
// Exit code 1 and the first differences when anything disagrees.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { pathToFileURL } from 'node:url';

const ROOT = process.cwd();
const { renderToday, todayBoxes, sliceData } = await import(pathToFileURL(path.join(ROOT, 'functions', 'panchang', '[slug].js')).href);
const CLIENT = fs.readFileSync(path.join(ROOT, 'panchang.js'), 'utf8');
const BOXES = ['panDate', 'panHindu', 'panSky', 'panWheel', 'panLimbs', 'panCal', 'panGood', 'panAvoid',
  'panChoghDay', 'panChoghNight', 'panVrats'];
const TEXT_BOXES = new Set(['panDate', 'panHindu']);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

async function client(P, raw, nowMs) {
  const els = {};
  const el = (id) => els[id] || (els[id] = { id, innerHTML: '', textContent: '', hidden: false, className: '', value: '',
    addEventListener() {}, set onclick(f) {} });
  class FakeDate extends Date {
    constructor(...a) { if (a.length) { super(...a); } else { super(nowMs); } }
    static now() { return nowMs; }
  }
  const ctx = {
    document: { readyState: 'complete', getElementById: el, addEventListener() {} },
    localStorage: { setItem() {}, getItem() { return null; } },
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve(JSON.parse(raw)) }),
    setInterval() {}, location: {}, Date: FakeDate, Intl, JSON, Math, Object, String, Number, Promise, parseInt,
    encodeURIComponent,
  };
  ctx.window = ctx;
  ctx.window.PANCHANG = JSON.parse(JSON.stringify(P));
  vm.createContext(ctx);
  vm.runInContext(CLIENT, ctx);
  for (let i = 0; i < 5; i++) { await new Promise((r) => setImmediate(r)); }
  const out = {};
  for (const id of BOXES) { out[id] = TEXT_BOXES.has(id) ? esc(el(id).textContent) : el(id).innerHTML; }
  return out;
}

function served(html, P, raw, nowMs) {
  // the boxes from the days the function slices out of the file, as it does when serving, and proof that the page
  // carries each one right inside its own element
  const data = sliceData(raw, nowMs);
  if (!data) { return null; }
  const boxes = todayBoxes(P, data, nowMs);
  const out = renderToday(html, P, data, nowMs);
  if (!boxes || !out) { return null; }
  for (const id of BOXES) {
    const open = out.match(new RegExp('<[a-z]+\\b[^>]*\\bid="' + id + '"[^>]*>'));
    if (!open || out.indexOf(open[0] + boxes[id]) === -1) { return null; }
  }
  return boxes;
}

const instants = [
  '2026-11-15T12:00:00Z', '2026-12-31T23:30:00Z', '2027-01-15T05:00:00Z', '2027-03-14T07:30:00Z',
  '2027-03-14T12:00:00Z', '2027-03-28T01:30:00Z', '2027-04-04T15:30:00Z', '2027-06-21T18:00:00Z',
  '2027-10-03T16:00:00Z', '2027-10-31T00:30:00Z', '2027-11-07T06:30:00Z', '2027-12-30T11:00:00Z',
].map((s) => Date.parse(s));

// Node's time-zone data can be older than the build's (tzdata): Alberta stopped changing its clocks on 2026-11-01,
// which Node with tz 2026a does not know. Where the two disagree on a city's offset, Node is not a fair reference,
// so that city is reported and skipped rather than counted.
function nodeOffset(tz, ms) {
  const parts = new Intl.DateTimeFormat('en-US', { timeZone: tz, timeZoneName: 'longOffset' }).formatToParts(new Date(ms));
  const m = (parts.find((p) => p.type === 'timeZoneName') || {}).value.match(/GMT(?:([+-])(\d\d):(\d\d))?/);
  return !m || !m[1] ? 0 : (m[1] === '-' ? -1 : 1) * (+m[2] * 3600 + +m[3] * 60);
}
function zoffAt(zoff, s) { let v = zoff[0][1]; for (const [t, o] of zoff) { if (t <= s) { v = o; } } return v; }

let checked = 0, bad = 0;
const skipped = [];
const pages = fs.readdirSync(path.join(ROOT, 'panchang')).filter((f) => f.endsWith('.html'));
for (const f of pages) {
  const html = fs.readFileSync(path.join(ROOT, 'panchang', f), 'utf8');
  const m = html.match(/<script>window\.PANCHANG = (\{[\s\S]*?\});<\/script>/);
  if (!m) { continue; }
  const P = JSON.parse(m[1]);
  const raw = fs.readFileSync(path.join(ROOT, P.data.replace(/^\//, '')), 'utf8');
  const data = JSON.parse(raw);
  const firstMs = Date.parse(data.first), lastMs = Date.parse(data.last);
  let disagree = false;
  for (let ms = firstMs; ms <= lastMs; ms += 6 * 3600 * 1000) {
    if (nodeOffset(P.tz, ms) !== zoffAt(data.zoff, ms / 1000)) { disagree = true; break; }
  }
  if (disagree) { skipped.push(`${f} (${P.tz})`); continue; }
  for (const now of instants) {
    const want = await client(P, raw, now);
    const got = served(html, P, raw, now);
    checked++;
    if (!got) { bad++; if (bad <= 5) { console.log('NO OUTPUT', f, new Date(now).toISOString()); } continue; }
    for (const id of BOXES) {
      if (want[id] !== got[id]) {
        bad++;
        if (bad <= 5) {
          let i = 0; while (i < want[id].length && want[id][i] === got[id][i]) { i++; }
          console.log('DIFF', f, new Date(now).toISOString(), id, '\n  client:', want[id].slice(Math.max(0, i - 60), i + 80),
            '\n  edge:  ', (got[id] || '').slice(Math.max(0, i - 60), i + 80));
        }
        break;
      }
    }
  }
}
if (skipped.length) {
  console.log(`skipped, Node's time-zone data (tz ${process.versions.tz}) differs from the build's: ${skipped.join(', ')}`);
}
console.log(`${checked} page-instants checked, ${bad} differing`);
process.exit(bad ? 1 : 0);
