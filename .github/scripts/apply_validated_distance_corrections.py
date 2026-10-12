#!/usr/bin/env python3
"""Apply only explicitly reviewed distance corrections; never consume the 157-row provisional list."""
import json
import os
from pathlib import Path

APPLY = os.environ.get("APPLY", "false").lower() == "true"
FIXES = [
    {"file":"viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json","index":154,"name":"NGC 4945","expected":13.0,"distance":13.0,"display":"13 million light-years","evidence":"ESO description: galaxy is 13 million light-years away; 62 light-years refers to image resolution."},
    {"file":"viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json","index":193,"name":"NGC 1097","expected":50.0,"distance":50.0,"display":"about 50 million light-years","evidence":"ESO description: NGC 1097 is about 50 million light-years away; 750–2500 light-years describes star-forming knots."},
    {"file":"viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json","index":197,"name":"Messier 95","expected":33.0,"distance":33.0,"display":"about 33 million light-years","evidence":"Independent NASA reference gives approximately 33 million light-years."},
    {"file":"viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json","index":786,"name":"Cone Nebula","expected":0.0000025,"distance":0.0025,"display":"2,500 light-years","evidence":"NASA/ESA Hubble description: Cone Nebula resides 2,500 light-years away; 2.5 light-years is pillar height."},
    {"file":"viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json","index":988,"name":"M 42","expected":0.00000129,"distance":0.0015,"display":"1,500 light-years","evidence":"Hubble record source states 1,500 light-years; 1.29 light-years is image width."},
]
for f in FIXES:
    path=Path(f["file"])
    doc=json.loads(path.read_text(encoding="utf-8"))
    entry=doc["entries"][f["index"]]
    if entry.get("name") != f["name"]:
        raise SystemExit(f"Identity guard failed: {f['file']}[{f['index']}] is {entry.get('name')!r}")
    current=entry.get("science",{}).get("distanceMly")
    if current == f["distance"]:
        print(f"Already corrected: {f['name']} -> {f['distance']} Mly")
        continue
    if current != f["expected"]:
        raise SystemExit(f"Value guard failed for {f['name']}: expected {f['expected']}, found {current}")
    print(f"{'APPLY' if APPLY else 'DRY RUN'}: {f['name']} {current} -> {f['distance']} Mly")
    if not APPLY:
        continue
    science=entry["science"]
    science["distanceMly"]=f["distance"]
    science["distanceMethod"]="independently_verified_distance_correction_20261012"
    science["distanceEvidence"]=f["evidence"]
    science["distanceDisplay"]=f["display"]
    science["distanceEstimated"]=True
    wf=entry.get("avmHorizontalFovDegrees",entry.get("imageFovXDeg"))
    hf=entry.get("avmVerticalFovDegrees",entry.get("imageFovYDeg"))
    if isinstance(wf,(int,float)) and isinstance(hf,(int,float)):
        import math
        w=f["distance"]*1000*wf*math.pi/180
        h=f["distance"]*1000*hf*math.pi/180
        science["sizeKly"]=[w,h]
        science["sizeMethod"]="derived_from_avm_wcs_fov_and_corrected_distance"
        science["sizeEstimated"]=True
        science["sizeDisplay"]=f"EST. {w:.4f} × {h:.4f} KLY"
    path.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
