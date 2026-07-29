const CACHE_NAME='galaxy-viewer-beta-5K-control-border-001';
const APP_SHELL=[
  './',
  './index.html',
  './manifest.webmanifest?v=5K-control-border-001',
  '../../viewer/artwork/icon_target_vector.svg?v=5K-control-border-001',
  '../../viewer/artwork/icon_transparent.png?v=5K-control-border-001',
  '../../viewer/artwork/GV-splash-0003.svg?v=5K-control-border-001',
  '../../viewer/artwork/GV-reticle-0001.svg?v=5K-control-border-001',
  '../../viewer/GV-beta-0005K.py?v=5K-control-border-001',
  '../../discovery/beautiful-galaxy-catalog-beta.json?v=5K-control-border-001',
  '../../discovery/galaxy-catalog-beta.json?v=5K-control-border-001'
];

self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(key=>key!==CACHE_NAME).map(key=>caches.delete(key))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('message',event=>{
  if(event.data==='SKIP_WAITING')self.skipWaiting();
});

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  event.respondWith(
    fetch(event.request)
      .then(response=>{
        if(response&&response.ok){
          const copy=response.clone();
          event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.put(event.request,copy)));
        }
        return response;
      })
      .catch(()=>caches.match(event.request).then(cached=>cached||caches.match('./')))
  );
});