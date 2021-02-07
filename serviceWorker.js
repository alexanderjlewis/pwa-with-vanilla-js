const staticDevRecipes = "dev-recipes-site-v1";
const assets = [
  "/",
  "/index.html",
  "/bagels.html",
  "/ragu.html",
  "/js/app.js",
  "/css/bootstrap.min.css",
  "/js/bootstrap.bundle.min.js",
  "/js/gitgraph.umd.js",
];

self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticDevRecipes).then(cache => {
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
