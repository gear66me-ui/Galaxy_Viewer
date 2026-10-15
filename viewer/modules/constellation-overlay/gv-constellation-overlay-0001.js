/* Galaxy Viewer constellation overlay module 0017.
 * Fornax uses the verified three-star V; glow layers are made visible after each redraw.
 */
(() => {
  "use strict";
  const VERSION = "0017";
  const LINE_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line.csv";
  const STAR_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line_star.csv";
  const COLOR = "#8EDCFF", WIDTH = 0.5;
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
      let e=overlays.get(name);if(!e){e={name,obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),glow:window.A.graphicOverlay({color:"#39BFFF",lineWidth:0.5}),stars:window.A.graphicOverlay({color:"#FFFFFF",lineWidth:0.5}),segments:0,starIds:new Set(),points:[],segmentPairs:[]};aladin.addOverlay(e.obj);aladin.addOverlay(e.glow);aladin.addOverlay(e.stars);overlays.set(name,e);}
      const p1=stars.get(a),p2=stars.get(b);
      for(const id of [a,b]){const p=stars.get(id);if(p&&!e.starIds.has(id)){e.starIds.add(id);e.points.push(p);}}
      // Fornax is deliberately rebuilt below from its three principal stars.
      // Ignore catalogue edges for Fornax so no extra segments close or distort the V.
      if(!["FOR","FORNAX"].includes(canon(name))&&p1&&p2){
        e.obj.add(window.A.polyline([p1,p2]));
        e.glow.add(window.A.polyline([p1,p2],{color:"#39BFFF",lineWidth:0.5}));
        e.segmentPairs.push([p1,p2]);e.segments++;
      } else if(!["FOR","FORNAX"].includes(canon(name))) {
        console.warn("GV CONSTELLATION: skipped segment with missing star coordinate",{constellation:name,start:a,end:b,hasStart:!!p1,hasEnd:!!p2});
      }
    }
    // The line-source CSV omits principal stars not used by its asterism segments.
    let fornax=[...overlays.values()].find(e=>["FOR","FORNAX"].includes(canon(e.name)));
    if(!fornax){
      fornax={name:"For",obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),glow:window.A.graphicOverlay({color:"#39BFFF",lineWidth:0.5}),stars:window.A.graphicOverlay({color:"#FFFFFF",lineWidth:0.5}),segments:0,starIds:new Set(),points:[],segmentPairs:[]};
      aladin.addOverlay(fornax.obj);aladin.addOverlay(fornax.glow);aladin.addOverlay(fornax.stars);overlays.set(fornax.name,fornax);
    }
    const fornaxPrincipalStars=[
      {name:"Dalim (Alpha Fornacis)",ra:48.018875,dec:-28.9876111111},
      {name:"Beta Fornacis",ra:42.2725833333,dec:-32.4058888889},
      {name:"Nu Fornacis",ra:31.1226666667,dec:-29.2968055556}
    ];
    // The requested Fornax asterism is exactly two thin edges, Dalim—Beta—Nu.
    // Reset the point list so only these three stars receive the Fornax glow.
    fornax.points=fornaxPrincipalStars.map(star=>[star.ra,star.dec]);
    fornax.segmentPairs=[
      [fornax.points[0],fornax.points[1]],
      [fornax.points[1],fornax.points[2]]
    ];
    fornax.segments=2;
    for(const pair of fornax.segmentPairs){
      fornax.obj.add(window.A.polyline(pair,{color:COLOR,lineWidth:WIDTH}));
      fornax.glow.add(window.A.polyline(pair,{color:"#39BFFF",lineWidth:0.5}));
    }
    console.info("GV CONSTELLATION: Fornax V registered",{stars:fornaxPrincipalStars.map(s=>s.name),edges:2,closed:false});

    // Keep the normal map quiet; a separate, wider duplicate overlay creates an actual line halo.
    for(const e of overlays.values()){
      for(const [ra,dec] of e.points){
        try{e.glow.add(window.A.circle([ra,dec],0.075,{color:"#26AFFF",lineWidth:0.5,fillColor:"#26AFFF",fillOpacity:0.28}));e.stars.add(window.A.circle([ra,dec],0.035,{color:"#FFFFFF",lineWidth:0.5,fillColor:"#FFFFFF",fillOpacity:1}));}catch(_){}
      }
      e.obj.hide();e.glow.hide();e.stars.hide();
    }
    let enabled=false,glowEntry=null;
    function stopGlow(){
      if(glowEntry){glowEntry.glow.hide();glowEntry.stars.hide();glowEntry.obj.hide();}
      glowEntry=null;
    }
    function setEnabled(next){
      enabled=!!next;
      for(const e of overlays.values()){
        if(enabled)e.obj.show();else e.obj.hide();
        e.glow.hide();
        if(!enabled)e.stars.hide();
      }
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
    // Static highlight only: no timers, frame callbacks, per-frame rebuilds, or color interpolation.
    function startGlow(found,{travel=false}={}){
      stopGlow();
      if(!enabled&&!travel)return false;
      glowEntry=found;
      found.obj.setOptions?.({color:"#8EDCFF",lineWidth:0.5});
      found.obj.show();
      found.glow.hide();
      found.stars.show();
      return true;
    }
    function setTravelGlow(name,active){
      if(!active||!name){stopGlow();return false;}
      const found=findByName(name);
      if(!found)return false;
      return startGlow(found,{travel:true});
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