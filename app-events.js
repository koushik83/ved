/*
 * Usage tracking for Ved Prashnavali. Events go to Google Analytics (GA4) through the gtag snippet on each page.
 * It records which tool was used and which answer number was shown. It never records the visitor's question.
 *
 * Events: answer_revealed, new_question, share, install_prompt_shown, install_click, install_accepted,
 * install_dismissed, app_installed, app_launch. The Today page adds daily_view and daily_draw.
 */
(function () {
  'use strict';

  function track(name, params) {
    try {
      if (typeof window.gtag === 'function') { window.gtag('event', name, params || {}); }
    } catch (e) { /* tracking must never break the page */ }
  }
  window.vedTrack = track;

  function oncePerSession(key, fn) {
    try {
      if (sessionStorage.getItem(key)) { return; }
      sessionStorage.setItem(key, '1');
    } catch (e) { /* storage blocked: still count it */ }
    fn();
  }

  // Run our hook first, then the page's own function of the same name
  function wrap(name, before) {
    var original = window[name];
    if (typeof original !== 'function') { return; }
    window[name] = function () {
      try { before.apply(this, arguments); } catch (e) { /* ignore */ }
      return original.apply(this, arguments);
    };
  }

  var path = location.pathname.replace(/\.html$/, '') || '/';
  var TOOLS = { '/prash': 'ram', '/hanumanprash': 'hanuman', '/saibabaprash': 'sai' };
  var tool = TOOLS[path] || null;

  // Installed app (opened from the home screen) or an ordinary browser tab
  var standalone = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
    window.navigator.standalone === true;
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('set', 'user_properties', { app_mode: standalone ? 'installed_app' : 'browser' });
    }
  } catch (e) { /* ignore */ }
  if (standalone) {
    oncePerSession('ved_app_launch', function () { track('app_launch', { page: path }); });
  }

  // Install funnel: offer shown, button pressed, accepted or dismissed, installed
  window.addEventListener('beforeinstallprompt', function (event) {
    oncePerSession('ved_install_prompt', function () { track('install_prompt_shown', { page: path }); });
    if (event.userChoice && typeof event.userChoice.then === 'function') {
      event.userChoice.then(function (choice) {
        track(choice && choice.outcome === 'accepted' ? 'install_accepted' : 'install_dismissed', { page: path });
      });
    }
  });
  window.addEventListener('appinstalled', function () { track('app_installed', { page: path }); });

  document.addEventListener('click', function (event) {
    var target = event.target;
    if (!target || !target.closest) { return; }

    var button = target.closest('button');
    if (button && button.textContent.trim() === 'Install App') { track('install_click', { page: path }); }

    // Ram Shalaka: the cell number decides which of the nine chaupais is shown
    var cell = target.closest('.grid-item');
    if (cell && tool === 'ram') {
      var cellNumber = parseInt(String(cell.getAttribute('data-answer') || '').replace(/[^0-9]/g, ''), 10);
      if (cellNumber) { track('answer_revealed', { tool: 'ram', answer_id: String(((cellNumber - 1) % 9) + 1) }); }
    }

    if (target.closest('#newQuestion')) { track('new_question', { tool: tool || 'unknown' }); }
  }, true);

  if (tool === 'hanuman') {
    wrap('displayMessage', function (number) { track('answer_revealed', { tool: 'hanuman', answer_id: String(number) }); });
    wrap('askNewQuestion', function () { track('new_question', { tool: 'hanuman' }); });
  }

  if (tool === 'sai') {
    wrap('getAnswer', function () {
      var input = document.getElementById('numberInput');
      var number = input ? parseInt(input.value, 10) : NaN;
      if (number >= 1 && number <= 720) { track('answer_revealed', { tool: 'sai', answer_id: String(number) }); }
    });
  }

  if (tool) {
    wrap('shareResult', function (platform) { track('share', { method: String(platform), content_type: tool }); });
  }
})();
