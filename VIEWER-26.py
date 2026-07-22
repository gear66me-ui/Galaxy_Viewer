from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-25.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-25-base.py", "exec"))


display(Javascript(r'''
(() => {
  const VIEWER26_MAGIC_GALAXIES = [
    {name:"Andromeda Galaxy — M31",ra:10.684708,dec:41.268750,fov:3.200,morphology:"SA(s)b",angular_size:"190 × 60 arcmin"},
    {name:"Whirlpool Galaxy — M51",ra:202.469575,dec:47.195258,fov:0.280,morphology:"Grand-design spiral",angular_size:"11.2 × 6.9 arcmin"},
    {name:"Sombrero Galaxy — M104",ra:189.997633,dec:-11.623054,fov:0.180,morphology:"SA(s)a / edge-on",angular_size:"8.7 × 3.5 arcmin"},
    {name:"Pinwheel Galaxy — M101",ra:210.802267,dec:54.348950,fov:0.480,morphology:"SAB(rs)cd",angular_size:"28.8 × 26.9 arcmin"},
    {name:"Sculptor Galaxy — NGC 253",ra:11.888000,dec:-25.288200,fov:0.500,morphology:"SAB(s)c / starburst",angular_size:"27.5 × 6.8 arcmin"},
    {name:"Bode's Galaxy — M81",ra:148.888200,dec:69.065300,fov:0.420,morphology:"SA(s)ab",angular_size:"26.9 × 14.1 arcmin"},
    {name:"Cigar Galaxy — M82",ra:148.968500,dec:69.679700,fov:0.220,morphology:"Starburst / edge-on",angular_size:"11.2 × 4.3 arcmin"},
    {name:"Black Eye Galaxy — M64",ra:194.182100,dec:21.682700,fov:0.180,morphology:"SA(rs)ab",angular_size:"10.7 × 5.1 arcmin"},
    {name:"Sunflower Galaxy — M63",ra:198.955500,dec:42.029300,fov:0.220,morphology:"SA(rs)bc",angular_size:"12.6 × 7.2 arcmin"},
    {name:"Triangulum Galaxy — M33",ra:23.462100,dec:30.659900,fov:1.200,morphology:"SA(s)cd",angular_size:"70.8 × 41.7 arcmin"},
    {name:"Cartwheel Galaxy",ra:9.421300,dec:-33.716000,fov:0.100,morphology:"Collisional ring galaxy",angular_size:"1.3 × 1.2 arcmin"},
    {name:"Stephan's Quintet — HCG 92",ra:338.989600,dec:33.956000,fov:0.120,morphology:"Compact galaxy group",angular_size:"4.7 × 3.5 arcmin"},
    {name:"Antennae Galaxies — NGC 4038/4039",ra:180.470800,dec:-18.875000,fov:0.180,morphology:"Interacting galaxy pair",angular_size:"5.2 × 3.1 arcmin"},
    {name:"Tadpole Galaxy — UGC 10214",ra:241.568900,dec:55.424900,fov:0.100,morphology:"Disturbed barred spiral",angular_size:"3.6 × 0.8 arcmin"},
    {name:"Hoag's Object",ra:229.586700,dec:21.585300,fov:0.060,morphology:"Ring galaxy",angular_size:"0.28 × 0.28 arcmin"},
    {name:"Centaurus A — NGC 5128",ra:201.365100,dec:-43.019100,fov:0.500,morphology:"Peculiar elliptical / radio galaxy",angular_size:"25.7 × 20.0 arcmin"},
    {name:"Great Barred Spiral — NGC 1365",ra:53.401600,dec:-36.140400,fov:0.220,morphology:"SB(s)b",angular_size:"11.2 × 6.2 arcmin"},
    {name:"NGC 1300",ra:49.920800,dec:-19.411700,fov:0.160,morphology:"Grand-design barred spiral",angular_size:"6.2 × 4.1 arcmin"},
    {name:"Southern Pinwheel — M83",ra:204.253900,dec:-29.865800,fov:0.420,morphology:"SAB(s)c",angular_size:"12.9 × 11.5 arcmin"},
    {name:"NGC 6744",ra:287.442100,dec:-63.857500,fov:0.400,morphology:"Milky-Way-like barred spiral",angular_size:"20.0 × 12.9 arcmin"}
  ];

  function viewer26CurrentSurvey() {
    return document.getElementById('viewer14SurveySelect')?.value || 'P/DSS2/color';
  }

  function viewer26ShowMagic(index) {
    const item = VIEWER26_MAGIC_GALAXIES[index];
    if (!item || typeof window.viewer14ShowGalaxy !== 'function') return;
    const galaxy = {
      ok: true,
      name: item.name,
      catalog: 'Aladin Magic — 20 showpiece galaxies',
      ra: item.ra,
      dec: item.dec,
      fov: item.fov,
      survey_id: viewer26CurrentSurvey(),
      morphology: item.morphology,
      angular_size: item.angular_size,
      redshift_distance: 'Select Get Info for live SIMBAD data',
      velocity_kms: null,
      physical_size: null,
      magnitude: null,
      attempts: 1,
      elapsed_seconds: 0,
      source: 'Aladin Magic curated demonstration catalog'
    };
    window.viewer14ShowGalaxy(galaxy);
    const select = document.getElementById('viewer26MagicSelect');
    if (select) select.value = String(index);
  }

  window.viewer26ShowMagic = viewer26ShowMagic;

  function installViewer26Magic() {
    const root = document.getElementById('viewer14-root');
    const controls = root?.querySelector('.controls');
    const catalog = document.getElementById('viewer14CatalogMode');
    if (!root || !controls || !catalog) return false;

    let wrap = document.getElementById('viewer26MagicWrap');
    if (!wrap) {
      wrap = document.createElement('label');
      wrap.id = 'viewer26MagicWrap';
      wrap.className = 'viewer26-magic-wrap';
      wrap.innerHTML = `
        <span class="viewer26-magic-label">Aladin Magic</span>
        <select id="viewer26MagicSelect" aria-label="Aladin Magic beautiful galaxy selector">
          <option value="">Choose one of 20 showpiece galaxies…</option>
          ${VIEWER26_MAGIC_GALAXIES.map((g,i)=>`<option value="${i}">${i+1}. ${g.name}</option>`).join('')}
        </select>`;
      catalog.parentElement.insertAdjacentElement('beforebegin', wrap);
      document.getElementById('viewer26MagicSelect').addEventListener('change', event => {
        const index = Number(event.target.value);
        if (Number.isInteger(index)) viewer26ShowMagic(index);
      });
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-26';
    return true;
  }

  const oldStyle = document.getElementById('viewer26-magic-style');
  if (oldStyle) oldStyle.remove();
  const style = document.createElement('style');
  style.id = 'viewer26-magic-style';
  style.textContent = `
    #viewer14-root .viewer26-magic-wrap {
      display:flex;
      align-items:center;
      gap:8px;
      min-width:360px;
    }
    #viewer14-root .viewer26-magic-label {
      color:#ffd84d;
      font-weight:800;
      white-space:nowrap;
    }
    #viewer14-root #viewer26MagicSelect {
      min-width:285px;
      max-width:430px;
      border-color:#8a4fd4;
      box-shadow:0 0 8px rgba(138,79,212,.38);
    }
    #viewer14-root #viewer26MagicSelect:focus {
      border-color:#c98cff;
      box-shadow:0 0 12px rgba(201,140,255,.72);
    }
    @media (max-width:700px) {
      #viewer14-root .viewer26-magic-wrap {min-width:100%;width:100%;flex-wrap:wrap}
      #viewer14-root #viewer26MagicSelect {min-width:100%;max-width:100%;width:100%}
    }
  `;
  document.head.appendChild(style);

  installViewer26Magic();
  const timer = setInterval(() => {
    if (installViewer26Magic()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installViewer26Magic();
    clearInterval(timer);
  }, 16000);
})();
'''))