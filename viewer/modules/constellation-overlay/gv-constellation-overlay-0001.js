/* Galaxy Viewer constellation overlay module 0017.
 * Fornax uses the verified three-star V; glow layers are made visible after each redraw.
 */
(() => {
  "use strict";
  const VERSION = "0020";
  const LINE_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line.csv";
  const STAR_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line_star.csv";
  const COLOR = "#8EDCFF", WIDTH = 0.5, HIGHLIGHT_COLOR = "#AEEBFF", HIGHLIGHT_WIDTH = 0.7;
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
      let e=overlays.get(name);if(!e){e={name,obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),highlight:window.A.graphicOverlay({color:HIGHLIGHT_COLOR,lineWidth:HIGHLIGHT_WIDTH}),segments:0,starIds:new Set(),points:[],segmentPairs:[]};aladin.addOverlay(e.obj);aladin.addOverlay(e.highlight);overlays.set(name,e);}
      const p1=stars.get(a),p2=stars.get(b);
      for(const id of [a,b]){const p=stars.get(id);if(p&&!e.starIds.has(id)){e.starIds.add(id);e.points.push(p);}}
      // Fornax is deliberately rebuilt below from its three principal stars.
      // Ignore catalogue edges for Fornax so no extra segments close or distort the V.
      if(!["FOR","FORNAX"].includes(canon(name))&&p1&&p2){
        e.obj.add(window.A.polyline([p1,p2]));
        e.highlight.add(window.A.polyline([p1,p2],{color:HIGHLIGHT_COLOR,lineWidth:HIGHLIGHT_WIDTH}));
        e.segmentPairs.push([p1,p2]);e.segments++;
      } else if(!["FOR","FORNAX"].includes(canon(name))) {
        console.warn("GV CONSTELLATION: skipped segment with missing star coordinate",{constellation:name,start:a,end:b,hasStart:!!p1,hasEnd:!!p2});
      }
    }
    // The line-source CSV omits principal stars not used by its asterism segments.
    let fornax=[...overlays.values()].find(e=>["FOR","FORNAX"].includes(canon(e.name)));
    if(!fornax){
      fornax={name:"For",obj:window.A.graphicOverlay({color:COLOR,lineWidth:WIDTH}),highlight:window.A.graphicOverlay({color:HIGHLIGHT_COLOR,lineWidth:HIGHLIGHT_WIDTH}),segments:0,starIds:new Set(),points:[],segmentPairs:[]};
      aladin.addOverlay(fornax.obj);aladin.addOverlay(fornax.highlight);overlays.set(fornax.name,fornax);
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
      fornax.highlight.add(window.A.polyline(pair,{color:HIGHLIGHT_COLOR,lineWidth:HIGHLIGHT_WIDTH}));
    }
    console.info("GV CONSTELLATION: Fornax V registered",{stars:fornaxPrincipalStars.map(s=>s.name),edges:2,closed:false});

    // Static line highlight only: no star circles, glow layers, timers, or animation.
    for(const e of overlays.values()){e.obj.hide();e.highlight.hide();}
    let enabled=false,highlightEntry=null;
    function stopGlow(){
      if(highlightEntry){highlightEntry.highlight.hide();if(!enabled)highlightEntry.obj.hide();}
      highlightEntry=null;
    }
    function setEnabled(next){
      enabled=!!next;
      for(const e of overlays.values()){if(enabled)e.obj.show();else e.obj.hide();e.highlight.hide();}
      if(!enabled)stopGlow();
      return enabled;
    }
    function findByName(name){
      const wanted=canon(name);if(!wanted)return null;
      const aliases={
        ANDROMEDA:"AND",ANTLIA:"ANT",APUS:"APS",AQUARIUS:"AQR",AQUILA:"AQL",
        ARIES:"ARI",AURIGA:"AUR",BOOTES:"BOO",CAELUM:"CAE",CAMELOPARDALIS:"CAM",
        CANCER:"CNC",CANESVENATICI:"CVN",CANISMAJOR:"CMA",CANISMINOR:"CMI",
        CAPRICORNUS:"CAP",CARINA:"CAR",CASSIOPEIA:"CAS",CENTAURUS:"CEN",CEPHEUS:"CEP",
        CETUS:"CET",CHAMAELEON:"CHA",CIRCINUS:"CIR",COLUMBA:"COL",COMABERENICES:"COM",
        CORONAAUSTRALIS:"CRA",CORONABOREALIS:"CRB",CORVUS:"CRV",CRATER:"CRT",CRUX:"CRU",
        CYGNUS:"CYG",DELPHINUS:"DEL",DORADO:"DOR",DRACO:"DRA",EQUULEUS:"EQU",ERIDANUS:"ERI",
        FORNAX:"FOR",GEMINI:"GEM",GRUS:"GRU",HERCULES:"HER",HOROLOGIUM:"HOR",HYDRA:"HYA",
        HYDRUS:"HYI",INDUS:"IND",LACERTA:"LAC",LEO:"LEO",LEOMINOR:"LMI",LEPUS:"LEP",LIBRA:"LIB",
        LUPUS:"LUP",LYNX:"LYN",LYRA:"LYR",MENSA:"MEN",MICROSCOPIUM:"MIC",MONOCEROS:"MON",
        MUSCA:"MUS",NORMA:"NOR",OCTANS:"OCT",OPHIUCHUS:"OPH",ORION:"ORI",PAVO:"PAV",
        PEGASUS:"PEG",PERSEUS:"PER",PHOENIX:"PHE",PICTOR:"PIC",PISCES:"PSC",
        PISCISAUSTRINUS:"PSA",PUPPIS:"PUP",PYXIS:"PYX",RETICULUM:"RET",SAGITTA:"SGE",
        SAGITTARIUS:"SGR",SCORPIUS:"SCO",SCULPTOR:"SCL",SCUTUM:"SCT",SERPENS:"SER",
        SEXTANS:"SEX",TAURUS:"TAU",TELESCOPIUM:"TEL",TRIANGULUM:"TRI",
        TRIANGULUMAUSTRALIS:"TRA",TUCANA:"TUC",URSAMAJOR:"UMA",URSAMINOR:"UMI",
        VELA:"VEL",VIRGO:"VIR",VOLANS:"VOL",VULPECULA:"VUL"
      };
      const alternate=aliases[wanted];
      for(const [key,e] of overlays){
        const k=canon(key);
        if(k===wanted||k===alternate||aliases[k]===wanted||aliases[wanted]===k)return e;
      }
      // No substring fallback: it can select a neighboring constellation.
      return null;
    }
    // Highlight the destination with a separate 0.5px static line overlay.
    function startGlow(found,{travel=false}={}){
      stopGlow();
      if(!enabled&&!travel)return false;
      highlightEntry=found;
      found.obj.show();
      found.highlight.show();
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