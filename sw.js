const cacheName = "DoFScouting";
const precacheResources = [
    "/DoF-Scouting/",
    "/DoF-Scouting/index.html",
    "/DoF-Scouting/qrcode.min.js",
    "/DoF-Scouting/bootstrap.min.css",
    "/DoF-Scouting/bootstrap.min.css.map",
    "/DoF-Scouting/jquery-3.6.1.min.js"
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(cacheName);
    await cache.addAll(precacheResources);
  })());
});

self.addEventListener('fetch', (event) => {
  event.respondWith((async () => {
    // try the cache first
    const r = await caches.match(event.request);
    if (r) { return r; }

    // cache the new resource and return it
    const response = await fetch(event.request);
    const cache = await caches.open(cacheName);

    cache.put(event.request, response.clone());
    return response;
  })());
});
