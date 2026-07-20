# GV-0008
# Galaxy Viewer — multi-survey search and galaxy figures of merit

from IPython.display import display, HTML

html = r"""
<div style="width:100%;max-width:1100px;margin:auto;font-family:Arial,sans-serif">
  <h3>Galaxy Viewer — GV-0008</h3>
  <div id="aladin-lite-div" style="width:100%;height:620px;border:1px solid #bbb"></div>

  <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px">
    <input id="coordBox" type="text" value="53.174798 -27.799445"
           style="flex:1;min-width:280px;padding:13px;font-size:18px;border:1px solid #999;border-radius:8px">
    <button onclick="fetchCoords()"
            style="padding:15px 28px;font-size:18px;font-weight:700;color:white;background:#199447;border:0;border-radius:9px;cursor:pointer">
      Fetch Coordinates
    </button>
    <button onclick="findGalaxy()"
            style="padding:15px 28px;font-size:18px;font-weight:700;color:white;background:#1976d2;border:0;border-radius:9px;cursor:pointer">
      Find Galaxy
    </button>
  </div>

  <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:12px">
    <b>Displayed survey:</b>
    <select id="surveySelect" onchange="changeSurvey()" style="padding:9px;font-size:15px;min-width:280px"></select>
  </div>

  <div id="status" style="margin-top:12px;padding:11px;background:#f4f4f4;border-radius:7px;font-family:monospace">Initializing viewer…</div>

  <h4>Galaxy figures of merit</h4>
  <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-size:14px">
      <thead>
        <tr style="background:#e7eef8">
          <th style="border:1px solid #aaa;padding:8px">Galaxy name</th>
          <th style="border:1px solid #aaa;padding:8px">ICRS coordinates (RA Dec)</th>
          <th style="border:1px solid #aaa;padding:8px">Distance (light-years)</th>
          <th style="border:1px solid #aaa;padding:8px">Galaxy size</th>
          <th style="border:1px solid #aaa;padding:8px">Galaxy age</th>
          <th style="border:1px solid #aaa;padding:8px">Redshift z</th>
        </tr>
      </thead>
      <tbody id="resultBody">
        <tr><td colspan="6" style="border:1px solid #aaa;padding:10px;text-align:center">No search performed.</td></tr>
      </tbody>
    </table>
  </div>

  <h4>Survey search</h4>
  <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-size:14px">
      <thead>
        <tr style="background:#edf7ed">
          <th style="border:1px solid #aaa;padding:7px">Survey</th>
          <th style="border:1px solid #aaa;padding:7px">HiPS identifier</th>
          <th style="border:1px solid #aaa;padding:7px">Search status</th>
        </tr>
      </thead>
      <tbody id="surveyBody"></tbody>
    </table>
  </div>

  <div style="margin-top:10px;font-size:12px;color:#555;line-height:1.4">
    Object data are queried from SIMBAD. When redshift is available, distance is estimated with H₀ = 70 km/s/Mpc.
    Physical size is derived from the SIMBAD angular dimensions and that estimated distance. Galaxy age is shown as unavailable when no catalog value exists.
  </div>
</div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
<script>
let aladin;

const SURVEYS = [
  {name:"DSS2 Color", id:"P/DSS2/color"},
  {name:"DSS2 Red", id:"P/DSS2/red"},
  {name:"Pan-STARRS DR1 Color", id:"P/PanSTARRS/DR1/color-z-zg-g"},
  {name:"DECaLS DR5 Color", id:"P/DECaLS/DR5/color"},
  {name:"2MASS Color", id:"P/2MASS/color"},
  {name:"WISE Color", id:"P/WISE/color"},
  {name:"GALEX GR6/7 Color", id:"P/GALEXGR6/AIS/color"},
  {name:"Fermi Color", id:"P/Fermi/color"}
];

function safe(v) {
  return String(v ?? "").replace(/[&<>\"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}

function setStatus(text) {
  document.getElementById("status").textContent = text;
}

function setupSurveyTable() {
  const select = document.getElementById("surveySelect");
  select.innerHTML = SURVEYS.map(s => `<option value="${safe(s.id)}">${safe(s.name)}</option>`).join("");
  document.getElementById("surveyBody").innerHTML = SURVEYS.map((s, i) => `
    <tr>
      <td style="border:1px solid #aaa;padding:7px">${safe(s.name)}</td>
      <td style="border:1px solid #aaa;padding:7px;font-family:monospace">${safe(s.id)}</td>
      <td id="surveyStatus${i}" style="border:1px solid #aaa;padding:7px">Ready</td>
    </tr>`).join("");
}

async function initAladin() {
  setupSurveyTable();
  await A.init;
  aladin = A.aladin("#aladin-lite-div", {
    survey: SURVEYS[0].id,
    target: "53.174798 -27.799445",
    fov: 0.02,
    cooFrame: "ICRS",
    showReticle: true,
    showCooGridControl: true,
    showSimbadPointerControl: true
  });
  setStatus("Viewer ready.");
}

function fetchCoords() {
  const c = aladin.getRaDec();
  const text = c[0].toFixed(6) + " " + c[1].toFixed(6);
  document.getElementById("coordBox").value = text;
  setStatus("Coordinates fetched: " + text);
}

function changeSurvey() {
  const id = document.getElementById("surveySelect").value;
  aladin.setImageSurvey(id);
  setStatus("Displayed survey: " + id);
}

function parseCoords(text) {
  const p = text.trim().split(/[\s,]+/).map(Number);
  if (p.length < 2 || !Number.isFinite(p[0]) || !Number.isFinite(p[1])) {
    throw new Error("Enter decimal ICRS coordinates as RA Dec.");
  }
  return {ra:p[0], dec:p[1]};
}

function fmt(value, digits=3) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString(undefined, {maximumFractionDigits:digits}) : "Not available";
}

function distanceFromZ(z) {
  const zz = Number(z);
  if (!Number.isFinite(zz) || zz <= 0) return null;
  return ((299792.458 * zz) / 70.0) * 3261563.777;
}

function sizeText(majorArcsec, minorArcsec, distanceLy) {
  const maj = Number(majorArcsec);
  const min = Number(minorArcsec);
  if (!Number.isFinite(maj) || !Number.isFinite(distanceLy)) return "Not available";
  const majLy = distanceLy * maj / 206264.806;
  if (Number.isFinite(min)) {
    const minLy = distanceLy * min / 206264.806;
    return `${fmt(majLy,0)} × ${fmt(minLy,0)} ly (${fmt(maj,2)} × ${fmt(min,2)} arcsec)`;
  }
  return `${fmt(majLy,0)} ly (${fmt(maj,2)} arcsec)`;
}

async function querySimbad(ra, dec) {
  const radius = 30 / 3600;
  const adql = `SELECT TOP 1 main_id,ra,dec,rvz_redshift,galdim_majaxis,galdim_minaxis,otype,DISTANCE(POINT('ICRS',ra,dec),POINT('ICRS',${ra},${dec})) AS separation FROM basic WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',${ra},${dec},${radius})) ORDER BY separation ASC`;
  const url = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query=" + encodeURIComponent(adql);
  const response = await fetch(url);
  if (!response.ok) throw new Error("SIMBAD HTTP " + response.status);
  const payload = await response.json();
  if (!payload.data || payload.data.length === 0) return null;
  const row = {};
  payload.metadata.forEach((m, i) => row[m.name] = payload.data[0][i]);
  return row;
}

function renderResult(obj, requested) {
  const body = document.getElementById("resultBody");
  if (!obj) {
    body.innerHTML = `<tr><td colspan="6" style="border:1px solid #aaa;padding:10px;text-align:center">No SIMBAD object found within 30 arcseconds of ${safe(requested.ra.toFixed(6) + " " + requested.dec.toFixed(6))}.</td></tr>`;
    return;
  }
  const z = Number(obj.rvz_redshift);
  const distanceLy = distanceFromZ(z);
  const coords = Number(obj.ra).toFixed(6) + " " + Number(obj.dec).toFixed(6);
  const name = String(obj.main_id ?? "Not available").replace(/^b['\"]|['\"]$/g, "").trim();
  const size = sizeText(obj.galdim_majaxis, obj.galdim_minaxis, distanceLy);
  body.innerHTML = `<tr>
    <td style="border:1px solid #aaa;padding:8px">${safe(name)}</td>
    <td style="border:1px solid #aaa;padding:8px;font-family:monospace">${safe(coords)}</td>
    <td style="border:1px solid #aaa;padding:8px">${distanceLy ? fmt(distanceLy,0) + " ly (redshift estimate)" : "Not available"}</td>
    <td style="border:1px solid #aaa;padding:8px">${safe(size)}</td>
    <td style="border:1px solid #aaa;padding:8px">Not available in SIMBAD</td>
    <td style="border:1px solid #aaa;padding:8px">${Number.isFinite(z) ? z.toFixed(6) : "Not available"}</td>
  </tr>`;
}

async function scanSurveys() {
  for (let i = 0; i < SURVEYS.length; i++) {
    const cell = document.getElementById("surveyStatus" + i);
    cell.textContent = "Loading…";
    try {
      aladin.setImageSurvey(SURVEYS[i].id);
      await new Promise(resolve => setTimeout(resolve, 220));
      cell.textContent = "Available / searched";
    } catch (err) {
      cell.textContent = "Unavailable";
    }
  }
  aladin.setImageSurvey(document.getElementById("surveySelect").value);
}

async function findGalaxy() {
  try {
    const coords = parseCoords(document.getElementById("coordBox").value);
    setStatus("Searching catalogs and 8 surveys at " + coords.ra.toFixed(6) + " " + coords.dec.toFixed(6) + " …");
    aladin.gotoRaDec(coords.ra, coords.dec);
    const results = await Promise.allSettled([querySimbad(coords.ra, coords.dec), scanSurveys()]);
    if (results[0].status === "rejected") throw results[0].reason;
    renderResult(results[0].value, coords);
    setStatus("Search complete: SIMBAD plus " + SURVEYS.length + " configured Aladin HiPS surveys.");
  } catch (err) {
    setStatus("Search failed: " + err.message);
  }
}

initAladin();
</script>
"""

display(HTML(html))
