/* Galaxy Viewer Heads-Up Display 0001
 * Five-row route HUD: current destination + next four; probes raster readiness for LED status.
 * Reads Route Engine / Random Galaxy state only.
 * Does NOT own navigation, queueing, camera, Aladin, AVM, or route mutation.
 */
(function(global){
'use strict';

const VERSION='0001';
const ROWS=5;
const PROVIDER_CODES=Object.freeze({
  HUBBLE:'HUB',HUB:'HUB',
  JWST:'JWS',JWS:'JWS',
  CHANDRA:'CHA',CHA:'CHA',
  SPITZER:'SPZ',SPZ:'SPZ',
  ESO:'ESO',
  NOIRLAB:'NLR','NOIR LAB':'NLR',NOIR:'NLR',NLR:'NLR'
});

const clean=value=>String(value??'').replace(/\s+/g,' ').trim();

function providerCode(record){
  const raw=clean(record?.provider??record?.source??record?.catalogKey).toUpperCase();
  if(PROVIDER_CODES[raw])return PROVIDER_CODES[raw];
  for(const [name,code] of Object.entries(PROVIDER_CODES)){
    if(raw.includes(name))return code;
  }
  return raw.slice(0,3)||'---';
}

function readinessKey(record){
  return clean(record?.imageUrl??record?.selectedImageUrl??record?.hdUrl??record?.url);
}

function resourceState(record,readiness){
  const key=readinessKey(record);
  if(key&&readiness?.has(key))return readiness.get(key);
  const state=clean(record?.resourceState??record?.downloadState??record?.assetState??record?.state).toUpperCase();
  if(state==='READY')return 'ready';
  if(state==='FAILED'||state==='ERROR')return 'failed';
  if(state==='RETRY'||state.includes('RETRY')||state==='STALE')return 'stale';
  if(state==='DOWNLOADING'||state==='DECODING'||state==='PREPARING'||state==='LOADING')return 'working';
  return 'queued';
}

function ledSvg(state){
  const palette={
    ready:'#78FFAB',
    working:'#FFD45C',
    queued:'#F4FBFF',
    failed:'#FF5757',
    stale:'#58BFFF'
  };
  const fill=palette[state]??palette.queued;
  return `<svg class="gv-hud-led" viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="3.25" fill="${fill}"/><circle cx="6" cy="6" r="5" fill="none" stroke="${fill}" stroke-opacity=".34"/></svg>`;
}

function routeWindow(routeEngine,randomGalaxy){
  const route=Array.isArray(routeEngine?.active?.route)?routeEngine.active.route:[];
  const cursor=Number.isInteger(routeEngine?.routeCursor)?routeEngine.routeCursor:0;
  const current=randomGalaxy?.activeDestination??randomGalaxy?.currentDestination??randomGalaxy?.getState?.()?.activeDestination??null;
  const start=Math.max(0,cursor);
  if(!current)return route.slice(start,start+ROWS);
  const upcoming=route.slice(start,start+ROWS-1);
  return [current,...upcoming].slice(0,ROWS);
}

function installStyle(){
  if(document.getElementById('gv-heads-up-display-0001-style'))return;
  const style=document.createElement('style');
  style.id='gv-heads-up-display-0001-style';
  style.textContent=`
.gv-heads-up-display{position:absolute;right:8px;top:128px;z-index:7210;width:48px;border-radius:6px;overflow:hidden;pointer-events:none;user-select:none;-webkit-user-select:none;font-family:"GV Space Age",Arial,sans-serif}
.gv-hud-row{display:grid;grid-template-columns:28px 12px;align-items:center;justify-content:end;gap:3px;min-height:18px;padding:1px 2px;border:1px solid rgba(67,207,255,.72);border-radius:6px;background:linear-gradient(180deg,rgba(23,78,134,.90),rgba(4,27,62,.92) 54%,rgba(13,90,152,.86));box-shadow:inset 0 1px 1px rgba(225,251,255,.70),inset 0 -2px 3px rgba(0,0,0,.45),inset 0 0 8px rgba(41,153,255,.26),0 0 2px rgba(221,248,255,.82),0 0 7px rgba(50,190,255,.52);color:#DDF8FF;text-shadow:0 0 5px rgba(88,191,255,.35);font-size:7px;line-height:1;letter-spacing:.2px}
.gv-hud-row[data-state="current"]{background:linear-gradient(180deg,rgba(17,83,91,.94),rgba(5,42,62,.94) 54%,rgba(12,104,119,.88))}
.gv-hud-led{display:block;width:12px;height:12px;overflow:visible;filter:drop-shadow(0 0 2px rgba(221,248,255,.92)) drop-shadow(0 0 5px rgba(88,191,255,.72))}
.gv-hud-provider{color:#7CCBFF;font-weight:700;text-shadow:0 0 3px rgba(221,248,255,.74),0 0 7px rgba(88,191,255,.60)}
.gv-hud-row[data-state="current"] .gv-hud-provider{color:#78FFAB}
.gv-hud-empty{opacity:.42}
`;
  document.head.appendChild(style);
}

function mount(root,options={}){
  if(!root)throw new Error('HEADS-UP DISPLAY ROOT MISSING');
  installStyle();
  const routeEngine=options.routeEngine??global.GalaxyRouteEngine;
  const randomGalaxy=options.randomGalaxy??global.GalaxyRandomGalaxy;
  if(!routeEngine)throw new Error('HEADS-UP DISPLAY ROUTE ENGINE MISSING');

  const existing=root.querySelector?.('.gv-heads-up-display');
  if(existing)existing.remove();

  const readiness=new Map();
  const probes=new Map();

  const probeReadiness=record=>{
    const key=readinessKey(record);
    if(!key||readiness.has(key)||probes.has(key))return;
    readiness.set(key,'working');
    const task=(async()=>{
      await new Promise((resolve,reject)=>{
        const image=new Image();
        image.decoding='async';
        image.onload=async()=>{
          try{
            if(typeof image.decode==='function')await image.decode();
            resolve();
          }catch(error){reject(error)}
        };
        image.onerror=()=>reject(new Error('HUD IMAGE LOAD FAILED'));
        image.src=key;
      });
      readiness.set(key,'ready');
    })().catch(()=>{if(readiness.get(key)!=='ready')readiness.set(key,'failed')}).finally(()=>{
      probes.delete(key);
      if(hud?.isConnected)render();
    });
    probes.set(key,task);
  };

  const hud=document.createElement('div');
  hud.className='gv-heads-up-display';
  hud.setAttribute('aria-label','Galaxy route heads-up display');
  root.appendChild(hud);

  function render(){
    const records=routeWindow(routeEngine,randomGalaxy);
    hud.replaceChildren();
    for(let i=0;i<ROWS;i++){
      const record=records[i]??null;
      const position=i===0?'current':'upcoming';
      const state=resourceState(record,readiness);
      const row=document.createElement('div');
      row.className='gv-hud-row'+(record?'':' gv-hud-empty');
      row.dataset.state=position;
      row.dataset.resourceState=state;
      row.dataset.row=String(i);
      row.innerHTML=`<span class="gv-hud-provider">${record?providerCode(record):'---'}</span>`+ledSvg(state);
      hud.appendChild(row);
      if(record)probeReadiness(record);
    }
    return records;
  }

  render();
  return Object.freeze({
    root:hud,
    render,
    markReady(record){
      const key=readinessKey(record);
      if(!key)return false;
      readiness.set(key,'ready');
      render();
      return true;
    },
    destroy(){hud.remove();readiness.clear();probes.clear()}
  });
}

global.GalaxyViewerHeadsUpDisplay=Object.freeze({
  VERSION,
  mount,
  providerCode,
  readinessKey,
  resourceState,
  routeWindow
});
})(typeof window!=='undefined'?window:globalThis);
