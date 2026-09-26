from IPython.display import HTML, Javascript, display

# Galaxy Viewer 12M analytics fast-start bootstrap.
# 12L remains frozen. 12M preloads the two resources that gate the first
# Aladin canvas (frozen 12F source + Aladin Lite) before mounting 12L.

display(HTML("""
<style>
#gv-12m-bootstrap{position:fixed;inset:0;z-index:1;background:#000;pointer-events:none}
</style>
<div id="gv-12m-bootstrap" aria-hidden="true"></div>
"""))

display(Javascript(r"""
(async()=>{
  'use strict';
  const audit=(type,detail={})=>{try{window.__GV_ANALYTICS_AUDIT__?.emit?.(type,detail)}catch(_){}};
  const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
  const BASE12F='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/archive/GV-beta-0012F.py';
  const VIEWER12L='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/GV-beta-0012L.py';
  const fetchText=async(url,label)=>{
    const started=performance.now();audit(label+'_FETCH_START',{url});
    const response=await fetch(url+(url.includes('?')?'&':'?')+'gv12m='+Date.now(),{cache:'no-store'});
    audit(label+'_FETCH_END',{url,status:response.status,ok:response.ok,durationMs:Math.round(performance.now()-started)});
    if(!response.ok)throw new Error(`${label} HTTP ${response.status}: ${url}`);
    return response.text();
  };
  const loadAladin=async()=>{
    const started=performance.now();
    if(window.A?.init){audit('12M_ALADIN_ALREADY_PRESENT');await window.A.init;audit('12M_ALADIN_READY',{durationMs:Math.round(performance.now()-started)});return}
    audit('12M_ALADIN_PRELOAD_START',{url:ALADIN_URL});
    await new Promise((resolve,reject)=>{
      const existing=[...document.scripts].find(s=>s.src===ALADIN_URL);
      if(existing){
        if(window.A?.init){resolve();return}
        existing.addEventListener('load',resolve,{once:true});
        existing.addEventListener('error',()=>reject(new Error('12M ALADIN PRELOAD FAILED')),{once:true});
        return;
      }
      const script=document.createElement('script');script.src=ALADIN_URL;script.charset='utf-8';script.dataset.gv12mAladin='true';
      script.addEventListener('load',resolve,{once:true});script.addEventListener('error',()=>reject(new Error('12M ALADIN PRELOAD FAILED')),{once:true});
      document.head.appendChild(script);
    });
    if(!window.A?.init)throw new Error('12M ALADIN EXPORT MISSING');
    await window.A.init;
    audit('12M_ALADIN_READY',{durationMs:Math.round(performance.now()-started)});
  };
  const extract=source=>{
    const html=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    const js=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(html.length!==1||js.length!==1)throw new Error('12M 12L EXTRACTION FAILED');
    return [html[0][1],js[0][1]];
  };
  const mountHtml=html=>{
    const template=document.createElement('template');template.innerHTML=html;
    for(const node of [...template.content.childNodes]){
      if(node.nodeName==='SCRIPT'){
        const script=document.createElement('script');for(const attr of [...node.attributes])script.setAttribute(attr.name,attr.value);script.textContent=node.textContent;document.body.appendChild(script);
      }else document.body.appendChild(node);
    }
  };
  try{
    audit('12M_BOOT_START');
    const basePromise=fetchText(BASE12F,'12M_BASE12F');
    const viewerPromise=fetchText(VIEWER12L,'12M_12L');
    const aladinPromise=loadAladin();
    const [base12F,source12L]=await Promise.all([basePromise,viewerPromise,aladinPromise]).then(([base,viewer])=>[base,viewer]);
    audit('12M_PRELOADS_READY',{baseChars:base12F.length,viewerChars:source12L.length});

    const priorFetch=window.fetch.bind(window);
    window.fetch=async(input,init)=>{
      const raw=typeof input==='string'?input:String(input?.url||'');
      if(/raw\.githubusercontent\.com\/gear66me-ui\/Galaxy_Viewer\/beta\/viewer\/archive\/GV-beta-0012F\.py(?:[?#]|$)/i.test(raw)){
        audit('12M_BASE12F_MEMORY_HIT',{url:raw,bytes:base12F.length});
        return new Response(base12F,{status:200,statusText:'OK',headers:{'content-type':'text/plain; charset=utf-8','x-gv-12m-cache':'memory'}});
      }
      return priorFetch(input,init);
    };

    let [html,js]=extract(source12L);
    js=js.replace("version.textContent='VERSION 12L'","version.textContent='VERSION 12M'");
    js=js.replace("const DISPLAY_VERSION='12L';","const DISPLAY_VERSION='12M';");
    document.getElementById('gv-12m-bootstrap')?.remove();
    mountHtml(html);
    const script=document.createElement('script');script.textContent=js;document.body.appendChild(script);
    audit('12M_12L_MOUNTED');
  }catch(error){
    audit('12M_BOOT_FAILED',{error:String(error?.stack||error)});
    document.getElementById('gv-12m-bootstrap')?.remove();
    const failure=document.createElement('pre');failure.style.cssText='position:fixed;inset:0;z-index:2147483647;margin:0;padding:20px;overflow:auto;background:#000;color:#ff9b7a;font:12px sans-serif';failure.textContent='GALAXY VIEWER 12M FAILED\n\n'+String(error?.stack||error);document.body.appendChild(failure);
    throw error;
  }
})();
"""))
