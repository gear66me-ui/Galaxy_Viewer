from __future__ import annotations

import csv
import io
import json
import math
import random
import time
import urllib.request
from pathlib import Path
from google.colab import output
from IPython.display import HTML, Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/2472b542f8ee64422d39188adcf1d866762c392b/VIEWER-14.py"
HECATE_URL = "https://hecate.ia.forth.gr/assets/files/HECATE_v1.1.csv"
CACHE_PATH = Path("/content/GALAXY-BEAUTY-CATALOG-0001.json")
BEAUTY_ROWS: list[dict] | None = None
BEAUTY_RECENT: list[int] = []
C_KMS_15 = 299792.458

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-14-base.py", "exec"))


def _num15(value):
    try:
        text = str(value).strip()
        if not text or text.lower() in {"nan", "none", "--", "-99", "-999"}:
            return None
        number = float(text)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def _text15(row, *names):
    lookup = {str(k).upper(): v for k, v in row.items()}
    for name in names:
        value = lookup.get(name.upper())
        if value is not None and str(value).strip() not in {"", "nan", "None", "--"}:
            return str(value).strip()
    return ""


def _score15(row):
    r1 = _num15(_text15(row, "R1"))
    bt = _num15(_text15(row, "BT"))
    t = _num15(_text15(row, "T"))
    incl = _num15(_text15(row, "INCL"))
    dist = _num15(_text15(row, "D"))
    vel = _num15(_text15(row, "V"))
    name = _text15(row, "OBJNAME", "ID_NED")
    score = 0.0
    if r1 is not None:
        score += min(34.0, 13.0 * math.log10(max(1.0, 2.0 * r1 * 60.0)))
    if bt is not None:
        score += max(0.0, min(22.0, (18.0 - bt) * 3.0))
    if t is not None:
        if 1 <= t <= 9:
            score += 18.0
        elif t >= 9:
            score += 12.0
        elif -3 <= t < 1:
            score += 7.0
    if incl is not None:
        score += max(0.0, 10.0 - abs(incl - 42.0) / 5.0)
    if name.upper().startswith(("M ", "MESSIER", "NGC", "IC", "ARP", "UGC")):
        score += 10.0
    if dist is not None:
        score += 4.0
    if vel is not None:
        score += 2.0
    completeness = sum(_num15(_text15(row, key)) is not None for key in ("D", "V", "BT", "R1", "R2", "T", "INCL"))
    score += completeness * 1.5
    return round(score, 3)


def _build_beauty15():
    global BEAUTY_ROWS
    if BEAUTY_ROWS is not None:
        return BEAUTY_ROWS
    if CACHE_PATH.exists():
        try:
            data = json.loads(CACHE_PATH.read_text("utf-8"))
            if isinstance(data, list) and len(data) >= 30000:
                BEAUTY_ROWS = data
                return BEAUTY_ROWS
        except Exception:
            pass
    request = urllib.request.Request(HECATE_URL, headers={"User-Agent": "GalaxyViewer/15"})
    with urllib.request.urlopen(request, timeout=180) as response:
        text = response.read().decode("utf-8", errors="replace")
    rows = list(csv.DictReader(io.StringIO(text)))
    scored = []
    for row in rows:
        ra = _num15(_text15(row, "RA")); dec = _num15(_text15(row, "DEC"))
        r1 = _num15(_text15(row, "R1")); r2 = _num15(_text15(row, "R2"))
        if ra is None or dec is None or r1 is None or r1 <= 0:
            continue
        score = _score15(row)
        scored.append({
            "pgc": _text15(row, "PGC"),
            "name": _text15(row, "OBJNAME", "ID_NED") or ("PGC " + _text15(row, "PGC")),
            "ra": ra, "dec": dec,
            "r1": r1, "r2": r2,
            "t": _num15(_text15(row, "T")),
            "incl": _num15(_text15(row, "INCL")),
            "velocity": _num15(_text15(row, "V")),
            "distance_mpc": _num15(_text15(row, "D")),
            "distance_method": _text15(row, "DMETHOD"),
            "magnitude": _num15(_text15(row, "BT")),
            "score": score,
        })
    scored.sort(key=lambda item: item["score"], reverse=True)
    BEAUTY_ROWS = scored[:30000]
    CACHE_PATH.write_text(json.dumps(BEAUTY_ROWS, separators=(",", ":"), ensure_ascii=False), "utf-8")
    return BEAUTY_ROWS


def _beauty_result15(item):
    major = 2.0 * item["r1"] if item.get("r1") else None
    minor = 2.0 * item["r2"] if item.get("r2") else None
    dist_mpc = item.get("distance_mpc")
    vel = item.get("velocity")
    z = vel / C_KMS_15 if vel is not None and vel > 0 else None
    if dist_mpc is not None and dist_mpc > 0:
        distance_bly = dist_mpc * 3.26156e6 / 1e9
        distance_text = f"{distance_bly:.6f} billion ly"
    else:
        distance_text = "Not available"
    if major and dist_mpc:
        major_kly = dist_mpc * 1000 * math.tan(math.radians(major / 60)) * 3.26156
        minor_kly = dist_mpc * 1000 * math.tan(math.radians((minor or major) / 60)) * 3.26156
        physical = f"{major_kly:,.1f} × {minor_kly:,.1f} thousand ly — derived"
    else:
        physical = "Not available"
    t = item.get("t")
    morphology = f"de Vaucouleurs T={t:g}" if t is not None else "Not available"
    return {
        "ok": True,
        "name": item["name"],
        "catalog": "Beauty Catalog — HECATE Top 30,000",
        "source": "HECATE v1.1 scored by size, brightness, morphology, inclination, and data completeness",
        "ra": item["ra"], "dec": item["dec"],
        "fov": max(0.035, min(4.0, (major or 3.0) * 3.2 / 60.0)),
        "survey_id": "P/DSS2/color",
        "morphology": morphology,
        "angular_size": f"{major:.3f} × {(minor or major):.3f} arcmin" if major else "Not available",
        "redshift_distance": f"{z:.8f} / {distance_text}" if z is not None else f"Not available / {distance_text}",
        "distance_bly": distance_text,
        "age": "Not available",
        "velocity_kms": vel,
        "physical_size": physical,
        "magnitude": "Not available" if item.get("magnitude") is None else f"{item['magnitude']:.3f}",
        "interest_score": item["score"],
        "distance_method": item.get("distance_method") or "Not available",
        "attempts": 1,
        "elapsed_seconds": 0.0,
    }


def viewer15_beauty_callback():
    started = time.monotonic()
    try:
        rows = _build_beauty15()
        pool = rows[:5000] if random.random() < 0.75 else rows
        available = [i for i in range(len(pool)) if i not in BEAUTY_RECENT[-100:]]
        idx = random.choice(available or list(range(len(pool))))
        BEAUTY_RECENT.append(idx)
        result = _beauty_result15(pool[idx])
        result["elapsed_seconds"] = time.monotonic() - started
    except Exception as exc:
        result = {"ok": False, "catalog": "Beauty Catalog", "error": str(exc)}
    return json.dumps(result, ensure_ascii=False)


output.register_callback("viewer15.randomBeauty", viewer15_beauty_callback)

display(HTML(r'''
<style>
#viewer14Status{white-space:normal!important;padding:0!important;overflow:hidden}
#viewer14Status .fom-title{padding:11px 14px;background:#03131d;color:#35c6ff;font-weight:700;border-bottom:1px solid #0d668a}
#viewer14Status table{width:100%;border-collapse:collapse;font-family:Arial,Helvetica,sans-serif}
#viewer14Status th,#viewer14Status td{padding:9px 12px;border-bottom:1px solid #0b526f;text-align:left;vertical-align:top}
#viewer14Status th{width:34%;color:#7FDBFF;background:#02080d}
#viewer14Status td{color:#d7f5ff;background:#000}
#viewer14Status tr.emphasis th,#viewer14Status tr.emphasis td{color:#ffd84d;font-weight:700;font-size:17px}
</style>
'''))

display(Javascript(r'''
(() => {
  const wait = setInterval(() => {
    const select = document.getElementById('viewer14CatalogMode');
    const menu = document.getElementById('viewer14CatalogMenu');
    const button = document.getElementById('viewer14CatalogButton');
    if (!select || !menu || !button || typeof viewer14RandomGalaxy !== 'function') return;
    clearInterval(wait);
    document.querySelector('#viewer14-root h3').textContent = 'Galaxy Viewer — VIEWER-15';
    if (![...select.options].some(o => o.value === 'Beauty')) {
      const opt = document.createElement('option'); opt.value='Beauty'; opt.textContent='Beauty Catalog — Top 30,000'; select.appendChild(opt);
      const b = document.createElement('button'); b.type='button'; b.textContent='Beauty Catalog — Top 30,000';
      Object.assign(b.style,{display:'block',width:'100%',textAlign:'left',background:'#000',color:'#7FDBFF',border:'0',borderBottom:'1px solid #0b526f',borderRadius:'0',padding:'12px',fontSize:'16px',fontWeight:'400'});
      b.onclick=(e)=>{e.stopPropagation();select.value='Beauty';select.dispatchEvent(new Event('change',{bubbles:true}));button.textContent='Beauty Catalog — Top 30,000 ▾';menu.style.display='none';};
      menu.appendChild(b);
    }
    window.viewer14CatalogOrder = function(){
      const mode=select.value;
      if(mode==='Beauty') return ['Beauty'];
      if(['Arp','RC3','HyperLEDA'].includes(mode)) return [mode];
      if(mode==='all') return ['Beauty','Arp','RC3','HyperLEDA'].sort(()=>Math.random()-.5);
      return Math.random()<0.70 ? ['Beauty','Arp','RC3','HyperLEDA'] : [['Arp','RC3','HyperLEDA'][Math.floor(Math.random()*3)],'Beauty'];
    };
    window.viewer14CallbackName = c => c==='Beauty'?'viewer15.randomBeauty':c==='Arp'?'viewer14.randomArp':c==='RC3'?'viewer14.randomRC3':'viewer14.randomHyperLEDA';
    window.viewer14Panel = function(g,survey,fov){
      const v=(g.velocity_kms!==null&&g.velocity_kms!==undefined&&Number.isFinite(Number(g.velocity_kms)))?`${Number(g.velocity_kms).toLocaleString(undefined,{maximumFractionDigits:1})} km/s`:'Not available';
      const rows=[
        ['Object',g.name],['Source catalog',g.catalog],['ICRS coordinates',`${Number(g.ra).toFixed(6)} ${Number(g.dec).toFixed(6)}`],
        ['Galaxy age',g.age||'Not available','emphasis'],['Distance',g.distance_bly||(String(g.redshift_distance||'').split('/')[1]||'Not available').trim(),'emphasis'],
        ['Redshift / Distance',g.redshift_distance||'Not available / Not available'],['Morphological type',g.morphology||'Not available'],
        ['Angular size',g.angular_size||'Not available'],['Radial velocity',v],['Physical size',g.physical_size||'Not available'],
        ['Magnitude',g.magnitude||'Not available'],['Interest score',g.interest_score??'Not available'],['Distance method',g.distance_method||'Not available'],
        ['Displayed survey',survey],['Field of view',`${fov.toFixed(3)}°`],['Catalog elapsed time',`${Number(g.elapsed_seconds||0).toFixed(2)} s`],['Data source',g.source]
      ];
      return `<div class="fom-title">RANDOM GALAXY FIGURES OF MERIT</div><table>${rows.map(r=>`<tr class="${r[2]||''}"><th>${r[0]}</th><td>${r[1]}</td></tr>`).join('')}</table>`;
    };
    window.viewer14Status = function(t){const el=document.getElementById('viewer14Status');if(typeof t==='string'&&t.startsWith('<div class="fom-title">'))el.innerHTML=t;else el.textContent=t;};
  },100);
  setTimeout(()=>clearInterval(wait),15000);
})();
'''))
