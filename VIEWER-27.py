from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-26.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-26-base.py", "exec"))


display(Javascript(r'''
(() => {
  const MAGIC = [
    {name:"Cartwheel Galaxy",ra:9.4213,dec:-33.7160,fov:0.060,survey:"CDS/P/JWST/EPO",morphology:"Collisional ring galaxy"},
    {name:"Stephan's Quintet — HCG 92",ra:338.9896,dec:33.9560,fov:0.095,survey:"CDS/P/JWST/EPO",morphology:"Compact interacting galaxy group"},
    {name:"Whirlpool Galaxy — M51",ra:202.4696,dec:47.1953,fov:0.180,survey:"CDS/P/HST/EPO",morphology:"Grand-design interacting spiral"},
    {name:"Sombrero Galaxy — M104",ra:189.9976,dec:-11.6231,fov:0.130,survey:"CDS/P/HST/EPO",morphology:"Edge-on spiral galaxy"},
    {name:"Antennae Galaxies — NGC 4038/4039",ra:180.4708,dec:-18.8750,fov:0.120,survey:"CDS/P/HST/EPO",morphology:"Interacting galaxy pair"},
    {name:"Tadpole Galaxy — UGC 10214",ra:241.5689,dec:55.4249,fov:0.075,survey:"CDS/P/HST/EPO",morphology:"Disturbed spiral with tidal tail"},
    {name:"Hoag's Object",ra:229.5867,dec:21.5853,fov:0.035,survey:"CDS/P/HST/EPO",morphology:"Nearly perfect ring galaxy"},
    {name:"NGC 1300",ra:49.9208,dec:-19.4117,fov:0.110,survey:"CDS/P/HST/EPO",morphology:"Grand-design barred spiral"},
    {name:"Great Barred Spiral — NGC 1365",ra:53.4016,dec:-36.1404,fov:0.150,survey:"CDS/P/JWST/EPO",morphology:"Barred spiral galaxy"},
    {name:"Pinwheel Galaxy — M101",ra:210.8023,dec:54.3490,fov:0.360,survey:"CDS/P/HST/EPO",morphology:"Face-on grand-design spiral"},
    {name:"Cigar Galaxy — M82",ra:148.9685,dec:69.6797,fov:0.140,survey:"CDS/P/HST/EPO",morphology:"Starburst galaxy"},
    {name:"Black Eye Galaxy — M64",ra:194.1821,dec:21.6827,fov:0.120,survey:"CDS/P/HST/EPO",morphology:"Spiral galaxy with dark dust lane"},
    {name:"Southern Pinwheel — M83",ra:204.2539,dec:-29.8658,fov:0.230,survey:"CDS/P/HST/EPO",morphology:"Barred spiral galaxy"},
    {name:"Phantom Galaxy — M74",ra:24.1740,dec:15.7837,fov:0.150,survey:"CDS/P/JWST/EPO",morphology:"Face-on grand-design spiral"},
    {name:"NGC 628 — JWST spiral",ra:24.1740,dec:15.7837,fov:0.105,survey:"CDS/P/JWST/EPO",morphology:"Face-on spiral galaxy"},
    {name:"NGC 1566 — Spanish Dancer",ra:65.0017,dec:-54.9380,fov:0.115,survey:"CDS/P/JWST/EPO",morphology:"Intermediate spiral galaxy"},
    {name:"NGC 7496",ra:347.4470,dec:-43.4279,fov:0.090,survey:"CDS/P/JWST/EPO",morphology:"Barred spiral galaxy"},
    {name:"NGC 1433",ra:55.5060,dec:-47.2214,fov:0.105,survey:"CDS/P/JWST/EPO",morphology:"Ringed barred spiral"},
    {name:"NGC 3351 — M95",ra:160.9906,dec:11.7037,fov:0.110,survey:"CDS/P/JWST/EPO",morphology:"Ringed barred spiral"},
    {name:"Centaurus A — NGC 5128",ra:201.3651,dec:-43.0191,fov:0.270,survey:"CDS/P/HST/EPO",morphology:"Peculiar dust-lane radio galaxy"}
  ];

  let current = 0;
  window.viewer27MagicActive = true;

  function galaxyData(item) {
    return {
      ok:true,name:item.name,catalog:"Aladin Magic — curated showpiece catalog",
      ra:item.ra,dec:item.dec,fov:item.fov,survey_id:item.survey,
      morphology:item.morphology,angular_size:"Curated display framing",
      redshift_distance:"Use Get Info for live SIMBAD data",velocity_kms:null,
      physical_size:null,magnitude:null,attempts:1,elapsed_seconds:0,
      source:"Aladin Magic curated Hubble/JWST outreach selection"
    };
  }

  function show(index) {
    if (!window.viewer14Aladin || typeof window.viewer14ShowGalaxy !== 'function') return false;
    current = (index + MAGIC.length) % MAGIC.length;
    const item = MAGIC[current];
    window.viewer14ShowGalaxy(galaxyData(item));
    const select = document.getElementById('viewer27MagicSelect');
    if (select) select.value = String(current);
    return true;
  }
  window.viewer27ShowMagic = show;

  function disableRandomStartup() {
    window.viewer14RandomGalaxy = async function() {
      if (!window.viewer27MagicActive) return;
      show(current);
    };
  }
  disableRandomStartup();

  function install() {
    const root = document.getElementById('viewer14-root');
    const controls = root?.querySelector('.controls');
    const randomButton = document.getElementById('viewer14RandomButton');
    if (!root || !controls || !randomButton) return false;

    document.getElementById('viewer26MagicWrap')?.remove();
    let wrap = document.getElementById('viewer27MagicWrap');
    if (!wrap) {
      wrap = document.createElement('label');
      wrap.id = 'viewer27MagicWrap';
      wrap.className = 'viewer27-magic-wrap';
      wrap.innerHTML = `<span>Aladin Magic</span><select id="viewer27MagicSelect" aria-label="Aladin Magic galaxy selector">${MAGIC.map((g,i)=>`<option value="${i}">${i+1}. ${g.name}</option>`).join('')}</select>`;
      randomButton.insertAdjacentElement('beforebegin', wrap);
      document.getElementById('viewer27MagicSelect').addEventListener('change', e => show(Number(e.target.value)));
    }

    randomButton.textContent = 'Aladin Magic';
    randomButton.title = 'Show next curated galaxy';
    randomButton.onclick = () => show(current + 1);
    randomButton.disabled = false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-27';
    return true;
  }

  const style = document.createElement('style');
  style.id = 'viewer27-magic-style';
  style.textContent = `
    #viewer14-root .viewer27-magic-wrap{display:flex;align-items:center;gap:8px;min-width:390px}
    #viewer14-root .viewer27-magic-wrap span{color:#ffd84d;font-weight:800;white-space:nowrap}
    #viewer14-root #viewer27MagicSelect{min-width:300px;border-color:#b566ff;box-shadow:0 0 9px rgba(181,102,255,.55)}
    #viewer14-root #viewer27MagicSelect:focus{border-color:#e1b8ff;box-shadow:0 0 14px rgba(225,184,255,.85)}
    @media(max-width:700px){#viewer14-root .viewer27-magic-wrap{min-width:100%;width:100%;flex-wrap:wrap}#viewer14-root #viewer27MagicSelect{width:100%;min-width:100%}}
  `;
  document.head.appendChild(style);

  install();
  const timer = setInterval(() => {
    disableRandomStartup();
    install();
    if (show(0)) clearInterval(timer);
  }, 150);
  setTimeout(() => show(0), 1200);
  setTimeout(() => show(0), 3000);
  setTimeout(() => { install(); show(0); clearInterval(timer); }, 7000);
})();
'''))