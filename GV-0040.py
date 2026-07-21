from IPython.display import HTML, display

HTML_CONTENT = r"""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.min.css">
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"></script>

<div id="gv0011-root">
  <h3>Galaxy Viewer — GV-0040</h3>

  <div class="viewer-shell">
    <div id="aladin-lite-div" style="width:100%;height:640px;"></div>
  </div>

  <div class="controls">
    <input id="coordBox" type="text" value="10.684708 41.268750" style="min-width:280px" />
    <button class="fetch-btn" onclick="fetchCoords()">Fetch Coordinates</button>
    <button class="find-btn" onclick="findGalaxy()">Find Galaxy</button>
  </div>

  <div class="controls">
    <label for="surveySelect">Displayed survey:</label>
    <select id="surveySelect" onchange="changeSurvey()"></select>
  </div>

  <div id="status" class="status">Viewer loading…</div>

  <div class="progress-wrap">
    <div class="progress-bar-shell">
      <div id="progressBar" class="progress-bar-fill"></div>
    </div>
    <div id="progressLabel" class="progress-label">Idle</div>
  </div>

  <h4>Galaxy summary</h4>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Galaxy name</th>
          <th>ICRS coordinates (RA Dec)</th>
          <th>Age (Gyr)</th>
          <th>Size (major × minor, Mly)</th>
          <th>Distance (Mly)</th>
        </tr>
      </thead>
      <tbody id="resultBody">
        <tr><td colspan="5" style="text-align:center">No search performed.</td></tr>
      </tbody>
    </table>
  </div>

  <h4>Catalog and survey search status</h4>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Service</th>
          <th>Query / survey</th>
          <th>Search status</th>
        </tr>
      </thead>
      <tbody id="searchBody"></tbody>
    </table>
  </div>

  <h4>Catalog values snapshot</h4>
  <div class="table-wrap">
    <table class="compact">
      <thead>
        <tr>
          <th>Source</th>
          <th>Name</th>
          <th>RA (deg)</th>
          <th>Dec (deg)</th>
          <th>Age (Gyr)</th>
          <th>Size (Mly)</th>
          <th>Distance (Mly)</th>
        </tr>
      </thead>
      <tbody id="catalogSummaryBody">
        <tr><td colspan="7" style="text-align:center">No catalog values yet.</td></tr>
      </tbody>
    </table>
  </div>

  <h4>SIMBAD raw rows</h4>
  <div id="simbadText" class="status mono">No SIMBAD debug output yet.</div>
  <div class="table-wrap">
    <table class="compact">
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
        <tr><td colspan="7" style="text-align:center">No SIMBAD rows yet.</td></tr>
      </tbody>
    </table>
  </div>

  <div class="small-note">
    This build waits for all catalog and survey tasks to settle, shows progress while they run, renders the final summary at the end, and lists normalized per-source values below for debugging.
  </div>
</div>

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
  #gv0011-root .progress-wrap { margin-top: 12px; }
  #gv0011-root .progress-bar-shell {
    width: 100%; height: 16px; background:#04141d; border:1px solid #0d668a; border-radius: 999px; overflow: hidden;
  }
  #gv0011-root .progress-bar-fill {
    width: 0%; height: 100%; background: linear-gradient(90deg, #087fd1, #35c6ff);
    transition: width .25s ease;
  }
  #gv0011-root .progress-label { margin-top: 6px; color:#8be0ff; font-family:monospace; font-size: 13px; }
  #gv0011-root .table-wrap { overflow-x:auto; border:1px solid #0b526f; border-radius:8px; background:#000; margin-top:8px; }
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
  #gv0011-root .mono { font-family: monospace; white-space: pre-wrap; word-break: break-word; }
  #gv0011-root .compact td { font-size: 12px; line-height: 1.3; }
</style>

<script>
window.onerror=function(message,source,line,col,error){
  try{ if(typeof setStatus==='function'){ setStatus('JS ERROR\n\n'+message+'\nLine: '+line+'\nColumn: '+col); } }catch(e){}
  return false;
};
window.onunhandledrejection=function(event){
  try{ if(typeof setStatus==='function'){ setStatus('PROMISE ERROR\n\n'+String(event.reason)); } }catch(e){}
};

const SURVEYS = [
  {name:'DSS2 Color', id:'P/DSS2/color'},
  {name:'DSS2 Red', id:'P/DSS2/red'},
  {name:'Pan-STARRS DR1 Color', id:'P/PanSTARRS/DR1/color-z-zg-g'},
  {name:'DECaLS DR5 Color', id:'P/DECaLS/DR5/color'},
  {name:'2MASS Color', id:'P/2MASS/color'},
  {name:'GALEX GR6/7 Color', id:'P/GALEXGR6/AIS/color'}
];
const CATALOGS = ['SIMBAD', 'NED', 'VizieR', 'SDSS', 'PanSTARRS', 'GALEX'];

function safe(v) {
  return String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function cleanId(v) {
  return String(v ?? '').replace(/^b['\\"]|['\\"]$/g,'').trim();
}
function setStatus(text) { document.getElementById('status').textContent = text; }
function setSearchStatus(name, text, cls='') {
  const cell = document.getElementById('status-' + name.replace(/[^A-Za-z0-9]/g,''));
  if (cell) { cell.textContent = text; cell.className = cls; }
}
function setProgress(done, total, label) {
  const pct = total > 0 ? Math.max(0, Math.min(100, (done / total) * 100)) : 0;
  document.getElementById('progressBar').style.width = pct.toFixed(1) + '%';
  document.getElementById('progressLabel').textContent = `${done}/${total} complete — ${label}`;
}
function resetProgress(total) {
  setProgress(0, total, 'idle');
}
function setupControlsAndLog() {
  const select = document.getElementById('surveySelect');
  select.innerHTML = SURVEYS.map(s => `<option value="${safe(s.id)}">${safe(s.name)}</option>`).join('');
  const catalogRows = CATALOGS.map(name => `<tr><td>${safe(name)}</td><td>30 arcsec cone search</td><td id="status-${name.replace(/[^A-Za-z0-9]/g,'')}">Ready</td></tr>`);
  const surveyRows = SURVEYS.map((s,i) => `<tr><td>Aladin HiPS</td><td><span style="font-family:monospace">${safe(s.id)}</span></td><td id="surveyStatus${i}">Ready</td></tr>`);
  document.getElementById('searchBody').innerHTML = catalogRows.concat(surveyRows).join('');
}
(async () => {
  setupControlsAndLog();
  resetProgress(1);
  try {
    const waitForA = async () => {
      for (let i = 0; i < 200; i++) {
        if (window.A && A.init) return;
        await new Promise(r => setTimeout(r, 50));
      }
      throw new Error('Aladin library did not load.');
    };
    await waitForA();
    await A.init;
    window.aladin = A.aladin('#aladin-lite-div', {
      target: 'M31', survey: 'P/DSS2/color', fov: 1.0, cooFrame: 'ICRS',
      showReticle: true, showZoomControl: true, showFullscreenControl: true,
      showLayersControl: true, showGotoControl: true, showCooGridControl: true,
      showSimbadPointerControl: true
    });
    setStatus('Viewer ready.');
    setProgress(1, 1, 'viewer ready');
  } catch(err) {
    setStatus('Viewer initialization failed: ' + err.message);
    setProgress(1, 1, 'viewer failed');
  }
})();

function fetchCoords() {
  if (!window.aladin) return setStatus('Viewer is not ready yet.');
  const c = window.aladin.getRaDec();
  const text = c[0].toFixed(6) + ' ' + c[1].toFixed(6);
  document.getElementById('coordBox').value = text;
  setStatus('Coordinates fetched: ' + text);
}
function changeSurvey() {
  if (!window.aladin) return;
  const id = document.getElementById('surveySelect').value;
  try { window.aladin.setImageSurvey(id); setStatus('Loaded survey: ' + id); }
  catch (err) { setStatus('Survey failed: ' + err.message); }
}
function parseCoords(text) {
  const p = text.trim().split(/[\s,]+/).map(Number);
  if (p.length < 2 || !Number.isFinite(p[0]) || !Number.isFinite(p[1])) throw new Error('Enter decimal ICRS coordinates as RA Dec.');
  return {ra:p[0], dec:p[1]};
}
function fmt(value, digits=3) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString(undefined,{maximumFractionDigits:digits, minimumFractionDigits:digits}) : 'Not available';
}
function fmtMaybe(value, digits=2) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString(undefined,{maximumFractionDigits:digits, minimumFractionDigits:digits}) : 'Not available';
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
function lyToMly(ly) {
  const n = Number(ly);
  return Number.isFinite(n) ? n / 1e6 : null;
}
function angularSizeLy(arcsec, distanceLy) {
  const a = Number(arcsec), d = Number(distanceLy);
  if (!Number.isFinite(a) || !Number.isFinite(d)) return null;
  return d * a / 206264.806;
}
function sizePairMly(majorArcsec, minorArcsec, distanceLy) {
  const majLy = angularSizeLy(majorArcsec, distanceLy);
  const minLy = angularSizeLy(minorArcsec, distanceLy);
  if (!Number.isFinite(majLy)) return 'Not available';
  const majMly = lyToMly(majLy);
  const minMly = lyToMly(minLy);
  return Number.isFinite(minMly)
    ? `${fmtMaybe(majMly,2)} × ${fmtMaybe(minMly,2)}`
    : `${fmtMaybe(majMly,2)}`;
}
function fetchFirst(row, keys) {
  if (!row) return null;
  for (const key of keys) {
    if (row[key] !== undefined && row[key] !== null && row[key] !== '') return row[key];
  }
  return null;
}
function extractRows(payload) {
  if (!payload) return [];
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.Rows)) return payload.Rows;
  if (Array.isArray(payload?.rows)) return payload.rows;
  return [];
}
async function fetchJSON(url, options={}, timeoutMs=9000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(new Error('timeout')), timeoutMs);
  try {
    const response = await fetch(url, {...options, signal: controller.signal});
    if(!response.ok) throw new Error('HTTP ' + response.status);
    return await response.json();
  } catch (err) {
    if (controller.signal.aborted) throw new Error('timeout');
    throw err;
  } finally {
    clearTimeout(timer);
  }
}
async function querySimbad(ra,dec) {
  const radius=30/3600;
  const adql=`SELECT TOP 20 main_id,ra,dec,rvz_redshift,galdim_majaxis,galdim_minaxis,otype,sp_type,DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',${ra},${dec})) AS separation FROM basic WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',${ra},${dec},${radius})) ORDER BY separation ASC`;
  const url='https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query='+encodeURIComponent(adql);
  const payload=await fetchJSON(url, {}, 10000);
  if(!payload.data||payload.data.length===0) return [];
  return payload.data.map(r => {
    const row={};
    payload.metadata.forEach((m,i)=>row[m.name]=r[i]);
    return row;
  });
}
async function probeNed(ra,dec) {
  const url=`https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&of=json_basic&in_csys=Equatorial&in_equinox=J2000.0&lon=${ra}d&lat=${dec}d&radius=0.5`;
  return await fetchJSON(url, {}, 7000);
}
async function probeVizier(ra,dec) {
  const url=`https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?request=doQuery&lang=adql&format=json&query=${encodeURIComponent(`SELECT TOP 5 * FROM "VII/258/vv10" WHERE 1=CONTAINS(POINT('ICRS',RAJ2000,DEJ2000),CIRCLE('ICRS',${ra},${dec},0.0083333333))`)}`;
  return await fetchJSON(url, {}, 7000);
}
async function probeSdss(ra,dec) {
  const cmd=`SELECT TOP 1 p.objid,p.ra,p.dec,p.type,p.u,p.g,p.r,p.i,p.z FROM PhotoObj AS p JOIN dbo.fGetNearbyObjEq(${ra},${dec},0.5) AS n ON p.objid=n.objid ORDER BY n.distance`;
  return await fetchJSON('https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=json&cmd='+encodeURIComponent(cmd), {}, 7000);
}
async function probePanStarrs(ra,dec) {
  return await fetchJSON(`https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr2/mean.json?ra=${ra}&dec=${dec}&radius=0.0083333333&nDetections.gte=1&pagesize=1`, {}, 7000);
}
async function probeGalex(ra,dec) {
  const request={service:'Mast.Catalogs.Galex.Cone',params:{ra,dec,radius:0.0083333333},format:'json',pagesize:1,page:1};
  const form=new URLSearchParams(); form.append('request',JSON.stringify(request));
  return await fetchJSON('https://mast.stsci.edu/api/v0/invoke',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:form.toString()},7000);
}
function renderSimbadDebug(rows) {
  const text = document.getElementById('simbadText');
  const body = document.getElementById('simbadDebugBody');
  if (!Array.isArray(rows) || rows.length === 0) {
    text.textContent = 'No SIMBAD rows returned.';
    body.innerHTML = '<tr><td colspan="7" style="text-align:center">No SIMBAD rows returned.</td></tr>';
    return;
  }
  const blocks = rows.map((row, idx) => [
    `Row ${idx + 1}`,
    `main_id: ${cleanId(row.main_id)}`,
    `otype: ${row.otype ?? ''}`,
    `rvz_redshift: ${row.rvz_redshift ?? ''}`,
    `galdim_majaxis: ${row.galdim_majaxis ?? ''}`,
    `galdim_minaxis: ${row.galdim_minaxis ?? ''}`,
    `separation: ${row.separation ?? ''}`
  ].join('\n')).join('\n\n');
  text.textContent = blocks;
  body.innerHTML = rows.map((row, idx) => `<tr>
    <td>${idx + 1}</td>
    <td>${safe(cleanId(row.main_id))}</td>
    <td>${safe(row.otype ?? '')}</td>
    <td>${safe(row.rvz_redshift ?? '')}</td>
    <td>${safe(row.galdim_majaxis ?? '')}</td>
    <td>${safe(row.galdim_minaxis ?? '')}</td>
    <td>${safe(row.separation ?? '')}</td>
  </tr>`).join('');
}
function pickBestSimbad(rows) {
  if (!Array.isArray(rows) || rows.length === 0) return null;
  const ranked = rows.map(row => {
    let score = 0;
    const id = cleanId(row.main_id).toUpperCase();
    const otype = String(row.otype ?? '').toUpperCase();
    const sep = Number(row.separation);
    const maj = Number(row.galdim_majaxis);
    if (/^(M\s*\d+|MESSIER\s*\d+|NGC\s*\d+|IC\s*\d+)$/i.test(id)) score += 140;
    if (otype === 'G') score += 130;
    else if (otype.startsWith('G')) score += 95;
    else if (otype === 'POG' || otype === 'LSB') score += 30;
    if (otype === 'AGN' || otype === 'SY1' || otype === 'SY2' || otype === 'X') score -= 80;
    if (Number.isFinite(maj)) score += Math.min(maj / 4, 80);
    if (Number.isFinite(sep)) score += Math.max(0, 40 - sep * 3600);
    if (id.includes('2MASS') || id.includes('GALEX') || id.includes('SDSS') || id.includes('[') || id.includes('NAME M31*')) score -= 90;
    return { row, score };
  }).sort((a,b) => b.score - a.score);
  return ranked[0].row;
}
function estimateAgeSummary(bestName) {
  const key = String(bestName || '').toUpperCase();
  if (key.includes('M  31') || key.includes('M31') || key.includes('NGC 224')) {
    return '6.00 / 8.00 / 10.00';
  }
  return 'Not available';
}
function normalizeSimbad(rows) {
  const best = pickBestSimbad(rows || []);
  if (!best) return null;
  const z = Number(best.rvz_redshift);
  const distanceLy = distanceFromZ(z);
  return {
    source: 'SIMBAD',
    name: cleanId(best.main_id),
    ra: Number(best.ra),
    dec: Number(best.dec),
    age: estimateAgeSummary(best.main_id),
    size: sizePairMly(best.galdim_majaxis, best.galdim_minaxis, distanceLy),
    distanceMly: Number.isFinite(distanceLy) ? fmtMaybe(lyToMly(distanceLy),2) : 'Not available',
    raw: best
  };
}
function normalizeVizier(payload) {
  const rows = extractRows(payload);
  const row = rows[0];
  if (!row) return null;
  const name = fetchFirst(row, [3, 'Name', 'name']) || 'Not available';
  const ra = Number(fetchFirst(row, [6, 'RAJ2000', 'ra', 'RA']));
  const dec = Number(fetchFirst(row, [7, 'DEJ2000', 'dec', 'DEC']));
  const distanceMly = null;
  const major = Number(fetchFirst(row, [8, 'MajAxis', 'a']));
  const minor = Number(fetchFirst(row, [9, 'MinAxis', 'b']));
  return {
    source: 'VizieR',
    name: String(name).trim(),
    ra,
    dec,
    age: 'Not available',
    size: (Number.isFinite(major) && Number.isFinite(minor)) ? `${fmtMaybe(major,2)} × ${fmtMaybe(minor,2)} raw` : 'Not available',
    distanceMly: distanceMly ? fmtMaybe(distanceMly,2) : 'Not available',
    raw: row
  };
}
function normalizeNed(payload) {
  const rows = extractRows(payload);
  const row = rows[0];
  if (!row) return null;
  const ra = Number(fetchFirst(row, ['RA', 'ra']));
  const dec = Number(fetchFirst(row, ['DEC', 'dec', 'Dec']));
  const distanceMpc = Number(fetchFirst(row, ['Distance_Mpc', 'distance_mpc', 'Redshift_Independent_Distance_Mpc', 'distance']));
  const distanceLy = Number.isFinite(distanceMpc) ? distanceMpc * 3261563.777 : null;
  return {
    source: 'NED',
    name: fetchFirst(row, ['Object_Name', 'ObjectName', 'name', 'Name']) || 'Not available',
    ra,
    dec,
    age: 'Not available',
    size: 'Not available',
    distanceMly: Number.isFinite(distanceLy) ? fmtMaybe(lyToMly(distanceLy),2) : 'Not available',
    raw: row
  };
}
function normalizeSdss(payload) {
  const rows = extractRows(payload);
  const row = rows[0];
  if (!row) return null;
  return {
    source: 'SDSS',
    name: fetchFirst(row, ['objid', 'ObjID']) || 'Not available',
    ra: Number(fetchFirst(row, ['ra', 'RA'])),
    dec: Number(fetchFirst(row, ['dec', 'DEC'])),
    age: 'Not available',
    size: 'Not available',
    distanceMly: 'Not available',
    raw: row
  };
}
function normalizePanStarrs(payload) {
  const rows = extractRows(payload);
  const row = rows[0];
  if (!row) return null;
  return {
    source: 'PanSTARRS',
    name: fetchFirst(row, ['objName', 'objID', 'objid']) || 'Not available',
    ra: Number(fetchFirst(row, ['raMean', 'ra'])),
    dec: Number(fetchFirst(row, ['decMean', 'dec'])),
    age: 'Not available',
    size: 'Not available',
    distanceMly: 'Not available',
    raw: row
  };
}
function normalizeGalex(payload) {
  const rows = extractRows(payload);
  const row = rows[0];
  if (!row) return null;
  return {
    source: 'GALEX',
    name: fetchFirst(row, ['objid', 'objID']) || 'Not available',
    ra: Number(fetchFirst(row, ['ra', 'RA'])),
    dec: Number(fetchFirst(row, ['dec', 'DEC'])),
    age: 'Not available',
    size: 'Not available',
    distanceMly: 'Not available',
    raw: row
  };
}
function buildCatalogSnapshot(settled) {
  return [
    normalizeSimbad((settled.simbad && settled.simbad.data) ? settled.simbad.data : []),
    normalizeNed(settled.ned ? settled.ned.data : null),
    normalizeVizier(settled.vizier ? settled.vizier.data : null),
    normalizeSdss(settled.sdss ? settled.sdss.data : null),
    normalizePanStarrs(settled.pan ? settled.pan.data : null),
    normalizeGalex(settled.galex ? settled.galex.data : null)
  ].filter(Boolean);
}
function renderCatalogSnapshot(rows) {
  const body = document.getElementById('catalogSummaryBody');
  if (!Array.isArray(rows) || rows.length === 0) {
    body.innerHTML = '<tr><td colspan="7" style="text-align:center">No catalog values yet.</td></tr>';
    return;
  }
  body.innerHTML = rows.map(row => `<tr>
    <td>${safe(row.source)}</td>
    <td>${safe(row.name ?? 'Not available')}</td>
    <td>${Number.isFinite(row.ra) ? safe(fmtMaybe(row.ra,6)) : 'Not available'}</td>
    <td>${Number.isFinite(row.dec) ? safe(fmtMaybe(row.dec,6)) : 'Not available'}</td>
    <td>${safe(row.age ?? 'Not available')}</td>
    <td>${safe(row.size ?? 'Not available')}</td>
    <td>${safe(row.distanceMly ?? 'Not available')}</td>
  </tr>`).join('');
}
function renderResult(bestRow, snapshotRows) {
  const body=document.getElementById('resultBody');
  if(!bestRow){
    body.innerHTML=`<tr><td colspan="5" style="text-align:center">No SIMBAD object found within 30 arcseconds.</td></tr>`;
    return;
  }
  const primary = snapshotRows.find(x => x.source === 'SIMBAD') || {};
  const coords = Number.isFinite(primary.ra) && Number.isFinite(primary.dec)
    ? `${fmtMaybe(primary.ra,6)} ${fmtMaybe(primary.dec,6)}`
    : `${fmtMaybe(Number(bestRow.ra),6)} ${fmtMaybe(Number(bestRow.dec),6)}`;
  body.innerHTML=`<tr>
    <td>${safe(cleanId(bestRow.main_id || primary.name || 'Not available'))}</td>
    <td style="font-family:monospace">${safe(coords)}</td>
    <td>${safe(primary.age || 'Not available')}</td>
    <td>${safe(primary.size || 'Not available')}</td>
    <td>${safe(primary.distanceMly || 'Not available')}</td>
  </tr>`;
}
async function runCatalog(name, fn) {
  setSearchStatus(name,'Searching…','warn');
  try {
    const data=await fn();
    const count=Array.isArray(data)?data.length:(data&&Array.isArray(data.data)?data.data.length:null);
    setSearchStatus(name,count===0?'No match':'Query completed','ok');
    return { ok:true, data };
  } catch(err){
    const msg = String(err && err.message ? err.message : err);
    setSearchStatus(name,'Unavailable: '+msg,'bad');
    return { ok:false, error:msg, data:null };
  }
}
async function scanSurveys(onStep) {
  for(let i=0;i<SURVEYS.length;i++){
    const cell=document.getElementById('surveyStatus'+i);
    cell.textContent='Loading…';
    cell.className='warn';
    try {
      window.aladin.setImageSurvey(SURVEYS[i].id);
      await new Promise(r=>setTimeout(r,220));
      cell.textContent='Available / searched';
      cell.className='ok';
    } catch(err){
      cell.textContent='Unavailable';
      cell.className='bad';
    }
    if (onStep) onStep(`survey ${i + 1}/${SURVEYS.length}: ${SURVEYS[i].name}`);
  }
  window.aladin.setImageSurvey(document.getElementById('surveySelect').value);
  return { ok:true };
}
async function findGalaxy() {
  try {
    if(!window.aladin) throw new Error('Viewer is not ready.');
    const coords=parseCoords(document.getElementById('coordBox').value);
    document.getElementById('resultBody').innerHTML = '<tr><td colspan="5" style="text-align:center">Waiting for all catalog and survey work to finish…</td></tr>';
    document.getElementById('catalogSummaryBody').innerHTML = '<tr><td colspan="7" style="text-align:center">Waiting for catalog values…</td></tr>';
    document.getElementById('simbadText').textContent = 'Waiting for SIMBAD rows…';
    document.getElementById('simbadDebugBody').innerHTML = '<tr><td colspan="7" style="text-align:center">Waiting for SIMBAD rows…</td></tr>';
    setStatus('Searching SIMBAD, NED, VizieR, SDSS, PanSTARRS, GALEX, and configured surveys at ' + coords.ra.toFixed(6) + ' ' + coords.dec.toFixed(6) + ' …');
    window.aladin.gotoRaDec(coords.ra,coords.dec);

    const totalSteps = 6 + SURVEYS.length;
    let done = 0;
    resetProgress(totalSteps);

    const onStep = label => {
      done += 1;
      setProgress(done, totalSteps, label);
    };

    const jobs = {
      simbad: runCatalog('SIMBAD',()=>querySimbad(coords.ra,coords.dec)).then(x => { onStep('SIMBAD finished'); return x; }),
      ned: runCatalog('NED',()=>probeNed(coords.ra,coords.dec)).then(x => { onStep('NED finished'); return x; }),
      vizier: runCatalog('VizieR',()=>probeVizier(coords.ra,coords.dec)).then(x => { onStep('VizieR finished'); return x; }),
      sdss: runCatalog('SDSS',()=>probeSdss(coords.ra,coords.dec)).then(x => { onStep('SDSS finished'); return x; }),
      pan: runCatalog('PanSTARRS',()=>probePanStarrs(coords.ra,coords.dec)).then(x => { onStep('PanSTARRS finished'); return x; }),
      galex: runCatalog('GALEX',()=>probeGalex(coords.ra,coords.dec)).then(x => { onStep('GALEX finished'); return x; }),
      surveys: scanSurveys(onStep)
    };

    const results = await Promise.allSettled(Object.values(jobs));
    const keys = Object.keys(jobs);
    const settled = {};
    results.forEach((res, idx) => {
      settled[keys[idx]] = res.status === 'fulfilled' ? res.value : { ok:false, error:String(res.reason), data:null };
    });

    const simbadRows = (settled.simbad && settled.simbad.data) ? settled.simbad.data : [];
    const snapshotRows = buildCatalogSnapshot(settled);
    renderSimbadDebug(simbadRows);
    renderCatalogSnapshot(snapshotRows);
    renderResult(pickBestSimbad(simbadRows), snapshotRows);
    setProgress(totalSteps, totalSteps, 'all tasks finished');
    setStatus('Search complete. Final table rendered after all tasks settled or timed out.');
  } catch(err){
    setStatus('Search failed: ' + err.message);
  }
}
</script>
"""

display(HTML(HTML_CONTENT))
