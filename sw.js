// Service Worker with proper fetch handling and safety checks
const CACHE_NAME = 'static-v1';
const HTML_EXT_REGEX = /\/(saibabaprash|hanumanprash|prash)\.html$/;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll([
        '/',
        '/saibabaprash',
        '/hanumanprash',
        '/prash'
      ]);
    })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
  console.log("Service Worker Activated");
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  
  // Only handle same-origin navigation requests
  if (url.origin === self.location.origin && 
      event.request.mode === 'navigate') {
    
    const cleanPath = url.pathname.replace(HTML_EXT_REGEX, '/$1');
    
    if (cleanPath !== url.pathname) {
      const newUrl = new URL(cleanPath, self.location.origin);
      return event.respondWith(
        Response.redirect(newUrl, 301) // Permanent redirect
      );
    }
  }
  
  // Network-first strategy with cache fallback
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});