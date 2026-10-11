/*
 * Desktop side ads for Ved Prashnavali (AdSense, vertical units, not sticky).
 *
 * Desktops only, 1024px and wider (phones and tablets get the bottom anchor
 * from anchor-ad.js instead). The content column leaves empty margins on both
 * sides. This script measures those margins at load and, on each side where a unit fits
 * with 12px clear of the content and of the screen edge, places one vertical
 * "Desktop_Sidebar_Manual" unit level with the top of the content: 300x600
 * when the margin allows, otherwise 160x600, otherwise 120x600, otherwise
 * nothing. The units are
 * part of the page, not pinned: they scroll away with the content. They never
 * cover content, never appear on phones, tablets or scaled laptops, and are
 * removed when the ad comes back unfilled, when adsbygoogle.js never loads, or
 * when a resize closes the gap. Hidden when printing.
 *
 * Included with <script src="/side-ads.js" defer></script> after anchor-ad.js
 * on the pages that carry ads.
 */
(function () {
  'use strict';

  var CLIENT = 'ca-pub-4804498427753837';
  var SLOT = '4472775589';
  var SIZES = [[300, 600], [160, 600], [120, 600]];   // 120x600 fits a 1536px laptop at 125% scaling (1229px viewport)
  var CLEARANCE = 12;          // px between a unit and the content, and the screen edge
  var MIN_VIEWPORT = 1024;     // narrower screens get the bottom anchor (anchor-ad.js), never side units
  var MIN_TOP = 80;            // px from the top of the page, clear of the Install App button
  var FIRST_CHECK_MS = 6000;
  var SECOND_CHECK_MS = 12000;

  var mounted = {};            // side -> { box, ins, width }

  function viewport() {
    var d = document.documentElement;
    return { w: d.clientWidth, h: d.clientHeight };
  }

  // The content column: the leftmost and rightmost edges, and the top, of the
  // centred blocks on the page. Full-width wrappers (header, footer, body-wide
  // divs) are skipped, as are small widgets and anything fixed or absolute.
  function contentEdges() {
    var vp = viewport();
    var left = vp.w, right = 0, top = Infinity;
    var all = document.body.querySelectorAll('*');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      var tag = el.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'INS' || tag === 'LINK' || tag === 'META') { continue; }
      if (el.closest('#ved-anchor') || el.closest('.ved-side')) { continue; }
      var r = el.getBoundingClientRect();
      if (r.width < 240 || r.width > vp.w * 0.9 || r.height < 40) { continue; }
      var pos = getComputedStyle(el).position;
      if (pos === 'fixed' || pos === 'absolute') { continue; }
      if (r.left < left) { left = r.left; }
      if (r.right > right) { right = r.right; }
      if (r.top < top) { top = r.top; }
    }
    if (right <= left) { return null; }
    return { left: left, right: right, top: top + (window.pageYOffset || 0) };
  }

  function fit(gap) {
    for (var i = 0; i < SIZES.length; i++) {
      if (gap >= SIZES[i][0] + 2 * CLEARANCE) { return SIZES[i]; }
    }
    return null;
  }

  function gaps() {
    var vp = viewport();
    if (vp.w < MIN_VIEWPORT) { return null; }
    var edges = contentEdges();
    if (!edges) { return null; }
    return { left: edges.left, right: vp.w - edges.right, top: edges.top };
  }

  function offset(gap, width) {
    return Math.round((gap - width) / 2) + 'px';
  }

  function remove(side) {
    var m = mounted[side];
    if (!m) { return; }
    if (m.box.parentNode) { m.box.parentNode.removeChild(m.box); }
    delete mounted[side];
  }

  function watch(side, ins) {
    var status = function () { return ins.getAttribute('data-ad-status'); };
    if (typeof MutationObserver === 'function') {
      var observer = new MutationObserver(function () {
        if (status() === 'unfilled') { observer.disconnect(); remove(side); }
        else if (status() === 'filled') { observer.disconnect(); }
      });
      observer.observe(ins, { attributes: true, attributeFilter: ['data-ad-status'] });
    }
    var scriptLoaded = function () { return !!(window.adsbygoogle && window.adsbygoogle.loaded); };
    setTimeout(function () {
      if (!mounted[side]) { return; }
      if (status() === 'unfilled') { remove(side); return; }
      if (status() === 'filled') { return; }
      if (!scriptLoaded()) { remove(side); return; }
      setTimeout(function () {
        if (mounted[side] && status() !== 'filled') { remove(side); }
      }, SECOND_CHECK_MS - FIRST_CHECK_MS);
    }, FIRST_CHECK_MS);
  }

  function mount(side, size, gap, top) {
    var box = document.createElement('div');
    box.className = 'ved-side ved-side-' + side;
    box.setAttribute('role', 'complementary');
    box.setAttribute('aria-label', 'Advertisement');
    box.style.cssText = 'position:absolute;top:' + top + 'px;' + side + ':' + offset(gap, size[0]) +
      ';width:' + size[0] + 'px;height:' + size[1] + 'px;z-index:1;line-height:0';

    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.cssText = 'display:inline-block;width:' + size[0] + 'px;height:' + size[1] + 'px';
    ins.setAttribute('data-ad-client', CLIENT);
    ins.setAttribute('data-ad-slot', SLOT);
    box.appendChild(ins);

    document.body.appendChild(box);
    mounted[side] = { box: box, ins: ins, width: size[0] };
    watch(side, ins);
    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
      remove(side);
    }
  }

  function start() {
    if (!document.body) { return; }
    var g = gaps();
    if (!g) { return; }
    var top = Math.max(MIN_TOP, Math.round(g.top));
    var tall = SIZES[0][1];
    if (document.body.scrollHeight < top + tall + CLEARANCE) { return; }   // page too short to hold a unit

    var style = document.createElement('style');
    style.textContent = '@media print{.ved-side{display:none}}';
    document.head.appendChild(style);

    var sides = ['left', 'right'];
    for (var i = 0; i < sides.length; i++) {
      var size = fit(g[sides[i]]);
      if (size) { mount(sides[i], size, g[sides[i]], top); }
    }
  }

  // On resize a unit is re-centred in its margin, or taken away if the margin
  // no longer holds it; it never comes back on the same page load, so no
  // second ad request is made.
  var timer = null;
  window.addEventListener('resize', function () {
    if (timer) { clearTimeout(timer); }
    timer = setTimeout(function () {
      var any = false;
      for (var s in mounted) { if (mounted.hasOwnProperty(s)) { any = true; } }
      if (!any) { return; }
      var g = gaps();
      for (var side in mounted) {
        if (!mounted.hasOwnProperty(side)) { continue; }
        var m = mounted[side];
        if (!g || g[side] < m.width + 2 * CLEARANCE) { remove(side); }
        else { m.box.style[side] = offset(g[side], m.width); }
      }
    }, 300);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
