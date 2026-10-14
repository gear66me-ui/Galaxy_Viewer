/* Galaxy Viewer constellation overlay module 0002.
 * Adds destination-only soft pulsing star points during navigation.
 */
(() => {
  "use strict";
  const VERSION = "0002";
  const LINE_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line.csv";
  const STAR_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line_star.csv";
  const COLOR = "#8EDCFF", WIDTH = 0.25;
  async function csv(url) { const r=await fetch(url,{cache:"force-cache"}); if(!r.ok)throw Error("CONSTELLATION DATA HTTP "+r.status); return r.text(); }
  function parseStars(text) {
    const map=new Map();
    for(const line of text.split(/\r?\n/)){const c=line.trim().split(",");if(c.length<7)continue;
      const id=Number(c[0]),h=Number(c[1]),m=Number(c[2]),s=Number(c[3]),ds=String(c[4]).trim(),d=Number(ds),dm=Number(c[5]),sec=Number(c[6]);
      if(![id,h,m,s,d,dm,sec].every(Number.isFinite))continue;
      map.set(id,[(h+m/60+s/3600)*15,Math.sign(d||(ds.startsWith("-")?-1:1))*(Math.abs(d)+dm/60+sec/3600)]);
    } return map;
  }
  function parseLines(text){const rows=[];for(const line of text.split(/\r?\n/)){const c=line.trim().split(",");if(c.length>=3&&c[0]&&Number.isFinite(Number(c[1]))&&Number.isFinite(Number(c[2])))rows.push([c[0],Number(c[1]),Number(c[2])]);}return rows;}
  const canon=v=>String(v||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toUpperCase().replace(/[^A-Z0-9]/g,"");
  async function mount(aladin) {
    if(!aladin||typeof aladin.addOverlay!=="function"||!window.A?.graphicOverlay||!window.A?.polyline)throw Error("CONSTELLATIONS: Aladin overlay API unavailable");
    const [lt,st]=await Promise.all([csv(LINE_URL),csv(STAR_URL)]),stars=parseStars(st),segments=parseLines(lt);
    if(stars.size<100||segments.length<100)throw Error("CONSTELLATIONS: source data failed validation");
    const overlays=new Map();
    for(const [name,a,b] of segments){
      let e=overlays.get(name);if(!e){e={name,obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),segments:0,starIds:new Set(),points:[]};aladin.addOverlay(e.obj);overlays.set(name,e);}
      const p1=stars.get(a),p2=stars.get(b);if(p1&&p2){e.obj.add(window.A.polyline([p1,p2]));e.segments++;for(const id of [a,b])if(!e.starIds.has(id)&&stars.has(id)){e.starIds.add(id);e.points.push(stars.get(id));}}
    }
    // Draw each star as a tiny sky-coordinate circle; its angular radius is animated for a soft halo.
    for(const e of overlays.values()){
      for(const [ra,dec] of e.points){
        try{e.obj.add(window.A.circle([ra,dec],0.035,{color:"#D8F6FF",lineWidth:1,fillColor:"#8EDCFF",fillOpacity:0.85}));}catch(_){}
      }
      e.obj.hide();
    }
    let enabled=false,glowTimer=null,glowEntry=null,phase=0;
    function stopGlow(){if(glowTimer!==null){clearInterval(glowTimer);glowTimer=null;}if(glowEntry){glowEntry.obj.setOptions?.({color:COLOR,lineWidth:WIDTH});}glowEntry=null;}
    function setEnabled(next){enabled=!!next;for(const e of overlays.values())enabled?e.obj.show():e.obj.hide();return enabled;}
    function setTravelGlow(name,active){
      stopGlow();if(!active||!name)return false;
      const wanted=canon(name);let found=null;
      for(const [key,e] of overlays){const k=canon(key);if(k===wanted||k.includes(wanted)||wanted.includes(k)){found=e;break;}}
      if(!found){console.info("GV CONSTELLATION GLOW: no matching constellation",name);return false;}
      glowEntry=found;if(enabled)found.obj.show();
      glowTimer=setInterval(()=>{phase=(phase+1)%4;const widths=[0.25,0.8,1.35,0.8];found.obj.setOptions?.({color:phase===2?"#EAFBFF":"#8EDCFF",lineWidth:widths[phase]});},220);
      return true;
    }
    const result=Object.freeze({VERSION,get enabled(){return enabled;},setEnabled,setTravelGlow,toggle(){return setEnabled(!enabled);},constellationCount:overlays.size,segmentCount:[...overlays.values()].reduce((n,e)=>n+e.segments,0)});
    window.GalaxyViewerConstellations=result;return result;
  }
  window.GalaxyViewerConstellationOverlay=Object.freeze({VERSION,mount});
})();