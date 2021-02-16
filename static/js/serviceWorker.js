const staticJOLRecipes = "JOL-recipes-site-v1";
const assets = [
    "/",
    "/list.html",
    "/recipe/bagels",
    "/recipe/ragu",
    "/recipe/pizza_dough",
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