/*
GALAXY VIEWER MOBILE 0021 — INSTALLED-APP CACHE REFRESH
Date: 2026-07-28

Reason for maintenance change:
The installed Galaxy Viewer application could continue opening an older cached launcher.
The visible Galaxy Viewer release remains Mobile 0021. The maintenance suffix below exists
only to force Chrome to install a fresh application cache without renumbering the release.

Previous cache declaration retained for traceability:
const CACHE_NAME = 'galaxy-viewer-mobile-0021-refresh-2';

Replacement behavior:
- create a fresh Mobile 0021 maintenance cache;
- activate the new worker immediately;
- remove every older Galaxy Viewer cache;
- claim open Galaxy Viewer clients;
- use the network first and retain the cache only as an offline fallback.
*/
const CACHE_NAME = 'galaxy-viewer-mobile-0021-refresh-3';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  '../viewer/artwork/icon.svg',
  '../viewer/artwork/GV-splash-0003.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response && response.ok) {
          const copy = response.clone();
          event.waitUntil(
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy))
          );
        }
        return response;
      })
      .catch(() =>
        caches.match(event.request).then(cached => cached || caches.match('./'))
      )
  );
});