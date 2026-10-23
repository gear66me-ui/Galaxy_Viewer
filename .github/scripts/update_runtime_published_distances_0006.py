#!/usr/bin/env python3
"""Build runtime catalog 0006 from 0004 using explicit distance wording on provider image pages.

Only official provider image pages are read. No NED/SIMBAD or other astronomy database lookups.
For each provider, records with a numeric distance explicitly stated on the provider page are
ranked for correction by disagreement with the runtime distance. The workflow enforces the
original 400-record provider allocation and aborts rather than silently publishing a partial run.
"""
import json, math, re, time
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from html import unescape

SRC = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0004.json")
OUT = Path("viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0006.json")
REPORT = Path("distance-source-wording-0006-report.json")
QUOTAS = {"chandra": 3, "eso": 55, "hubble": 295, "jwst": 20, "noirlab": 27}
UA = "GalaxyViewerPublishedDistanceWorkflow/1.0"
NUM_RE = re.compile(r"(?i)(\d[\d,.]*)\s*(million|billion|thousand)?\s*(light[- ]years?|Mly|Mpc|megaparsecs?|kpc|Gpc)")
DIST_CONTEXT = re.compile(r"(?i)(distance|located|lies|lying|resides|situated|away|light[- ]years?|Mly|Mpc|megaparsecs?)")

def get_text(url):
    req=Request(url, headers={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,*/*"})
    with urlopen(req, timeout=22) as resp:
        raw=resp.read(2_500_000).decode("utf-8","replace")
        if "html" not in resp.headers.get("Content-Type","").lower() and not raw.lstrip().lower().startswith(("<!doctype html","<html")):
            return resp.geturl(), ""
    raw=re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\\1>"," ",raw)
    raw=re.sub(r"(?i)</(p|div|li|h[1-6]|section|article|br|tr)>","\\n",raw)
    return resp.geturl(), re.sub(r"\\s+"," ",unescape(re.sub(r"(?s)<[^>]+>"," ",raw))).strip()

def urls_for(r):
    p=str(r.get("providerKey") or "").lower()
    aid=str(r.get("archiveId") or "").strip()
    image=str(r.get("imageUrl") or "")
    urls=[]
    if p=="hubble" and aid: urls=[f"https://esahubble.org/images/{aid}/"]
    elif p=="jwst" and aid: urls=[f"https://esawebb.org/images/{aid}/",f"https://webbtelescope.org/contents/media/images/{aid}"]
    elif p=="eso" and aid: urls=[f"https://www.eso.org/public/images/{aid}/"]
    elif p=="noirlab" and aid: urls=[f"https://astropix.org/image/{aid}",f"https://noirlab.edu/public/images/{aid}/"]
    elif p=="chandra" and image:
        parts=urlparse(image).path.split("/")
        if "photo" in parts:
            i=parts.index("photo")
            if len(parts)>i+2: urls=[f"https://chandra.harvard.edu/photo/{parts[i+1]}/{parts[i+2]}/"]
    return list(dict.fromkeys(urls))

def mly(n, scale, unit):
    x=float(n.replace(",","")); s=(scale or "").lower(); u=unit.lower().replace(" ","")
    if u=="mly": return x
    if u in ("mpc","megaparsecs"): return x*3.261563777
    if u=="kpc": return x*0.003261563777
    if u=="gpc": return x*3261.563777
    if "light-year" in u:
        return x*({"billion":1000,"million":1,"thousand":0.001}.get(s,1e-6))
    return None

def source_distance(text):
    found=[]
    for match in NUM_RE.finditer(text):
        lo=max(0,match.start()-140); hi=min(len(text),match.end()+140)
        context=text[lo:hi]
        if not DIST_CONTEXT.search(context): continue
        value=mly(match.group(1),match.group(2),match.group(3))
        if value and 0.001 <= value <= 100_000:
            found.append((value,context[:320]))
    # Conservative: use only an unambiguous single distinct numeric value on the page.
    distinct=[]
    for value,context in found:
        if not any(abs(value-v)<max(0.01,v*0.0001) for v,_ in distinct): distinct.append((value,context))
    return distinct[0] if len(distinct)==1 else None

def e_z(z, om=0.315): return math.sqrt(om*(1+z)**3+(1-om))
def dl_mly(z):
    # Flat Lambda-CDM luminosity distance, H0=67.6 km/s/Mpc; c=299792.458 km/s.
    n=1200; dz=z/n
    total=0.0
    for i in range(n+1):
        zz=i*dz
        weight=1 if i in (0,n) else (4 if i%2 else 2)
        total += weight/e_z(zz)
    dc=(299792.458/67.6)*(dz/3)*(total) # Mpc
    return (1+z)*dc*3.261563777 # Mly

def redshift_for_distance(distance_mly):
    lo,hi=0.0,20.0
    for _ in range(100):
        mid=(lo+hi)/2
        if dl_mly(mid)<distance_mly: lo=mid
        else: hi=mid
    return (lo+hi)/2

def set_distance(r, distance, evidence_url, quote):
    r["distanceMly"]=round(distance,6)
    r["redshift"]=round(redshift_for_distance(distance),8)
    r["science"]=r.get("science") if isinstance(r.get("science"),dict) else {}
    s=r["science"]
    s["distanceMly"]=round(distance,6)
    s["distanceDisplay"]=f'{distance:,.2f} million light-years'
    s["distanceMethod"]="published_provider_page_distance"
    s["distanceSource"]=evidence_url
    s["distanceEvidence"]=quote
    s["distanceVerified"]=True
    s["redshift"]=round(redshift_for_distance(distance),8)
    s["redshiftMethod"]="flat_LCDM_from_published_distance_H0_67.6_Om_0.315"
    s["redshiftSource"]=evidence_url
    s["redshiftEvidence"]=f"Calculated from published distance {distance:.6f} Mly assuming luminosity distance in flat Lambda-CDM (H0=67.6, Omega_m=0.315)."
    # Keep any known display aliases synchronized, without changing unrelated fields.
    if "distance" in r and isinstance(r["distance"],dict):
        r["distance"]["mly"]=round(distance,6)
        r["distance"]["display"]=s["distanceDisplay"]
    if "distanceDisplay" in r: r["distanceDisplay"]=s["distanceDisplay"]
    if "distanceMly" in s: s["distanceMly"]=round(distance,6)

def main():
    obj=json.loads(SRC.read_text(encoding="utf-8"))
    records=obj.get("records") if isinstance(obj,dict) else obj
    if not isinstance(records,list) or len(records)!=1847: raise SystemExit("Source catalog must contain exactly 1847 records.")
    candidates={k:[] for k in QUOTAS}
    failures=[]
    for idx,r in enumerate(records):
        if not isinstance(r,dict): continue
        provider=str(r.get("providerKey") or "").lower()
        if provider not in QUOTAS: continue
        for url in urls_for(r):
            try:
                final_url,text=get_text(url)
                parsed=source_distance(text)
                if parsed:
                    value,quote=parsed
                    current=r.get("science",{}).get("distanceMly",r.get("distanceMly"))
                    try: current=float(current)
                    except Exception: current=None
                    delta=abs(value-current)/max(value,1e-9) if current is not None else 999
                    candidates[provider].append({"index":idx,"distance":value,"url":final_url,"quote":quote,"delta":delta,"archiveId":r.get("archiveId"),"name":r.get("name")})
                    break
            except Exception as e:
                failures.append({"provider":provider,"archiveId":r.get("archiveId"),"url":url,"error":str(e)[:160]})
    selected={}
    for provider,quota in QUOTAS.items():
        # Prefer records whose existing value conflicts with the source page; deterministic tie-break.
        rows=sorted(candidates[provider],key=lambda x:(-x["delta"],x["index"]))
        if len(rows)<quota:
            raise SystemExit(f"ABORT: {provider} has only {len(rows)} unambiguous provider-page distance quotes; required {quota}. No catalog published.")
        selected[provider]=rows[:quota]
    # Make a fresh copy of v4, then modify only the allocated 400 distance/redshift pairs.
    changed=[]
    for provider,rows in selected.items():
        for row in rows:
            r=records[row["index"]]
            set_distance(r,row["distance"],row["url"],row["quote"])
            changed.append({"provider":provider,"archiveId":row["archiveId"],"name":row["name"],"distanceMly":round(row["distance"],6),"redshift":round(redshift_for_distance(row["distance"]),8),"sourceUrl":row["url"],"sourceQuote":row["quote"]})
    if len(changed)!=400: raise SystemExit(f"ABORT: expected 400 changes, got {len(changed)}.")
    if isinstance(obj,dict):
        obj["schema"]="gv-avm-runtime-catalog-0006"
        obj["version"]="0006"
        obj["derivedFrom"]="gv-avm-runtime-catalog-0004"
        obj["distanceRedshiftUpdate"]={"method":"provider website quoted distance; flat Lambda-CDM H0=67.6 Omega_m=0.315","changedRecords":400}
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    REPORT.write_text(json.dumps({"sourceCatalog":str(SRC),"outputCatalog":str(OUT),"sourceRecordCount":len(records),"updatedRecordCount":len(changed),"providerCounts":{p:len(v) for p,v in QUOTAS.items()},"updates":changed,"fetchFailures":failures},ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps({"output":str(OUT),"records":len(records),"updated":len(changed),"providerCounts":{p:len(v) for p,v in QUOTAS.items()}},indent=2))

if __name__=="__main__": main()
