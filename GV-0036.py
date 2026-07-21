# GV-0036
# Galaxy Viewer — GV-0036

from google.colab import output
from IPython.display import display, HTML, Javascript

output.no_vertical_scroll()

display(Javascript("""
google.colab.output.setIframeHeight(0, true, {
    maxHeight: 7000
});
"""))

html = r"""
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
  #gv0011-root .tiny { font-size:12px; color:#8ecfe4; }
  #gv0011-root .mono { font-family:monospace; white-space:pre-wrap; word-break:break-word; }
</style>

<div id="gv0011-root">
  <h3>Galaxy Viewer — GV-0036</h3>
  <div class="viewer-shell">
    <div id="aladin-lite-div" style="width:100%;height:700px;border:1px solid #444;overflow:hidden;"></div>
  </div>

  <div class="controls">
    <input id="coordBox" type="text" value="10.684708 41.268750" style="flex:1;min-width:280px" aria-label="ICRS coordinates">
    <button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button>
    <button class="find-btn" onclick="findGalaxy()">Find Galaxy</button>
  </div>

  <div class="controls" style="margin-top:12px">
    <b style="color:#35c6ff">Displayed survey:</b>
    <input id="surveyBox" type="text" placeholder="Enter HiPS survey ID (example: P/DSS2/color)" style="min-width:420px;flex:1">
    <button class="find-btn" onclick="loadSurvey()">Load Survey</button>
    <select id="surveySelect" onchange="changeSurvey()" style="min-width:300px"></select>
  </div>

  <div id="status" class="status">Initializing viewer…</div>

  <h4>Galaxy figures of merit</h4>
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th>Galaxy name</th><th>ICRS coordinates (RA Dec)</th><th>Distance (light-years)</th>
        <th>Galaxy size</th><th>Galaxy age</th><th>Z</th><th>SIMBAD information</th>
      </tr></thead>
      <tbody id="resultBody"><tr><td colspan="7" style="text-align:center">No search performed.</td></tr></tbody>
    </table>
  </div>

  <h4>Catalog and survey search status</h4>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Service</th><th>Query / survey</th><th>Search status</th></tr></thead>
      <tbody id="searchBody"></tbody>
    </table>
  </div>

  <h4>Raw catalog values fetched</h4>
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th>Service</th><th>Row</th><th>Object / ID</th><th>Type / class</th><th>RA</th><th>Dec</th>
        <th>Z / distance</th><th>Major axis</th><th>Minor axis</th><th>Notes / raw excerpt</th>
      </tr></thead>
      <tbody id="rawDataBody"><tr><td colspan="10" style="text-align:center">No raw catalog data captured yet.</td></tr></tbody>
    </table>
  </div>

  <div class="small-note">
    This revision adds a raw-data inspection table so we can see exactly what each catalog returned before choosing a final galaxy candidate. Whole-galaxy size still prefers larger diameter measurements from returned catalog data and rejects obviously nuclear/component-sized values when possible.
  </div>
</div>

<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.css">
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

function safe(v) {
  return String(v ?? "").replace(/[&<>\"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
function cleanId(v) {
  return String(v ?? "").replace(/^b['\"]|['\"]$/g,"").trim();
}
function setStatus(text) { document.getElementById("status").textContent = text; }
function setSearchStatus(name, text, cls="") {
  const cell = document.getElementById("status-" + name.replace(/[^A-Za-z0-9]/g,""));
  if (cell) { cell.textContent = text; cell.className = cls; }
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
  try {
    await A.init;
    window.aladin = A.aladin("#aladin-lite-div", {
      target: "M31",
      survey: "P/DSS2/color",
      fov: 1.0,
      cooFrame: "ICRS",
      showReticle: true,
      showZoomControl: true,
      showFullscreenControl: true,
      showLayersControl: true,
      showGotoControl: true,
      showCooGridControl: true,
      showSimbadPointerControl: true
    });
    setStatus("Viewer ready.");
  } catch(err) {
    setStatus("Viewer initialization failed: " + err.message);
  }
})();

function fetchCoords() {
  if (!window.aladin) return setStatus("Viewer is not ready yet.");
  const c = window.aladin.getRaDec();
  const text = c[0].toFixed(6) + " " + c[1].toFixed(6);
  document.getElementById("coordBox").value = text;
  setStatus("Coordinates fetched: " + text);
}
function loadSurvey() {
  if (!window.aladin) return;
  const id = document.getElementById("surveyBox").value.trim();
  if (!id) return;
  setStatus("Loading survey: " + id);
  try {
    window.aladin.setImageSurvey(id);
    setStatus("Loaded survey: " + id);
  } catch (err) {
    setStatus("Survey failed: " + err.message);
  }
}
function changeSurvey() {
  if (!window.aladin) return;
  const id = document.getElementById("surveySelect").value;
  setStatus("Loading survey: " + id);
  try {
    window.aladin.setImageSurvey(id);
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
  const url=`https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?request=doQuery&lang=adql&format=json&query=${encodeURIComponent(`SELECT TOP 5 * FROM \"VII/258/vv10\" WHERE 1=CONTAINS(POINT('ICRS',RAJ2000,DEJ2000),CIRCLE('ICRS',${ra},${dec},0.0083333333))`)}`;
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
function scoreGalaxyCandidate(row) {
  let score = 0;
  const id = cleanId(row.main_id).toUpperCase();
  const otype = String(row.otype ?? "").trim().toUpperCase();
  const sep = Number(row.separation);
  const maj = Number(row.galdim_majaxis);

  if (/^(M\s*\d+|MESSIER\s*\d+|NGC\s*\d+|IC\s*\d+)$/.test(id)) score += 120;
  if (otype === "G") score += 150;
  else if (otype.startsWith("G")) score += 100;
  else if (["POG","LSB","IG","PAG"].includes(otype)) score += 70;
  if (/AGN|SY1|SY2|LINER|BLLAC|QSO|BLAZAR|SEYFERT|X/.test(otype)) score -= 110;
  if (id.includes("[") || id.includes("LDC") || id.includes("2MASS") || id.includes("GALEX") || id.includes("SDSS") || id.includes("WISE") || id.includes("CLUSTER")) score -= 70;
  if (Number.isFinite(maj)) score += Math.min(maj / 5, 90);
  if (Number.isFinite(sep)) score += Math.max(0, 30 - sep * 3600);
  return score;
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
function resolveWholeGalaxySize(simbadRows, ned, vizier, distanceLy) {
  const candidates = [];

  for (const row of simbadRows || []) {
    const maj = Number(row.galdim_majaxis);
    const min = Number(row.galdim_minaxis);
    if (Number.isFinite(maj) && maj > 0) {
      candidates.push({source:"SIMBAD", majorArcsec:maj, minorArcsec:Number.isFinite(min) ? min : null, quality: maj >= 30 ? 70 : maj >= 10 ? 35 : 5});
    }
  }

  for (const row of extractRows(vizier)) {
    const majArcmin = parseNumberFromAny(row, ["D25", "d25"]);
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
function summarizeGalaxyCandidates(rows, requested, ned=null, vizier=null) {
  if (!Array.isArray(rows) || rows.length === 0) return null;

  const ranked = rows.map(row => ({row, score:scoreGalaxyCandidate(row)})).sort((a,b) => b.score - a.score);
  const bestIdentity = ranked[0]?.row ?? rows[0];
  const bestRedshift = ranked.find(x => Number.isFinite(Number(x.row.rvz_redshift)) && Number(x.row.rvz_redshift) > 0)?.row ?? bestIdentity;
  const bestType = ranked.find(x => !/AGN|SY1|SY2|LINER|BLLAC|QSO|SEYFERT|X/i.test(String(x.row.otype ?? "")))?.row ?? bestIdentity;

  const merged = {...bestIdentity};
  merged.rvz_redshift = bestRedshift.rvz_redshift;
  merged.otype = bestType.otype;
  merged.sp_type = bestType.sp_type;
  merged._candidateCount = rows.length;

  let distanceLy = distanceFromZ(merged.rvz_redshift);
  if (!Number.isFinite(distanceLy) || distanceLy === null) distanceLy = distanceFromNed(ned);

  const size = resolveWholeGalaxySize(rows, ned, vizier, distanceLy);
  if (size) {
    merged.galdim_majaxis = size.majorArcsec;
    merged.galdim_minaxis = size.minorArcsec;
    merged._sizeSource = size.source;
  } else {
    merged._sizeSource = "Unavailable";
  }
  return merged;
}
function renderResult(obj, requested, ned=null) {
  const body=document.getElementById("resultBody");
  if(!obj){
    body.innerHTML=`<tr><td colspan="7" style="text-align:center">No SIMBAD object found within 30 arcseconds of ${safe(requested.ra.toFixed(6)+" "+requested.dec.toFixed(6))}.</td></tr>`;
    return;
  }
  const z=Number(obj.rvz_redshift);
  let distanceLy=distanceFromZ(z);
  if(!Number.isFinite(distanceLy) || distanceLy===null) distanceLy=distanceFromNed(ned);
  const coords=Number(obj.ra).toFixed(6)+" "+Number(obj.dec).toFixed(6);
  const name=cleanId(obj.main_id||"Not available");
  const sizeSource = obj._sizeSource ? `Size source: ${obj._sizeSource}` : null;
  const info=[obj.otype?"Type: "+obj.otype:null,obj.sp_type?"Spectrum: "+obj.sp_type:null,sizeSource,obj._candidateCount?`Candidates: ${obj._candidateCount}`:null].filter(Boolean).join("; ") || "No additional SIMBAD classification";

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
function clearRawDataTable() {
  document.getElementById("rawDataBody").innerHTML = "<tr><td colspan=\"10\" style=\"text-align:center\">Waiting for catalog responses…</td></tr>";
}
function addRawRow(service, idx, objectId, kind, ra, dec, zOrDist, major, minor, note) {
  const body = document.getElementById("rawDataBody");
  const empty = body.querySelector("td[colspan='10']");
  if (empty) body.innerHTML = "";
  body.insertAdjacentHTML("beforeend",
    `<tr>
      <td>${safe(service)}</td>
      <td>${safe(idx)}</td>
      <td>${safe(objectId)}</td>
      <td>${safe(kind)}</td>
      <td class="mono">${safe(ra)}</td>
      <td class="mono">${safe(dec)}</td>
      <td>${safe(zOrDist)}</td>
      <td>${safe(major)}</td>
      <td>${safe(minor)}</td>
      <td class="tiny mono">${safe(note)}</td>
    </tr>`);
}
function excerpt(obj, maxLen=220) {
  try {
    const s = JSON.stringify(obj);
    return s.length > maxLen ? s.slice(0, maxLen) + "…" : s;
  } catch (err) {
    return String(obj);
  }
}
function populateRawTable(service, payload) {
  const rows = extractRows(payload);
  if (!rows.length) {
    addRawRow(service, "-", "No rows", "-", "-", "-", "-", "-", "-", payload ? excerpt(payload) : "No payload");
    return;
  }
  rows.slice(0, 12).forEach((row, i) => {
    let objectId = cleanId(row.main_id || row.Object_Name || row.objname || row.name || row.oid || row.objid || row.designation || row.MatchID || row.id || `row ${i+1}`);
    let kind = row.otype || row.Type || row.type || row.class || row.objType || row.OTYPE || "-";
    let ra = row.ra || row.RA || row.RAJ2000 || row.raMean || row.RAdeg || row.raStack || row.MatchRA || "-";
    let dec = row.dec || row.DEC || row.DEJ2000 || row.decMean || row.DECdeg || row.decStack || row.MatchDec || "-";
    let zOrDist = row.rvz_redshift || row.Redshift || row.redshift || row.Distance || row.distance || row.Distance_Mpc || row.z || "-";
    let major = row.galdim_majaxis || row.MajorAxis || row.major_axis || row.MajAxis || row.D25 || row.diam || row.a || "-";
    let minor = row.galdim_minaxis || row.MinorAxis || row.minor_axis || row.MinAxis || row.b || "-";
    addRawRow(service, String(i+1), objectId, String(kind), String(ra), String(dec), String(zOrDist), String(major), String(minor), excerpt(row));
  });
}
async function runCatalog(name, fn) {
  setSearchStatus(name,"Searching…","warn");
  try {
    const data=await fn();
    const count=Array.isArray(data)?data.length:(data&&Array.isArray(data.data)?data.data.length:null);
    setSearchStatus(name,count===0?"No match":"Query completed","ok");
    populateRawTable(name, data);
    return data;
  } catch(err){
    setSearchStatus(name,"Unavailable: "+err.message,"bad");
    addRawRow(name, "-", "Request failed", "-", "-", "-", "-", "-", "-", String(err.message || err));
    return null;
  }
}
async function scanSurveys() {
  for(let i=0;i<SURVEYS.length;i++){
    const cell=document.getElementById("surveyStatus"+i); cell.textContent="Loading…"; cell.className="warn";
    try { window.aladin.setImageSurvey(SURVEYS[i].id); await new Promise(r=>setTimeout(r,220)); cell.textContent="Available / searched"; cell.className="ok"; }
    catch(err){ cell.textContent="Unavailable"; cell.className="bad"; }
  }
  window.aladin.setImageSurvey(document.getElementById("surveySelect").value);
}
async function findGalaxy() {
  try {
    if(!window.aladin) throw new Error("Viewer is not ready.");
    const coords=parseCoords(document.getElementById("coordBox").value);
    clearRawDataTable();
    document.getElementById("resultBody").innerHTML = '<tr><td colspan="7" style="text-align:center">Collecting catalog values…</td></tr>';
    setStatus("Searching SIMBAD, NED, VizieR, SDSS, PanSTARRS, GALEX, and configured surveys at "+coords.ra.toFixed(6)+" "+coords.dec.toFixed(6)+" …");
    window.aladin.gotoRaDec(coords.ra,coords.dec);

    const simbadPromise=runCatalog("SIMBAD",()=>querySimbad(coords.ra,coords.dec));
    const nedPromise=runCatalog("NED",()=>probeNed(coords.ra,coords.dec));
    const vizierPromise=runCatalog("VizieR",()=>probeVizier(coords.ra,coords.dec));
    const sdssPromise=runCatalog("SDSS",()=>probeSdss(coords.ra,coords.dec));
    const panPromise=runCatalog("PanSTARRS",()=>probePanStarrs(coords.ra,coords.dec));
    const galexPromise=runCatalog("GALEX",()=>probeGalex(coords.ra,coords.dec));
    const surveyPromise=scanSurveys();

    const simbadRows=await simbadPromise;
    const ned=await nedPromise;
    const vizier=await vizierPromise;
    const finalSummary=summarizeGalaxyCandidates(simbadRows,coords,ned,vizier);
    renderResult(finalSummary,coords,ned);

    await Promise.allSettled([sdssPromise, panPromise, galexPromise, surveyPromise]);
    setStatus("Search complete. GV-0036 now shows the raw fetched catalog rows below so we can inspect exactly which values are coming back before tuning the selector.");
  } catch(err){
    setStatus("Search failed: "+err.message);
  }
}
</script>
"""

display(HTML(html))
