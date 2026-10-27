#!/usr/bin/env python3
"""Algorithmically audit all 88 Galaxy Viewer constellation line drawings."""
import csv, io, json, math, os, re, urllib.request
from collections import defaultdict, Counter

BASE = "https://raw.githubusercontent.com/creativival/hipparcos_planetarium_data_creator/main/data/"
JS_PATH = "viewer/modules/constellation-overlay/gv-constellation-overlay-0001.js"
OUT = "constellation_algorithmic_audit"
os.makedirs(OUT, exist_ok=True)

ITEMS = [
("And","Andromeda"),("Ant","Antlia"),("Aps","Apus"),("Aqr","Aquarius"),("Aql","Aquila"),("Ara","Ara"),("Ari","Aries"),("Aur","Auriga"),("Boo","Boötes"),("Cae","Caelum"),("Cam","Camelopardalis"),("Cnc","Cancer"),("CVn","Canes Venatici"),("CMa","Canis Major"),("CMi","Canis Minor"),("Cap","Capricornus"),("Car","Carina"),("Cas","Cassiopeia"),("Cen","Centaurus"),("Cep","Cepheus"),("Cet","Cetus"),("Cha","Chamaeleon"),("Cir","Circinus"),("Col","Columba"),("Com","Coma Berenices"),("CrA","Corona Australis"),("CrB","Corona Borealis"),("Crv","Corvus"),("Crt","Crater"),("Cru","Crux"),("Cyg","Cygnus"),("Del","Delphinus"),("Dor","Dorado"),("Dra","Draco"),("Equ","Equuleus"),("Eri","Eridanus"),("For","Fornax"),("Gem","Gemini"),("Gru","Grus"),("Her","Hercules"),("Hor","Horologium"),("Hya","Hydra"),("Hyi","Hydrus"),("Ind","Indus"),("Lac","Lacerta"),("Leo","Leo"),("LMi","Leo Minor"),("Lep","Lepus"),("Lib","Libra"),("Lup","Lupus"),("Lyn","Lynx"),("Lyr","Lyra"),("Men","Mensa"),("Mic","Microscopium"),("Mon","Monoceros"),("Mus","Musca"),("Nor","Norma"),("Oct","Octans"),("Oph","Ophiuchus"),("Ori","Orion"),("Pav","Pavo"),("Peg","Pegasus"),("Per","Perseus"),("Phe","Phoenix"),("Pic","Pictor"),("Psc","Pisces"),("PsA","Piscis Austrinus"),("Pup","Puppis"),("Pyx","Pyxis"),("Ret","Reticulum"),("Sge","Sagitta"),("Sgr","Sagittarius"),("Sco","Scorpius"),("Scl","Sculptor"),("Sct","Scutum"),("Ser","Serpens"),("Sex","Sextans"),("Tau","Taurus"),("Tel","Telescopium"),("Tri","Triangulum"),("TrA","Triangulum Australe"),("Tuc","Tucana"),("UMa","Ursa Major"),("UMi","Ursa Minor"),("Vel","Vela"),("Vir","Virgo"),("Vol","Volans"),("Vul","Vulpecula")]

def get(url):
    req=urllib.request.Request(url, headers={"User-Agent":"GalaxyViewer-Constellation-Algorithmic-Audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read().decode("utf-8-sig")

def norm(s): return re.sub(r"[^A-Z0-9]","",s.upper())
def angle(ra1,dec1,ra2,dec2):
    r=math.pi/180
    a1,d1,a2,d2=map(lambda x:x*r,(ra1,dec1,ra2,dec2))
    q=math.sin((d2-d1)/2)**2+math.cos(d1)*math.cos(d2)*math.sin((a2-a1)/2)**2
    return math.degrees(2*math.asin(min(1,math.sqrt(max(0,q)))))

line_text=get(BASE+"hip_constellation_line.csv")
star_text=get(BASE+"hip_constellation_line_star.csv")
js=get("https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/"+JS_PATH)
stars={}
for row in csv.reader(io.StringIO(star_text)):
    if len(row)<7: continue
    try:
        hip=int(row[0]); h=int(row[1]); m=int(row[2]); s=float(row[3])
        d=float(row[4].strip()); dm=float(row[5]); sec=float(row[6])
        sign=-1 if (d<0 or (d==0 and (dm<0 or (dm==0 and sec<0)))) else 1
        stars[hip]=((h+m/60+s/3600)*15, sign*(abs(d)+abs(dm)/60+abs(sec)/3600))
    except Exception: pass
source=defaultdict(list)
for row in csv.reader(io.StringIO(line_text)):
    if len(row)>=3:
        try: source[row[0]].append((int(row[1]),int(row[2])))
        except Exception: pass
source_by_norm={norm(k):k for k in source}

# Extract custom edge declarations from the same release JS that the viewer executes.
def array_edges(var):
    m=re.search(r"(?:const|let)\s+"+re.escape(var)+r"\s*=\s*\[(.*?)\];",js,re.S)
    if not m: raise RuntimeError("Cannot parse release JS edge array: "+var)
    return [(int(a),int(b)) for a,b in re.findall(r"\[\s*(\d+)\s*,\s*(\d+)\s*\]",m.group(1))]
cam_edges=array_edges("camLines")
libra_edges=array_edges("libraEdges")
# Read custom star coordinate declarations from release JS.
cam_block=re.search(r"const\s+camelopardalisStars\s*=\s*\[(.*?)\];",js,re.S)
if not cam_block: raise RuntimeError("Cannot parse Camelopardalis star array")
cam_stars=[]
for hip,ra,dec in re.findall(r"\{\s*hip\s*:\s*(\d+)\s*,\s*ra\s*:\s*([-+\d.]+)\s*,\s*dec\s*:\s*([-+\d.]+)\s*\}",cam_block.group(1)):
    cam_stars.append((int(hip),float(ra),float(dec)))
libra_block=re.search(r"const\s+libraStars\s*=\s*\[(.*?)\];",js,re.S)
if not libra_block: raise RuntimeError("Cannot parse Libra star array")
libra_stars=[]
for ra,dec,name in re.findall(r"\{\s*id\s*:\s*(\d+)\s*,\s*ra\s*:\s*([-+\d.]+)\s*,\s*dec\s*:\s*([-+\d.]+)\s*\}",libra_block.group(1)):
    libra_stars.append((int(ra),float(dec),float(name))) # corrected below
# regex above captures id,ra,dec; retain proper tuple
libra_stars=[]
for sid,ra,dec in re.findall(r"\{\s*id\s*:\s*(\d+)\s*,\s*ra\s*:\s*([-+\d.]+)\s*,\s*dec\s*:\s*([-+\d.]+)",libra_block.group(1)):
    libra_stars.append((int(sid),float(ra),float(dec)))
fornax_block=re.search(r"const\s+fornaxPrincipalStars\s*=\s*\[(.*?)\];",js,re.S)
if not fornax_block: raise RuntimeError("Cannot parse Fornax star list")
fornax_stars=[]
for name,ra,dec in re.findall(r"\{\s*name\s*:\s*([^,]+),\s*ra\s*:\s*([-+\d.]+),\s*dec\s*:\s*([-+\d.]+)\s*\}",fornax_block.group(1)):
    fornax_stars.append((name.strip().strip("'\""),float(ra),float(dec)))
if len(cam_stars)!=8 or len(cam_edges)!=7 or len(libra_stars)!=6 or len(libra_edges)!=6 or len(fornax_stars)!=3:
    raise RuntimeError(f"Unexpected parsed custom definitions: Cam {len(cam_stars)}/{len(cam_edges)}, Libra {len(libra_stars)}/{len(libra_edges)}, Fornax {len(fornax_stars)}")

custom={}
custom["Cam"]=(set(i for i,_,_ in cam_stars),cam_edges,[(i,ra,dec) for i,ra,dec in cam_stars])
custom["For"]=(set(range(3)),[(0,1),(1,2)],[(i,ra,dec) for i,(_,ra,dec) in enumerate(fornax_stars)])
custom["Lib"]=(set(i for i,_,_, in []),[],[]) if False else (set(i for i,_,_ in libra_stars),libra_edges,[(i,ra,dec) for i,ra,dec in libra_stars])

rows=[]; edge_rows=[]; errors=[]; warnings=[]
for abbr,name in ITEMS:
    key=source_by_norm.get(norm(abbr))
    is_custom=abbr in custom
    source_edges=source.get(key,[]) if key else []
    if is_custom:
        _, expected, custom_pts=custom[abbr]
        expected=[tuple(e) for e in expected]
        point_ids={p[0] for p in custom_pts}
        coord_map={p[0]:(p[1],p[2]) for p in custom_pts}
        # For source HIP-based custom points, validate their declared positions against source HIP coordinates.
        if abbr=="Cam":
            for hip,ra,dec in custom_pts:
                if hip not in stars:
                    errors.append(f"{abbr}: custom HIP {hip} has no source star coordinate")
                else:
                    sep=angle(ra,dec,*stars[hip])
                    if sep>0.02: errors.append(f"{abbr}: HIP {hip} custom/source coordinate differs by {sep:.5f} deg")
        # Find nearest source star for every non-HIP custom point and report it for human review.
        if abbr in ("For","Lib"):
            for pid,(ra,dec) in coord_map.items():
                nearest=min(((angle(ra,dec,sra,sdec),hip) for hip,(sra,sdec) in stars.items()),default=(999,None))
                if nearest[0] > 0.20:
                    warnings.append(f"{abbr}: custom point {pid} nearest source HIP {nearest[1]} is {nearest[0]:.4f} deg away")
    else:
        expected=source_edges
        point_ids=set()
        coord_map={}
    # Mirror the actual JS behavior: source edges are drawn only if both endpoints have coordinates;
    # Cam/For/Lib source edges are suppressed and replaced by explicit custom edges.
    rendered=[]
    if not is_custom:
        for a,b in source_edges:
            if a in stars and b in stars: rendered.append((a,b))
            else: errors.append(f"{abbr}: edge {a}-{b} is skipped by JS because an endpoint has no coordinate")
    else:
        rendered=list(expected)
    missing=Counter(expected)-Counter(rendered)
    extra=Counter(rendered)-Counter(expected)
    if missing: errors.append(f"{abbr}: {sum(missing.values())} expected edges missing")
    if extra: errors.append(f"{abbr}: {sum(extra.values())} unexpected edges")
    duplicate_count=len(rendered)-len(set(tuple(sorted(e)) for e in rendered))
    if duplicate_count: errors.append(f"{abbr}: {duplicate_count} duplicate edges")
    if not key and not is_custom: errors.append(f"{abbr}: no source line group matched abbreviation")
    if not is_custom and not source_edges: errors.append(f"{abbr}: zero source line edges")
    # Endpoint coordinate availability / custom coordinate validity.
    if is_custom:
        for a,b in rendered:
            if a not in point_ids or b not in point_ids:
                errors.append(f"{abbr}: edge {a}-{b} references a point not defined in custom star list")
    else:
        for a,b in source_edges:
            if a not in stars or b not in stars: pass # already reported above
    rows.append({
      "abbr":abbr,"constellation":name,"source_group":key or ("custom override" if is_custom else ""),
      "implementation":"custom override" if is_custom else "upstream HIP line CSV",
      "source_edges":len(source_edges),"expected_edges":len(expected),"rendered_edges":len(rendered),
      "unique_edges":len(set(tuple(sorted(e)) for e in rendered)),
      "missing_edges":sum(missing.values()),"extra_edges":sum(extra.values()),
      "source_stars":len({v for e in source_edges for v in e}),
      "coordinate_points":len(point_ids) if is_custom else len({v for e in source_edges for v in e if v in stars}),
      "status":"FAIL" if any(x.startswith(abbr+":") for x in errors) else "PASS"
    })
    for a,b in rendered:
        edge_rows.append({"abbr":abbr,"constellation":name,"star_a":a,"star_b":b,"source":"custom override" if is_custom else "upstream HIP line CSV","has_coords_a":(a in point_ids if is_custom else a in stars),"has_coords_b":(b in point_ids if is_custom else b in stars)})

# Check total recognized constellation count and report exact source-level edge integrity.
if len(ITEMS)!=88: errors.append(f"IAU list has {len(ITEMS)} entries, not 88")
if len(set(a for a,_ in ITEMS))!=88: errors.append("Duplicate constellation abbreviations in audit list")
for row in rows:
    row["status"]="FAIL" if any(x.startswith(row["abbr"]+":") for x in errors) else "PASS"

def write_csv(path, data):
    if not data: return
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
write_csv(os.path.join(OUT,"constellation_summary.csv"),rows)
write_csv(os.path.join(OUT,"edge_register.csv"),edge_rows)
with open(os.path.join(OUT,"audit_report.json"),"w",encoding="utf-8") as f:
    json.dump({"constellations":rows,"edge_count":len(edge_rows),"errors":errors,"warnings":warnings,"source_line_group_count":len(source),"star_coordinate_count":len(stars)},f,indent=2)
with open(os.path.join(OUT,"audit_report.md"),"w",encoding="utf-8") as f:
    f.write("# Galaxy Viewer constellation algorithmic audit\n\n")
    f.write(f"- Constellations checked: {len(rows)}\n- Rendered edge records: {len(edge_rows)}\n- Source HIP coordinates: {len(stars)}\n- Source constellation groups: {len(source)}\n- Errors: {len(errors)}\n- Warnings: {len(warnings)}\n\n")
    f.write("## Per-constellation results\n\n| Abbr | Constellation | Implementation | Expected edges | Rendered edges | Missing | Extra | Result |\n|---|---|---|---:|---:|---:|---:|---|\n")
    for r in rows: f.write(f"| {r['abbr']} | {r['constellation']} | {r['implementation']} | {r['expected_edges']} | {r['rendered_edges']} | {r['missing_edges']} | {r['extra_edges']} | {r['status']} |\n")
    f.write("\n## Errors\n")
    f.write("\n".join("- "+e for e in errors) if errors else "\nNone detected by structural edge/coordinate checks.\n")
    f.write("\n## Warnings\n")
    f.write("\n".join("- "+w for w in warnings) if warnings else "\nNone.\n")
print(f"constellations={len(rows)} edges={len(edge_rows)} errors={len(errors)} warnings={len(warnings)}")
print("\n".join(errors[:100]))
print("\n".join(warnings[:30]))
if errors: raise SystemExit(1)
