/*
 * Bottom anchor ad for Ved Prashnavali (AdSense, manual sticky footer).
 *
 * Phones and tablets only: below 1024px one bar fixed to the bottom of the
 * screen holding the "Manual_Bottom_Unit" slot (desktops get the vertical side
 * units from side-ads.js instead). The unit is sized the way Google documents
 * for responsive slots with CSS: 320x50 on phones, 468x60 from 500px, 728x90
 * from 800px, so the bar never grows into a tall rectangle. The page gets
 * matching bottom padding, so the bar
 * never covers content or the footer links. A small tab above the bar closes it
 * for the rest of the session. If the ad comes back unfilled, or adsbygoogle.js
 * never loads (offline, blocked, or a domain AdSense does not serve), the bar
 * is removed so there is never an empty white strip. Hidden when printing.
 *
 * Included with <script src="/anchor-ad.js" defer></script> right after the
 * adsbygoogle.js tag on the pages that carry ads.
 */
(function () {
  'use strict';

  var CLIENT = 'ca-pub-4804498427753837';
  var SLOT = '9617291058';
  var CLOSED_KEY = 'ved_anchor_closed';
  var DESKTOP_MIN = 1024;      // from this width up the page carries the side units instead (side-ads.js)
  var FIRST_CHECK_MS = 6000;
  var SECOND_CHECK_MS = 12000;

  if (document.documentElement.clientWidth >= DESKTOP_MIN) { return; }
  try { if (sessionStorage.getItem(CLOSED_KEY)) { return; } } catch (e) { /* storage blocked: show */ }

  var page = location.pathname.replace(/\.html$/, '') || '/';

  function track(name) {
    try {
      if (typeof window.vedTrack === 'function') { window.vedTrack(name, { page: page }); }
    } catch (e) { /* tracking must never break the page */ }
  }

  var bar = null;

  function remove() {
    if (bar && bar.parentNode) { bar.parentNode.removeChild(bar); }
    bar = null;
    if (document.body) { document.body.classList.remove('ved-anchor-open'); }
  }

  function close() {
    remove();
    try { sessionStorage.setItem(CLOSED_KEY, '1'); } catch (e) { /* ignore */ }
    track('ad_anchor_closed');
  }

  function mount() {
    if (!document.body || document.getElementById('ved-anchor')) { return; }

    var style = document.createElement('style');
    style.textContent = [
      '#ved-anchor{position:fixed;bottom:0;left:0;right:0;z-index:9000;background:#fff;',
      'box-shadow:0 -2px 6px rgba(0,0,0,.12);text-align:center;line-height:0;',
      'padding-bottom:env(safe-area-inset-bottom)}',
      '#ved-anchor .ved-anchor-unit{display:inline-block;vertical-align:top;width:320px;height:50px}',
      '#ved-anchor-close{position:absolute;top:-22px;right:8px;width:34px;height:22px;border:0;',
      'border-radius:6px 6px 0 0;background:#fff;color:#555;font:16px/22px Arial,sans-serif;',
      'box-shadow:0 -2px 6px rgba(0,0,0,.12);cursor:pointer;padding:0;margin:0}',
      'body.ved-anchor-open{padding-bottom:calc(50px + env(safe-area-inset-bottom))}',
      '@media(min-width:500px){#ved-anchor .ved-anchor-unit{width:468px;height:60px}',
      'body.ved-anchor-open{padding-bottom:calc(60px + env(safe-area-inset-bottom))}}',
      '@media(min-width:800px){#ved-anchor .ved-anchor-unit{width:728px;height:90px}',
      'body.ved-anchor-open{padding-bottom:calc(90px + env(safe-area-inset-bottom))}}',
      '@media print{#ved-anchor{display:none}body.ved-anchor-open{padding-bottom:0}}'
    ].join('');
    document.head.appendChild(style);

    bar = document.createElement('div');
    bar.id = 'ved-anchor';
    bar.setAttribute('role', 'complementary');
    bar.setAttribute('aria-label', 'Advertisement');

    var closeBtn = document.createElement('button');
    closeBtn.id = 'ved-anchor-close';
    closeBtn.type = 'button';
    closeBtn.setAttribute('aria-label', 'Close advertisement');
    closeBtn.textContent = '✕';
    closeBtn.addEventListener('click', close);
    bar.appendChild(closeBtn);

    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle ved-anchor-unit';
    ins.style.display = 'inline-block';
    ins.setAttribute('data-ad-client', CLIENT);
    ins.setAttribute('data-ad-slot', SLOT);
    bar.appendChild(ins);

    document.body.appendChild(bar);
    document.body.classList.add('ved-anchor-open');

    // AdSense writes data-ad-status="filled" or "unfilled" once it has answered
    var status = function () { return ins.getAttribute('data-ad-status'); };
    if (typeof MutationObserver === 'function') {
      var observer = new MutationObserver(function () {
        if (status() === 'unfilled') { observer.disconnect(); remove(); }
        else if (status() === 'filled') { observer.disconnect(); }
      });
      observer.observe(ins, { attributes: true, attributeFilter: ['data-ad-status'] });
    }

    // No answer at all: the script never loaded (offline, blocked) or is slow
    var scriptLoaded = function () { return !!(window.adsbygoogle && window.adsbygoogle.loaded); };
    setTimeout(function () {
      if (!bar) { return; }
      if (status() === 'unfilled') { remove(); return; }
      if (status() === 'filled') { return; }
      if (!scriptLoaded()) { remove(); return; }
      setTimeout(function () {
        if (bar && status() !== 'filled') { remove(); }
      }, SECOND_CHECK_MS - FIRST_CHECK_MS);
    }, FIRST_CHECK_MS);

    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
      remove();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
