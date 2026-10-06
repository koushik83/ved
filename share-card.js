/*
 * Share an answer as an image. Draws a card with the verse and the answer on a faint picture of the deity,
 * then hands it to the phone's share sheet (WhatsApp and the rest). Where that is not possible, the page
 * falls back to its usual text link. Nothing is uploaded anywhere: the image is made on the device.
 */
(function () {
  'use strict';
  var W = 1080, H = 1080;
  var DEV = "'Noto Sans Devanagari', 'Nirmala UI', 'Devanagari Sangam MN', 'Mangal', Arial, sans-serif";
  var cache = {};

  function loadImage(src) {
    if (!src) { return Promise.resolve(null); }
    if (cache[src]) { return cache[src]; }
    cache[src] = new Promise(function (resolve) {
      var img = new Image();
      img.onload = function () { resolve(img); };
      img.onerror = function () { resolve(null); };
      img.src = src;
    });
    return cache[src];
  }

  function wrap(ctx, text, maxWidth) {
    var words = String(text || '').split(/\s+/), lines = [], line = '';
    for (var i = 0; i < words.length; i++) {
      var test = line ? line + ' ' + words[i] : words[i];
      if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = words[i]; } else { line = test; }
    }
    if (line) { lines.push(line); }
    return lines;
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }

  // opts: title, verse, meaning, result, tone (good | caution | wait), image, url, text
  function render(opts) {
    return loadImage(opts.image).then(function (img) {
      var c = document.createElement('canvas'); c.width = W; c.height = H;
      var ctx = c.getContext('2d');
      ctx.fillStyle = '#FDF4E7'; ctx.fillRect(0, 0, W, H);
      if (img) {
        ctx.globalAlpha = 0.13;
        var s = Math.min(W / img.width, H / img.height) * 0.8, iw = img.width * s, ih = img.height * s;
        ctx.drawImage(img, (W - iw) / 2, (H - ih) / 2, iw, ih);
        ctx.globalAlpha = 1;
      }
      ctx.textAlign = 'center'; ctx.textBaseline = 'top';
      ctx.fillStyle = '#D35400'; ctx.font = 'bold 44px ' + DEV; ctx.fillText(opts.title, W / 2, 56);

      var y = 150, i;
      ctx.font = 'bold 54px ' + DEV;
      var vl = wrap(ctx, opts.verse, 900).slice(0, 4), vh = vl.length * 74 + 50;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.92)'; roundRect(ctx, 60, y, 960, vh, 24); ctx.fill();
      ctx.strokeStyle = '#ff9933'; ctx.lineWidth = 4; ctx.stroke();
      ctx.fillStyle = '#5D2E00';
      for (i = 0; i < vl.length; i++) { ctx.fillText(vl[i], W / 2, y + 28 + i * 74); }
      y += vh + 34;

      if (opts.meaning) {
        ctx.font = '32px ' + DEV; ctx.fillStyle = '#555';
        var ml = wrap(ctx, opts.meaning, 900).slice(0, 4);
        for (i = 0; i < ml.length; i++) { ctx.fillText(ml[i], W / 2, y + i * 42); }
        y += ml.length * 42 + 30;
      }

      ctx.font = 'bold 40px ' + DEV;
      var rl = wrap(ctx, opts.result, 880).slice(0, 6), rh = rl.length * 54 + 50;
      var colors = { good: ['#E8F5E9', '#4CAF50', '#2E7D32'], caution: ['#FFF3EF', '#FF5733', '#D32F2F'], wait: ['#FFF8E1', '#FB8C00', '#E65100'] }[opts.tone] || ['#FFFFFF', '#A04000', '#A04000'];
      ctx.fillStyle = colors[0]; roundRect(ctx, 60, y, 960, rh, 24); ctx.fill();
      ctx.strokeStyle = colors[1]; ctx.lineWidth = 4; ctx.stroke();
      ctx.fillStyle = colors[2];
      for (i = 0; i < rl.length; i++) { ctx.fillText(rl[i], W / 2, y + 26 + i * 54); }

      ctx.fillStyle = '#A04000'; ctx.font = 'bold 34px Arial, sans-serif';
      ctx.fillText(String(opts.url || '').replace(/^https?:\/\//, ''), W / 2, H - 80);
      return c;
    });
  }

  function toBlob(c) { return new Promise(function (resolve) { c.toBlob(resolve, 'image/jpeg', 0.88); }); }

  // Resolves to true when the image reached the share sheet (or the person closed it), false when the page should share text instead
  function share(opts) {
    if (!navigator.share || !navigator.canShare || typeof File === 'undefined') { return Promise.resolve(false); }
    return render(opts).then(toBlob).then(function (blob) {
      if (!blob) { return false; }
      var file = new File([blob], 'prashnavali-answer.jpg', { type: 'image/jpeg' });
      if (!navigator.canShare({ files: [file] })) { return false; }
      return navigator.share({ files: [file], text: opts.text, url: opts.url })
        .then(function () { return true; }, function (err) { return !!(err && err.name === 'AbortError'); });
    }).catch(function () { return false; });
  }

  window.vedShareCard = share;
  window.vedShareCard.render = render;
  window.vedShareCard.preload = loadImage;
})();
