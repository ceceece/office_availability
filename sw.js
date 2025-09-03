// sw.js
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installed');
});

self.addEventListener('fetch', (event) => {
  // You can add custom caching logic here
});
