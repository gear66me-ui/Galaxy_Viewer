import base0053 from './gv-cloudflare-auto-astrometry-curator-0053-worker.js';

const REV='0054';
const BROKEN="validated_by:'human-live-aladin-0026'}catch{}";
const FIXED="validated_by:'human-live-aladin-0026'}}catch{}";

function replaceExactlyOnce(html,before,after){
  let count=0,pos=0;
  while(true){
    const i=html.indexOf(before,pos);
    if(i<0)break;
    count++;
    pos=i+before.length;
  }
  if(count!==1)return{ok:false,count,html};
  return{ok:true,count:1,html:html.replace(before,after)};
}

export default {
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname!=='/'&&url.pathname!=='/index.html')return base0053.fetch(request,env);
    const response=await base0053.fetch(request,env);
    const type=(response.headers.get('content-type')||'').toLowerCase();
    if(!response.ok||!type.includes('text/html'))return response;
    const html=await response.text();
    const patched=replaceExactlyOnce(html,BROKEN,FIXED);
    if(!patched.ok)return new Response('0054 STARTUP ERROR: malformed 0026 try/catch boundary count '+patched.count,{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
    const headers=new Headers(response.headers);
    headers.set('content-type','text/html; charset=utf-8');
    headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
    headers.set('x-gv-revision',REV);
    headers.set('x-gv-startup-catch-fix','0026-try-block-brace-restored');
    return new Response(patched.html,{status:response.status,headers});
  }
};
