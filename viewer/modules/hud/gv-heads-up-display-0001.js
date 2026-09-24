/* Galaxy Viewer Heads-Up Display 0001
 * Read-only five-row route HUD: current destination + next four.
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

function compactName(record){
  const name=clean(record?.name??record?.title??record?.displayName??record?.archiveId);
  if(!name)return '—';
  return name.length<=22?name:`${name.slice(0,21)}…`;
}

function ledSvg(state){
  const on=state==='current';
  const fill=on?'#78FFAB':'#58BFFF';
  const opacity=on?'1':'.72';
  return `<svg class="gv-hud-led" viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="3.25" fill="${fill}" opacity="${opacity}"/><circle cx="6" cy="6" r="5" fill="none" stroke="${fill}" stroke-opacity=".34"/></svg>`;
}

function routeWindow(routeEngine,randomGalaxy){
  const route=Array.isArray(routeEngine?.active?.route)?routeEngine.active.route:[];
  const cursor=Number.isInteger(routeEngine?.routeCursor)?routeEngine.routeCursor:0;
  const current=randomGalaxy?.activeDestination??randomGalaxy?.currentDestination??randomGalaxy?.getState?.()?.activeDestination??null;
  const upcoming=route.slice(Math.max(0,cursor),Math.max(0,cursor)+4);
  return [current,...upcoming].slice(0,ROWS);
}

function installStyle(){
  if(document.getElementById('gv-heads-up-display-0001-style'))return;
  const style=document.createElement('style');
  style.id='gv-heads-up-display-0001-style';
  style.textContent=`
.gv-heads-up-display{position:absolute;right:82px;top:270px;z-index:7210;width:min(210px,calc(100vw - 102px));pointer-events:none;user-select:none;-webkit-user-select:none;font-family:"GV Space Age",Arial,sans-serif}
.gv-hud-row{display:grid;grid-template-columns:14px 30px minmax(0,1fr);align-items:center;gap:4px;min-height:18px;padding:1px 5px;border-bottom:1px solid rgba(88,191,255,.18);background:rgba(4,16,35,.58);color:#DDF8FF;text-shadow:0 0 5px rgba(88,191,255,.35);font-size:8px;line-height:1.15;letter-spacing:.35px}
.gv-hud-row:first-child{border-radius:5px 5px 0 0}
.gv-hud-row:last-child{border-radius:0 0 5px 5px;border-bottom:0}
.gv-hud-row[data-state="current"]{background:rgba(8,35,45,.72)}
.gv-hud-led{display:block;width:12px;height:12px;overflow:visible}
.gv-hud-provider{color:#7CCBFF;font-weight:700}
.gv-hud-row[data-state="current"] .gv-hud-provider{color:#78FFAB}
.gv-hud-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
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

  const hud=document.createElement('div');
  hud.className='gv-heads-up-display';
  hud.setAttribute('aria-label','Galaxy route heads-up display');
  root.appendChild(hud);

  function render(){
    const records=routeWindow(routeEngine,randomGalaxy);
    hud.replaceChildren();
    for(let i=0;i<ROWS;i++){
      const record=records[i]??null;
      const state=i===0?'current':'upcoming';
      const row=document.createElement('div');
      row.className='gv-hud-row'+(record?'':' gv-hud-empty');
      row.dataset.state=state;
      row.dataset.row=String(i);
      row.innerHTML=ledSvg(state)+
        `<span class="gv-hud-provider">${record?providerCode(record):'---'}</span>`+
        `<span class="gv-hud-name"></span>`;
      row.querySelector('.gv-hud-name').textContent=record?compactName(record):'—';
      hud.appendChild(row);
    }
    return records;
  }

  render();
  return Object.freeze({
    root:hud,
    render,
    destroy(){hud.remove()}
  });
}

global.GalaxyViewerHeadsUpDisplay=Object.freeze({
  VERSION,
  mount,
  providerCode,
  compactName,
  routeWindow
});
})(typeof window!=='undefined'?window:globalThis);
