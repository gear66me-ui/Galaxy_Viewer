from IPython.display import HTML, Javascript, display

display(HTML("""
<div id="gv011" style="font:14px monospace;background:#07111d;color:#d8ecff;padding:16px;border-radius:10px">
<b style="color:#58bfff">GALAXY VIEWER · GV-beta-200-011</b><pre id="gv011log">BOOT\n</pre></div>
"""))

display(Javascript(r"""
(async()=>{'use strict';
const VERSION='GV-beta-200-011';
const RUNTIME_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/navigation-runtime/gv-navigation-runtime-0001.js';
const DIAG='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0019.js';
const log=(m,x)=>{console.info('[GV011]',m,x??'');const e=document.getElementById('gv011log');if(e)e.textContent+=m+(x===undefined?'':' '+JSON.stringify(x))+'\n'};
function script(url){return new Promise((ok,no)=>{const s=document.createElement('script');s.src=url;s.async=true;s.onload=()=>ok(s);s.onerror=()=>no(Error(`SCRIPT LOAD FAILED ${url}`));document.head.appendChild(s)})}
try{
 log('LOAD NAVIGATION RUNTIME 0001');await script(RUNTIME_URL);
 const R=window.GalaxyNavigationRuntime;if(!R||R.VERSION!=='0001')throw Error('NAVIGATION RUNTIME 0001 API MISSING');
 log('MASTER CATALOG → 130 → ACTIVE 100 + RESERVE 30');const state=await R.initialize();
 log('RUNTIME READY',state);
 log('FIRST 10 ACTIVE');R.active.route.slice(0,10).forEach((r,i)=>log(`${String(i+1).padStart(3,'0')} ${r.provider} · ${r.name} · ${r.archiveId}`));
 log('RESERVE 30');R.active.reserve.forEach((r,i)=>log(`${String(i+101).padStart(3,'0')} ${r.provider} · ${r.name} · ${r.archiveId}`));
 try{await script(DIAG);log('DIAGNOSTICS 0019 LOADED')}catch(e){log('DIAGNOSTICS WARNING',String(e))}
 window.dispatchEvent(new CustomEvent('gv-navigation-runtime-ready',{detail:{viewer:VERSION,...state}}));
}catch(e){log('FATAL',String(e?.stack||e));console.error(e)}
})();
"""))
