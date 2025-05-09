const CACHE_NAME = 'tku-cache-v1';
const urlsToCache = [
  '/',
  '/static/icon-192.png',
  '/static/icon-512.png',
  '/static/manifest.json',
  // Add more paths if needed like CSS, JS, logo, etc.
];

// Install event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch event
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
