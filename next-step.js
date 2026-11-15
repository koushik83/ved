/*
 * The calm next step under a prashnavali answer: the next fast or festival in the reader's city, a link to that
 * city's panchang, and one related reading. Owner's rule: nothing here sells, nothing plays on worry.
 *
 * It never touches the tool's own code. It watches the answer element named in its data-watch attribute, adds its
 * own block just below the answer (or below the answer's buttons, #actions, where the page has them), shows it while
 * an answer is on screen and hides it when the answer is cleared. The fasts load only after the first answer, from
 * /panchang/data/next/<city>.json; the city is the one last opened on the panchang, else the first city listed in
 * the browser's time zone. Any failure leaves the block hidden or without the fasts line; the tool is unaffected.
 *
 * <script src="/next-step.js" defer data-watch="result" data-lang="en"
 *         data-read-href="/rudrashtakam-with-meaning" data-read-text="Rudrashtakam with meaning"></script>
 */
(function () {
  'use strict';
  var me = document.currentScript;
  if (!me || !window.MutationObserver) { return; }
  var cfg = {
    watch: me.getAttribute('data-watch') || 'result',
    lang: me.getAttribute('data-lang') === 'hi' ? 'hi' : 'en',
    readHref: me.getAttribute('data-read-href') || '',
    readText: me.getAttribute('data-read-text') || ''
  };
  var W = {
    en: { next: 'Next in {city}', today: "Today's panchang for {city}", yours: "Today's panchang for your city",
          other: 'Another city', panchang: '/panchang', now: 'Today' },
    hi: { next: '{city} में आगे', today: '{city} का आज का पंचांग', yours: 'आपके शहर का आज का पंचांग',
          other: 'दूसरा शहर', panchang: '/hi/panchang', now: 'आज' }
  }[cfg.lang];
  var block = null, filled = false, seen = false;
  var baseline = '';   // what the answer element says before any answer (some pages show an instruction there)

  function track(name, params) {
    try { if (typeof window.vedTrack === 'function') { window.vedTrack(name, params); } } catch (e) { /* never break the page */ }
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function text(el) { return el && el.textContent ? el.textContent.replace(/\s+/g, '') : ''; }
  function shown(el) {
    if (!el || el.hidden || !text(el) || text(el) === baseline) { return false; }
    return window.getComputedStyle(el).display !== 'none';
  }

  function build() {
    block = document.createElement('div');
    block.className = 'ved-next';
    block.hidden = true;
    var style = document.createElement('style');
    style.textContent = '.ved-next{margin:14px 0;padding:14px 16px;border:1px solid #F3D9B1;border-radius:12px;background:#FFFDF8;'
      + 'font-size:15px;line-height:1.6;color:#4E342E;text-align:left}.ved-next h3{margin:0 0 6px;font-size:16px;color:#A04000}'
      + '.ved-next a{color:#A04000}.ved-next p{margin:4px 0}.ved-next .x{color:#666}';
    document.head.appendChild(style);
    var read = cfg.readHref ? '<p><a href="' + esc(cfg.readHref) + '">' + esc(cfg.readText) + '</a></p>' : '';
    block.innerHTML = '<div class="ved-next-fasts"></div>'
      + '<p><a href="' + W.panchang + '" class="ved-next-city">' + esc(W.yours) + '</a></p>' + read;
    var answer = document.getElementById(cfg.watch);
    var after = document.getElementById('actions') || answer;
    after.insertAdjacentElement('afterend', block);
    block.addEventListener('click', function (ev) {
      var a = ev.target && ev.target.closest ? ev.target.closest('a') : null;
      if (a) { track('next_step_click', { to: a.getAttribute('href'), lang: cfg.lang }); }
    });
  }

  function cityLink(city) {
    var a = block.querySelector('.ved-next-city');
    a.href = W.panchang + '/' + city.slug;
    a.textContent = W.today.replace('{city}', city[cfg.lang]);
    a.insertAdjacentHTML('afterend', ' · <a href="' + W.panchang + '">' + esc(W.other) + '</a>');
  }

  function dateText(iso) {
    var p = iso.split('-');
    var d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2], 12));
    return new Intl.DateTimeFormat(cfg.lang === 'hi' ? 'hi-IN' : 'en-IN',
      { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' }).format(d);
  }

  function fill() {
    if (filled) { return; }
    filled = true;
    var slug = null;
    try { slug = localStorage.getItem('ved_panchang_city'); } catch (e) { /* storage blocked */ }
    var start = slug ? Promise.resolve(slug) : fetch('/panchang/data/next/zones.json').then(function (r) { return r.json(); })
      .then(function (z) { return z[Intl.DateTimeFormat().resolvedOptions().timeZone] || null; });
    start.then(function (s) {
      if (!s || !/^[a-z-]+$/.test(s)) { return null; }
      return fetch('/panchang/data/next/' + s + '.json').then(function (r) { return r.ok ? r.json() : null; });
    }).then(function (city) {
      if (!city) { return; }
      var today = new Intl.DateTimeFormat('en-CA', { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: city.tz }).format(new Date());
      var coming = city.items.filter(function (o) { return o.d >= today; }).slice(0, 2);
      cityLink(city);
      if (!coming.length) { return; }
      var html = '<h3>' + esc(W.next.replace('{city}', city[cfg.lang])) + '</h3>';
      coming.forEach(function (o) {
        var name = esc(o[cfg.lang]);
        if (o.p) { name = '<a href="' + W.panchang + '/' + o.p + '">' + name + '</a>'; }
        var moment = cfg.lang === 'hi' ? o.thi : o.ten;
        var when = o.d === today ? W.now : dateText(o.d);
        html += '<p><b>' + name + '</b> · ' + esc(when) + (moment ? ' <span class="x">· ' + esc(moment) + '</span>' : '') + '</p>';
      });
      block.querySelector('.ved-next-fasts').innerHTML = html;
    }).catch(function () { /* the block stays without the fasts line */ });
  }

  function update() {
    try {
      var answer = document.getElementById(cfg.watch);
      if (!answer) { return; }
      if (!block) { build(); }
      var on = shown(answer);
      block.hidden = !on;
      if (on) {
        fill();
        if (!seen) { seen = true; track('next_step_view', { lang: cfg.lang }); }
      }
    } catch (e) { /* never break the page */ }
  }

  function start() {
    var answer = document.getElementById(cfg.watch);
    if (!answer) { return; }
    baseline = text(answer);
    var mo = new MutationObserver(function () { window.setTimeout(update, 0); });
    mo.observe(answer, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'hidden', 'class'] });
    update();
  }

  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', start); } else { start(); }
})();
