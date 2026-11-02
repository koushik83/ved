/*
 * The panchang page. Reads window.PANCHANG, written into the page at build time: the city, its IANA time zone,
 * the language, the labels and names, and one row per day holding UTC epoch seconds for sunrise, sunset, the
 * next sunrise, moonrise and moonset, and for the end of each tithi, nakshatra, yoga and karana.
 *
 * Everything shown in local time goes through Intl with the city's zone, so daylight saving is the browser's
 * problem, not ours. The muhurtas and the choghadiya are fractions of the day and night, computed here from
 * the exact sunrise and sunset and rounded to the minute only when displayed, the same arithmetic as the
 * generator's. The page shows the city's current date, switches at the city's midnight, and lets a reader
 * pick any date the data holds.
 */
(function () {
  'use strict';

  var P = window.PANCHANG;
  if (!P) { return; }
  var L = P.labels, N = P.names, TZ = P.tz;
  var LOCALE = P.lang === 'hi' ? 'hi-IN' : 'en-IN';
  var byDate = {};
  var vrats = [];              // the fasts and festivals, in date order

  // the day rows live in one file per city, shared by both languages; their seconds are offsets from a base
  function absorb(data) {
    var base = data.base;
    function abs(v) { return (v === null || v === undefined) ? null : base + v; }
    for (var i = 0; i < data.rows.length; i++) {
      var r = data.rows[i];
      r.sr = abs(r.sr); r.ss = abs(r.ss); r.nsr = abs(r.nsr); r.mr = abs(r.mr); r.ms = abs(r.ms);
      r.bm = [abs(r.bm[0]), abs(r.bm[1])];
      var limbs = ['t', 'n', 'y', 'k'];
      for (var j = 0; j < limbs.length; j++) {
        var items = r[limbs[j]];
        for (var k = 0; k < items.length; k++) { items[k][1] = abs(items[k][1]); }
      }
      byDate[r.d] = r;
    }
    vrats = data.vrats || [];
    for (var v = 0; v < vrats.length; v++) {
      var o = vrats[v];
      o.mr = abs(o.mr); o.te = abs(o.te);
      if (o.fast) { o.fast = [abs(o.fast[0]), abs(o.fast[1])]; }
      if (o.win) { o.win = [abs(o.win[0]), abs(o.win[1])]; }
      if (o.pr) { o.pr = [abs(o.pr[0]), abs(o.pr[1])]; }
    }
  }

  // one fast or festival as a line: its name, and the moment that matters for it
  function vratLine(o, row, withDate) {
    var name = (P.lang === 'hi' ? o.hi : o.en) + (o.ang ? ' (' + L.angarki + ')' : '');
    var extra = [];
    if (o.mr !== null && o.mr !== undefined) { extra.push(L.moonriseAt + ' ' + when(o.mr, row)); }
    if (o.fast) { extra.push(L.fastTill + ' ' + clock(o.fast[0]) + ' ' + L.to + ' ' + when(o.fast[1], row)); }
    if (o.win) { extra.push(L.pujaTime + ' ' + span(o.win[0], o.win[1], row)); }
    if (o.pr) { extra.push(L.parana + ' ' + clock(o.pr[0]) + ' ' + L.to + ' ' + clock(o.pr[1]) + ' (' + L.nextDay + ')'); }
    if (!extra.length && o.te !== null && o.te !== undefined) { extra.push(L.tithiEnds + ' ' + when(o.te, row)); }
    var dateText = withDate ? longFmt.format(new Date(Date.UTC(+o.d.slice(0, 4), +o.d.slice(5, 7) - 1, +o.d.slice(8, 10), 12))) : '';
    return '<div class="vrat">' + (dateText ? '<span class="d">' + esc(dateText) + '</span> · ' : '') + '<b>' + esc(name) + '</b>'
      + (extra.length ? '<span class="x">' + esc(extra.join(' · ')) + '</span>' : '') + '</div>';
  }

  function renderVrats(row) {
    var today = [], next = [];
    for (var i = 0; i < vrats.length; i++) {
      var o = vrats[i];
      if (o.d === row.d) { today.push(o); }
      else if (o.d > row.d && next.length < 6) {
        var days = (Date.parse(o.d) - Date.parse(row.d)) / 86400000;
        if (days <= 45) { next.push(o); }
      }
    }
    var html = '<h3 style="margin-top:0">' + esc(L.vratToday) + '</h3>';
    html += today.length ? today.map(function (o) { return vratLine(o, row, false); }).join('') : '<p class="x" style="color:#666">' + esc(L.vratNone) + '</p>';
    if (next.length) {
      html += '<h3>' + esc(L.vratNext) + '</h3>' + next.map(function (o) { return vratLine(o, byDate[o.d] || row, true); }).join('');
    }
    $('panVrats').innerHTML = html;
  }

  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function track(name, params) { if (typeof window.vedTrack === 'function') { try { window.vedTrack(name, params); } catch (e) { /* never break the page */ } } }

  var timeFmt = new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: TZ });
  var keyFmt = new Intl.DateTimeFormat('en-CA', { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: TZ });
  var longFmt = new Intl.DateTimeFormat(LOCALE, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: TZ });

  function dateKey(epoch) { return keyFmt.format(new Date(epoch * 1000)); }          // YYYY-MM-DD in the city
  function clock(epoch) { return timeFmt.format(new Date((epoch + 30) * 1000)).replace(/ | /g, ' ').toUpperCase(); }
  function when(epoch, row) {                                                          // a clock time, flagged if after midnight
    if (epoch === null || epoch === undefined) { return ''; }
    var s = clock(epoch);
    return dateKey(epoch) !== row.d ? s + ' (' + L.nextDay + ')' : s;
  }
  function span(a, b, row) { return when(a, row) + ' ' + L.to + ' ' + when(b, row); }
  function part(a, b, n, k) { var d = (b - a) / n; return [a + d * (k - 1), a + d * k]; }
  function hm(seconds) { var h = Math.floor(seconds / 3600), m = Math.round((seconds - h * 3600) / 60); return h + ' ' + L.hours + ' ' + m + ' ' + L.minutes; }

  // segments (1-based of 8) and the choghadiya order, by weekday Mon=0 .. Sun=6, as in the generator
  var RAHU = { 6: 8, 0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3 };
  var YAMA = { 6: 5, 0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6 };
  var GULIKA = { 6: 7, 0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1 };
  var ORDER = ['udveg', 'chal', 'labh', 'amrit', 'kaal', 'shubh', 'rog'];
  var DAY_FIRST = { 6: 'udveg', 0: 'amrit', 1: 'rog', 2: 'labh', 3: 'shubh', 4: 'chal', 5: 'kaal' };
  var NIGHT_FIRST = { 6: 'shubh', 0: 'chal', 1: 'kaal', 2: 'udveg', 3: 'amrit', 4: 'rog', 5: 'labh' };

  function choghadiya(a, b, first) {
    var start = ORDER.indexOf(first), out = [];
    for (var k = 0; k < 8; k++) { var p = part(a, b, 8, k + 1); out.push([ORDER[(start + k) % 7], p[0], p[1]]); }
    return out;
  }

  // ---- the Hindu date line: "Kartika, Krishna Saptami · Vikram Samvat 2083 · Raviwara"
  function hinduLine(row) {
    var tithi = row.t[0][0];
    var month = (row.pa ? N.adhika : '') + N.month[row.pm];
    return month + ', ' + N.paksha[row.p === 's' ? 'shukla' : 'krishna'] + ' ' + N.tithi[tithi] + ' · ' + L.vikram + ' ' + row.vs + ' · ' + N.weekday[row.w];
  }

  function limbRow(label, items, table, row) {
    var html = '';
    for (var i = 0; i < items.length; i++) {
      var name = table[items[i][0]], end = items[i][1];
      html += '<div class="limb"><span class="k">' + (i === 0 ? esc(label) : '') + '</span><span class="v"><b>' + esc(name) + '</b>'
        + (end !== null ? ' <span class="till">' + esc(L.till) + ' ' + esc(when(end, row)) + '</span>' : '') + '</span></div>';
    }
    return html;
  }

  function dd(label, value, sub) {
    return '<dt>' + esc(label) + '</dt><dd>' + esc(value) + (sub ? '<span class="sub">' + esc(sub) + '</span>' : '') + '</dd>';
  }

  function spanRow(label, a, b, row) {
    return '<div class="limb"><span class="k">' + esc(label) + '</span><span class="v">' + esc(span(a, b, row)) + '</span></div>';
  }

  function choghTable(list, row) {
    var html = '';
    for (var i = 0; i < list.length; i++) {
      var key = list[i][0];
      html += '<tr><td class="tone-' + N.tone[key] + '">' + esc(N.choghadiya[key]) + '</td><td>' + esc(span(list[i][1], list[i][2], row)) + '</td></tr>';
    }
    return html;
  }

  // ---- the sky at sunrise: the zodiac ring, the nakshatra ring, the Sun and the Moon with its phase
  function wheel(row) {
    var R = 160, cx = R, cy = R;
    function pt(deg, r) { var a = deg * Math.PI / 180; return [cx - r * Math.sin(a), cy - r * Math.cos(a)]; }
    function arc(a0, a1, r0, r1, fill, cls) {
      var p0 = pt(a0, r1), p1 = pt(a1, r1), p2 = pt(a1, r0), p3 = pt(a0, r0);
      return '<path d="M' + p0[0].toFixed(1) + ',' + p0[1].toFixed(1) + ' A' + r1 + ',' + r1 + ' 0 0,0 ' + p1[0].toFixed(1) + ',' + p1[1].toFixed(1)
        + ' L' + p2[0].toFixed(1) + ',' + p2[1].toFixed(1) + ' A' + r0 + ',' + r0 + ' 0 0,1 ' + p3[0].toFixed(1) + ',' + p3[1].toFixed(1) + ' Z" fill="' + fill + '"' + (cls ? ' class="' + cls + '"' : '') + ' stroke="#F3E7D3" stroke-width="0.6"/>';
    }
    var s = '<svg viewBox="0 0 320 320" role="img" aria-label="' + esc(L.sky) + '">';
    var sunRashi = Math.floor(row.sl / 30), moonRashi = Math.floor(row.ml / 30), moonNak = Math.floor(row.ml / (360 / 27));
    for (var r = 0; r < 12; r++) {
      var fill = r === moonRashi ? '#FFE0B2' : (r === sunRashi ? '#FFF3C4' : (r % 2 ? '#FDF4E7' : '#FFFFFF'));
      s += arc(r * 30, (r + 1) * 30, 126, 152, fill);
      var lp = pt(r * 30 + 15, 139);
      s += '<text x="' + lp[0].toFixed(1) + '" y="' + (lp[1] + 3).toFixed(1) + '" font-size="8.5" text-anchor="middle" fill="#5D2E00" font-family="Arial, sans-serif">' + esc(N.rashi[r]) + '</text>';
    }
    for (var k = 0; k < 27; k++) {
      s += arc(k * 360 / 27, (k + 1) * 360 / 27, 108, 124, k === moonNak ? '#FFCC80' : (k % 2 ? '#FBF0DF' : '#FFFFFF'));
    }
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="92" fill="none" stroke="#E0C9A6" stroke-width="1" stroke-dasharray="3 4"/>';
    var sp = pt(row.sl, 92), mp = pt(row.ml, 92);
    s += '<circle cx="' + sp[0].toFixed(1) + '" cy="' + sp[1].toFixed(1) + '" r="13" fill="#FFB300" opacity="0.35"/>';
    s += '<circle cx="' + sp[0].toFixed(1) + '" cy="' + sp[1].toFixed(1) + '" r="8" fill="#FF8F00"/>';
    // the Moon: the lit part faces the Sun; its width follows the elongation
    var e = ((row.ml - row.sl) % 360 + 360) % 360;
    var phase = e <= 180 ? e : 360 - e;                       // 0 new .. 180 full
    var rx = 9 * Math.abs(Math.cos(phase * Math.PI / 180));
    var sweep = phase < 90 ? 0 : 1;                           // crescent or gibbous
    var face = Math.atan2(sp[1] - mp[1], sp[0] - mp[0]) * 180 / Math.PI;
    s += '<g transform="translate(' + mp[0].toFixed(1) + ',' + mp[1].toFixed(1) + ') rotate(' + face.toFixed(1) + ')">'
      + '<circle r="9" fill="#5D4037"/>'
      + '<path d="M0,-9 A9,9 0 0,1 0,9 A' + rx.toFixed(2) + ',9 0 0,' + sweep + ' 0,-9 Z" fill="#FFF8E1"/>'
      + '<circle r="9" fill="none" stroke="#8D6E63" stroke-width="0.8"/></g>';
    var sunDeg = Math.floor(row.sl % 30), moonDeg = Math.floor(row.ml % 30);
    s += '<text x="' + cx + '" y="' + (cy - 14) + '" font-size="11" text-anchor="middle" fill="#A04000" font-family="Arial, sans-serif">' + esc(L.sun) + ' ' + sunDeg + '° ' + esc(N.rashi[sunRashi]) + '</text>';
    s += '<text x="' + cx + '" y="' + (cy + 2) + '" font-size="11" text-anchor="middle" fill="#5D2E00" font-family="Arial, sans-serif">' + esc(L.moon) + ' ' + moonDeg + '° ' + esc(N.rashi[moonRashi]) + '</text>';
    s += '<text x="' + cx + '" y="' + (cy + 18) + '" font-size="10" text-anchor="middle" fill="#666" font-family="Arial, sans-serif">' + esc(N.nakshatra[moonNak]) + ' · ' + esc(L.elong) + ' ' + Math.round(e) + '°</text>';
    s += '</svg><figcaption>' + esc(L.sky) + '</figcaption>';
    return s;
  }

  // ---- render one day
  var shown = null;
  function render(row) {
    shown = row;
    var midDay = (row.sr + row.ss) / 2;
    $('panDate').textContent = longFmt.format(new Date(midDay * 1000));
    $('panHindu').textContent = hinduLine(row);

    var sky = dd(L.sunrise, clock(row.sr)) + dd(L.sunset, clock(row.ss))
      + dd(L.moonrise, row.mr !== null ? when(row.mr, row) : L.noMoonrise)
      + dd(L.moonset, row.ms !== null ? when(row.ms, row) : L.noMoonset)
      + dd(L.dayLength, hm(row.ss - row.sr));
    $('panSky').innerHTML = sky;
    $('panWheel').innerHTML = wheel(row);

    $('panLimbs').innerHTML = limbRow(L.tithi, row.t, N.tithi, row) + limbRow(L.nakshatra, row.n, N.nakshatra, row)
      + limbRow(L.yoga, row.y, N.yoga, row) + limbRow(L.karana, row.k, N.karana, row);
    var sunRashi = row.sun;
    $('panCal').innerHTML = dd(L.paksha, N.paksha[row.p === 's' ? 'shukla' : 'krishna'])
      + dd(L.purnimanta, (row.pa ? N.adhika : '') + N.month[row.pm])
      + dd(L.amanta, (row.aa ? N.adhika : '') + N.month[row.am])
      + dd(L.vikram, String(row.vs)) + dd(L.shaka, String(row.sk)) + dd(L.gujarati, String(row.gs))
      + dd(L.sunRashi, N.rashi[row.sun]) + dd(L.moonRashi, N.rashi[row.moon])
      + dd(L.ritu, N.ritu[Math.floor(sunRashi / 2) % 6]) + dd(L.ayana, N.ayana[(sunRashi >= 3 && sunRashi <= 8) ? 1 : 0]);

    var dayMuhurta = (row.ss - row.sr) / 15;
    var abhijit = [row.sr + dayMuhurta * 7, row.sr + dayMuhurta * 8];
    $('panGood').innerHTML = spanRow(L.brahma, row.bm[0], row.bm[1], row) + spanRow(L.abhijit, abhijit[0], abhijit[1], row);
    var rahu = part(row.sr, row.ss, 8, RAHU[row.w]), yama = part(row.sr, row.ss, 8, YAMA[row.w]), gul = part(row.sr, row.ss, 8, GULIKA[row.w]);
    $('panAvoid').innerHTML = spanRow(L.rahu, rahu[0], rahu[1], row) + spanRow(L.yamaganda, yama[0], yama[1], row) + spanRow(L.gulika, gul[0], gul[1], row);

    $('panChoghDay').innerHTML = choghTable(choghadiya(row.sr, row.ss, DAY_FIRST[row.w]), row);
    $('panChoghNight').innerHTML = choghTable(choghadiya(row.ss, row.nsr, NIGHT_FIRST[row.w]), row);
    if ($('panVrats')) { renderVrats(row); }

    $('panShare').onclick = function () {
      track('share', { method: 'whatsapp', content_type: 'panchang', city: P.slug, lang: P.lang });
      var text = '🗓️ ' + L.shareHead + ', ' + longFmt.format(new Date(midDay * 1000)) + '\n' + hinduLine(row)
        + '\n' + L.tithi + ': ' + N.tithi[row.t[0][0]] + (row.t[0][1] !== null ? ' ' + L.till + ' ' + when(row.t[0][1], row) : '')
        + '\n' + L.nakshatra + ': ' + N.nakshatra[row.n[0][0]] + (row.n[0][1] !== null ? ' ' + L.till + ' ' + when(row.n[0][1], row) : '')
        + '\n' + L.sunrise + ' ' + clock(row.sr) + ', ' + L.sunset + ' ' + clock(row.ss)
        + '\n' + L.rahu + ' ' + span(rahu[0], rahu[1], row);
      window.open('https://wa.me/?text=' + encodeURIComponent(text + '\n\n' + P.url));
    };
  }

  // ---- which day: the city's today unless the reader picks a date
  var picked = null;
  function todayKey() { return dateKey(Math.floor(Date.now() / 1000)); }

  function show() {
    var key = picked || todayKey();
    var row = byDate[key];
    $('panNote').hidden = true;
    if (!row) {
      $('panNote').textContent = L.range;
      $('panNote').hidden = false;
      var keys = Object.keys(byDate).sort();
      row = byDate[key < keys[0] ? keys[0] : keys[keys.length - 1]];
    }
    $('todayBtn').className = picked ? '' : 'on';
    render(row);
  }

  function start() {
    try { localStorage.setItem('ved_panchang_city', P.slug); } catch (e) { /* storage blocked */ }
    $('city').addEventListener('change', function () {
      var slug = this.value;
      track('panchang_city', { from: P.slug, to: slug, lang: P.lang });
      location.href = (P.lang === 'hi' ? '/hi' : '') + '/panchang/' + slug;
    });
    $('todayBtn').addEventListener('click', function () { picked = null; $('pickDate').value = ''; show(); });
    $('pickDate').addEventListener('change', function () {
      picked = this.value && byDate[this.value] ? this.value : null;
      if (picked) { track('panchang_date', { city: P.slug, lang: P.lang }); }
      show();
    });
    show();
    track('panchang_view', { city: P.slug, lang: P.lang, state: byDate[todayKey()] ? 'in_range' : 'out_of_range' });
    // the page follows the city's clock: a new day is shown when it begins or when the page is looked at again
    var shownKey = todayKey();
    function tick() { if (!picked && todayKey() !== shownKey) { shownKey = todayKey(); show(); } }
    setInterval(tick, 30000);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) { tick(); } });
  }

  function failed() {
    $('panDate').textContent = '';
    $('panNote').textContent = L.loadFail;
    $('panNote').hidden = false;
  }

  function load() {
    fetch(P.data).then(function (res) {
      if (!res.ok) { throw new Error('status ' + res.status); }
      return res.json();
    }).then(function (data) {
      absorb(data);
      start();
    }).catch(function () { failed(); });
  }

  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', load); } else { load(); }
})();
