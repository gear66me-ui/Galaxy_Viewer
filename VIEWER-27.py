from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from google.colab import output
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-26.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-26-base.py", "exec"))


def viewer27_resolve_magic_name(name):
    try:
        encoded = urllib.parse.quote(str(name).strip(), safe="")
        request = urllib.request.Request(
            f"https://cds.unistra.fr/cgi-bin/nph-sesame/-oxp/SNV?{encoded}",
            headers={"User-Agent": "GalaxyViewer/27"},
        )
        with urllib.request.urlopen(request, timeout=35) as response:
            root = ET.fromstring(response.read())
        ra = root.find(".//jradeg")
        dec = root.find(".//jdedeg")
        if ra is None or dec is None:
            raise RuntimeError(f"CDS Sesame could not resolve {name}")
        return json.dumps({"ok": True, "name": str(name), "ra": float(ra.text), "dec": float(dec.text)})
    except Exception as exc:
        return json.dumps({"ok": False, "name": str(name), "error": str(exc)})


output.register_callback("viewer27.resolveMagicName", viewer27_resolve_magic_name)


display(Javascript(r'''
(() => {
  const FEATURED = [
    {name:"Cartwheel Galaxy",query:"Cartwheel Galaxy",ra:9.4213,dec:-33.7160,fov:.060,survey:"CDS/P/JWST/EPO"},
    {name:"Stephan's Quintet — HCG 92",query:"HCG 92",ra:338.9896,dec:33.9560,fov:.095,survey:"CDS/P/JWST/EPO"},
    {name:"Whirlpool Galaxy — M51",query:"M 51",ra:202.4696,dec:47.1953,fov:.180,survey:"CDS/P/HST/EPO"},
    {name:"Sombrero Galaxy — M104",query:"M 104",ra:189.9976,dec:-11.6231,fov:.130,survey:"CDS/P/HST/EPO"},
    {name:"Antennae Galaxies — NGC 4038/4039",query:"NGC 4038",ra:180.4708,dec:-18.8750,fov:.120,survey:"CDS/P/HST/EPO"},
    {name:"Tadpole Galaxy — UGC 10214",query:"UGC 10214",ra:241.5689,dec:55.4249,fov:.075,survey:"CDS/P/HST/EPO"},
    {name:"Hoag's Object",query:"Hoag's Object",ra:229.5867,dec:21.5853,fov:.035,survey:"CDS/P/HST/EPO"},
    {name:"NGC 1300",query:"NGC 1300",ra:49.9208,dec:-19.4117,fov:.110,survey:"CDS/P/HST/EPO"},
    {name:"Great Barred Spiral — NGC 1365",query:"NGC 1365",ra:53.4016,dec:-36.1404,fov:.150,survey:"CDS/P/JWST/EPO"},
    {name:"Pinwheel Galaxy — M101",query:"M 101",ra:210.8023,dec:54.3490,fov:.360,survey:"CDS/P/HST/EPO"},
    {name:"Cigar Galaxy — M82",query:"M 82",ra:148.9685,dec:69.6797,fov:.140,survey:"CDS/P/HST/EPO"},
    {name:"Black Eye Galaxy — M64",query:"M 64",ra:194.1821,dec:21.6827,fov:.120,survey:"CDS/P/HST/EPO"},
    {name:"Southern Pinwheel — M83",query:"M 83",ra:204.2539,dec:-29.8658,fov:.230,survey:"CDS/P/HST/EPO"},
    {name:"Phantom Galaxy — M74",query:"M 74",ra:24.1740,dec:15.7837,fov:.150,survey:"CDS/P/JWST/EPO"},
    {name:"Andromeda Galaxy — M31",query:"M 31",ra:10.6847,dec:41.2688,fov:3.20,survey:"P/DSS2/color"},
    {name:"Triangulum Galaxy — M33",query:"M 33",ra:23.4621,dec:30.6599,fov:1.20,survey:"CDS/P/HST/EPO"},
    {name:"Centaurus A — NGC 5128",query:"NGC 5128",ra:201.3651,dec:-43.0191,fov:.270,survey:"CDS/P/HST/EPO"},
    {name:"Sculptor Galaxy — NGC 253",query:"NGC 253",ra:11.8880,dec:-25.2882,fov:.350,survey:"CDS/P/HST/EPO"},
    {name:"Bode's Galaxy — M81",query:"M 81",ra:148.8882,dec:69.0653,fov:.320,survey:"CDS/P/HST/EPO"},
    {name:"Sunflower Galaxy — M63",query:"M 63",ra:198.9555,dec:42.0293,fov:.180,survey:"CDS/P/HST/EPO"}
  ];

  const EXTRA_NAMES = `M 49|M 58|M 59|M 60|M 61|M 65|M 66|M 77|M 84|M 85|M 86|M 87|M 88|M 89|M 90|M 91|M 94|M 95|M 96|M 98|M 99|M 100|M 102|M 105|M 106|M 108|M 109|M 110|NGC 55|NGC 247|NGC 300|NGC 488|NGC 520|NGC 660|NGC 772|NGC 891|NGC 925|NGC 1023|NGC 1055|NGC 1097|NGC 1232|NGC 1266|NGC 1316|NGC 1398|NGC 1512|NGC 1532|NGC 1566|NGC 1672|NGC 1808|NGC 2207|IC 2163|NGC 2403|NGC 2683|NGC 2775|NGC 2841|NGC 2903|NGC 2976|NGC 3079|NGC 3109|NGC 3184|NGC 3190|NGC 3198|NGC 3227|NGC 3310|NGC 3344|NGC 3351|NGC 3368|NGC 3370|NGC 3377|NGC 3379|NGC 3384|NGC 3486|NGC 3521|NGC 3556|NGC 3621|NGC 3627|NGC 3628|NGC 3718|NGC 3729|NGC 3949|NGC 3953|NGC 4013|NGC 4027|NGC 4088|NGC 4214|NGC 4216|NGC 4244|NGC 4254|NGC 4258|NGC 4274|NGC 4298|NGC 4302|NGC 4303|NGC 4314|NGC 4321|NGC 4388|NGC 4395|NGC 4402|NGC 4414|NGC 4435|NGC 4438|NGC 4449|NGC 4450|NGC 4490|NGC 4526|NGC 4535|NGC 4536|NGC 4548|NGC 4559|NGC 4565|NGC 4567|NGC 4568|NGC 4571|NGC 4594|NGC 4625|NGC 4631|NGC 4656|NGC 4697|NGC 4725|NGC 4736|NGC 474|NGC 4826|NGC 4945|NGC 5005|NGC 5033|NGC 5055|NGC 5194|NGC 5195|NGC 5236|NGC 5253|NGC 5457|NGC 5474|NGC 5584|NGC 5866|NGC 5907|NGC 6503|NGC 6822|NGC 6946|NGC 7331|NGC 7479|NGC 7496|NGC 7552|NGC 7590|NGC 7814|IC 342|IC 2574|IC 5332|Arp 220|Arp 273|Arp 244|Arp 147|Arp 87|Arp 104|Arp 105|Arp 116|Arp 188|Arp 214|Arp 240|Arp 242|Arp 256|Arp 261|Arp 272|Arp 284|Arp 286|Arp 295|Arp 299|Arp 302|Arp 319|Arp 321|Arp 331|Arp 337|Arp 81|Arp 84|Arp 91|Arp 93|Arp 94|Arp 97|UGC 2885|UGC 1810|UGC 1813|ESO 137-001|ESO 510-G13|AM 0644-741|II Zw 96|VV 340|Mayall's Object|Comet Galaxy|Medusa Merger|Atoms-for-Peace Galaxy|Malin 1|Malin 2|NGC 1275|NGC 1705|NGC 2146|NGC 2623|NGC 3256|NGC 3314|NGC 3923|NGC 4194|NGC 4261|NGC 4472|NGC 4486|NGC 4649|NGC 5018|NGC 5044|NGC 5846|NGC 6166|NGC 6240|NGC 7252|NGC 7600|NGC 7742|NGC 7743|NGC 7714|NGC 4676A|NGC 4676B|NGC 6621|NGC 6622|NGC 6872|IC 4970|NGC 5291|NGC 7317|NGC 7318A|NGC 7318B|NGC 7319|NGC 7320|NGC 922|NGC 985|NGC 1614|NGC 6052|NGC 7674`.split('|');

  const MAGIC200 = [...FEATURED, ...EXTRA_NAMES.map(name => ({name, query:name, fov:.16, survey:'CDS/P/HST/EPO'}))].slice(0, 200);
  let magicIndex = Math.floor(Math.random() * MAGIC200.length);
  let currentMagicGalaxy = null;

  function parsedResult(response) {
    return typeof window.viewer14Result === 'function' ? window.viewer14Result(response) : (response?.data || response);
  }

  async function resolveItem(item) {
    if (Number.isFinite(item.ra) && Number.isFinite(item.dec)) return item;
    const response = await google.colab.kernel.invokeFunction('viewer27.resolveMagicName', [item.query || item.name], {});
    const resolved = parsedResult(response);
    if (!resolved || resolved.ok !== true) throw new Error(resolved?.error || `Could not resolve ${item.name}`);
    item.ra = Number(resolved.ra);
    item.dec = Number(resolved.dec);
    return item;
  }

  async function showMagic(index) {
    magicIndex = (Number(index) + MAGIC200.length) % MAGIC200.length;
    const item = await resolveItem(MAGIC200[magicIndex]);
    const galaxy = {
      ok:true,
      name:item.name,
      catalog:'Aladin Magic 200',
      ra:item.ra,
      dec:item.dec,
      fov:Number(item.fov || .16),
      survey_id:item.survey || 'CDS/P/HST/EPO',
      morphology:'Use Get Info for live SIMBAD classification',
      angular_size:'Use Get Info for catalog angular size',
      redshift_distance:'Use Get Info for live SIMBAD data',
      velocity_kms:null,
      physical_size:'Research pending',
      magnitude:'Research pending',
      age:'Research pending — use Google Chrome Search',
      interest_score:'Aladin Magic 200 selection',
      distance_method:'Use Get Info for catalog method',
      attempts:1,
      elapsed_seconds:0,
      source:'Aladin Magic 200 curated named-galaxy list'
    };
    currentMagicGalaxy = galaxy;
    window.viewer14ShowGalaxy(galaxy);
    const select = document.getElementById('viewer27MagicSelect');
    if (select) select.value = String(magicIndex);
  }

  window.viewer27PreviousMagic = () => showMagic(magicIndex - 1);
  window.viewer27NextMagic = () => showMagic(magicIndex + 1);

  function chromeSearch() {
    let galaxy = currentMagicGalaxy;
    if (!galaxy) {
      const coordinateText = document.getElementById('viewer14CoordBox')?.value || '';
      const parts = coordinateText.trim().split(/\s+/);
      galaxy = {name:'Galaxy', ra:parts[0] || '', dec:parts[1] || ''};
    }
    const query = `${galaxy.name} galaxy RA ${galaxy.ra} Dec ${galaxy.dec} age redshift distance morphology physical size magnitude`;
    window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank', 'noopener,noreferrer');
  }
  window.viewer27ChromeSearch = chromeSearch;

  function install() {
    const root = document.getElementById('viewer14-root');
    const controls = root?.querySelector('.controls');
    if (!root || !controls) return false;

    document.getElementById('viewer26MagicWrap')?.remove();

    let wrap = document.getElementById('viewer27MagicWrap');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.id = 'viewer27MagicWrap';
      wrap.className = 'viewer27-magic-wrap';
      wrap.innerHTML = `
        <span class="viewer27-magic-label">Aladin Magic 200</span>
        <button id="viewer27MagicPrevious" type="button" class="viewer27-magic-arrow viewer27-magic-left" title="Previous Aladin Magic galaxy" aria-label="Previous Aladin Magic galaxy">◀</button>
        <select id="viewer27MagicSelect" aria-label="Aladin Magic 200 galaxy selector">
          ${MAGIC200.map((g,i)=>`<option value="${i}">${i+1}. ${g.name}</option>`).join('')}
        </select>
        <button id="viewer27MagicNext" type="button" class="viewer27-magic-arrow viewer27-magic-right" title="Next Aladin Magic galaxy" aria-label="Next Aladin Magic galaxy">▶</button>`;
      controls.appendChild(wrap);
      document.getElementById('viewer27MagicPrevious').onclick = window.viewer27PreviousMagic;
      document.getElementById('viewer27MagicNext').onclick = window.viewer27NextMagic;
      document.getElementById('viewer27MagicSelect').addEventListener('change', event => showMagic(Number(event.target.value)));
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-27';
    return true;
  }

  const originalShowGalaxy = window.viewer14ShowGalaxy;
  if (typeof originalShowGalaxy === 'function' && !originalShowGalaxy.viewer27Wrapped) {
    const wrapped = function(galaxy) {
      currentMagicGalaxy = galaxy;
      if (!galaxy.age || /^not available/i.test(String(galaxy.age))) {
        galaxy = {...galaxy, age:'Research pending — use Google Chrome Search'};
      }
      originalShowGalaxy(galaxy);
      setTimeout(() => {
        const title = document.querySelector('#viewer14Status .fom-title');
        if (title && !document.getElementById('viewer27ChromeSearch')) {
          const button = document.createElement('button');
          button.id = 'viewer27ChromeSearch';
          button.type = 'button';
          button.className = 'viewer27-chrome-search';
          button.textContent = 'Google Chrome Search';
          button.onclick = chromeSearch;
          title.appendChild(button);
        }
      }, 0);
    };
    wrapped.viewer27Wrapped = true;
    window.viewer14ShowGalaxy = wrapped;
  }

  const oldStyle = document.getElementById('viewer27-style');
  if (oldStyle) oldStyle.remove();
  const style = document.createElement('style');
  style.id = 'viewer27-style';
  style.textContent = `
    #viewer14-root .viewer27-magic-wrap{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
    #viewer14-root .viewer27-magic-label{color:#ffd84d;font-weight:800;white-space:nowrap}
    #viewer14-root #viewer27MagicSelect{min-width:285px;max-width:430px;border-color:#8a4fd4}
    #viewer14-root .viewer27-magic-arrow{width:29px!important;min-width:29px!important;height:29px!important;padding:0!important;border-radius:7px!important;background:#000!important;font-size:18px!important;line-height:1!important}
    #viewer14-root .viewer27-magic-left{color:#ff1a1a!important;border:1px solid #ff1a1a!important}
    #viewer14-root .viewer27-magic-right{color:#9dff00!important;border:1px solid #9dff00!important}
    #viewer14-root .viewer27-magic-arrow:active{filter:brightness(1.8);transform:scale(1.08)}
    #viewer14Status .fom-title{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
    #viewer14-root .viewer27-chrome-search{padding:7px 12px;font-size:13px;background:#1a73e8;border-radius:7px;color:#fff}
    @media(max-width:700px){#viewer14-root .viewer27-magic-wrap{width:100%}#viewer14-root #viewer27MagicSelect{min-width:220px;flex:1}}
  `;
  document.head.appendChild(style);

  install();
  const timer = setInterval(() => {
    if (install()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    install();
    showMagic(magicIndex).catch(error => window.viewer14Status(`Aladin Magic 200 failed: ${error.message}`));
    clearInterval(timer);
  }, 1200);
})();
'''))
