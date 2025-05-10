const CACHE_NAME = 'tku-cache-v1';
const urlsToCache = [
  '/',
  '/static/favicon.png',
  '/static/manifest.json',
  // Add more paths if needed like CSS, JS, logo, etc.
];

// Install event
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('v1').then((cache) => {
      return cache.addAll([
        '/static/favicon.png',
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

self.addEventListener('activate', (event) => {
  const cacheWhitelist = ['tku-cache-v1']; // Update this version if the cache changes

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('push', (event) => {
  const options = {
    body: event.data.text(),
    icon: '/static/favicon.png',
    badge: '/static/favicon.png'
  };

  event.waitUntil(
    self.registration.showNotification('New Notification!', options)
  );
});