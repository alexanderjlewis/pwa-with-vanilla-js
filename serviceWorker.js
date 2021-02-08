const staticJOLRecipes = "JOL-recipes-site-v1";
const assets = [
    "/",
    "/index.html",
    "/list.html",
    "/bagels.html",
    "/ragu.html",
    "/js/app.js",
    "/css/bootstrap.min.css",
    "/custom.min.css",
    "/js/bootstrap.min.js",
    "/js/gitgraph.umd.js",
    "/js/jquery-3.5.1.slim.min.js"
];

self.addEventListener("install", installEvent => {
    installEvent.waitUntil(
        caches.open(staticJOLRecipes).then(cache => {
            cache.addAll(assets);
        })
    );
});

self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
        caches.match(fetchEvent.request).then(res => {
            return res || fetch(fetchEvent.request);
        })
    );
});