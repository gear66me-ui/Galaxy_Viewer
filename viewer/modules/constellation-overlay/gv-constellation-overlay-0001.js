/* Galaxy Viewer constellation overlay module 0013.
 * Repairs Fornax stars and pulses actual Aladin overlay visibility.
 */
(() => {
  "use strict";
  const VERSION = "0014";
  const LINE_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line.csv";
  const STAR_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line_star.csv";
  const COLOR = "#8EDCFF", WIDTH = 0.25;
  async function csv(url) { const r=await fetch(url,{cache:"force-cache"}); if(!r.ok)throw Error("CONSTELLATION DATA HTTP "+r.status); return r.text(); }
  function parseStars(text) {
    const map=new Map();
    for(const line of text.split(/\r?\n/)){const c=line.trim().split(",");if(c.length<7)continue;
      const id=Number(c[0]),h=Number(c[1]),m=Number(c[2]),s=Number(c[3]),ds=String(c[4]).trim(),d=Number(ds),dm=Number(c[5]),sec=Number(c[6]);
      if(![id,h,m,s,d,dm,sec].every(Number.isFinite))continue;
      const sign=(d<0||(d===0&&(dm<0||(dm===0&&sec<0))))?-1:1;
      map.set(id,[(h+m/60+s/3600)*15,sign*(Math.abs(d)+Math.abs(dm)/60+Math.abs(sec)/3600)]);
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
      let e=overlays.get(name);if(!e){e={name,obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),glow:window.A.graphicOverlay({color:"#39BFFF",lineWidth:0.5}),stars:window.A.graphicOverlay({color:"#FFFFFF",lineWidth:0.5}),segments:0,starIds:new Set(),points:[]};aladin.addOverlay(e.obj);aladin.addOverlay(e.glow);aladin.addOverlay(e.stars);overlays.set(name,e);}
      const p1=stars.get(a),p2=stars.get(b);
      for(const id of [a,b]){const p=stars.get(id);if(p&&!e.starIds.has(id)){e.starIds.add(id);e.points.push(p);}}
      if(p1&&p2){e.obj.add(window.A.polyline([p1,p2]));e.glow.add(window.A.polyline([p1,p2],{color:"#39BFFF",lineWidth:0.5}));e.segments++;}
      else console.warn("GV CONSTELLATION: skipped segment with missing star coordinate",{constellation:name,start:a,end:b,hasStart:!!p1,hasEnd:!!p2});
    }
    // The line-source CSV omits principal stars not used by its asterism segments.
    let fornax=[...overlays.values()].find(e=>["FOR","FORNAX"].includes(canon(e.name)));
    if(!fornax){
      fornax={name:"For",obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),glow:window.A.graphicOverlay({color:"#39BFFF",lineWidth:0.5}),stars:window.A.graphicOverlay({color:"#FFFFFF",lineWidth:0.5}),segments:0,starIds:new Set(),points:[]};
      aladin.addOverlay(fornax.obj);aladin.addOverlay(fornax.glow);aladin.addOverlay(fornax.stars);overlays.set(fornax.name,fornax);
    }
    const fornaxPrincipalStars=[
      {name:"Dalim (Alpha Fornacis)",ra:48.018875,dec:-28.9876111111},
      {name:"Beta Fornacis",ra:42.2725833333,dec:-32.4058888889},
      {name:"Nu Fornacis",ra:31.1226666667,dec:-29.2968055556}
    ];
    for(const star of fornaxPrincipalStars){
      const alreadyPresent=fornax.points.some(p=>Math.abs(p[0]-star.ra)<0.01&&Math.abs(p[1]-star.dec)<0.01);
      if(!alreadyPresent)fornax.points.push([star.ra,star.dec]);
    }
    console.info("GV CONSTELLATION: Fornax principal stars registered",fornaxPrincipalStars.map(s=>s.name));

    // Keep the normal map quiet; a separate, wider duplicate overlay creates an actual line halo.
    for(const e of overlays.values()){
      for(const [ra,dec] of e.points){
        try{e.glow.add(window.A.circle([ra,dec],0.075,{color:"#26AFFF",lineWidth:0.5,fillColor:"#26AFFF",fillOpacity:0.28}));e.stars.add(window.A.circle([ra,dec],0.035,{color:"#FFFFFF",lineWidth:0.5,fillColor:"#FFFFFF",fillOpacity:1}));}catch(_){}
      }
      e.obj.hide();e.glow.hide();e.stars.hide();
    }
    let enabled=false,glowTimer=null,glowEntry=null,frameHandle=null,phase=0;
    function stopGlow(){
      if(glowTimer!==null){clearInterval(glowTimer);glowTimer=null;}
      if(frameHandle!==null){cancelAnimationFrame(frameHandle);frameHandle=null;}
      if(glowEntry){glowEntry.glow.hide();glowEntry.stars.hide();glowEntry.glow.setOptions?.({color:"#39BFFF",lineWidth:0.5});glowEntry.stars.setOptions?.({color:"#FFFFFF",lineWidth:0.5});}
      glowEntry=null;phase=0;
    }
    function setEnabled(next){
      enabled=!!next;
      for(const e of overlays.values()){enabled?e.obj.show():e.obj.hide();if(!enabled)e.glow.hide();}
      if(!enabled)stopGlow();
      return enabled;
    }
    function findByName(name){
      const wanted=canon(name);if(!wanted)return null;
      const aliases={FORNAX:"FOR",FOR:"FORNAX"};
      for(const [key,e] of overlays){const k=canon(key);if(k===wanted||aliases[wanted]===k||aliases[k]===wanted)return e;}
      for(const [key,e] of overlays){const k=canon(key);if(k.length>3&&(k.includes(wanted)||wanted.includes(k)))return e;}
      return null;
    }
    function setTravelGlow(name,active){
      stopGlow();if(!active||!name)return false;
      const found=findByName(name);
      if(!found){console.info("GV CONSTELLATION GLOW: no matching constellation",name);return false;}
      startGlow(found,{travel:true});return true;
    }
    function applyGlow(found,brightness){
      const alpha=Math.max(0,Math.min(1,brightness));
      try{
        if(typeof found.glow.setOpacity==="function")found.glow.setOpacity(alpha);else found.glow.setOptions?.({opacity:alpha});
        if(typeof found.stars.setOpacity==="function")found.stars.setOpacity(alpha);else found.stars.setOptions?.({opacity:alpha});
        if(alpha<=0.001){found.glow.hide();found.stars.hide();}else{found.glow.show();found.stars.show();}
      }catch(error){console.warn("GV CONSTELLATION GRADIENT FADE FAILED",error)}
    }
    function startGlow(found,{travel=false}={}){
      stopGlow();glowEntry=found;
      // Destination glow is independent of the user-facing constellation-line toggle.
      if(!enabled&&!travel)return false;
      found.glow.setOptions?.({color:"#39BFFF",lineWidth:0.5});
      applyGlow(found,0);
      found.glow.show();found.stars.show();
      // A true 2-second triangular brightness ramp: 0→100% in 1s, then 100→0% in 1s.
      // Only visibility pulses; all line strokes are capped at 0.5px.
      const started=performance.now(),period=2000;
      const animate=now=>{
        if((!enabled&&!travel)||glowEntry!==found){frameHandle=null;return;}
        const phase=((now-started)%period)/period;
        const brightness=phase<0.5?phase*2:(1-phase)*2;
        applyGlow(found,brightness);
        frameHandle=requestAnimationFrame(animate);
      };
      frameHandle=requestAnimationFrame(animate);
      return true;
    }
    function setTravelGlowAt(ra,dec,active=true){
      console.warn("GV CONSTELLATION GLOW: coordinate fallback deprecated; pass archive constellation name");
      const targetRa=Number(ra),targetDec=Number(dec);
      if(!active||!Number.isFinite(targetRa)||!Number.isFinite(targetDec)){stopGlow();return false;}
      const rad=Math.PI/180;let best=null,bestDot=-Infinity;
      for(const e of overlays.values())for(const [sra,sdec] of e.points){const dot=Math.sin(targetDec*rad)*Math.sin(sdec*rad)+Math.cos(targetDec*rad)*Math.cos(sdec*rad)*Math.cos((targetRa-sra)*rad);if(dot>bestDot){bestDot=dot;best=e;}}
      if(!best)return false;console.info("GV CONSTELLATION GLOW: coordinate fallback matched",best.name);return startGlow(best,{travel:true});
    }
    function setTravelGlowByName(name,active=true){
      if(!active||!String(name||"").trim()){stopGlow();return false;}
      const found=findByName(name);
      if(!found){stopGlow();console.warn("GV CONSTELLATION GLOW: archive name has no exact overlay match",{archiveConstellation:name,available:[...overlays.keys()]});return false;}
      console.info("GV CONSTELLATION GLOW: archive constellation matched",{archiveConstellation:name,overlay:found.name,starPoints:found.points.length,segments:found.segments});
      return startGlow(found,{travel:true});
    }
    const result=Object.freeze({VERSION,get enabled(){return enabled;},setEnabled,setTravelGlow,setTravelGlowAt,setTravelGlowByName,clearTravelGlow:stopGlow,toggle(){return setEnabled(!enabled);},constellationCount:overlays.size,segmentCount:[...overlays.values()].reduce((n,e)=>n+e.segments,0)});
    window.GalaxyViewerConstellations=result;return result;
  }
  window.GalaxyViewerConstellationOverlay=Object.freeze({VERSION,mount});
})();