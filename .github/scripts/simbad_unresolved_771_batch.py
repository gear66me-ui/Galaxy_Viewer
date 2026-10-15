#!/usr/bin/env python3
"""Batch SIMBAD distance lookup for the 771 records unresolved by NED."""
import csv, io, os, re, sys, time, math, statistics, zipfile, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

REPO = os.environ.get("GITHUB_REPOSITORY", "gear66me-ui/Galaxy_Viewer")
RUN_ID = os.environ.get("SOURCE_RUN_ID", "38762527419")
ARTIFACT_ID = os.environ.get("SOURCE_ARTIFACT_ID", "11993062820")
TOKEN = os.environ["GITHUB_TOKEN"]
API = "https://api.github.com"
TAP = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
MPC_TO_MLY = 3.261563777
UA = "GalaxyViewerDistanceAudit/2.0 (batch SIMBAD review)"

def http(url, data=None, headers=None, timeout=120):
    h = {"User-Agent": UA, "Accept": "application/x-votable+xml, application/zip, */*"}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def parse_votable(payload):
    root = ET.fromstring(payload)
    fields = root.findall(".//{*}FIELD")
    names = [f.attrib.get("name") or f.attrib.get("ID") or f"col{i}" for i,f in enumerate(fields)]
    out=[]
    for tr in root.findall(".//{*}TABLEDATA/{*}TR"):
        vals=[(td.text or "").strip() for td in tr.findall("{*}TD")]
        out.append(dict(zip(names, vals)))
    return out

def pick(d, *keys):
    m={str(k).strip().lower():v for k,v in d.items()}
    for k in keys:
        v=m.get(k.lower(),"")
        if v not in ("", "--", "null", "None"): return v
    return ""

def num(x):
    try:
        v=float(str(x).strip())
        return v if math.isfinite(v) else None
    except Exception: return None

def ident_list(row):
    out=[]
    for key in ("designation","name","displayName","archiveId"):
        raw=(row.get(key) or "").strip()
        for x in re.split(r"\s*/\s*",raw):
            x=x.strip()
            if x and x not in out and len(x)<=100: out.append(x)
    return out[:3]

def sqlstr(s): return "'" + s.replace("\\","\\\\").replace("'","''") + "'"

def run_batch(names):
    inlist=",".join(sqlstr(n) for n in names)
    query=("SELECT i.id AS query_identifier, b.main_id, b.ra, b.dec, d.* "
           "FROM ident AS i JOIN basic AS b ON i.oidref=b.oid "
           "LEFT OUTER JOIN mesDistance AS d ON d.oidref=b.oid "
           f"WHERE i.id IN ({inlist})")
    data=urllib.parse.urlencode({"request":"doQuery","lang":"adql","format":"votable","query":query}).encode()
    return parse_votable(http(TAP,data=data,timeout=180))

def main():
    hdr={"Authorization":"Bearer "+TOKEN,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}
    # Download the completed source audit artifact from the prior workflow run.
    meta=json_load(http(f"{API}/repos/{REPO}/actions/artifacts/{ARTIFACT_ID}",headers=hdr))
    zipbytes=http(meta["archive_download_url"],headers=hdr,timeout=180)
    with zipfile.ZipFile(io.BytesIO(zipbytes)) as z:
        csvname=next((n for n in z.namelist() if n.endswith(".csv")),None)
        if not csvname: raise RuntimeError("CSV not found in source artifact")
        raw=z.read(csvname).decode("utf-8-sig")
    rows=list(csv.DictReader(io.StringIO(raw)))
    rows=[r for r in rows if r.get("review_status")=="NO_SOURCE_DISTANCE" or r.get("ned_status")=="NO_MATCH"]
    if not rows: raise RuntimeError("No unresolved records found in downloaded source artifact")
    print(f"Loaded {len(rows)} unresolved rows from artifact",flush=True)
    by_name=defaultdict(list); allnames=[]
    for idx,row in enumerate(rows):
        row["_source_row"]=str(idx+1)
        for name in ident_list(row):
            by_name[name].append(idx)
            if name not in allnames: allnames.append(name)
    result_by_idx=defaultdict(list)
    errors=[]
    for start in range(0,len(allnames),60):
        batch=allnames[start:start+60]
        try:
            got=run_batch(batch)
            for r in got:
                qid=pick(r,"query_identifier","id")
                mly=[]
                rawdist=num(pick(r,"distance","dist","value","d"))
                unit=pick(r,"unit","distance_unit","dist_unit").lower()
                if rawdist is not None:
                    if "mpc" in unit: val=rawdist*MPC_TO_MLY
                    elif "kpc" in unit: val=rawdist*0.003261563777
                    elif "pc" in unit: val=rawdist/1e6*3.261563777
                    else: val=None
                    if val and val>0: mly.append(val)
                matched=by_name.get(qid,[])
                for ix in matched:
                    result_by_idx[ix].append({
                        "query_identifier":qid,"main_id":pick(r,"main_id"),"ra":pick(r,"ra"),"dec":pick(r,"dec"),
                        "distance_raw":pick(r,"distance","dist","value","d"),"distance_unit":unit,
                        "distance_mly":f"{mly[0]:.8g}" if mly else "",
                        "method":pick(r,"method","bibcode","r"),"reference":pick(r,"bibcode","reference","ref")
                    })
            print(f"SIMBAD batch {start+1}-{start+len(batch)} identifiers: {len(got)} measurement rows",flush=True)
        except Exception as e:
            errors.append(f"batch {start+1}-{start+len(batch)}: {type(e).__name__}: {e}")
            print(errors[-1],flush=True)
        time.sleep(1)
    out_fields=list(rows[0].keys())+["simbad_batch_match_ids","simbad_batch_distance_count","simbad_batch_distances_mly","simbad_batch_median_distance_mly","simbad_batch_methods","simbad_batch_references","simbad_batch_status"]
    for r in rows:
        ix=int(r.pop("_source_row"))-1
        hits=result_by_idx.get(ix,[])
        vals=[num(x.get("distance_mly")) for x in hits]
        vals=[v for v in vals if v and v>0]
        med=statistics.median(vals) if vals else None
        r["simbad_batch_match_ids"]=" | ".join(dict.fromkeys(x["main_id"] for x in hits if x.get("main_id")))
        r["simbad_batch_distance_count"]=str(len(vals))
        r["simbad_batch_distances_mly"]=";".join(f"{v:.8g}" for v in vals)
        r["simbad_batch_median_distance_mly"]=f"{med:.8g}" if med else ""
        r["simbad_batch_methods"]=" | ".join(dict.fromkeys(x["method"] for x in hits if x.get("method")))
        r["simbad_batch_references"]=" | ".join(dict.fromkeys(x["reference"] for x in hits if x.get("reference")))
        r["simbad_batch_status"]="MATCH_WITH_DISTANCE" if vals else ("IDENTIFIER_MATCH_NO_DISTANCE" if hits else "NO_IDENTIFIER_MATCH")
    out=Path("simbad-unresolved-771-batch-results.csv")
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=out_fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print(f"Wrote {out} with {len(rows)} records",flush=True)
    print("SUMMARY: "+str({s:sum(1 for r in rows if r["simbad_batch_status"]==s) for s in sorted(set(r["simbad_batch_status"] for r in rows))}),flush=True)
    if errors: print("BATCH_ERRORS: "+ " || ".join(errors),flush=True)

def json_load(b):
    import json
    return json.loads(b.decode("utf-8"))

if __name__=="__main__": main()
