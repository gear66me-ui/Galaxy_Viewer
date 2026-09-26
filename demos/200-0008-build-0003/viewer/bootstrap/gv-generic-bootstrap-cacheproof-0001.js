(async()=>{'use strict';
const R='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/';
const LAUNCHER_REVISION='CACHEPROOF-0001';
const c=document.getElementById('gv-apk-cover');
const p=document.getElementById('gv-splash-frame');
const e=document.getElementById('gv-launch-error');
let activeVersion='CURRENT';
const text=async u=>{const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);return r.text()};
const setCoverVersion=v=>{activeVersion=v;if(!c)return;const nodes=[...c.querySelectorAll('.v,.gv-10e-version')];if(nodes.length){nodes[0].textContent='VERSION '+v;nodes.slice(1).forEach(n=>n.remove())}else{const n=document.createElement('div');n.className='v';n.textContent='VERSION '+v;c.appendChild(n)}};
const extract=s=>{const h=[...s.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)],j=[...s.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];if(h.length!==1||j.length!==1)throw new Error('Viewer extraction failed');return[h[0][1],j[0][1]]};
const validManifest=m=>m&&typeof m.version==='string'&&/^(?:[0-9]+[A-Z]|[0-9]+[A-Z]{2}-[0-9]+[A-Z])$/.test(m.version)&&typeof m.viewer==='string'&&/^GV-(?:beta-[A-Za-z0-9._-]+|[0-9]+[A-Z]{2}-[A-Za-z0-9._-]+)\.py$/.test(m.viewer);
const loadViewerPayload=async()=>{const nonce=Date.now()+'-'+Math.random().toString(36).slice(2);const pointerUrl=R+'gv-current-viewer.json?gvnocache='+encodeURIComponent(nonce);const m=JSON.parse(await text(pointerUrl));if(!validManifest(m))throw new Error('Invalid LIVE Viewer manifest');setCoverVersion(m.version);const viewerUrl=R+m.viewer+'?gvnocache='+encodeURIComponent(nonce);return[m,await text(viewerUrl)]};
const waitForInteractiveViewer=()=>new Promise((ok,no)=>{const d=performance.now()+30000;let settled=false;const finishFail=err=>{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);no(err)};const finishOk=()=>{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);ok()};const viewerFailed=event=>finishFail(new Error(String(event?.detail?.message||activeVersion+' Viewer startup failed')));document.addEventListener('gv-viewer-failed',viewerFailed,{once:true});const f=()=>{if(settled)return;try{const root=document.getElementById('aladin-cosmic-command-test');if(root?.querySelector('canvas')&&window.aladin_cosmic_command_test)return finishOk();if(performance.now()>d)return finishFail(new Error(activeVersion+' interactive Viewer readiness timeout'));setTimeout(f,50)}catch(z){finishFail(z)}};f()});
const startViewer=async payloadPromise=>{const[m,s]=await payloadPromise;setCoverVersion(m.version);const[h,j]=extract(s);document.body.insertAdjacentHTML('beforeend',h);setCoverVersion(m.version);const z=document.createElement('script');z.textContent=j;document.body.appendChild(z);setCoverVersion(m.version);await waitForInteractiveViewer();return true};
const runSplash=()=>new Promise((ok,no)=>{let timer=0,done=false;const finish=()=>{if(done)return;done=true;if(timer)clearTimeout(timer);ok()};p.addEventListener('load',()=>{try{p.contentWindow.addEventListener('galaxy-splash-complete',finish,{once:true});p.style.visibility='visible';c?.remove();timer=setTimeout(()=>no(new Error(activeVersion+' splash completion timeout')),22000)}catch(z){no(z)}},{once:true});p.addEventListener('error',()=>no(new Error(activeVersion+' splash failed to load')),{once:true});p.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'});
try{
 const payloadPromise=loadViewerPayload();
 const viewerReadyPromise=startViewer(payloadPromise);
 await runSplash();
 await viewerReadyPromise;
 p.remove();
}catch(z){e.style.display='block';e.textContent='GALAXY VIEWER '+activeVersion+' FAILED TO LOAD\n\n'+String(z?.stack||z)}
})();
