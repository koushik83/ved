/*
 * Cloudflare Pages Function for the English city pages, /panchang/<city>.
 *
 * It fills today's panchang into the page as it is served (the date, the Hindu date line, sunrise and moonrise, the
 * tithi, nakshatra, yoga and karana, the calendar, the good times and the times to avoid, both choghadiyas, the
 * sky drawing and the coming fasts), so search engines and readers without scripts see today's figures. In the
 * browser, /panchang.js then renders the same boxes exactly as before; nothing on the page changes for a reader.
 *
 * The drawing code is panchang.js's, with one difference: local times come from the offsets the build writes into
 * each city's data file ("zoff"), not from Intl, because building an Intl time-zone formatter costs more CPU than
 * the free plan allows a request on a cold start. tools/check_edge.mjs runs the real panchang.js in Node and checks
 * that every box comes out the same, for every city, on ordinary days and on the days the clocks change.
 *
 * Any failure, or any page that is not a city page, returns the page exactly as it was.
 */

const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
  'November', 'December'];

export async function onRequest(context) {
  const res = await context.next();
  try {
    const type = res.headers.get('content-type') || '';
    if (res.status !== 200 || type.indexOf('text/html') === -1) { return res; }
    const html = await res.clone().text();
    const m = html.match(/<script>window\.PANCHANG = (\{[\s\S]*?\});<\/script>/);
    if (!m) { return res; }
    const P = JSON.parse(m[1]);
    if (P.lang !== 'en' || !/^\/panchang\/data\/[a-z-]+\.json$/.test(P.data)) { return res; }
    const dres = await context.env.ASSETS.fetch(new URL(P.data, context.request.url));
    if (!dres.ok) { return res; }
    const now = Date.now();
    const data = sliceData(await dres.text(), now);
    if (!data) { return res; }
    const out = renderToday(html, P, data, now);
    if (!out) { return res; }
    const headers = new Headers(res.headers);
    headers.delete('content-length');
    // the static file's validators describe yesterday's page too: without removing them a crawler that revalidates
    // gets a 304 and keeps an old day's figures
    headers.delete('etag');
    headers.delete('last-modified');
    headers.set('cache-control', 'public, max-age=0, must-revalidate');
    return new Response(out, { status: 200, headers });
  } catch (e) {
    return res;
  }
}

// ------------------------------------------------------------------ the data: only the days needed

// the city's UTC offset at an instant, and its civil date then, from the build's offsets
function offsetAt(zoff, e) {
  let lo = 0, hi = zoff.length - 1;
  if (e < zoff[0][0]) { return zoff[0][1]; }
  while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (zoff[mid][0] <= e) { lo = mid; } else { hi = mid - 1; } }
  return zoff[lo][1];
}
function cityDate(zoff, e) { return new Date((e + offsetAt(zoff, e)) * 1000).toISOString().slice(0, 10); }
function shiftKey(iso, days) { return new Date(Date.parse(iso) + days * 86400000).toISOString().slice(0, 10); }

// Parsing a whole year (195 KB) costs most of the CPU a request may use, so only the base, the offsets, the days
// from yesterday to 47 days ahead and the fasts are parsed. The build writes the fields in this order (slug, tz,
// first, last, base, rows, vrats, zoff) and starts each day with its date; anything unexpected returns null and
// the page is served as it is.
export function sliceData(raw, nowMs) {
  try {
    const base = Number((raw.match(/"base":(-?\d+)/) || [])[1]);
    const zi = raw.indexOf('"zoff":[');
    const ri = raw.indexOf('"rows":[');
    const vi = raw.indexOf('],"vrats":[', ri);
    if (!Number.isFinite(base) || zi < 0 || ri < 0 || vi < 0) { return null; }
    const zoff = JSON.parse(raw.slice(zi + 7, raw.indexOf(']]', zi) + 2));
    const key = cityDate(zoff, Math.floor(nowMs / 1000));
    const rowsText = raw.slice(ri + 8, vi);
    const first = rowsText.slice(6, 16);
    const lo = shiftKey(key, -1) < first ? first : shiftKey(key, -1);
    const start = rowsText.indexOf('{"d":"' + lo + '"');
    if (start < 0) { return null; }
    let end = rowsText.indexOf('{"d":"' + shiftKey(key, 48) + '"', start);
    end = end < 0 ? rowsText.length : end - 1;               // drop the comma before the next day
    const rows = JSON.parse('[' + rowsText.slice(start, end) + ']');
    const vrats = JSON.parse(raw.slice(vi + 10, raw.indexOf('],"zoff":', vi) + 1));
    return { base, zoff, rows, vrats };
  } catch (e) {
    return null;
  }
}

// ------------------------------------------------------------------ the page, filled for one instant

export function renderToday(html, P, data, nowMs) {
  const boxes = todayBoxes(P, data, nowMs);
  if (!boxes) { return null; }
  let out = html, filled = 0;
  for (const id of Object.keys(boxes)) {
    const re = new RegExp('(<([a-z]+)\\b[^>]*\\bid="' + id + '"[^>]*>)(?:…)?(</\\2>)');
    if (re.test(out)) { out = out.replace(re, (all, open, tag, close) => open + boxes[id] + close); filled++; }
  }
  return filled === Object.keys(boxes).length ? out : null;
}

// the content of each box panchang.js draws, for the city's today at nowMs
export function todayBoxes(P, data, nowMs) {
  const L = P.labels, N = P.names;
  const zoff = data.zoff;
  if (!zoff || !zoff.length) { return null; }
  const base = data.base;
  const abs = (v) => (v === null || v === undefined) ? null : base + v;

  // ---- local time from the offsets: the same instants Intl would show for the city's zone
  function local(e) { return new Date((e + offsetAt(zoff, e)) * 1000); }
  const pad = (n) => (n < 10 ? '0' : '') + n;
  function dateKey(epoch) { const d = local(epoch); return d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate()); }
  function clock(epoch) {
    const d = local(Math.floor(epoch) + 30), h = d.getUTCHours();
    return pad(h % 12 || 12) + ':' + pad(d.getUTCMinutes()) + ' ' + (h < 12 ? 'AM' : 'PM');
  }
  function longDate(epoch) { const d = local(Math.floor(epoch)); return DAYS[d.getUTCDay()] + ', ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }
  function dayText(iso) { const d = new Date(Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10), 12)); return DAYS[d.getUTCDay()] + ', ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }

  // ---- only the days the boxes can show: today, and the 45 days the coming fasts look ahead (CPU is scarce)
  const key = dateKey(Math.floor(nowMs / 1000));
  const lo = shiftKey(key, -1), hi = shiftKey(key, 47);
  const byDate = {};
  for (const r0 of data.rows) {
    if (r0.d < lo || r0.d > hi) { continue; }
    const r = Object.assign({}, r0);
    r.sr = abs(r.sr); r.ss = abs(r.ss); r.nsr = abs(r.nsr); r.mr = abs(r.mr); r.ms = abs(r.ms);
    r.bm = [abs(r.bm[0]), abs(r.bm[1])];
    for (const limb of ['t', 'n', 'y', 'k']) { r[limb] = r[limb].map((it) => [it[0], abs(it[1])]); }
    byDate[r.d] = r;
  }
  const vrats = (data.vrats || []).filter((o0) => o0.d >= key && o0.d <= hi).map((o0) => {
    const o = Object.assign({}, o0);
    o.mr = abs(o.mr); o.te = abs(o.te);
    if (o.fast) { o.fast = [abs(o.fast[0]), abs(o.fast[1])]; }
    if (o.win) { o.win = [abs(o.win[0]), abs(o.win[1])]; }
    if (o.pr) { o.pr = [abs(o.pr[0]), abs(o.pr[1])]; }
    return o;
  });

  // ---- from here on, panchang.js's own drawing code
  function esc(s) { return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
  function when(epoch, row) {
    if (epoch === null || epoch === undefined) { return ''; }
    const s = clock(epoch);
    return dateKey(epoch) !== row.d ? s + ' (' + L.nextDay + ')' : s;
  }
  function span(a, b, row) { return when(a, row) + ' ' + L.to + ' ' + when(b, row); }
  function part(a, b, n, k) { const d = (b - a) / n; return [a + d * (k - 1), a + d * k]; }
  function hm(seconds) { const h = Math.floor(seconds / 3600), m = Math.round((seconds - h * 3600) / 60); return h + ' ' + L.hours + ' ' + m + ' ' + L.minutes; }

  const RAHU = { 6: 8, 0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3 };
  const YAMA = { 6: 5, 0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6 };
  const GULIKA = { 6: 7, 0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1 };
  const ORDER = ['udveg', 'chal', 'labh', 'amrit', 'kaal', 'shubh', 'rog'];
  const DAY_FIRST = { 6: 'udveg', 0: 'amrit', 1: 'rog', 2: 'labh', 3: 'shubh', 4: 'chal', 5: 'kaal' };
  const NIGHT_FIRST = { 6: 'shubh', 0: 'chal', 1: 'kaal', 2: 'udveg', 3: 'amrit', 4: 'rog', 5: 'labh' };

  function choghadiya(a, b, first) {
    const start = ORDER.indexOf(first), out = [];
    for (let k = 0; k < 8; k++) { const p = part(a, b, 8, k + 1); out.push([ORDER[(start + k) % 7], p[0], p[1]]); }
    return out;
  }
  function hinduLine(row) {
    const tithi = row.t[0][0];
    const month = (row.pa ? N.adhika : '') + N.month[row.pm];
    return month + ', ' + N.paksha[row.p === 's' ? 'shukla' : 'krishna'] + ' ' + N.tithi[tithi] + ' · ' + L.vikram + ' ' + row.vs + ' · ' + N.weekday[row.w];
  }
  function limbRow(label, items, table, row) {
    let out = '';
    for (let i = 0; i < items.length; i++) {
      const name = table[items[i][0]], end = items[i][1];
      out += '<div class="limb"><span class="k">' + (i === 0 ? esc(label) : '') + '</span><span class="v"><b>' + esc(name) + '</b>'
        + (end !== null ? ' <span class="till">' + esc(L.till) + ' ' + esc(when(end, row)) + '</span>' : '') + '</span></div>';
    }
    return out;
  }
  function dd(label, value, sub) { return '<dt>' + esc(label) + '</dt><dd>' + esc(value) + (sub ? '<span class="sub">' + esc(sub) + '</span>' : '') + '</dd>'; }
  function spanRow(label, a, b, row) { return '<div class="limb"><span class="k">' + esc(label) + '</span><span class="v">' + esc(span(a, b, row)) + '</span></div>'; }
  function choghTable(list, row) {
    let out = '';
    for (let i = 0; i < list.length; i++) {
      const key = list[i][0];
      out += '<tr><td class="tone-' + N.tone[key] + '">' + esc(N.choghadiya[key]) + '</td><td>' + esc(span(list[i][1], list[i][2], row)) + '</td></tr>';
    }
    return out;
  }
  function wheel(row) {
    const R = 160, cx = R, cy = R;
    function pt(deg, r) { const a = deg * Math.PI / 180; return [cx - r * Math.sin(a), cy - r * Math.cos(a)]; }
    function arc(a0, a1, r0, r1, fill, cls) {
      const p0 = pt(a0, r1), p1 = pt(a1, r1), p2 = pt(a1, r0), p3 = pt(a0, r0);
      return '<path d="M' + p0[0].toFixed(1) + ',' + p0[1].toFixed(1) + ' A' + r1 + ',' + r1 + ' 0 0,0 ' + p1[0].toFixed(1) + ',' + p1[1].toFixed(1)
        + ' L' + p2[0].toFixed(1) + ',' + p2[1].toFixed(1) + ' A' + r0 + ',' + r0 + ' 0 0,1 ' + p3[0].toFixed(1) + ',' + p3[1].toFixed(1) + ' Z" fill="' + fill + '"' + (cls ? ' class="' + cls + '"' : '') + ' stroke="#F3E7D3" stroke-width="0.6"/>';
    }
    let s = '<svg viewBox="0 0 320 320" role="img" aria-label="' + esc(L.sky) + '">';
    const sunRashi = Math.floor(row.sl / 30), moonRashi = Math.floor(row.ml / 30), moonNak = Math.floor(row.ml / (360 / 27));
    for (let r = 0; r < 12; r++) {
      const fill = r === moonRashi ? '#FFE0B2' : (r === sunRashi ? '#FFF3C4' : (r % 2 ? '#FDF4E7' : '#FFFFFF'));
      s += arc(r * 30, (r + 1) * 30, 126, 152, fill);
      const lp = pt(r * 30 + 15, 139);
      s += '<text x="' + lp[0].toFixed(1) + '" y="' + (lp[1] + 3).toFixed(1) + '" font-size="8.5" text-anchor="middle" fill="#5D2E00" font-family="Arial, sans-serif">' + esc(N.rashi[r]) + '</text>';
    }
    for (let k = 0; k < 27; k++) {
      s += arc(k * 360 / 27, (k + 1) * 360 / 27, 108, 124, k === moonNak ? '#FFCC80' : (k % 2 ? '#FBF0DF' : '#FFFFFF'));
    }
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="92" fill="none" stroke="#E0C9A6" stroke-width="1" stroke-dasharray="3 4"/>';
    const sp = pt(row.sl, 92), mp = pt(row.ml, 92);
    s += '<circle cx="' + sp[0].toFixed(1) + '" cy="' + sp[1].toFixed(1) + '" r="13" fill="#FFB300" opacity="0.35"/>';
    s += '<circle cx="' + sp[0].toFixed(1) + '" cy="' + sp[1].toFixed(1) + '" r="8" fill="#FF8F00"/>';
    const e = ((row.ml - row.sl) % 360 + 360) % 360;
    const phase = e <= 180 ? e : 360 - e;
    const rx = 9 * Math.abs(Math.cos(phase * Math.PI / 180));
    const sweep = phase < 90 ? 0 : 1;
    const face = Math.atan2(sp[1] - mp[1], sp[0] - mp[0]) * 180 / Math.PI;
    s += '<g transform="translate(' + mp[0].toFixed(1) + ',' + mp[1].toFixed(1) + ') rotate(' + face.toFixed(1) + ')">'
      + '<circle r="9" fill="#5D4037"/>'
      + '<path d="M0,-9 A9,9 0 0,1 0,9 A' + rx.toFixed(2) + ',9 0 0,' + sweep + ' 0,-9 Z" fill="#FFF8E1"/>'
      + '<circle r="9" fill="none" stroke="#8D6E63" stroke-width="0.8"/></g>';
    const sunDeg = Math.floor(row.sl % 30), moonDeg = Math.floor(row.ml % 30);
    s += '<text x="' + cx + '" y="' + (cy - 14) + '" font-size="11" text-anchor="middle" fill="#A04000" font-family="Arial, sans-serif">' + esc(L.sun) + ' ' + sunDeg + '° ' + esc(N.rashi[sunRashi]) + '</text>';
    s += '<text x="' + cx + '" y="' + (cy + 2) + '" font-size="11" text-anchor="middle" fill="#5D2E00" font-family="Arial, sans-serif">' + esc(L.moon) + ' ' + moonDeg + '° ' + esc(N.rashi[moonRashi]) + '</text>';
    s += '<text x="' + cx + '" y="' + (cy + 18) + '" font-size="10" text-anchor="middle" fill="#666" font-family="Arial, sans-serif">' + esc(N.nakshatra[moonNak]) + ' · ' + esc(L.elong) + ' ' + Math.round(e) + '°</text>';
    s += '</svg><figcaption>' + esc(L.sky) + '</figcaption>';
    return s;
  }
  function vratLine(o, row, withDate) {
    const name = (P.lang === 'hi' ? o.hi : o.en) + (o.ang ? ' (' + L.angarki + ')' : '');
    const extra = [];
    if (o.mr !== null && o.mr !== undefined) { extra.push(L.moonriseAt + ' ' + when(o.mr, row)); }
    if (o.fast) { extra.push(L.fastTill + ' ' + clock(o.fast[0]) + ' ' + L.to + ' ' + when(o.fast[1], row)); }
    if (o.win) { extra.push(L.pujaTime + ' ' + span(o.win[0], o.win[1], row)); }
    if (o.pr) { extra.push(L.parana + ' ' + clock(o.pr[0]) + ' ' + L.to + ' ' + clock(o.pr[1]) + ' (' + L.nextDay + ')'); }
    if (!extra.length && o.te !== null && o.te !== undefined) { extra.push(L.tithiEnds + ' ' + when(o.te, row)); }
    const dateText = withDate ? dayText(o.d) : '';
    return '<div class="vrat">' + (dateText ? '<span class="d">' + esc(dateText) + '</span> · ' : '') + '<b>' + esc(name) + '</b>'
      + (extra.length ? '<span class="x">' + esc(extra.join(' · ')) + '</span>' : '') + '</div>';
  }
  function renderVrats(row) {
    const today = [], next = [];
    for (const o of vrats) {
      if (o.d === row.d) { today.push(o); } else if (o.d > row.d && next.length < 6) {
        const days = (Date.parse(o.d) - Date.parse(row.d)) / 86400000;
        if (days <= 45) { next.push(o); }
      }
    }
    let out = '<h3 style="margin-top:0">' + esc(L.vratToday) + '</h3>';
    out += today.length ? today.map((o) => vratLine(o, row, false)).join('') : '<p class="x" style="color:#666">' + esc(L.vratNone) + '</p>';
    if (next.length) { out += '<h3>' + esc(L.vratNext) + '</h3>' + next.map((o) => vratLine(o, byDate[o.d] || row, true)).join(''); }
    return out;
  }

  // ---- the day: the city's today, as panchang.js picks it
  const row = byDate[key];
  if (!row) { return null; }
  const midDay = (row.sr + row.ss) / 2;
  const sunRashi = row.sun;
  const dayMuhurta = (row.ss - row.sr) / 15;
  const abhijit = [row.sr + dayMuhurta * 7, row.sr + dayMuhurta * 8];
  const rahu = part(row.sr, row.ss, 8, RAHU[row.w]), yama = part(row.sr, row.ss, 8, YAMA[row.w]), gul = part(row.sr, row.ss, 8, GULIKA[row.w]);
  const boxes = {
    panDate: esc(longDate(midDay)),
    panHindu: esc(hinduLine(row)),
    panSky: dd(L.sunrise, clock(row.sr)) + dd(L.sunset, clock(row.ss))
      + dd(L.moonrise, row.mr !== null ? when(row.mr, row) : L.noMoonrise)
      + dd(L.moonset, row.ms !== null ? when(row.ms, row) : L.noMoonset)
      + dd(L.dayLength, hm(row.ss - row.sr)),
    panWheel: wheel(row),
    panLimbs: limbRow(L.tithi, row.t, N.tithi, row) + limbRow(L.nakshatra, row.n, N.nakshatra, row)
      + limbRow(L.yoga, row.y, N.yoga, row) + limbRow(L.karana, row.k, N.karana, row),
    panCal: dd(L.paksha, N.paksha[row.p === 's' ? 'shukla' : 'krishna'])
      + dd(L.purnimanta, (row.pa ? N.adhika : '') + N.month[row.pm])
      + dd(L.amanta, (row.aa ? N.adhika : '') + N.month[row.am])
      + dd(L.vikram, String(row.vs)) + dd(L.shaka, String(row.sk)) + dd(L.gujarati, String(row.gs))
      + dd(L.sunRashi, N.rashi[row.sun]) + dd(L.moonRashi, N.rashi[row.moon])
      + dd(L.ritu, N.ritu[Math.floor(sunRashi / 2) % 6]) + dd(L.ayana, N.ayana[(sunRashi >= 3 && sunRashi <= 8) ? 1 : 0]),
    panGood: spanRow(L.brahma, row.bm[0], row.bm[1], row) + spanRow(L.abhijit, abhijit[0], abhijit[1], row),
    panAvoid: spanRow(L.rahu, rahu[0], rahu[1], row) + spanRow(L.yamaganda, yama[0], yama[1], row) + spanRow(L.gulika, gul[0], gul[1], row),
    panChoghDay: choghTable(choghadiya(row.sr, row.ss, DAY_FIRST[row.w]), row),
    panChoghNight: choghTable(choghadiya(row.ss, row.nsr, NIGHT_FIRST[row.w]), row),
    panVrats: renderVrats(row),
  };
  return boxes;
}
