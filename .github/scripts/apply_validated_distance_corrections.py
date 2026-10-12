#!/usr/bin/env python3
"""Reconcile supplied distance log and correct the JW100/IC 5337 catastrophic distance."""
import csv, json, math
from pathlib import Path

CSV_PATH = Path(".github/data/distance-fix-157-log-20261012_204406.csv")
CATALOGS = {
    "gv-hubble-galaxies-full-0035-ESA-FOV.json": Path("viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json"),
    "gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json": Path("viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json"),
    "gv-eso-galaxies-full-0001.json": Path("viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json"),
    "gv-chandra-galaxies-full-0007.json": Path("viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0007.json"),
    "gv-spitzer-galaxies-full-0011.json": Path("viewer/image-databases/Spitzer/databases/gv-spitzer-galaxies-full-0011.json"),
    "gv-noirlab-galaxies-full-0001.json": Path("viewer/image-databases/NoirLab/databases/gv-noirlab-galaxies-full-0001.json"),
}
PROTECTED = {
    ("gv-eso-galaxies-full-0001.json", 154): 13.0,
    ("gv-eso-galaxies-full-0001.json", 193): 50.0,
    ("gv-eso-galaxies-full-0001.json", 197): 33.0,
}
def alias_text(entry):
    parts=[]
    for k in ("name","title","objectName","target","description","caption"):
        v=entry.get(k)
        if isinstance(v,str): parts.append(v)
    for k in ("aliases","objectNames","names","identifiers","alternateNames"):
        v=entry.get(k)
        if isinstance(v,list): parts.extend(str(x) for x in v)
        elif isinstance(v,str): parts.append(v)
    science=entry.get("science",{})
    if isinstance(science,dict):
        for k in ("name","objectName","target","aliases","objectNames"):
            v=science.get(k)
            if isinstance(v,list): parts.extend(str(x) for x in v)
            elif isinstance(v,str): parts.append(v)
    return " | ".join(parts).casefold()

docs={}
changed_paths=set()
for fname,path in CATALOGS.items():
    if not path.exists():
        print(f"CATALOG_MISSING {path}")
        continue
    doc=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc.get("entries"),list):
        print(f"CATALOG_INVALID {path}: no entries")
        continue
    docs[fname]=doc

# First, apply rows from the supplied CSV with strict index, identity, and old-value guards.
rows=list(csv.DictReader(CSV_PATH.open(newline="",encoding="utf-8-sig")))
if len(rows)!=157: raise SystemExit(f"Expected 157 CSV rows, found {len(rows)}")
applied=already=protected=conflicts=0
for row in rows:
    fname=row["catalog_file"].strip()
    if fname not in docs: conflicts+=1; continue
    idx=int(row["entry_index"]); expected=float(row["before_Mly"]); target=float(row["after_Mly"])
    entries=docs[fname]["entries"]
    if idx<0 or idx>=len(entries): conflicts+=1; print(f"CONFLICT {fname}[{idx}] out of range"); continue
    e=entries[idx]; name=str(e.get("name","")).strip()
    if name!=row["name"].strip():
        conflicts+=1; print(f"CONFLICT {fname}[{idx}] name CSV={row['name']!r} catalog={name!r}"); continue
    science=e.setdefault("science",{}); cur=science.get("distanceMly")
    if (fname,idx) in PROTECTED and isinstance(cur,(int,float)) and math.isclose(cur,PROTECTED[(fname,idx)],rel_tol=1e-8,abs_tol=1e-10):
        protected+=1; continue
    if isinstance(cur,(int,float)) and math.isclose(cur,target,rel_tol=1e-8,abs_tol=1e-10):
        already+=1; continue
    if not isinstance(cur,(int,float)) or not math.isclose(cur,expected,rel_tol=1e-7,abs_tol=1e-10):
        conflicts+=1; print(f"CONFLICT {fname}[{idx}] {name}: current={cur!r}, expected={expected}, target={target}"); continue
    science["distanceMly"]=target
    science["distanceMethod"]="provisional_NED_match_batch_20261012"
    science["distanceEvidence"]="Supplied distance-fix-157 log; NED object match marked provisional and not independently verified."
    science["distanceEstimated"]=True
    science["distanceDisplay"]=f"{target*1_000_000:,.0f} light-years" if target<1 else f"{target:,.6g} million light-years"
    wf=e.get("avmHorizontalFovDegrees",e.get("imageFovXDeg")); hf=e.get("avmVerticalFovDegrees",e.get("imageFovYDeg"))
    if isinstance(wf,(int,float)) and isinstance(hf,(int,float)) and wf>0 and hf>0:
        w=target*1000*wf*math.pi/180; h=target*1000*hf*math.pi/180
        science["sizeKly"]=[w,h]; science["sizeMethod"]="derived_from_avm_wcs_fov_and_provisional_corrected_distance"
        science["sizeEstimated"]=True; science["sizeDisplay"]=f"EST. {w:.4f} × {h:.4f} KLY"
    changed_paths.add(path); applied+=1

# JW100 is also IC 5337 (PGC 71875; z≈0.054988): NASA/ESA describes it as over 800 million light-years away.
# Only alter a matching named object if its current distance is beyond the observable-universe radius,
# which catches the impossible 52.8-billion-light-year error without changing normal distances.
jw_hits=0
for fname,doc in docs.items():
    for idx,e in enumerate(doc["entries"]):
        aliases=alias_text(e)
        if not any(term in aliases for term in ("jw100","ic 5337","ic5337","pgc 71875","pgc71875")):
            continue
        science=e.setdefault("science",{})
        cur=science.get("distanceMly")
        print(f"JW100_CANDIDATE catalog={fname} index={idx} name={e.get('name')!r} distanceMly={cur!r} aliases={aliases[:260]}")
        jw_hits+=1
        if isinstance(cur,(int,float)) and cur>46500:
            science["distanceMly"]=800.0
            science["distanceMethod"]="NASA_ESA_verified_distance_20261012"
            science["distanceEvidence"]="NASA/ESA Hubble release: JW100 is over 800 million light-years away; IC 5337/JW100 redshift z≈0.054988 and distance 245.2 Mpc."
            science["distanceEstimated"]=True
            science["distanceDisplay"]="over 800 million light-years"
            wf=e.get("avmHorizontalFovDegrees",e.get("imageFovXDeg")); hf=e.get("avmVerticalFovDegrees",e.get("imageFovYDeg"))
            if isinstance(wf,(int,float)) and isinstance(hf,(int,float)) and wf>0 and hf>0:
                w=800*1000*wf*math.pi/180; h=800*1000*hf*math.pi/180
                science["sizeKly"]=[w,h]; science["sizeMethod"]="derived_from_avm_wcs_fov_and_verified_distance"
                science["sizeEstimated"]=True; science["sizeDisplay"]=f"EST. {w:.4f} × {h:.4f} KLY"
            changed_paths.add(CATALOGS[fname]); print(f"JW100_FIXED {fname}[{idx}] {cur} -> 800 Mly")
        elif isinstance(cur,(int,float)) and 0<cur<=46500:
            print(f"JW100_NOT_OVERWRITTEN distance {cur} Mly is not beyond observable-universe radius")
if jw_hits==0: print("JW100_NOT_FOUND in six runtime catalogs")

for fname,doc in docs.items():
    path=CATALOGS[fname]
    if path not in changed_paths: continue
    path.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    parsed=json.loads(path.read_text(encoding="utf-8"))
    assert len(parsed["entries"])==len(doc["entries"])
    for i,e in enumerate(parsed["entries"]):
        v=e.get("science",{}).get("distanceMly")
        if not isinstance(v,(int,float)) or v<=0: raise SystemExit(f"Invalid distance {path}[{i}]")
    print(f"VALIDATED {path}: {len(parsed['entries'])} entries")
print(f"SUMMARY rows={len(rows)} applied={applied} already_target={already} protected={protected} conflicts={conflicts} jw100_candidates={jw_hits}")
