from IPython.display import HTML, display

HTML_CONTENT = r"""
<div id="gv0040-root">
  <style>
    #gv0040-root { box-sizing: border-box; }
    #gv0040-root {
      width: 100%; max-width: 1180px; margin: 0 auto; padding: 14px;
      background: #000000; color: #7FDBFF; font-family: Arial, Helvetica, sans-serif;
      border: 1px solid #0b4f6c; border-radius: 10px;
      box-shadow: 0 0 18px rgba(0, 174, 239, 0.18);
    }
    #gv0040-root h3, #gv0040-root h4 { color: #35c6ff; margin: 12px 0 9px; }
    #gv0040-root .viewer-shell { background:#000; border:1px solid #137aa3; border-radius:8px; overflow:hidden; }
    #gv0040-root .controls { display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin-top:14px; }
    #gv0040-root input, #gv0040-root select {
      background:#000; color:#7FDBFF; border:1px solid #169ac7; border-radius:8px;
      padding:12px; font-size:16px; outline:none;
      box-shadow: inset 0 0 8px rgba(0,174,239,.10);
    }
    #gv0040-root input:focus, #gv0040-root select:focus { border-color:#45d5ff; box-shadow:0 0 8px rgba(69,213,255,.35); }
    #gv0040-root select option { background:#000; color:#7FDBFF; }
    #gv0040-root button {
      padding:14px 24px; font-size:17px; font-weight:700; color:#fff; border:0;
      border-radius:9px; cursor:pointer; transition:filter .15s ease, transform .05s ease;
    }
    #gv0040-root button:hover { filter:brightness(1.12); }
    #gv0040-root button:active { transform:translateY(1px); }
    #gv0040-root .fetch-btn { background:#159447; }
    #gv0040-root .find-btn { background:#087fd1; }
    #gv0040-root .status, #gv0040-root .progress-panel {
      margin-top:12px; padding:11px; background:#02080d; color:#8be0ff;
      border:1px solid #0d668a; border-radius:7px; font-family:monospace; white-space:pre-wrap;
    }
    #gv0040-root .table-wrap { overflow-x:auto; border:1px solid #0b526f; border-radius:8px; background:#000; margin-top:8px; }
    #gv0040-root table { width:100%; border-collapse:collapse; font-size:14px; background:#000; color:#7FDBFF; }
    #gv0040-root thead tr { background:#031723; }
    #gv0040-root th { color:#43d2ff; font-weight:700; text-align:left; border:1px solid #116482; padding:9px; }
    #gv0040-root td { background:#000; color:#7FDBFF; border:1px solid #0b506b; padding:8px; vertical-align:top; }
    #gv0040-root tbody tr:nth-child(even) td { background:#020b10; }
    #gv0040-root tbody tr:hover td { background:#04141d; }
    #gv0040-root .small-note { margin-top:10px; font-size:12px; color:#61b9d5; line-height:1.45; }
    #gv0040-root .ok { color:#75ff9b; }
    #gv0040-root .warn { color:#ffd166; }
    #gv0040-root .bad { color:#ff7f8b; }
    #gv0040-root .mono { font-family: monospace; white-space: pre-wrap; word-break: break-word; }
    #gv0040-root .spinner {
      display:inline-block; width:12px; height:12px; margin-right:8px;
      border:2px solid #169ac7; border-top-color:transparent; border-radius:50%;
      animation: gv0040spin 0.9s linear infinite; vertical-align:middle;
    }
    #gv0040-root .spinner.done { border-color:#159447; animation:none; }
    #gv0040-root .spinner.fail { border-color:#ff7f8b; animation:none; }
    #gv0040-root .progress-row { display:flex; align-items:center; justify-content:space-between; gap:10px; }
    #gv0040-root .progress-bar-wrap {
      width:100%; height:14px; border:1px solid #0d668a; border-radius:999px;
      overflow:hidden; background:#000; margin-top:10px;
    }
    #gv0040-root .progress-bar {
      height:100%; width:0%; background:linear-gradient(90deg,#087fd1,#35c6ff);
      transition:width .2s ease;
    }
    @keyframes gv0040spin { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }
  </style>

  <h3>Galaxy Viewer — GV-0040</h3>

  <div class="viewer-shell">
    <div id="aladin-lite-div" style="width:100%;height:560px;"></div>
  </div>

  <div class="controls">
    <input id="coordBox" type="text" value="10.684708 41.268750" style="min-width:280px" />
    <button class="fetch-btn" onclick="gv0040_fetchCoords()">Fetch Coordinates</button>
    <button class="find-btn" onclick="gv0040_findGalaxy()">Find Galaxy</button>
    <select id="surveySelect" onchange="gv0040_changeSurvey()"></select>
  </div>

  <div class="progress-panel">
    <div class="progress-row">
      <div><span id="gv0040-spinner" class="spinner"></span><span id="gv0040-stepLabel">Idle.</span></div>
      <div id="gv0040-stepCount">0 / 7</div>
    </div>
    <div class="progress-bar-wrap"><div id="gv0040-progressBar" class="progress-bar"></div></div>
  </div>

  <div id="status" class="status">Viewer starting…</div>

  <h4>Galaxy figures of merit</h4>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Galaxy name</th>
          <th>ICRS coordinates (RA Dec)</th>
          <th>Distance (light-years)</th>
          <th>Galaxy size</th>
          <th>Galaxy age</th>
          <th>Z</th>
          <th>SIMBAD information</th>
        </tr>
      </thead>
      <tbody id="resultBody">
        <tr><td colspan="7" style="text-align:center">Waiting for search.</td></tr>
      </tbody>
    </table>
  </div>

  <h4>Catalog and survey search status</h4>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Service</th><th>Query / survey</th><th>Search status</th></tr></thead>
      <tbody id="searchBody"></tbody>
    </table>
  </div>

  <h4>SIMBAD raw rows</h4>
  <div id="simbadText" class="status mono">Waiting for SIMBAD rows…</div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>main_id</th>
          <th>otype</th>
          <th>rvz_redshift</th>
          <th>galdim_majaxis</th>
          <th>galdim_minaxis</th>
          <th>separation</th>
        </tr>
      </thead>
      <tbody id="simbadDebugBody">
        <tr><td colspan="7" style="text-align:center">Waiting for SIMBAD rows…</td></tr>
      </tbody>
    </table>
  </div>

  <div class="small-note">
    GV-0040 adds a visible progress bar and step counter so long background work is obvious while the viewer cycles through catalogs and surveys.
  </div>
</div>

<script>
window.onerror = function(message, source, line, col) {
  try { if (typeof gv0040_setStatus === "function") gv0040_setStatus("JS ERROR\n\n" + message + "\nLine: " + line + "\nColumn: " + col); } catch(e) {}
  return false;
};
window.onunhandledrejection = function(event) {
  try { if (typeof gv0040_setStatus === "function") gv0040_setStatus("PROMISE ERROR\n\n" + String(event.reason)); } catch(e) {}
};

const GV0040_SURVEYS = [
  {name:"DSS2 Color", id:"P/DSS2/color"},
  {name:"DSS2 Red", id:"P/DSS2/red"},
  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},
  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},
  {name:"2MASS Color", id:"P/2MASS/color"},
  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"}
];
const GV0040_CATALOGS = ["SIMBAD", "NED", "VizieR", "SDSS", "PanSTARRS", "GALEX"];
const GV0040_TOTAL_STEPS = 7;

function gv0040_safe(v) {
  return String(v ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
function gv0040_cleanId(v) { return String(v ?? "").replace(/^b['\\"]|['\\"]$/g,"").trim(); }
function gv0040_setStatus(text) { document.getElementById("status").textContent = text; }
function gv0040_setSearchStatus(name, text, cls="") {
  const cell = document.getElementById("status-" + name.replace(/[^A-Za-z0-9]/g,""));
  if (cell) { cell.textContent = text; cell.className = cls; }
}
function gv0040_setProgress(completed, label, state="running") {
  const count = document.getElementById("gv0040-stepCount");
  const stepLabel = document.getElementById("gv0040-stepLabel");
  const bar = document.getElementById("gv0040-progressBar");
  const spinner = document.getElementById("gv0040-spinner");
  count.textContent = completed + " / " + GV0040_TOTAL_STEPS;
  stepLabel.textContent = label;
  bar.style.width = Math.max(0, Math.min(100, (completed / GV0040_TOTAL_STEPS) * 100)) + "%";
  spinner.className = "spinner" + (state === "done" ? " done" : state === "fail" ? " fail" : "");
}
function gv0040_setupControlsAndLog() {
  const select = document.getElementById("surveySelect");
  select.innerHTML = GV0040_SURVEYS.map(s => `<option value="${gv0040_safe(s.id)}">${gv0040_safe(s.name)}</option>`).join("");
  const catalogRows = GV0040_CATALOGS.map(name => `<tr><td>${gv0040_safe(name)}</td><td>30 arcsec cone search</td><td id="status-${name.replace(/[^A-Za-z0-9]/g,"")}">Ready</td></tr>`);
  const surveyRows = GV0040_SURVEYS.map((s,i) => `<tr><td>Aladin HiPS</td><td><span style="font-family:monospace">${gv0040_safe(s.id)}</span></td><td id="surveyStatus${i}">Ready</td></tr>`);
  document.getElementById("searchBody").innerHTML = catalogRows.concat(surveyRows).join("");
}
(async () => {
  gv0040_setupControlsAndLog();
  try {
    const waitForA = async () => {
      for (let i = 0; i < 200; i++) {
        if (window.A && A.init) return;
        await new Promise(r => setTimeout(r, 50));
      }
      throw new Error("Aladin library did not load.");
    };
    await waitForA();
    await A.init;
    window.gv0040_aladin = A.aladin("#aladin-lite-div", {
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
    gv0040_setProgress(0, "Viewer ready.", "done");
    gv0040_setStatus("Viewer ready.");
  } catch(err) {
    gv0040_setProgress(0, "Viewer initialization failed.", "fail");
    gv0040_setStatus("Viewer initialization failed: " + err.message);
  }
})();

function gv0040_fetchCoords() {
  if (!window.gv0040_aladin) return gv0040_setStatus("Viewer is not ready yet.");
  const c = window.gv0040_aladin.getRaDec();
  const text = c[0].toFixed(6) + " " + c[1].toFixed(6);
  document.getElementById("coordBox").value = text;
  gv0040_setStatus("Coordinates fetched: " + text);
}
function gv0040_changeSurvey() {
  if (!window.gv0040_aladin) return;
  const id = document.getElementById("surveySelect").value;
  gv0040_setStatus("Loading survey: " + id);
  try {
    window.gv0040_aladin.setImageSurvey(id);
    gv0040_setStatus("Loaded survey: " + id);
  } catch (err) {
    gv0040_setStatus("Survey failed: " + err.message);
  }
}
function gv0040_parseCoords(text) {
  const p = text.trim().split(/[\\s,]+/).map(Number);
  if (p.length < 2 || !Number.isFinite(p[0]) || !Number.isFinite(p[1])) throw new Error("Enter decimal ICRS coordinates as RA Dec.");
  return {ra:p[0], dec:p[1]};
}
function gv0040_fmt(value, digits=3) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString(undefined,{maximumFractionDigits:digits}) : "Not available";
}
function gv0040_distanceFromZ(z){
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
function gv0040_sizeText(majorArcsec, minorArcsec, distanceLy) {
  const maj=Number(majorArcsec), min=Number(minorArcsec);
  if (!Number.isFinite(maj)||!Number.isFinite(distanceLy)) return "Not available";
  const majLy=distanceLy*maj/206264.806;
  if (Number.isFinite(min)) return `${gv0040_fmt(majLy,0)} × ${gv0040_fmt(distanceLy*min/206264.806,0)} ly (${gv0040_fmt(maj,2)} × ${gv0040_fmt(min,2)} arcsec)`;
  return `${gv0040_fmt(majLy,0)} ly (${gv0040_fmt(maj,2)} arcsec)`;
}
async function gv0040_fetchJSON(url, options={}) {
  const response=await fetch(url, options);
  if(!response.ok) throw new Error("HTTP " + response.status);
  return await response.json();
}
async function gv0040_querySimbad(ra,dec) {
  const radius=30/3600;
  const adql=`SELECT TOP 20 main_id,ra,dec,rvz_redshift,galdim_majaxis,galdim_minaxis,otype,sp_type,DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',${ra},${dec})) AS separation FROM basic WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',${ra},${dec},${radius})) ORDER BY separation ASC`;
  const url='https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query='+encodeURIComponent(adql);
  const payload=await gv0040_fetchJSON(url);
  if(!payload.data||payload.data.length===0) return [];
  return payload.data.map(r => {
    const row={};
    payload.metadata.forEach((m,i)=>row[m.name]=r[i]);
    return row;
  });
}
async function gv0040_probeNed(ra,dec) {
  const url=`https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&of=json_basic&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.5`;
  return await gv0040_fetchJSON(url);
}
async function gv0040_probeVizier(ra,dec) {
  const url=`https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?request=doQuery&lang=adql&format=json&query=${encodeURIComponent(`SELECT TOP 5 * FROM "VII/258/vv10" WHERE 1=CONTAINS(POINT('ICRS',RAJ2000,DEJ2000),CIRCLE('ICRS',${ra},${dec},0.0083333333))`)}`;
  return await gv0040_fetchJSON(url);
}
async function gv0040_probeSdss(ra,dec) {
  const cmd=`SELECT TOP 1 p.objid,p.ra,p.dec,p.type,p.u,p.g,p.r,p.i,p.z FROM PhotoObj AS p JOIN dbo.fGetNearbyObjEq(${ra},${dec},0.5) AS n ON p.objid=n.objid ORDER BY n.distance`;
  return await gv0040_fetchJSON('https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=json&cmd='+encodeURIComponent(cmd));
}
async function gv0040_probePanStarrs(ra,dec) {
  return await gv0040_fetchJSON(`https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr2/mean.json?ra=${ra}&dec=${dec}&radius=0.0083333333&nDetections.gte=1&pagesize=1`);
}
async function gv0040_probeGalex(ra,dec) {
  const request={service:'Mast.Catalogs.Galex.Cone',params:{ra,dec,radius:0.0083333333},format:'json',pagesize:1,page:1};
  const form=new URLSearchParams(); form.append('request',JSON.stringify(request));
  return await gv0040_fetchJSON('https://mast.stsci.edu/api/v0/invoke',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:form.toString()});
}
function gv0040_renderSimbadDebug(rows) {
  const text = document.getElementById('simbadText');
  const body = document.getElementById('simbadDebugBody');
  if (!Array.isArray(rows) || rows.length === 0) {
    text.textContent = 'No SIMBAD rows returned.';
    body.innerHTML = '<tr><td colspan="7" style="text-align:center">No SIMBAD rows returned.</td></tr>';
    return;
  }
  const blocks = rows.map((row, idx) => [
    `Row ${idx + 1}`,
    `main_id: ${gv0040_cleanId(row.main_id)}`,
    `otype: ${row.otype ?? ''}`,
    `rvz_redshift: ${row.rvz_redshift ?? ''}`,
    `galdim_majaxis: ${row.galdim_majaxis ?? ''}`,
    `galdim_minaxis: ${row.galdim_minaxis ?? ''}`,
    `separation: ${row.separation ?? ''}`
  ].join('\\n')).join('\\n\\n');
  text.textContent = blocks;
  body.innerHTML = rows.map((row, idx) => `<tr>
    <td>${idx + 1}</td>
    <td>${gv0040_safe(gv0040_cleanId(row.main_id))}</td>
    <td>${gv0040_safe(row.otype ?? '')}</td>
    <td>${gv0040_safe(row.rvz_redshift ?? '')}</td>
    <td>${gv0040_safe(row.galdim_majaxis ?? '')}</td>
    <td>${gv0040_safe(row.galdim_minaxis ?? '')}</td>
    <td>${gv0040_safe(row.separation ?? '')}</td>
  </tr>`).join('');
}
function gv0040_pickBestSimbad(rows) {
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const ranked = rows.map(row => {
    let score = 0;
    const id = gv0040_cleanId(row.main_id).toUpperCase();
    const otype = String(row.otype ?? '').toUpperCase();
    const sep = Number(row.separation);
    const maj = Number(row.galdim_majaxis);
    if (/^(M\\s*\\d+|MESSIER\\s*\\d+|NGC\\s*\\d+|IC\\s*\\d+)$/.test(id)) score += 120;
    if (otype === 'G') score += 120;
    else if (otype.startsWith('G')) score += 85;
    else if (otype === 'POG' || otype === 'LSB') score += 40;
    if (otype === 'AGN' || otype === 'SY1' || otype === 'SY2' || otype === 'X') score -= 60;
    if (Number.isFinite(maj)) score += Math.min(maj / 4, 80);
    if (Number.isFinite(sep)) score += Math.max(0, 30 - sep * 3600);
    if (id.includes('2MASS') || id.includes('GALEX') || id.includes('SDSS') || id.includes('[')) score -= 80;
    return { row, score };
  }).sort((a,b) => b.score - a.score);
  return ranked[0].row;
}
function gv0040_renderResult(obj) {
  const body=document.getElementById('resultBody');
  if(!obj){
    body.innerHTML=`<tr><td colspan="7" style="text-align:center">No SIMBAD object found within 30 arcseconds.</td></tr>`;
    return;
  }
  const z=Number(obj.rvz_redshift);
  const distanceLy=gv0040_distanceFromZ(z);
  const coords=Number(obj.ra).toFixed(6)+' '+Number(obj.dec).toFixed(6);
  const name=gv0040_cleanId(obj.main_id||'Not available');
  const info=[obj.otype?'Type: '+obj.otype:null,obj.sp_type?'Spectrum: '+obj.sp_type:null].filter(Boolean).join('; ') || 'No additional SIMBAD classification';
  let distanceText = 'Not available';
  if (distanceLy) distanceText = gv0040_fmt(distanceLy,0) + ' ly (redshift estimate)';
  let zText = 'Not available';
  if (Number.isFinite(z)) {
    zText = `${z.toFixed(6)}`;
    if (distanceLy && z > 0) zText += `<br><span style="color:#8be0ff">${(distanceLy/1e9).toFixed(3)} billion ly</span>`;
  }
  body.innerHTML=`<tr>
    <td>${gv0040_safe(name)}</td>
    <td style="font-family:monospace">${gv0040_safe(coords)}</td>
    <td>${distanceText}</td>
    <td>${gv0040_safe(gv0040_sizeText(obj.galdim_majaxis,obj.galdim_minaxis,distanceLy))}</td>
    <td>Not available in SIMBAD</td>
    <td>${zText}</td>
    <td>${gv0040_safe(info)}</td>
  </tr>`;
}
async function gv0040_runCatalog(name, fn) {
  gv0040_setSearchStatus(name,'Searching…','warn');
  try {
    const data=await fn();
    const count=Array.isArray(data)?data.length:(data&&Array.isArray(data.data)?data.data.length:null);
    gv0040_setSearchStatus(name,count===0?'No match':'Query completed','ok');
    return data;
  } catch(err){
    gv0040_setSearchStatus(name,'Unavailable: '+err.message,'bad');
    return null;
  }
}
async function gv0040_scanSurveys(progressCb) {
  for(let i=0;i<GV0040_SURVEYS.length;i++){
    const cell=document.getElementById('surveyStatus'+i);
    cell.textContent='Loading…';
    cell.className='warn';
    progressCb(`Survey scan ${i+1} / ${GV0040_SURVEYS.length}…`);
    try {
      window.gv0040_aladin.setImageSurvey(GV0040_SURVEYS[i].id);
      await new Promise(r=>setTimeout(r,220));
      cell.textContent='Available / searched';
      cell.className='ok';
    } catch(err){
      cell.textContent='Unavailable';
      cell.className='bad';
    }
  }
  window.gv0040_aladin.setImageSurvey(document.getElementById('surveySelect').value);
}
async function gv0040_findGalaxy() {
  try {
    if(!window.gv0040_aladin) throw new Error('Viewer is not ready.');
    const coords=gv0040_parseCoords(document.getElementById('coordBox').value);
    document.getElementById('resultBody').innerHTML = '<tr><td colspan="7" style="text-align:center">Waiting for all catalog and survey work to finish…</td></tr>';
    document.getElementById('simbadText').textContent = 'Waiting for SIMBAD rows…';
    document.getElementById('simbadDebugBody').innerHTML = '<tr><td colspan="7" style="text-align:center">Waiting for SIMBAD rows…</td></tr>';
    gv0040_setProgress(0, 'Starting search…', 'running');
    gv0040_setStatus('Searching SIMBAD, NED, VizieR, SDSS, PanSTARRS, GALEX, and configured surveys at ' + coords.ra.toFixed(6) + ' ' + coords.dec.toFixed(6) + ' …');
    window.gv0040_aladin.gotoRaDec(coords.ra,coords.dec);

    let completed = 0;
    const bump = (label) => { completed += 1; gv0040_setProgress(completed, label, completed >= GV0040_TOTAL_STEPS ? 'done' : 'running'); };

    const simbadPromise = gv0040_runCatalog('SIMBAD',()=>gv0040_querySimbad(coords.ra,coords.dec)).finally(()=>bump('SIMBAD finished.'));
    const nedPromise = gv0040_runCatalog('NED',()=>gv0040_probeNed(coords.ra,coords.dec)).finally(()=>bump('NED finished.'));
    const vizierPromise = gv0040_runCatalog('VizieR',()=>gv0040_probeVizier(coords.ra,coords.dec)).finally(()=>bump('VizieR finished.'));
    const sdssPromise = gv0040_runCatalog('SDSS',()=>gv0040_probeSdss(coords.ra,coords.dec)).finally(()=>bump('SDSS finished.'));
    const panPromise = gv0040_runCatalog('PanSTARRS',()=>gv0040_probePanStarrs(coords.ra,coords.dec)).finally(()=>bump('PanSTARRS finished.'));
    const galexPromise = gv0040_runCatalog('GALEX',()=>gv0040_probeGalex(coords.ra,coords.dec)).finally(()=>bump('GALEX finished.'));
    const surveyPromise = gv0040_scanSurveys((msg)=>gv0040_setProgress(completed, msg, 'running')).finally(()=>bump('Survey scan finished.'));

    const [simbadRows] = await Promise.all([
      simbadPromise, nedPromise, vizierPromise, sdssPromise, panPromise, galexPromise, surveyPromise
    ]);

    gv0040_setProgress(completed, 'Compiling final galaxy table…', 'running');
    gv0040_renderSimbadDebug(simbadRows || []);
    gv0040_renderResult(gv0040_pickBestSimbad(simbadRows || []));
    gv0040_setProgress(GV0040_TOTAL_STEPS, 'Search complete.', 'done');
    gv0040_setStatus('Search complete. Main table was rendered only after all catalog and survey tasks finished.');
  } catch(err){
    gv0040_setProgress(0, 'Search failed.', 'fail');
    gv0040_setStatus('Search failed: ' + err.message);
  }
}
</script>
"""

display(HTML(HTML_CONTENT))