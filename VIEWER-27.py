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


def viewer27_resolve_name(name):
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


output.register_callback("viewer27.resolveName", viewer27_resolve_name)


display(Javascript(r'''
(() => {
  const FEATURED = [
    ['Cartwheel Galaxy','Cartwheel Galaxy',9.4213,-33.7160,.060,'CDS/P/JWST/EPO','Collisional ring galaxy','7.0 ± 2.5 billion years — estimated','About 500 million ly — estimated','About 150,000 ly — estimated','15.2'],
    ["Stephan's Quintet — HCG 92",'HCG 92',338.9896,33.9560,.095,'CDS/P/JWST/EPO','Compact interacting galaxy group','9.0 ± 2.5 billion years — estimated member populations','About 290 million ly — estimated','About 250,000 ly group span — estimated','13.9'],
    ['Whirlpool Galaxy — M51','M 51',202.4696,47.1953,.180,'CDS/P/HST/EPO','Grand-design interacting spiral','9.0 ± 2.0 billion years — estimated','About 31 million ly — estimated','About 76,000 ly — estimated','8.4'],
    ['Sombrero Galaxy — M104','M 104',189.9976,-11.6231,.130,'CDS/P/HST/EPO','Early-type spiral / lenticular','11.0 ± 1.5 billion years — estimated','About 29 million ly — estimated','About 50,000 ly — estimated','8.0'],
    ['Antennae Galaxies — NGC 4038/4039','NGC 4038',180.4708,-18.8750,.120,'CDS/P/HST/EPO','Interacting merger pair','8.0 ± 2.5 billion years — estimated','About 45 million ly — estimated','About 100,000 ly system span — estimated','10.9'],
    ['Tadpole Galaxy — UGC 10214','UGC 10214',241.5689,55.4249,.075,'CDS/P/HST/EPO','Disturbed spiral with tidal tail','7.5 ± 2.5 billion years — estimated','About 420 million ly — estimated','About 280,000 ly including tail — estimated','14.4'],
    ["Hoag's Object","Hoag's Object",229.5867,21.5853,.035,'CDS/P/HST/EPO','Ring galaxy','9.0 ± 2.0 billion years — estimated old core and younger ring','About 600 million ly — estimated','About 120,000 ly — estimated','16.2'],
    ['NGC 1300','NGC 1300',49.9208,-19.4117,.110,'CDS/P/HST/EPO','Grand-design barred spiral','9.0 ± 2.0 billion years — estimated','About 61 million ly — estimated','About 110,000 ly — estimated','10.4'],
    ['Great Barred Spiral — NGC 1365','NGC 1365',53.4016,-36.1404,.150,'CDS/P/JWST/EPO','Barred spiral galaxy','9.0 ± 2.0 billion years — estimated','About 56 million ly — estimated','About 200,000 ly — estimated','9.6'],
    ['Pinwheel Galaxy — M101','M 101',210.8023,54.3490,.360,'CDS/P/HST/EPO','Face-on grand-design spiral','8.0 ± 2.5 billion years — estimated','About 21 million ly — estimated','About 170,000 ly — estimated','7.9'],
    ['Cigar Galaxy — M82','M 82',148.9685,69.6797,.140,'CDS/P/HST/EPO','Starburst galaxy','8.0 ± 2.5 billion years — estimated underlying population','About 12 million ly — estimated','About 37,000 ly — estimated','8.4'],
    ['Black Eye Galaxy — M64','M 64',194.1821,21.6827,.120,'CDS/P/HST/EPO','Spiral galaxy with dark dust lane','9.5 ± 2.0 billion years — estimated','About 17 million ly — estimated','About 54,000 ly — estimated','8.5'],
    ['Southern Pinwheel — M83','M 83',204.2539,-29.8658,.230,'CDS/P/HST/EPO','Barred star-forming spiral','8.5 ± 2.0 billion years — estimated','About 15 million ly — estimated','About 55,000 ly — estimated','7.5'],
    ['Phantom Galaxy — M74','M 74',24.1740,15.7837,.150,'CDS/P/JWST/EPO','Face-on grand-design spiral','8.5 ± 2.2 billion years — estimated','About 32 million ly — estimated','About 95,000 ly — estimated','9.4'],
    ['Andromeda Galaxy — M31','M 31',10.6847,41.2688,3.20,'P/DSS2/color','Large spiral galaxy','10.0 ± 2.0 billion years — estimated','2.54 million ly — established estimate','About 220,000 ly — estimated','3.44'],
    ['Triangulum Galaxy — M33','M 33',23.4621,30.6599,1.20,'CDS/P/HST/EPO','Late-type spiral galaxy','8.0 ± 2.5 billion years — estimated','2.73 million ly — established estimate','About 60,000 ly — estimated','5.7'],
    ['Centaurus A — NGC 5128','NGC 5128',201.3651,-43.0191,.270,'CDS/P/HST/EPO','Peculiar dust-lane radio galaxy','11.0 ± 1.5 billion years — estimated','About 12 million ly — estimated','About 60,000 ly — estimated','6.8'],
    ['Sculptor Galaxy — NGC 253','NGC 253',11.8880,-25.2882,.35,'CDS/P/HST/EPO','Starburst spiral galaxy','8.5 ± 2.0 billion years — estimated','About 11.4 million ly — estimated','About 90,000 ly — estimated','7.1'],
    ["Bode's Galaxy — M81",'M 81',148.8882,69.0653,.32,'CDS/P/HST/EPO','Grand-design spiral galaxy','10.0 ± 2.0 billion years — estimated','About 11.8 million ly — estimated','About 90,000 ly — estimated','6.9'],
    ['Sunflower Galaxy — M63','M 63',198.9555,42.0293,.18,'CDS/P/HST/EPO','Flocculent spiral galaxy','9.0 ± 2.0 billion years — estimated','About 27 million ly — estimated','About 98,000 ly — estimated','8.6']
  ].map(x=>({name:x[0],query:x[1],ra:x[2],dec:x[3],fov:x[4],survey:x[5],morphology:x[6],age:x[7],distance:x[8],physical:x[9],magnitude:x[10]}));

  const EXTRA = `M 49|M 58|M 59|M 60|M 61|M 65|M 66|M 77|M 84|M 85|M 86|M 87|M 88|M 89|M 90|M 91|M 94|M 95|M 96|M 98|M 99|M 100|M 102|M 105|M 106|M 108|M 109|M 110|NGC 55|NGC 247|NGC 300|NGC 488|NGC 520|NGC 660|NGC 772|NGC 891|NGC 925|NGC 1023|NGC 1055|NGC 1097|NGC 1232|NGC 1266|NGC 1316|NGC 1398|NGC 1512|NGC 1532|NGC 1566|NGC 1672|NGC 1808|NGC 2207|IC 2163|NGC 2403|NGC 2683|NGC 2775|NGC 2841|NGC 2903|NGC 2976|NGC 3079|NGC 3109|NGC 3184|NGC 3190|NGC 3198|NGC 3227|NGC 3310|NGC 3344|NGC 3351|NGC 3368|NGC 3370|NGC 3377|NGC 3379|NGC 3384|NGC 3486|NGC 3521|NGC 3556|NGC 3621|NGC 3627|NGC 3628|NGC 3718|NGC 3729|NGC 3949|NGC 3953|NGC 4013|NGC 4027|NGC 4088|NGC 4214|NGC 4216|NGC 4244|NGC 4254|NGC 4258|NGC 4274|NGC 4298|NGC 4302|NGC 4303|NGC 4314|NGC 4321|NGC 4388|NGC 4395|NGC 4402|NGC 4414|NGC 4435|NGC 4438|NGC 4449|NGC 4450|NGC 4490|NGC 4526|NGC 4535|NGC 4536|NGC 4548|NGC 4559|NGC 4565|NGC 4567|NGC 4568|NGC 4571|NGC 4594|NGC 4625|NGC 4631|NGC 4656|NGC 4697|NGC 4725|NGC 4736|NGC 474|NGC 4826|NGC 4945|NGC 5005|NGC 5033|NGC 5055|NGC 5194|NGC 5195|NGC 5236|NGC 5253|NGC 5457|NGC 5474|NGC 5584|NGC 5866|NGC 5907|NGC 6503|NGC 6822|NGC 6946|NGC 7331|NGC 7479|NGC 7496|NGC 7552|NGC 7590|NGC 7814|IC 342|IC 2574|IC 5332|Arp 220|Arp 273|Arp 244|Arp 147|Arp 87|Arp 104|Arp 105|Arp 116|Arp 188|Arp 214|Arp 240|Arp 242|Arp 256|Arp 261|Arp 272|Arp 284|Arp 286|Arp 295|Arp 299|Arp 302|Arp 319|Arp 321|Arp 331|Arp 337|Arp 81|Arp 84|Arp 91|Arp 93|Arp 94|Arp 97|UGC 2885|UGC 1810|UGC 1813|ESO 137-001|ESO 510-G13|AM 0644-741|II Zw 96|VV 340|Mayall's Object|Comet Galaxy|Medusa Merger|Atoms-for-Peace Galaxy|Malin 1|Malin 2|NGC 1275|NGC 1705|NGC 2146|NGC 2623|NGC 3256|NGC 3314|NGC 3923|NGC 4194|NGC 4261|NGC 4472|NGC 4486|NGC 4649|NGC 5018|NGC 5044|NGC 5846|NGC 6166|NGC 6240|NGC 7252|NGC 7600|NGC 7742|NGC 7743|NGC 7714|NGC 4676A|NGC 4676B|NGC 6621|NGC 6622|NGC 6872|IC 4970|NGC 5291|NGC 7317|NGC 7318A|NGC 7318B|NGC 7319|NGC 7320|NGC 922|NGC 985|NGC 1614|NGC 6052|NGC 7674`.split('|');
  const SHOWCASE = [...FEATURED, ...EXTRA.map(name=>({name,query:name,fov:.16,survey:'CDS/P/HST/EPO'}))].slice(0,200);
  let current=0, currentGalaxy=null;

  const parse=r=>typeof viewer14Result==='function'?viewer14Result(r):(r?.data||r);
  const filled=(v,f)=>{const s=v==null?'':String(v).trim();return !s||/^not available/i.test(s)?f:v};
  function ageFor(m){m=String(m||'').toLowerCase();if(/elliptical|lenticular|s0/.test(m))return'10.5 ± 1.8 billion years — estimated from morphology';if(/ring/.test(m))return'8.0 ± 2.5 billion years — estimated from morphology';if(/irregular|starburst|merger|interact|peculiar/.test(m))return'7.0 ± 2.8 billion years — estimated composite population';return'9.0 ± 2.2 billion years — estimated from morphology';}
  function enrich(item,info,res){const g={...(info||{})};g.ok=true;g.name=item.name;g.catalog='Showcase 200 — curated named galaxies';g.ra=Number(g.ra??res.ra??item.ra);g.dec=Number(g.dec??res.dec??item.dec);g.fov=Number(item.fov||g.fov||.16);g.survey_id=item.survey||'CDS/P/HST/EPO';g.morphology=filled(item.morphology||g.morphology,'Galaxy — detailed type pending catalog classification');g.age=item.age||ageFor(g.morphology);g.angular_size=filled(g.angular_size,'Estimated from displayed angular extent');g.distance_bly=filled(item.distance||g.distance_bly,'Estimated distance pending redshift measurement');g.redshift_distance=filled(g.redshift_distance,`Estimated redshift pending / ${g.distance_bly}`);g.velocity_kms=Number.isFinite(Number(g.velocity_kms))?Number(g.velocity_kms):0;g.physical_size=filled(item.physical||g.physical_size,'Estimated from angular extent after distance lookup');g.magnitude=filled(item.magnitude||g.magnitude,'Estimated photometry pending catalog match');g.interest_score='Showcase selected';g.distance_method=filled(g.distance_method,'Catalog value when present; otherwise labeled estimate');g.attempts=1;g.elapsed_seconds=Number(g.elapsed_seconds||0);g.source=`${g.source||'SIMBAD 30 arcsecond cone'}; CDS Sesame; Showcase 200 estimates`;return g;}

  async function show(index){index=(Number(index)+SHOWCASE.length)%SHOWCASE.length;current=index;const item=SHOWCASE[index];document.getElementById('viewer27ShowcaseSelect')?.setAttribute('value',String(index));const sel=document.getElementById('viewer27ShowcaseSelect');if(sel)sel.value=String(index);viewer14ProgressStart('Showcase 200');viewer14Status(`Resolving ${item.name}…`);try{let res={ok:true,ra:item.ra,dec:item.dec};if(!Number.isFinite(item.ra)){const rr=await google.colab.kernel.invokeFunction('viewer27.resolveName',[item.query],{});res=parse(rr);if(!res?.ok)throw Error(res?.error||'Name resolution failed');}let info=null;try{const ir=await google.colab.kernel.invokeFunction('viewer14.getInfo',[res.ra,res.dec],{});const x=parse(ir);if(x?.ok)info=x;}catch(_){}const g=enrich(item,info,res);currentGalaxy=g;viewer14ProgressDone('Showcase 200',`${index+1} of ${SHOWCASE.length}`);viewer14ShowGalaxy(g);}catch(e){viewer14ProgressFail('Showcase 200');viewer14Status(`Showcase lookup failed: ${String(e?.message||e)}`);}}

  function prompt(){const g=currentGalaxy||{};return`Research this galaxy using authoritative astronomy databases. Object: ${g.name||'unknown'}. ICRS coordinates: ${Number(g.ra).toFixed(6)} ${Number(g.dec).toFixed(6)}. Find identifiers, morphology, redshift, distance, radial velocity, angular size, physical size, magnitude, and stellar-population age or a clearly labeled age estimate. Distinguish measurements from estimates and cite sources.`;}
  async function search(kind){const p=prompt();try{await navigator.clipboard.writeText(p)}catch(_){}const q=encodeURIComponent(p);const u=kind==='chatgpt'?`https://chatgpt.com/?q=${q}`:kind==='gemini'?`https://gemini.google.com/app?q=${q}`:`https://www.google.com/search?q=${q}`;window.open(u,'_blank','noopener,noreferrer');}
  window.viewer27Show=show;window.viewer27Search=search;

  function install(){const root=document.getElementById('viewer14-root'),catalog=document.getElementById('viewer14CatalogMode'),random=document.getElementById('viewer14RandomButton');if(!root||!catalog||!random||typeof viewer14Panel!=='function')return false;document.getElementById('viewer26MagicWrap')?.remove();let wrap=document.getElementById('viewer27ShowcaseWrap');if(!wrap){wrap=document.createElement('div');wrap.id='viewer27ShowcaseWrap';wrap.className='viewer27-wrap';wrap.innerHTML=`<span>Showcase 200</span><button id="viewer27Prev" class="viewer27-arrow viewer27-red"><svg viewBox="0 0 32 32"><path d="M25 5Q27 5 25 8L12 16l13 8q2 3-1 3L7 18q-3-2 0-4L24 5Z"/></svg></button><select id="viewer27ShowcaseSelect">${SHOWCASE.map((g,i)=>`<option value="${i}">${i+1}. ${g.name}</option>`).join('')}</select><button id="viewer27Next" class="viewer27-arrow viewer27-green"><svg viewBox="0 0 32 32"><path d="M7 5Q5 5 7 8l13 8-13 8q-2 3 1 3l17-9q3-2 0-4L8 5Z"/></svg></button>`;random.insertAdjacentElement('beforebegin',wrap);document.getElementById('viewer27ShowcaseSelect').onchange=e=>show(Number(e.target.value));document.getElementById('viewer27Prev').onclick=()=>show(current-1);document.getElementById('viewer27Next').onclick=()=>show(current+1);}
    if(![...catalog.options].some(o=>o.value==='Showcase')){const o=document.createElement('option');o.value='Showcase';o.textContent='Showcase 200';catalog.insertBefore(o,catalog.firstChild);}catalog.value='Showcase';
    if(!window.viewer27OldRandom)window.viewer27OldRandom=window.viewer14RandomGalaxy;window.viewer14RandomGalaxy=async()=>catalog.value==='Showcase'?show(Math.floor(Math.random()*SHOWCASE.length)):window.viewer27OldRandom();
    if(!window.viewer27OldPanel)window.viewer27OldPanel=window.viewer14Panel;window.viewer14Panel=function(g,s,f){currentGalaxy=g;const base=window.viewer27OldPanel(g,s,f);const bar=`<div class="viewer27-searchbar"><button onclick="viewer27Search('gemini')"><img src="https://gemini.google.com/favicon.ico">Gemini Search</button><button onclick="viewer27Search('chatgpt')"><img src="https://chatgpt.com/favicon.ico">ChatGPT Search</button><button onclick="viewer27Search('google')"><img src="https://www.google.com/favicon.ico">Chrome Search</button></div>`;return base.replace('<div class="fom-title">',`<div class="fom-title">${bar}`)};
    const h=root.querySelector('h3');if(h)h.textContent='Galaxy Viewer — VIEWER-27';return true;}

  const st=document.createElement('style');st.textContent=`#viewer14-root .viewer27-wrap{display:flex;align-items:center;gap:7px;min-width:520px}#viewer14-root .viewer27-wrap>span{color:#ffd84d;font-weight:900;white-space:nowrap}#viewer14-root #viewer27ShowcaseSelect{min-width:330px;max-width:470px;border-color:#8a4fd4}.viewer27-arrow{min-width:29px!important;width:29px!important;height:29px!important;padding:0!important;border-radius:7px!important;background:#8a4fd4!important;display:inline-flex!important;align-items:center!important;justify-content:center!important}.viewer27-arrow svg{width:23px;height:23px}.viewer27-arrow path{stroke-width:1.5;stroke-linejoin:round}.viewer27-red path{fill:#ff1a1a;stroke:#ff1a1a}.viewer27-green path{fill:#b7ff00;stroke:#b7ff00}.viewer27-arrow:active path{filter:drop-shadow(0 0 2px currentColor) drop-shadow(0 0 5px currentColor);transform:scale(1.1)}#viewer14-root .viewer27-searchbar{display:flex;flex-wrap:wrap;gap:8px;float:right;margin:-5px 0 -5px 12px}#viewer14-root .viewer27-searchbar button{display:inline-flex;align-items:center;gap:6px;padding:7px 10px;font-size:13px;border-radius:7px;background:#07151d;border:1px solid #169ac7;color:#d7f5ff}#viewer14-root .viewer27-searchbar img{width:18px;height:18px;border-radius:4px}@media(max-width:760px){#viewer14-root .viewer27-wrap{min-width:100%;width:100%;flex-wrap:wrap}#viewer14-root #viewer27ShowcaseSelect{min-width:240px;flex:1}#viewer14-root .viewer27-searchbar{float:none;margin:8px 0 0;width:100%}}`;document.head.appendChild(st);
  install();const timer=setInterval(()=>{if(install())clearInterval(timer)},100);setTimeout(()=>{install();show(0);clearInterval(timer)},1800);
})();
'''))