const CACHE_NAME='galaxy-viewer-mobile-12ar64-beta-001';
const CACHE_PREFIX='galaxy-viewer-mobile-';
const APP_SHELL=[
  './',
  './index.html',
  './beta/',
  './beta/index.html',
  './beta/generic-app.html',
  '../viewer/gv-current-viewer.json?v=12AR-64'
];

self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(
        keys
          .filter(key=>key.startsWith(CACHE_PREFIX)&&key!==CACHE_NAME)
          .map(key=>caches.delete(key))
      ))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('message',event=>{
  if(event.data==='SKIP_WAITING')self.skipWaiting();
});

const cacheResponse=async(request,response)=>{
  if(response&&response.ok&&new URL(request.url).origin===self.location.origin){
    const cache=await caches.open(CACHE_NAME);
    await cache.put(request,response.clone());
  }
  return response;
};

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;

  const request=event.request;
  const url=new URL(request.url);
  const sameOrigin=url.origin===self.location.origin;
  const versioned=sameOrigin&&url.searchParams.get('v')==='6I-public-mobile-001';

  if(request.mode==='navigate'){
    event.respondWith(
      fetch(request)
        .then(response=>cacheResponse(request,response))
        .catch(()=>caches.match(request).then(cached=>cached||caches.match('./')))
    );
    return;
  }

  if(versioned){
    event.respondWith(
      caches.match(request).then(cached=>cached||fetch(request).then(response=>cacheResponse(request,response)))
    );
    return;
  }

  event.respondWith(
    fetch(request)
      .then(response=>cacheResponse(request,response))
      .catch(()=>caches.match(request))
  );
});