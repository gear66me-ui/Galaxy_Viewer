(async()=>{'use strict';
const R='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/';
const c=document.getElementById('gv-apk-cover');
const p=document.getElementById('gv-splash-frame');
const e=document.getElementById('gv-launch-error');
let activeVersion='CURRENT';
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const text=async u=>{const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);return r.text()};
const setCoverVersion=v=>{activeVersion=v;if(!c)return;const nodes=[...c.querySelectorAll('.v,.gv-10e-version')];if(nodes.length){nodes[0].textContent='VERSION '+v;nodes.slice(1).forEach(n=>n.remove())}else{const n=document.createElement('div');n.className='v';n.textContent='VERSION '+v;c.appendChild(n)}};
const extract=s=>{const h=[...s.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)],j=[...s.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];if(h.length!==1||j.length!==1)throw new Error('Viewer extraction failed');return[h[0][1],j[0][1]]};
const validManifest=m=>m&&typeof m.version==='string'&&/^[0-9]+[A-Z]$/.test(m.version)&&typeof m.viewer==='string'&&/^GV-beta-[A-Za-z0-9._-]+\.py$/.test(m.viewer);
const loadViewerPayload=async()=>{try{const m=JSON.parse(await text(R+'gv-current-viewer.json?t='+Date.now()));if(!validManifest(m))throw new Error('Invalid current Viewer manifest');setCoverVersion(m.version);return[m,await text(R+m.viewer+'?t='+Date.now())]}catch(_){const m=JSON.parse(await text('viewer/gv-current-viewer.json'));if(!validManifest(m))throw new Error('Invalid bundled Viewer manifest');setCoverVersion(m.version);return[m,await text('viewer/'+m.viewer)]}};
const warm=async s=>{try{const urls=[...new Set([...s.matchAll(/https:\/\/[^'\"`\s]+/g)].map(m=>m[0]))];const primary=urls.filter(u=>/aladin|viewer\/modules\/|gv-hubble-galaxies-full/i.test(u));await Promise.allSettled(primary.map(u=>fetch(u,{cache:'force-cache'})));const cu=primary.find(u=>/gv-hubble-galaxies-full/i.test(u));if(!cu)return;const r=await fetch(cu,{cache:'force-cache'});if(!r.ok)return;const j=await r.json();const a=Array.isArray(j?.entries)?[...j.entries]:[];for(let i=a.length-1;i>0;i--){const k=Math.floor(Math.random()*(i+1));[a[i],a[k]]=[a[k],a[i]]}const imgs=a.slice(0,10).map(o=>String(o?.githubImageUrl||o?.selectedImageUrl||'')).filter(u=>/^https:\/\//.test(u));Promise.allSettled(imgs.map(u=>fetch(u,{cache:'force-cache'}))).catch(()=>{})}catch(_){}};
const waitForInteractiveViewer=()=>new Promise((ok,no)=>{const d=performance.now()+30000;let settled=false;const finishFail=err=>{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);no(err)};const finishOk=()=>{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);ok()};const viewerFailed=event=>finishFail(new Error(String(event?.detail?.message||activeVersion+' Viewer startup failed')));document.addEventListener('gv-viewer-failed',viewerFailed,{once:true});const f=()=>{if(settled)return;try{const root=document.getElementById('aladin-cosmic-command-test');if(root?.querySelector('canvas')&&window.aladin_cosmic_command_test)return finishOk();if(performance.now()>d)return finishFail(new Error(activeVersion+' interactive Viewer readiness timeout'));setTimeout(f,50)}catch(z){finishFail(z)}};f()});
const startViewer=async payloadPromise=>{const[m,s]=await payloadPromise;setCoverVersion(m.version);warm(s);const[h,j]=extract(s);document.body.insertAdjacentHTML('beforeend',h);setCoverVersion(m.version);const z=document.createElement('script');z.textContent=j;document.body.appendChild(z);setCoverVersion(m.version);await waitForInteractiveViewer();return true};
const runSplash=()=>new Promise((ok,no)=>{let timer=0,done=false;const finish=()=>{if(done)return;done=true;if(timer)clearTimeout(timer);ok()};p.addEventListener('load',()=>{try{p.contentWindow.addEventListener('galaxy-splash-complete',finish,{once:true});p.style.visibility='visible';c?.remove();timer=setTimeout(()=>no(new Error(activeVersion+' splash completion timeout')),22000)}catch(z){no(z)}},{once:true});p.addEventListener('error',()=>no(new Error(activeVersion+' splash failed to load')),{once:true});p.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'});
try{
 const started=performance.now();
 const payloadPromise=loadViewerPayload();
 const viewerReadyPromise=startViewer(payloadPromise);
 await delay(Math.max(0,3500-(performance.now()-started)));
 await runSplash();
 await viewerReadyPromise;
 p.remove();
}catch(z){e.style.display='block';e.textContent='GALAXY VIEWER '+activeVersion+' FAILED TO LOAD\n\n'+String(z?.stack||z)}
})();
