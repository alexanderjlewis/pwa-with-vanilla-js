var cacheVersion = new Date().getTime();
var staticCacheName = "JOL-recipe-" + cacheVersion

var filesToCache = [
    '/',
    '/offline',
    '/static/images/favicon.ico',
    '/static/images/icons/72.png',
    '/static/images/icons/100.png',
    '/static/images/icons/128.png',
    '/static/images/icons/144.png',
    '/static/images/icons/152.png',
    '/static/images/icons/196.png',
    '/static/images/icons/256.png',
    '/static/images/icons/512.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
        .then(cache => {
            return cache.addAll(filesToCache);
        })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                .filter(cacheName => (cacheName.startsWith("JOL-recipe-")))
                .filter(cacheName => (cacheName !== staticCacheName))
                .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from cache, and return offline page if client is offline 
this.addEventListener('fetch', event => {
    if (event.request.mode === 'navigate' || (event.request.method === 'GET' && event.request.headers.get('accept').includes('text/html'))) {
        event.respondWith(
            fetch(event.request.url).catch(error => {
                return caches.match('/offline');
            })
        );
    } else {
        event.respondWith(caches.match(event.request)
            .then(function(response) {
                return response || fetch(event.request);
            })
        );
    }
});