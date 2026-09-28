from IPython.display import HTML, Javascript, display

VIEWER_VERSION = "GV-beta-200-014"

display(HTML("""
<div id="gv014-rollover-host" style="display:none"></div>
"""))

display(Javascript(r"""
(async()=>{
'use strict';
const VERSION='GV-beta-200-014';
const GV200001_BUILD='0001';
const GV_RUNTIME='0082';
const BASE='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/GV-beta-200-013.py';
const H5='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js';
const H7='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js';
const D19='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0019.js';
const text=async url=>{const r=await fetch(url+(url.includes('?')?'&':'?')+'v=gv014-0001-'+Date.now(),{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status+' '+url);return r.text()};
function mountHtml(html){const t=document.createElement('template');t.innerHTML=html;for(const n of [...t.content.childNodes])document.body.appendChild(n)}
function patch(s){
 s=String(s||'').replaceAll('GV-beta-200-013','GV-beta-200-014');
 s=s.replaceAll("const GV200001_BUILD='0049';","const GV200001_BUILD='0001';");
 s=s.replaceAll("GV200001_BUILD='0049'","GV200001_BUILD='0001'");
 s=s.replaceAll(H7,H5).replaceAll(D19,H5);
 s=s.replaceAll("if(window.GalaxyViewerHamburgerMenu?.version!=='0007')throw new Error('HAMBURGER 0007 EXPORT MISSING');","if(window.GalaxyViewerHamburgerMenu?.version!=='0005')throw new Error('HAMBURGER 0005 EXPORT MISSING');");
 s=s.replaceAll("if(window.GalaxyViewerDiagnostics?.VERSION!=='0019')throw new Error('DIAGNOSTICS 0019 EXPORT MISSING');","/* GV014: diagnostics intentionally not loaded. */");
 s=s.replaceAll('const diagnostics=window.GalaxyViewerDiagnostics;','const diagnostics=null;');
 return s;
}
try{
 const source=patch(await text(BASE));
 if(source.includes('gv-hamburger-menu-0007.js')||source.includes('gv-diagnostics-0019.js'))throw new Error('GV014 patch check failed');
 const html=(source.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/)||[])[1];
 const scripts=[...source.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)].map(m=>m[1]);
 if(!html||!scripts.length)throw new Error('GV014 extraction failed');
 mountHtml(html);
 for(const js of scripts){const el=document.createElement('script');el.textContent=js;document.body.appendChild(el)}
}catch(e){console.error(e);const p=document.createElement('pre');p.textContent='GV014 FAILED\n\n'+String(e?.stack||e);Object.assign(p.style,{position:'fixed',inset:'0',zIndex:'2147483647',background:'#000',color:'#FFD166',padding:'20px',margin:'0',whiteSpace:'pre-wrap'});document.body.appendChild(p)}
})();
"""))
