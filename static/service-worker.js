const CACHE_NAME = 'tku-cache-v1';
const urlsToCache = [
  '/',
  '/static/icon_small.png',
  '/static/icon_big.png',
  '/static/manifest.json',
  // Add more paths if needed like CSS, JS, logo, etc.
];

// Install event
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('v1').then((cache) => {
      return cache.addAll([
        '/static/icons/icon_small.png',
        '/static/style.css'
        // Add other critical assets
      ]);
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
