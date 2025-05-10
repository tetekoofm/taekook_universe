const CACHE_NAME = 'tku-cache-v1';
const urlsToCache = [
  '/', 
  '/static/favicon.png',
  '/static/manifest.json',
  '/static/style.css', // Add CSS or any other critical assets here
];

// Install event
self.addEventListener('install', (event) => {
  console.log('Service Worker Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Caching critical assets');
      return cache.addAll(urlsToCache); // Cache the files listed in `urlsToCache`
    })
  );
});

// Fetch event
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Return the cached response if available
      if (cachedResponse) {
        return cachedResponse;
      }

      // Otherwise, fetch the request from the network and cache the response
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, networkResponse.clone()); // Cache the new response
          });
        }
        return networkResponse;
      });
    })
  );
});

// Activate event: Clean up old caches
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME]; // Use the current cache version to clear old caches
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            console.log(`Deleting old cache: ${cacheName}`);
            return caches.delete(cacheName); // Delete caches not in the whitelist
          }
        })
      );
    })
  );
});

// Push notification handler (optional)
self.addEventListener('push', (event) => {
  const options = {
    body: event.data.text(),
    icon: '/static/favicon.png',
    badge: '/static/favicon.png',
  };

  event.waitUntil(
    self.registration.showNotification('New Notification!', options)
  );
});
