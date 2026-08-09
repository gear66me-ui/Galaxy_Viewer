const CACHE_NAME='galaxy-viewer-beta-7AI-global-glow-001';

const clearAllCaches=()=>caches.keys().then(keys=>Promise.all(keys.map(key=>caches.delete(key))));

self.addEventListener('install',event=>{
  event.waitUntil(clearAllCaches());
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil(clearAllCaches().then(()=>self.clients.claim()));
});

self.addEventListener('message',event=>{
  if(event.data==='SKIP_WAITING')self.skipWaiting();
  if(event.data==='CLEAR_BETA_CACHES')event.waitUntil(clearAllCaches());
});

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  event.respondWith(fetch(event.request,{cache:'no-store'}));
});
