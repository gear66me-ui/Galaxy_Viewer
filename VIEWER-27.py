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


display(Javascript(r"""
(() => {
  const FEATURED = [
{name:"Cartwheel Galaxy",query:"Cartwheel Galaxy",ra:9.4213,dec:-33.716,fov:0.06,survey:"CDS/P/JWST/EPO",morphology:"Collisional ring galaxy"},
{name:"Stephan's Quintet — HCG 92",query:"HCG 92",ra:338.9896,dec:33.956,fov:0.095,survey:"CDS/P/JWST/EPO",morphology:"Compact interacting galaxy group"},
{name:"Whirlpool Galaxy — M51",query:"M 51",ra:202.4696,dec:47.1953,fov:0.18,survey:"CDS/P/HST/EPO",morphology:"Grand-design interacting spiral"},
{name:"Sombrero Galaxy — M104",query:"M 104",ra:189.9976,dec:-11.6231,fov:0.13,survey:"CDS/P/HST/EPO",morphology:"Edge-on spiral galaxy"},
{name:"Antennae Galaxies — NGC 4038/4039",query:"NGC 4038",ra:180.4708,dec:-18.875,fov:0.12,survey:"CDS/P/HST/EPO",morphology:"Interacting galaxy pair"},
{name:"Tadpole Galaxy — UGC 10214",query:"UGC 10214",ra:241.5689,dec:55.4249,fov:0.075,survey:"CDS/P/HST/EPO",morphology:"Disturbed spiral with tidal tail"},
{name:"Hoag's Object",query:"Hoag's Object",ra:229.5867,dec:21.5853,fov:0.035,survey:"CDS/P/HST/EPO",morphology:"Ring galaxy"},
{name:"NGC 1300",query:"NGC 1300",ra:49.9208,dec:-19.4117,fov:0.11,survey:"CDS/P/HST/EPO",morphology:"Grand-design barred spiral"},
{name:"Great Barred Spiral — NGC 1365",query:"NGC 1365",ra:53.4016,dec:-36.1404,fov:0.15,survey:"CDS/P/JWST/EPO",morphology:"Barred spiral galaxy"},
{name:"Pinwheel Galaxy — M101",query:"M 101",ra:210.8023,dec:54.349,fov:0.36,survey:"CDS/P/HST/EPO",morphology:"Face-on grand-design spiral"},
{name:"Cigar Galaxy — M82",query:"M 82",ra:148.9685,dec:69.6797,fov:0.14,survey:"CDS/P/HST/EPO",morphology:"Starburst galaxy"},
{name:"Black Eye Galaxy — M64",query:"M 64",ra:194.1821,dec:21.6827,fov:0.12,survey:"CDS/P/HST/EPO",morphology:"Spiral galaxy with dark dust lane"},
{name:"Southern Pinwheel — M83",query:"M 83",ra:204.2539,dec:-29.8658,fov:0.23,survey:"CDS/P/HST/EPO",morphology:"Barred spiral galaxy"},
{name:"Phantom Galaxy — M74",query:"M 74",ra:24.174,dec:15.7837,fov:0.15,survey:"CDS/P/JWST/EPO",morphology:"Face-on grand-design spiral"},
{name:"Andromeda Galaxy — M31",query:"M 31",ra:10.6847,dec:41.2688,fov:3.2,survey:"P/DSS2/color",morphology:"Large spiral galaxy"},
{name:"Triangulum Galaxy — M33",query:"M 33",ra:23.4621,dec:30.6599,fov:1.2,survey:"CDS/P/HST/EPO",morphology:"Face-on spiral galaxy"},
{name:"Centaurus A — NGC 5128",query:"NGC 5128",ra:201.3651,dec:-43.0191,fov:0.27,survey:"CDS/P/HST/EPO",morphology:"Peculiar dust-lane radio galaxy"},
{name:"Sculptor Galaxy — NGC 253",query:"NGC 253",ra:11.888,dec:-25.2882,fov:0.35,survey:"CDS/P/HST/EPO",morphology:"Starburst spiral galaxy"},
{name:"Bode's Galaxy — M81",query:"M 81",ra:148.8882,dec:69.0653,fov:0.32,survey:"CDS/P/HST/EPO",morphology:"Grand-design spiral"},
{name:"Sunflower Galaxy — M63",query:"M 63",ra:198.9555,dec:42.0293,fov:0.18,survey:"CDS/P/HST/EPO",morphology:"Flocculent spiral galaxy"}
  ];

  const EXTRA_NAMES = "M 49|M 58|M 59|M 60|M 61|M 65|M 66|M 77|M 84|M 85|M 86|M 87|M 88|M 89|M 90|M 91|M 94|M 95|M 96|M 98|M 99|M 100|M 102|M 105|M 106|M 108|M 109|M 110|NGC 55|NGC 247|NGC 300|NGC 488|NGC 520|NGC 660|NGC 772|NGC 891|NGC 925|NGC 1023|NGC 1055|NGC 1097|NGC 1232|NGC 1266|NGC 1316|NGC 1398|NGC 1512|NGC 1532|NGC 1566|NGC 1672|NGC 1808|NGC 2207|IC 2163|NGC 2403|NGC 2683|NGC 2775|NGC 2841|NGC 2903|NGC 2976|NGC 3079|NGC 3109|NGC 3184|NGC 3190|NGC 3198|NGC 3227|NGC 3310|NGC 3344|NGC 3351|NGC 3368|NGC 3370|NGC 3377|NGC 3379|NGC 3384|NGC 3486|NGC 3521|NGC 3556|NGC 3621|NGC 3627|NGC 3628|NGC 3718|NGC 3729|NGC 3949|NGC 3953|NGC 4013|NGC 4027|NGC 4088|NGC 4214|NGC 4216|NGC 4244|NGC 4254|NGC 4258|NGC 4274|NGC 4298|NGC 4302|NGC 4303|NGC 4314|NGC 4321|NGC 4388|NGC 4395|NGC 4402|NGC 4414|NGC 4435|NGC 4438|NGC 4449|NGC 4450|NGC 4490|NGC 4526|NGC 4535|NGC 4536|NGC 4548|NGC 4559|NGC 4565|NGC 4567|NGC 4568|NGC 4571|NGC 4594|NGC 4625|NGC 4631|NGC 4656|NGC 4697|NGC 4725|NGC 4736|NGC 474|NGC 4826|NGC 4945|NGC 5005|NGC 5033|NGC 5055|NGC 5194|NGC 5195|NGC 5236|NGC 5253|NGC 5457|NGC 5474|NGC 5584|NGC 5866|NGC 5907|NGC 6503|NGC 6822|NGC 6946|NGC 7331|NGC 7479|NGC 7496|NGC 7552|NGC 7590|NGC 7814|IC 342|IC 2574|IC 5332|Arp 220|Arp 273|Arp 244|Arp 147|Arp 87|Arp 104|Arp 105|Arp 116|Arp 188|Arp 214|Arp 240|Arp 242|Arp 256|Arp 261|Arp 272|Arp 284|Arp 286|Arp 295|Arp 299|Arp 302|Arp 319|Arp 321|Arp 331|Arp 337|Arp 81|Arp 84|Arp 91|Arp 93|Arp 94|Arp 97|UGC 2885|UGC 1810|UGC 1813|ESO 137-001|ESO 510-G13|AM 0644-741|II Zw 96|VV 340|Mayall's Object|Comet Galaxy|Medusa Merger|Atoms-for-Peace Galaxy|Malin 1|Malin 2|NGC 1275|NGC 1705|NGC 2146|NGC 2623|NGC 3256|NGC 3314|NGC 3923|NGC 4194|NGC 4261|NGC 4472|NGC 4486|NGC 4649|NGC 5018|NGC 5044|NGC 5846|NGC 6166|NGC 6240|NGC 7252|NGC 7600|NGC 7742|NGC 7743|NGC 7714|NGC 4676A|NGC 4676B|NGC 6621|NGC 6622|NGC 6872|IC 4970|NGC 5291|NGC 7317|NGC 7318A|NGC 7318B|NGC 7319|NGC 7320|NGC 922|NGC 985|NGC 1614|NGC 6052|NGC 7674".split('|').slice(0,180);
  const MAGIC200 = [...FEATURED, ...EXTRA_NAMES.map(name => ({name, query:name, fov:.16, survey:'CDS/P/HST/EPO', morphology:'Galaxy'}))];

  let magicIndex = Math.floor(Math.random() * MAGIC200.length);
  let currentGalaxyForSearch = null;

  function parsedResult(response) {
    return typeof window.viewer14Result === 'function'
      ? window.viewer14Result(response)
      : (response?.data || response);
  }

  function ageEstimate(g) {
    const existing = String(g?.age || '').trim();
    if (existing && !/^not available$/i.test(existing)) return existing;

    const m = String(g?.morphology || '').toLowerCase();
    if (/(elliptical|lenticular|s0|radio galaxy)/.test(m))
      return 'Estimated 10–13 billion years — old stellar population inferred from morphology';
    if (/(starburst|irregular|interacting|merger|peculiar|tidal|collisional)/.test(m))
      return 'Estimated 1–10 billion years — mixed stellar populations; active recent star formation';
    if (/(spiral|barred|ring|sa|sb|sc|grand-design|flocculent)/.test(m))
      return 'Estimated 8–12 billion years — morphology-based stellar-population estimate';
    return 'Estimated 8–12 billion years — broad galaxy-population estimate; not a direct measurement';
  }

  function populateEstimates(g) {
    g.age = ageEstimate(g);
    if (!g.physical_size || /^not available$/i.test(String(g.physical_size)))
      g.physical_size = 'Estimate pending distance and angular-size solution';
    if (!g.magnitude || /^not available$/i.test(String(g.magnitude)))
      g.magnitude = 'Catalog photometry not returned';
    return g;
  }

  async function resolveItem(item) {
    if (Number.isFinite(item.ra) && Number.isFinite(item.dec)) return item;
    const response = await google.colab.kernel.invokeFunction(
      'viewer27.resolveMagicName', [item.query || item.name], {}
    );
    const resolved = parsedResult(response);
    if (!resolved || resolved.ok !== true)
      throw new Error(resolved?.error || `Could not resolve ${item.name}`);
    item.ra = Number(resolved.ra);
    item.dec = Number(resolved.dec);
    return item;
  }

  async function enrichFromSimbad(item) {
    try {
      const response = await google.colab.kernel.invokeFunction(
        'viewer14.getInfo', [Number(item.ra), Number(item.dec)], {}
      );
      const result = parsedResult(response);
      if (result && result.ok === true) return result;
    } catch (_) {}
    return null;
  }

  async function showMagic(index) {
    magicIndex = (Number(index) + MAGIC200.length) % MAGIC200.length;
    const item = await resolveItem(MAGIC200[magicIndex]);

    let galaxy = await enrichFromSimbad(item);
    galaxy = galaxy ? {...galaxy} : {
      ok:true,
      ra:item.ra,
      dec:item.dec,
      morphology:item.morphology || 'Galaxy',
      angular_size:'Catalog angular size not returned',
      redshift_distance:'Catalog redshift and distance not returned',
      velocity_kms:null,
      physical_size:null,
      magnitude:null,
      distance_method:'Catalog method not returned',
      attempts:1,
      elapsed_seconds:0
    };

    galaxy.ok = true;
    galaxy.name = item.name;
    galaxy.catalog = 'Aladin Magic 200';
    galaxy.ra = Number(item.ra);
    galaxy.dec = Number(item.dec);
    galaxy.fov = Number(item.fov || .16);
    galaxy.survey_id = item.survey || 'CDS/P/HST/EPO';
    galaxy.morphology = galaxy.morphology || item.morphology || 'Galaxy';
    galaxy.source = `${galaxy.source || 'SIMBAD'}; Aladin Magic 200 curated named-galaxy list`;
    galaxy.interest_score = 'Aladin Magic 200 curated selection';
    populateEstimates(galaxy);

    currentGalaxyForSearch = galaxy;
    window.viewer14ShowGalaxy(galaxy);

    const select = document.getElementById('viewer27MagicSelect');
    if (select) select.value = String(magicIndex);
  }

  window.viewer27PreviousMagic = () => showMagic(magicIndex - 1);
  window.viewer27NextMagic = () => showMagic(magicIndex + 1);
  window.viewer27RandomMagic = () => showMagic(Math.floor(Math.random() * MAGIC200.length));

  function chromeSearch() {
    const g = currentGalaxyForSearch || window.viewer27LastDisplayedGalaxy;
    const coordinateText = document.getElementById('viewer14CoordBox')?.value || '';
    const parts = coordinateText.trim().split(/\s+/);
    const name = g?.name || 'Galaxy';
    const ra = Number.isFinite(Number(g?.ra)) ? Number(g.ra).toFixed(6) : (parts[0] || '');
    const dec = Number.isFinite(Number(g?.dec)) ? Number(g.dec).toFixed(6) : (parts[1] || '');
    const query = `${name} galaxy RA ${ra} Dec ${dec} age redshift distance morphology physical size magnitude`;
    window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank', 'noopener,noreferrer');
  }
  window.viewer27ChromeSearch = chromeSearch;

  const originalShowGalaxy = window.viewer14ShowGalaxy;
  if (typeof originalShowGalaxy === 'function' && !originalShowGalaxy.viewer27Wrapped) {
    const wrapped = function(g) {
      populateEstimates(g);
      window.viewer27LastDisplayedGalaxy = g;
      currentGalaxyForSearch = g;
      return originalShowGalaxy(g);
    };
    wrapped.viewer27Wrapped = true;
    window.viewer14ShowGalaxy = wrapped;
  }

  const originalPanel = window.viewer14Panel;
  if (typeof originalPanel === 'function' && !originalPanel.viewer27Wrapped) {
    const wrappedPanel = function(g, survey, fov) {
      populateEstimates(g);
      let html = originalPanel(g, survey, fov);
      const button = `<button type="button" class="viewer27-chrome-search" onclick="viewer27ChromeSearch()" title="Search Google using object name and coordinates">Google Chrome Search</button>`;
      html = html.replace(
        '<div class="fom-title">RANDOM GALAXY FIGURES OF MERIT</div>',
        `<div class="fom-title"><span>RANDOM GALAXY FIGURES OF MERIT</span>${button}</div>`
      );
      return html;
    };
    wrappedPanel.viewer27Wrapped = true;
    window.viewer14Panel = wrappedPanel;
  }

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
      document.getElementById('viewer27MagicSelect').onchange = e => showMagic(Number(e.target.value));
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-27';
    return true;
  }

  document.getElementById('viewer27-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer27-style';
  style.textContent = `
    #viewer14-root .viewer27-magic-wrap{display:flex;align-items:center;gap:7px;min-width:420px}
    #viewer14-root .viewer27-magic-label{color:#ffd84d;font-weight:800;white-space:nowrap}
    #viewer14-root #viewer27MagicSelect{min-width:280px;max-width:420px;border-color:#8a4fd4}
    #viewer14-root .viewer27-magic-arrow{min-width:29px!important;width:29px!important;height:29px!important;padding:0!important;border-radius:7px!important;background:#161020!important;font-size:16px!important;line-height:1!important}
    #viewer14-root .viewer27-magic-left{color:#ff303f!important;border:1px solid #ff303f!important}
    #viewer14-root .viewer27-magic-right{color:#9dff00!important;border:1px solid #9dff00!important}
    #viewer14-root .viewer27-magic-arrow:active{filter:brightness(1.7);transform:scale(1.08)}
    #viewer14Status .fom-title{display:flex;align-items:center;justify-content:space-between;gap:10px}
    #viewer14Status .viewer27-chrome-search{padding:7px 11px!important;border-radius:7px!important;background:#ffffff!important;color:#202124!important;border:1px solid #dadce0!important;font-size:13px!important;font-weight:700!important;white-space:nowrap}
    #viewer14Status .viewer27-chrome-search:hover{filter:brightness(1.08)}
    @media(max-width:760px){
      #viewer14-root .viewer27-magic-wrap{min-width:100%;width:100%;flex-wrap:wrap}
      #viewer14-root #viewer27MagicSelect{min-width:220px;flex:1}
    }
  `;
  document.head.appendChild(style);

  install();
  const timer = setInterval(() => {
    install();
  }, 150);
  setTimeout(() => clearInterval(timer), 16000);
  setTimeout(() => showMagic(magicIndex), 1200);
})();
"""))
