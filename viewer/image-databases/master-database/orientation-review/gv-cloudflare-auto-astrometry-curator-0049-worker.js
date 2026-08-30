import base0048 from './gv-cloudflare-auto-astrometry-curator-0048-worker.js';

const FULL_FRAME_STYLE=String.raw`<style id="gv49-left-full-frame">
.viewbox:has(#published){aspect-ratio:auto!important;height:auto!important;max-height:none!important;overflow:visible!important}
#published{display:block!important;width:100%!important;height:auto!important;max-width:100%!important;max-height:none!important;object-fit:contain!important;object-position:center center!important}
</style>`;

function injectHead(html,addition){
  const i=html.indexOf('</head>');
  return i<0?null:html.slice(0,i)+addition+html.slice(i);
}

export default {
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname!=='/'&&url.pathname!=='/index.html')return base0048.fetch(request,env);
    const response=await base0048.fetch(request,env);
    const type=(response.headers.get('content-type')||'').toLowerCase();
    if(!response.ok||!type.includes('text/html'))return response;
    const html=await response.text();
    const patched=injectHead(html,FULL_FRAME_STYLE);
    if(!patched)return new Response('0049 STARTUP ERROR: head missing',{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
    return new Response(patched,{status:response.status,headers:response.headers});
  }
};
