import base0051 from './gv-cloudflare-auto-astrometry-curator-0051-worker.js';

const REV='0052';
const BROKEN_MARKER='window.__gv46GaiaSolverBound=true;';

function stripSingleScriptContaining(html,needle){
  let pos=0,found=[];
  while(true){
    const s=html.indexOf('<script',pos);
    if(s<0)break;
    const open=html.indexOf('>',s),e=html.indexOf('</script>',open);
    if(open<0||e<0)break;
    const code=html.slice(open+1,e);
    if(code.includes(needle))found.push({s,e:e+9});
    pos=e+9;
  }
  if(found.length!==1)return{ok:false,count:found.length,html};
  const x=found[0];
  return{ok:true,count:1,html:html.slice(0,x.s)+html.slice(x.e)};
}

export default {
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname!=='/'&&url.pathname!=='/index.html')return base0051.fetch(request,env);
    const response=await base0051.fetch(request,env);
    const type=(response.headers.get('content-type')||'').toLowerCase();
    if(!response.ok||!type.includes('text/html'))return response;
    const html=await response.text();
    const stripped=stripSingleScriptContaining(html,BROKEN_MARKER);
    if(!stripped.ok)return new Response('0052 STARTUP ERROR: broken Gaia script marker count '+stripped.count,{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
    const headers=new Headers(response.headers);
    headers.set('content-type','text/html; charset=utf-8');
    headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
    headers.set('x-gv-revision',REV);
    headers.set('x-gv-startup-isolation','removed-single-broken-0046-gaia-script');
    return new Response(stripped.html,{status:response.status,headers});
  }
};
