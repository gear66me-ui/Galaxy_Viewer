from IPython.display import HTML, display

html = r'''
<div id="gv0011-root">
  <style>
    #gv0011-root { box-sizing: border-box; }
    #gv0011-root {
      width: 100%; max-width: 1180px; margin: 0 auto; padding: 14px;
      background: #000000; color: #7FDBFF; font-family: Arial, Helvetica, sans-serif;
      border: 1px solid #0b4f6c; border-radius: 10px;
      box-shadow: 0 0 18px rgba(0, 174, 239, 0.18);
    }
    #gv0011-root h3, #gv0011-root h4 { color: #35c6ff; margin: 12px 0 9px; }
    #gv0011-root .viewer-shell { background:#000; border:1px solid #137aa3; border-radius:8px; overflow:hidden; }
    #gv0011-root .controls { display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-top:14px; }
    #gv0011-root input, #gv0011-root select {
      background:#000; color:#7FDBFF; border:1px solid #169ac7; border-radius:8px;
      padding:12px; font-size:16px; outline:none;
      box-shadow: inset 0 0 8px rgba(0,174,239,.10);
    }
    #gv0011-root input:focus, #gv0011-root select:focus { border-color:#45d5ff; box-shadow:0 0 8px rgba(69,213,255,.35); }
    #gv0011-root select option { background:#000; color:#7FDBFF; }
    #gv0011-root button {
      padding:14px 24px; font-size:17px; font-weight:700; color:#fff; border:0;
      border-radius:9px; cursor:pointer; transition:filter .15s ease, transform .05s ease;
    }
    #gv0011-root button:hover { filter:brightness(1.12); }
    #gv0011-root button:active { transform:translateY(1px); }
    #gv0011-root .fetch-btn { background:#159447; }
    #gv0011-root .find-btn { background:#087fd1; }
    #gv0011-root .status {
      margin-top:12px; padding:11px; background:#02080d; color:#8be0ff;
      border:1px solid #0d668a; border-radius:7px; font-family:monospace; white-space:pre-wrap;
    }
    #gv0011-root .table-wrap { overflow-x:auto; border:1px solid #0b526f; border-radius:8px; background:#000; }
    #gv0011-root table { width:100%; border-collapse:collapse; font-size:14px; background:#000; color:#7FDBFF; }
    #gv0011-root thead tr { background:#031723; }
    #gv0011-root th { color:#43d2ff; font-weight:700; text-align:left; border:1px solid #116482; padding:9px; }
    #gv0011-root td { background:#000; color:#7FDBFF; border:1px solid #0b506b; padding:8px; vertical-align:top; }
    #gv0011-root tbody tr:nth-child(even) td { background:#020b10; }
    #gv0011-root tbody tr:hover td { background:#04141d; }
    #gv0011-root .small-note { margin-top:10px; font-size:12px; color:#61b9d5; line-height:1.45; }
    #gv0011-root .ok { color:#75ff9b; }
    #gv0011-root .warn { color:#ffd166; }
    #gv0011-root .bad { color:#ff7f8b; }
    #gv0011-root .debug-wrap {
      margin-top: 14px; border:1px solid #0b526f; border-radius:8px; background:#000; overflow:hidden;
    }
    #gv0011-root .debug-head {
      padding:10px 12px; background:#031723; color:#43d2ff; font-weight:700; border-bottom:1px solid #116482;
    }
    #gv0011-root .debug-box {
      margin: 0; padding: 12px; white-space: pre-wrap; word-break: break-word;
      font-family: Consolas, Menlo, Monaco, monospace; font-size: 12px; line-height: 1.45;
      color: #9fe8ff; min-height: 180px;
    }
  </style>

  <h3>Galaxy Viewer — GV-0046</h3>
  <div class="viewer-shell">
    <div id="aladin-lite-div" style="width:100%;height:520px;"></div>
  </div>

  <div class="controls">
    <button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button>
    <input id="coordBox" type="text" value="10.684708 41.268750" style="min-width:280px" />
    <button class="find-btn" onclick="findGalaxy()">Find Galaxy / Star</button>
  </div>

  <div class="controls">
    <label for="surveySelect">Displayed survey:</label>
    <select id="surveySelect" onchange="changeSurvey()"></select>
  </div>

  <div id="status" class="status">Viewer loading…</div>

  <h4>Object figures of merit</h4>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Object name</th>
          <th>ICRS coordinates (RA Dec)</th>
          <th>Distance (light-years)</th>
          <th>Object size</th>
          <th>Galaxy age</th>
          <th>Z</th>
          <th>SIMBAD information</th>
        </tr>
      </thead>
      <tbody id="resultBody">
        <tr><td colspan="7" style="text-align:center">No search performed.</td></tr>
      </tbody>
    </table>
  </div>

  <h4>Catalog and survey search status</h4>
  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>Service</th><th>Query / survey</th><th>Search status</th></tr>
      </thead>
      <tbody id="searchBody"></tbody>
    </table>
  </div>

  <div class="debug-wrap">
    <div class="debug-head">Plain-text debug output</div>
    <pre id="debugOutput" class="debug-box">No debug output yet.</pre>
  </div>

  <div class="small-note">
    GV-0046 preserves the current viewer position, survey, and field of view in browser storage so switching tabs does not snap the viewer back to Andromeda. SIMBAD is queried with a 30-arcsecond cone and the first returned SIMBAD row is used as the displayed primary object.
  </div>
</div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
window.onerror=function(message,source,line,col,error){
  try{ if(typeof setStatus==="function"){ setStatus("JS ERROR\n\n"+message+"\nLine: "+line+"\nColumn: "+col); } }catch(e){}
  return false;
};
window.onunhandledrejection=function(event){
  try{ if(typeof setStatus==="function"){ setStatus("PROMISE ERROR\n\n"+String(event.reason)); } }catch(e){}
};

const SURVEYS = [
  {name:"DSS2 Color", id:"P/DSS2/color"},
  {name:"DSS2 Red", id:"P/DSS2/red"},
  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},
  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},
  {name:"2MASS Color", id:"P/2MASS/color"},
  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"}
];

const CATALOGS = ["SIMBAD", "NED", "VizieR", "SDSS", "PanSTARRS", "GALEX"];
const DEBUG_KEYS = [
  "main_id","name","id","otype","sp_type","rvz_redshift","separation",
  "ra","dec","RAJ2000","DEJ2000","galdim_majaxis","galdim_minaxis",
  "D25","d25","logD25","MajAxis","MinAxis","MajorAxis","MinorAxis",
  "Distance_Mpc","distance_mpc","Redshift_Independent_Distance_Mpc","distance","Distance"
];
const VIEWER_STATE_KEY = "galaxy-viewer-gv0046-state";

function safe(v) {
  return String(v ?? "").replace(/[&<>\"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
function cleanId(v) {
  return String(v ?? "").replace(/^b['\"]|['\"]$/g,"").trim();
}
function defaultViewerState() {
  return {
    ra: 10.684708,
    dec: 41.268750,
    survey: "P/DSS2/color",
    fov: 1.0
  };
}
function loadViewerState() {
  try {
    const raw = localStorage.getItem(VIEWER_STATE_KEY);
    if (!raw) return defaultViewerState();
    const parsed = JSON.parse(raw);
    return {
      ra: Number.isFinite(Number(parsed?.ra)) ? Number(parsed.ra) : defaultViewerState().ra,
      dec: Number.isFinite(Number(parsed?.dec)) ? Number(parsed.dec) : defaultViewerState().dec,
      survey: typeof parsed?.survey === "string" && parsed.survey ? parsed.survey : defaultViewerState().survey,
      fov: Number.isFinite(Number(parsed?.fov)) && Number(parsed.fov) > 0 ? Number(parsed.fov) : defaultViewerState().fov
    };
  } catch(err) {
    return defaultViewerState();
  }
}
function saveViewerState(override={}) {
  try {
    const current = captureViewerState();
    const nextState = {
      ...defaultViewerState(),
      ...current,
      ...override
    };
    localStorage.setItem(VIEWER_STATE_KEY, JSON.stringify(nextState));
    return nextState;
  } catch(err) {
    return defaultViewerState();
  }
}
function captureViewerState() {
  const fallback = loadViewerState();
  let ra = fallback.ra;
  let dec = fallback.dec;

  try {
    if (window.aladin && typeof window.aladin.getRaDec === "function") {
      const got = window.aladin.getRaDec();
      if (Array.isArray(got) && Number.isFinite(Number(got[0])) && Number.isFinite(Number(got[1]))) {
        ra = Number(got[0]);
        dec = Number(got[1]);
      }
    }
  } catch(err) {}

  if (!(Number.isFinite(ra) && Number.isFinite(dec))) {
    try {
      const parsed = parseCoords(document.getElementById("coordBox")?.value || `${fallback.ra.toFixed(6)} ${fallback.dec.toFixed(6)}`);
      ra = parsed.ra;
      dec = parsed.dec;
    } catch(err) {
      ra = fallback.ra;
      dec = fallback.dec;
    }
  }

  let fov = fallback.fov;
  try {
    if (window.aladin && typeof window.aladin.getFov === "function") {
      const got = Number(window.aladin.getFov());
      if (Number.isFinite(got) && got > 0) fov = got;
    }
  } catch(err) {}

  const survey = document.getElementById("surveySelect")?.value || fallback.survey;
  return { ra, dec, survey, fov };
}
function formatCoords(ra, dec) {
  return `${Number(ra).toFixed(6)} ${Number(dec).toFixed(6)}`;
}
function restoreViewerState(reason="") {
  if (!window.aladin) return;
  const state = loadViewerState();
  try {
    document.getElementById("coordBox").value = formatCoords(state.ra, state.dec);
    document.getElementById("surveySelect").value = state.survey;
    window.aladin.gotoRaDec(state.ra, state.dec);
    if (typeof window.aladin.setFoV === "function" && Number.isFinite(state.fov) && state.fov > 0) {
      window.aladin.setFoV(state.fov);
    }
    window.aladin.setImageSurvey(state.survey);
    if (reason) setStatus(reason);
  } catch(err) {
    if (reason) setStatus(reason + " (restore warning: " + err.message + ")");
  }
}
function setStatus(text) { document.getElementById("status").textContent = text; }
function setSearchStatus(name, text, cls="") {
  const cell = document.getElementById("status-" + name.replace(/[^A-Za-z0-9]/g,""));
  if (cell) { cell.textContent = text; cell.className = cls; }
}
function setDebugText(text) {
  document.getElementById("debugOutput").textContent = text;
}
function setPendingResult(message) {
  document.getElementById("resultBody").innerHTML = `<tr><td colspan="7" style="text-align:center">${safe(message)}</td></tr>`;
}
function setupControlsAndLog() {
  const select = document.getElementById("surveySelect");
  select.innerHTML = SURVEYS.map(s => `<option value="${safe(s.id)}">${safe(s.name)}</option>`).join("");
  const catalogRows = CATALOGS.map(name => `<tr><td>${safe(name)}</td><td>30 arcsec cone search</td><td id="status-${name.replace(/[^A-Za-z0-9]/g,"")}">Ready</td></tr>`);
  const surveyRows = SURVEYS.map((s,i) => `<tr><td>Aladin HiPS</td><td><span style="font-family:monospace">${safe(s.id)}</span></td><td id="surveyStatus${i}">Ready</td></tr>`);
  document.getElementById("searchBody").innerHTML = catalogRows.concat(surveyRows).join("");
}
(async () => {
  setupControlsAndLog();
  const initialState = loadViewerState();
  document.getElementById("coordBox").value = formatCoords(initialState.ra, initialState.dec);
  document.getElementById("surveySelect").value = initialState.survey;
  try {
    await A.init;
    window.aladin = A.aladin("#aladin-lite-div", {
      target: formatCoords(initialState.ra, initialState.dec),
      survey: initialState.survey,
      fov: initialState.fov,
      cooFrame: "ICRS",
      showReticle: true,
      showZoomControl: true,
      showFullscreenControl: true,
      showLayersControl: true,
      showGotoControl: true,
      showCooGridControl: true,
      showSimbadPointerControl: true
    });
    restoreViewerState("Viewer ready. Restored last saved view.");
    setDebugText("Viewer ready. Press Find Galaxy / Star to print raw catalog responses in plain text.");
    saveViewerState();
  } catch(err) {
    setStatus("Viewer initialization failed: " + err.message);
  }
})();

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    saveViewerState();
  } else {
    restoreViewerState("Viewer restored from saved tab state.");
  }
});
window.addEventListener("pagehide", () => saveViewerState());
window.addEventListener("beforeunload", () => saveViewerState());
window.addEventListener("blur", () => saveViewerState());

function fetchCoords() {
  if (!window.aladin) return setStatus("Viewer is not ready yet.");
  const c = window.aladin.getRaDec();
  const text = c[0].toFixed(6) + " " + c[1].toFixed(6);
  document.getElementById("coordBox").value = text;
  saveViewerState({ra:c[0], dec:c[1]});
  setStatus("Coordinates fetched: " + text);
}
function changeSurvey() {
  if (!window.aladin) return;
  const id = document.getElementById("surveySelect").value;
  setStatus("Loading survey: " + id);
  try {
    window.aladin.setImageSurvey(id);
    saveViewerState({survey:id});
    setStatus("Loaded survey: " + id);
  } catch (err) {
    setStatus("Survey failed: " + err.message);
  }
}
function parseCoords(text) {
  const p = text.trim().split(/[\s,]+/).map(Number);
  if (p.length < 2 || !Number.isFinite(p[0]) || !Number.isFinite(p[1])) throw new Error("Enter decimal ICRS coordinates as RA Dec.");
  return {ra:p[0], dec:p[1]};
}
function fmt(value, digits=3) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString(undefined,{maximumFractionDigits:digits}) : "Not available";
}
function angularSizeLy(arcsec, distanceLy) {
  const a = Number(arcsec), d = Number(distanceLy);
  if (!Number.isFinite(a) || !Number.isFinite(d)) return null;
  return d * a / 206264.806;
}
function distanceFromZ(z){
  const zz=Number(z);
  if(!Number.isFinite(zz)||zz<=0) return null;
  const H0=67.4, OMEGA_M=0.315, OMEGA_L=0.685, C=299792.458, N=4000;
  let integral=0.0;
  for(let i=0;i<N;i++){
      const zp=(i+0.5)*zz/N;
      const Ez=Math.sqrt(OMEGA_M*Math.pow(1+zp,3)+OMEGA_L);
      integral+=1.0/Ez;
  }
  integral*=zz/N;
  return (C/H0)*integral*3261563.777;
}
function distanceFromNed(ned) {
  try {
    const LY_PER_MPC = 3261563.777;
    if (!ned) return null;
    const rows = Array.isArray(ned?.data) ? ned.data : Array.isArray(ned) ? ned : [];
    for (const row of rows) {
      const dMpc =
        Number(row.Distance_Mpc) || Number(row.distance_mpc) ||
        Number(row.Redshift_Independent_Distance_Mpc) || Number(row.redshift_independent_distance_mpc) ||
        Number(row.distance) || Number(row.Distance);
      if (Number.isFinite(dMpc) && dMpc > 0) return dMpc * LY_PER_MPC;
    }
    const payloadText = JSON.stringify(ned);
    const match = payloadText.match(/(\d+(?:\.\d+)?)\s*(?:Mpc|mpc)/);
    if (match) return Number(match[1]) * LY_PER_MPC;
    return null;
  } catch (err) {
    return null;
  }
}
function sizeText(majorArcsec, minorArcsec, distanceLy) {
  const maj=Number(majorArcsec), min=Number(minorArcsec);
  if (!Number.isFinite(maj)||!Number.isFinite(distanceLy)) return "Not available";
  const majLy=distanceLy*maj/206264.806;
  if (Number.isFinite(min)) return `${fmt(majLy,0)} × ${fmt(distanceLy*min/206264.806,0)} ly (${fmt(maj,2)} × ${fmt(min,2)} arcsec)`;
  return `${fmt(majLy,0)} ly (${fmt(maj,2)} arcsec)`;
}
async function fetchJSON(url, options={}) {
  const response=await fetch(url, options);
  if(!response.ok) throw new Error("HTTP " + response.status);
  return await response.json();
}
async function querySimbad(ra,dec) {
  const radius=30/3600;
  const adql=`SELECT TOP 20 main_id,ra,dec,rvz_redshift,galdim_majaxis,galdim_minaxis,otype,sp_type,DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',${ra},${dec})) AS separation FROM basic WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',${ra},${dec},${radius})) ORDER BY separation ASC`;
  const url="https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query="+encodeURIComponent(adql);
  const payload=await fetchJSON(url);
  if(!payload.data||payload.data.length===0) return [];
  return payload.data.map(r => {
    const row={};
    payload.metadata.forEach((m,i)=>row[m.name]=r[i]);
    return row;
  });
}
async function probeNed(ra,dec) {
  const url=`https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&of=json_basic&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.5`;
  return await fetchJSON(url);
}
async function probeVizier(ra,dec) {
  const url=`https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?request=doQuery&lang=adql&format=json&query=${encodeURIComponent(`SELECT TOP 5 * FROM "VII/258/vv10" WHERE 1=CONTAINS(POINT('ICRS',RAJ2000,DEJ2000),CIRCLE('ICRS',${ra},${dec},0.0083333333))`)}`;
  return await fetchJSON(url);
}
async function probeSdss(ra,dec) {
  const cmd=`SELECT TOP 1 p.objid,p.ra,p.dec,p.type,p.u,p.g,p.r,p.i,p.z FROM PhotoObj AS p JOIN dbo.fGetNearbyObjEq(${ra},${dec},0.5) AS n ON p.objid=n.objid ORDER BY n.distance`;
  return await fetchJSON("https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=json&cmd="+encodeURIComponent(cmd));
}
async function probePanStarrs(ra,dec) {
  return await fetchJSON(`https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr2/mean.json?ra=${ra}&dec=${dec}&radius=0.0083333333&nDetections.gte=1&pagesize=1`);
}
async function probeGalex(ra,dec) {
  const request={service:"Mast.Catalogs.Galex.Cone",params:{ra,dec,radius:0.0083333333},format:"json",pagesize:1,page:1};
  const form=new URLSearchParams(); form.append("request",JSON.stringify(request));
  return await fetchJSON("https://mast.stsci.edu/api/v0/invoke",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:form.toString()});
}
function extractRows(payload) {
  if (!payload) return [];
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload)) return payload;
  return [];
}
function parseNumberFromAny(row, names) {
  for (const name of names) {
    const v = Number(row?.[name]);
    if (Number.isFinite(v) && v > 0) return v;
  }
  return null;
}
function resolveWholeGalaxySize(primaryRow, ned, vizier, distanceLy) {
  const candidates = [];
  const maj = Number(primaryRow?.galdim_majaxis);
  const min = Number(primaryRow?.galdim_minaxis);
  if (Number.isFinite(maj) && maj > 0) {
    candidates.push({source:"SIMBAD", majorArcsec:maj, minorArcsec:Number.isFinite(min) ? min : null, quality: maj >= 30 ? 70 : maj >= 10 ? 35 : 5});
  }
  for (const row of extractRows(vizier)) {
    const majArcmin = parseNumberFromAny(row, ["D25", "d25", "logD25"]);
    if (Number.isFinite(majArcmin) && majArcmin > 1) {
      candidates.push({source:"VizieR", majorArcsec:majArcmin*60, minorArcsec:null, quality:95});
    }
    const majArcsec = parseNumberFromAny(row, ["MajAxis", "majAxis", "a", "Dia", "diam", "diameter", "Ddiam"]);
    const minArcsec = parseNumberFromAny(row, ["MinAxis", "minAxis", "b"]);
    if (Number.isFinite(majArcsec) && majArcsec > 5) {
      candidates.push({source:"VizieR", majorArcsec:majArcsec, minorArcsec:minArcsec, quality:majArcsec >= 30 ? 90 : 45});
    }
  }
  for (const row of extractRows(ned)) {
    const majArcsec = parseNumberFromAny(row, ["MajorAxis", "major_axis", "diameter_arcsec", "DIA_MAJOR", "Diamajor"]);
    const minArcsec = parseNumberFromAny(row, ["MinorAxis", "minor_axis", "DIAMINOR", "Diaminor"]);
    if (Number.isFinite(majArcsec) && majArcsec > 5) {
      candidates.push({source:"NED", majorArcsec:majArcsec, minorArcsec:minArcsec, quality:majArcsec >= 30 ? 100 : 50});
    }
  }
  const filtered = candidates.filter(c => {
    if (!Number.isFinite(c.majorArcsec) || c.majorArcsec <= 0) return false;
    const majorLy = angularSizeLy(c.majorArcsec, distanceLy);
    if (Number.isFinite(distanceLy) && Number(distanceLy) > 5e7 && Number.isFinite(majorLy) && majorLy < 5000) return false;
    if (Number.isFinite(distanceLy) && Number(distanceLy) > 1e6 && c.majorArcsec < 3) return false;
    return true;
  });
  if (filtered.length === 0) return null;
  filtered.sort((a,b) => (b.quality - a.quality) || (b.majorArcsec - a.majorArcsec));
  return filtered[0];
}
function summarizeTopSimbadCandidate(rows, requested, ned=null, vizier=null) {
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const primary = {...rows[0]};
  primary._candidateCount = rows.length;
  primary._selectionRule = "SIMBAD row 1";
  let distanceLy = distanceFromZ(primary.rvz_redshift);
  if (!Number.isFinite(distanceLy) || distanceLy === null) distanceLy = distanceFromNed(ned);
  const size = resolveWholeGalaxySize(primary, ned, vizier, distanceLy);
  if (size) {
    primary.galdim_majaxis = size.majorArcsec;
    primary.galdim_minaxis = size.minorArcsec;
    primary._sizeSource = size.source;
  } else {
    primary._sizeSource = "Unavailable";
  }
  return primary;
}
function renderResult(obj, requested, ned=null) {
  const body=document.getElementById("resultBody");
  if(!obj){
    body.innerHTML=`<tr><td colspan="7" style="text-align:center">No SIMBAD object found within 30 arcseconds of ${safe(requested.ra.toFixed(6)+" "+requested.dec.toFixed(6))}</td></tr>`;
    return;
  }
  const z=Number(obj.rvz_redshift);
  let distanceLy=distanceFromZ(z);
  if(!Number.isFinite(distanceLy) || distanceLy===null) distanceLy=distanceFromNed(ned);
  const coords=Number(obj.ra).toFixed(6)+" "+Number(obj.dec).toFixed(6);
  const name=cleanId(obj.main_id||"Not available");
  const sizeSource = obj._sizeSource ? `Size source: ${obj._sizeSource}` : null;
  const selectionRule = obj._selectionRule ? `Selection: ${obj._selectionRule}` : null;
  const info=[obj.otype?"Type: "+obj.otype:null,obj.sp_type?"Spectrum: "+obj.sp_type:null,sizeSource,selectionRule,obj._candidateCount?`Candidates: ${obj._candidateCount}`:null].filter(Boolean).join("; ") || "No additional SIMBAD classification";

  let distanceText = "Not available";
  if (distanceLy) {
    distanceText = fmt(distanceLy,0) + " ly";
    distanceText += (Number.isFinite(z) && z > 0) ? " (redshift estimate)" : " (catalog distance)";
  }

  let zText = "Not available";
  if (Number.isFinite(z)) {
    zText = `${z.toFixed(6)}`;
    if (distanceLy && z > 0) zText += `<br><span style="color:#8be0ff">${(distanceLy/1e9).toFixed(3)} billion ly</span>`;
  }

  body.innerHTML=`<tr><td>${safe(name)}</td><td style="font-family:monospace">${safe(coords)}</td><td>${distanceText}</td><td>${safe(sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td><td>Not available in SIMBAD</td><td>${zText}</td><td>${safe(info)}</td></tr>`;
}
async function runCatalog(name, fn) {
  setSearchStatus(name,"Searching…","warn");
  try {
    const data=await fn();
    const count=Array.isArray(data)?data.length:(data&&Array.isArray(data.data)?data.data.length:null);
    setSearchStatus(name,count===0?"No match":"Query completed","ok");
    return data;
  } catch(err){
    setSearchStatus(name,"Unavailable: "+err.message,"bad");
    return null;
  }
}
async function scanSurveys() {
  const surveyLog = [];
  for(let i=0;i<SURVEYS.length;i++){
    const cell=document.getElementById("surveyStatus"+i); cell.textContent="Loading…"; cell.className="warn";
    try {
      window.aladin.setImageSurvey(SURVEYS[i].id);
      await new Promise(r=>setTimeout(r,220));
      cell.textContent="Available / searched"; cell.className="ok";
      surveyLog.push({survey:SURVEYS[i].id, status:"Available / searched"});
    }
    catch(err){
      cell.textContent="Unavailable"; cell.className="bad";
      surveyLog.push({survey:SURVEYS[i].id, status:"Unavailable", error:String(err?.message || err)});
    }
  }
  window.aladin.setImageSurvey(document.getElementById("surveySelect").value);
  saveViewerState();
  return surveyLog;
}
function formatDebugSection(title, payload) {
  let out = `${title}\n`;
  out += `${"=".repeat(title.length)}\n`;
  if (payload === null || payload === undefined) return out + "status: no data\n\n";

  const rows = Array.isArray(payload?.data) ? payload.data : (Array.isArray(payload) ? payload : null);
  if (rows) {
    out += `rows returned: ${rows.length}\n`;
    if (rows.length === 0) return out + "\n";
    rows.slice(0,3).forEach((row, idx) => {
      out += `row ${idx+1}:\n`;
      const keys = Object.keys(row).filter(k => DEBUG_KEYS.includes(k) || /ra|dec|dist|axis|diam|redshift|type|name|id/i.test(k));
      const chosen = keys.length ? keys.slice(0,16) : Object.keys(row).slice(0,16);
      chosen.forEach(k => {
        const v = row[k];
        out += `- ${k}: ${typeof v === 'object' ? JSON.stringify(v) : String(v)}\n`;
      });
    });
    return out + "\n";
  }

  const keys = Object.keys(payload);
  out += `object keys: ${keys.length}\n`;
  keys.slice(0,20).forEach(k => {
    const v = payload[k];
    out += `- ${k}: ${typeof v === 'object' ? JSON.stringify(v).slice(0,220) : String(v)}\n`;
  });
  return out + "\n";
}
function buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, finalSummary) {
  let text = `DEBUG DUMP FOR ${coords.ra.toFixed(6)} ${coords.dec.toFixed(6)}\n`;
  text += `${"#".repeat(54)}\n\n`;
  if (finalSummary) {
    text += "FINAL SUMMARY\n";
    text += "=============\n";
    text += `picked name: ${cleanId(finalSummary.main_id)}\n`;
    text += `otype: ${String(finalSummary.otype ?? "")}\n`;
    text += `redshift: ${String(finalSummary.rvz_redshift ?? "")}\n`;
    text += `major axis arcsec: ${String(finalSummary.galdim_majaxis ?? "")}\n`;
    text += `minor axis arcsec: ${String(finalSummary.galdim_minaxis ?? "")}\n`;
    text += `size source: ${String(finalSummary._sizeSource ?? "")}\n`;
    text += `selection rule: ${String(finalSummary._selectionRule ?? "")}\n`;
    text += `candidates: ${String(finalSummary._candidateCount ?? "")}\n\n`;
  }
  text += formatDebugSection("SIMBAD", simbadRows);
  text += formatDebugSection("NED", ned);
  text += formatDebugSection("VizieR", vizier);
  text += formatDebugSection("SDSS", sdss);
  text += formatDebugSection("PanSTARRS", panstarrs);
  text += formatDebugSection("GALEX", galex);
  text += formatDebugSection("SURVEY LOAD LOG", surveyLog || []);
  return text;
}
async function findGalaxy() {
  try {
    if(!window.aladin) throw new Error("Viewer is not ready.");
    const coords=parseCoords(document.getElementById("coordBox").value);
    setPendingResult("Waiting for final catalog aggregation…");
    setStatus("Searching SIMBAD, NED, VizieR, SDSS, PanSTARRS, GALEX, and configured surveys at "+coords.ra.toFixed(6)+" "+coords.dec.toFixed(6)+" …");
    setDebugText("Search started… gathering raw catalog payloads.");
    window.aladin.gotoRaDec(coords.ra,coords.dec);
    saveViewerState({ra:coords.ra, dec:coords.dec});

    const simbadPromise=runCatalog("SIMBAD",()=>querySimbad(coords.ra,coords.dec));
    const nedPromise=runCatalog("NED",()=>probeNed(coords.ra,coords.dec));
    const vizierPromise=runCatalog("VizieR",()=>probeVizier(coords.ra,coords.dec));
    const sdssPromise=runCatalog("SDSS",()=>probeSdss(coords.ra,coords.dec));
    const panstarrsPromise=runCatalog("PanSTARRS",()=>probePanStarrs(coords.ra,coords.dec));
    const galexPromise=runCatalog("GALEX",()=>probeGalex(coords.ra,coords.dec));
    const surveyPromise=scanSurveys();

    setStatus("Catalog queries in flight… waiting for final aggregation before populating the Object figures table.");

    const [simbadRows,ned,vizier,sdss,panstarrs,galex,surveyLog] = await Promise.all([
      simbadPromise, nedPromise, vizierPromise, sdssPromise, panstarrsPromise, galexPromise, surveyPromise
    ]);

    setStatus("All catalog responses returned. Using SIMBAD row 1 as the displayed primary object…");
    const finalSummary=summarizeTopSimbadCandidate(simbadRows,coords,ned,vizier);
    renderResult(finalSummary,coords,ned);
    setDebugText(buildDebugDump(coords, simbadRows, ned, vizier, sdss, panstarrs, galex, surveyLog, finalSummary));
    saveViewerState();
    setStatus("Search complete. GV-0046 used the first SIMBAD row from the 30-arcsecond cone search and kept your current view.");
  } catch(err){
    setStatus("Search failed: "+err.message);
    setDebugText("Search failed.\n\n" + String(err?.stack || err));
  }
}
</script>
'''

display(HTML(html))