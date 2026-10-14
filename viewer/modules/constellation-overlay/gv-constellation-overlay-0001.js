/* Galaxy Viewer constellation overlay module 0004.
 * Adds destination-only soft pulsing star points during navigation.
 */
(() => {
  "use strict";
  const VERSION = "0008";
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
      let e=overlays.get(name);if(!e){e={name,obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),glow:window.A.graphicOverlay({color:"#8EDCFF",lineWidth:0.75,opacity:0.18}),segments:0,starIds:new Set(),points:[]};aladin.addOverlay(e.obj);aladin.addOverlay(e.glow);overlays.set(name,e);}
      const p1=stars.get(a),p2=stars.get(b);if(p1&&p2){e.obj.add(window.A.polyline([p1,p2]));e.glow.add(window.A.polyline([p1,p2]));e.segments++;for(const id of [a,b])if(!e.starIds.has(id)&&stars.has(id)){e.starIds.add(id);e.points.push(stars.get(id));}}
    }
    // Keep the normal map quiet; a separate, wider duplicate overlay creates an actual line halo.
    for(const e of overlays.values()){
      for(const [ra,dec] of e.points){
        try{e.glow.add(window.A.circle([ra,dec],0.035,{color:"#EAFBFF",lineWidth:0.75,fillColor:"#8EDCFF",fillOpacity:0.35}));}catch(_){}
      }
      e.obj.hide();e.glow.hide();
    }
    let enabled=false,glowTimer=null,glowEntry=null,frameHandle=null,phase=0;
    function stopGlow(){
      if(glowTimer!==null){clearInterval(glowTimer);glowTimer=null;}
      if(frameHandle!==null){cancelAnimationFrame(frameHandle);frameHandle=null;}
      if(glowEntry){glowEntry.glow.hide();glowEntry.glow.setOptions?.({color:"#8EDCFF",lineWidth:0.75,opacity:0.18});}
      glowEntry=null;phase=0;
    }
    function setEnabled(next){
      enabled=!!next;
      for(const e of overlays.values()){enabled?e.obj.show():e.obj.hide();if(!enabled)e.glow.hide();}
      if(!enabled)stopGlow();
      return enabled;
    }
    function setTravelGlow(name,active){
      stopGlow();if(!active||!name)return false;
      const wanted=canon(name);let found=null;
      for(const [key,e] of overlays){const k=canon(key);if(k===wanted||k.includes(wanted)||wanted.includes(k)){found=e;break;}}
      if(!found){console.info("GV CONSTELLATION GLOW: no matching constellation",name);return false;}
      startGlow(found);return true;
    }
    function applyGlow(found,opacity){
      // Aladin GraphicOverlay versions differ: prefer their dedicated opacity setter,
      // then alpha, then options as a compatibility fallback.
      try{
        if(typeof found.glow.setOpacity==="function")found.glow.setOpacity(opacity);
        else if(typeof found.glow.setAlpha==="function")found.glow.setAlpha(opacity);
        else if(typeof found.glow.setOptions==="function")found.glow.setOptions({opacity,color:"#8EDCFF",lineWidth:0.75});
      }catch(error){console.warn("GV CONSTELLATION GLOW OPACITY UPDATE FAILED",error)}
    }
    function startGlow(found){
      stopGlow();glowEntry=found;
      if(!enabled)return false;
      found.glow.setOptions?.({color:"#8EDCFF",lineWidth:0.75});
      applyGlow(found,0);
      found.glow.show();
      // A true 2-second triangular brightness ramp: 0→100% in 1s, then 100→0% in 1s.
      // Only opacity animates; line width is fixed and never exceeds 0.75px.
      const started=performance.now(),period=2000;
      const animate=now=>{
        if(!enabled||glowEntry!==found){frameHandle=null;return;}
        const phase=((now-started)%period)/period;
        const brightness=phase<0.5?phase*2:(1-phase)*2;
        applyGlow(found,brightness);
        frameHandle=requestAnimationFrame(animate);
      };
      frameHandle=requestAnimationFrame(animate);
      return true;
    }
    function setTravelGlowAt(ra,dec,active=true){
      const targetRa=Number(ra),targetDec=Number(dec);
      if(!active||!Number.isFinite(targetRa)||!Number.isFinite(targetDec)){stopGlow();return false;}
      // Select the constellation whose line endpoint is closest to the destination on the celestial sphere.
      const rad=Math.PI/180;let best=null,bestDot=-Infinity;
      for(const e of overlays.values())for(const [sra,sdec] of e.points){
        const dot=Math.sin(targetDec*rad)*Math.sin(sdec*rad)+Math.cos(targetDec*rad)*Math.cos(sdec*rad)*Math.cos((targetRa-sra)*rad);
        if(dot>bestDot){bestDot=dot;best=e;}
      }
      if(!best){console.warn("GV CONSTELLATION GLOW: no destination constellation available");return false;}
      console.info("GV CONSTELLATION GLOW: destination matched",best.name,{ra:targetRa,dec:targetDec,separationDeg:Math.acos(Math.max(-1,Math.min(1,bestDot)))/rad});
      return startGlow(best);
    }
    const result=Object.freeze({VERSION,get enabled(){return enabled;},setEnabled,setTravelGlow,setTravelGlowAt,clearTravelGlow:stopGlow,toggle(){return setEnabled(!enabled);},constellationCount:overlays.size,segmentCount:[...overlays.values()].reduce((n,e)=>n+e.segments,0)});
    window.GalaxyViewerConstellations=result;return result;
  }
  window.GalaxyViewerConstellationOverlay=Object.freeze({VERSION,mount});
})();