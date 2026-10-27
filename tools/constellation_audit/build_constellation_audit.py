import csv, io, math, os, re, urllib.request
from collections import defaultdict
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = "https://raw.githubusercontent.com/creativival/hipparcos_planetarium_data_creator/main/data/"
LINE_URL = BASE + "hip_constellation_line.csv"
STAR_URL = BASE + "hip_constellation_line_star.csv"
IAU_URL = "https://www.iau.org/IAU/Astronomy-FAQs/Constellations.aspx"
OUT = "Galaxy_Viewer_88_Constellation_Audit.pdf"
EFFECTIVE_EDGES_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/tools/constellation_audit/release_effective_edges.csv"

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"GalaxyViewer-Constellation-Audit/1.0"})
    with urllib.request.urlopen(req,timeout=8) as r: return r.read()

lines_text=get(LINE_URL).decode("utf-8-sig")
effective_edges_text=get(EFFECTIVE_EDGES_URL).decode("utf-8-sig")
stars_text=get(STAR_URL).decode("utf-8-sig")
star={}
for row in csv.reader(io.StringIO(stars_text)):
    if len(row)<7: continue
    try:
        hip=int(row[0]); h=int(row[1]); m=int(row[2]); s=float(row[3])
        ds=row[4].strip(); d=float(ds); dm=float(row[5]); sec=float(row[6])
        sign=-1 if (d<0 or (d==0 and (dm<0 or (dm==0 and sec<0)))) else 1
        ra=(h+m/60+s/3600)*15
        dec=sign*(abs(d)+abs(dm)/60+abs(sec)/3600)
        star[hip]=(ra,dec)
    except Exception: continue
segments=defaultdict(list)
for row in csv.reader(io.StringIO(lines_text)):
    if len(row)>=3:
        try: segments[row[0]].append((int(row[1]),int(row[2])))
        except Exception: pass

# Standard IAU list: official three-letter abbreviations and Latin names.
items = [
("And","Andromeda"),("Ant","Antlia"),("Aps","Apus"),("Aqr","Aquarius"),("Aql","Aquila"),("Ara","Ara"),("Ari","Aries"),("Aur","Auriga"),("Boo","Boötes"),("Cae","Caelum"),("Cam","Camelopardalis"),("Cnc","Cancer"),("CVn","Canes Venatici"),("CMa","Canis Major"),("CMi","Canis Minor"),("Cap","Capricornus"),("Car","Carina"),("Cas","Cassiopeia"),("Cen","Centaurus"),("Cep","Cepheus"),("Cet","Cetus"),("Cha","Chamaeleon"),("Cir","Circinus"),("Col","Columba"),("Com","Coma Berenices"),("CrA","Corona Australis"),("CrB","Corona Borealis"),("Crv","Corvus"),("Crt","Crater"),("Cru","Crux"),("Cyg","Cygnus"),("Del","Delphinus"),("Dor","Dorado"),("Dra","Draco"),("Equ","Equuleus"),("Eri","Eridanus"),("For","Fornax"),("Gem","Gemini"),("Gru","Grus"),("Her","Hercules"),("Hor","Horologium"),("Hya","Hydra"),("Hyi","Hydrus"),("Ind","Indus"),("Lac","Lacerta"),("Leo","Leo"),("LMi","Leo Minor"),("Lep","Lepus"),("Lib","Libra"),("Lup","Lupus"),("Lyn","Lynx"),("Lyr","Lyra"),("Men","Mensa"),("Mic","Microscopium"),("Mon","Monoceros"),("Mus","Musca"),("Nor","Norma"),("Oct","Octans"),("Oph","Ophiuchus"),("Ori","Orion"),("Pav","Pavo"),("Peg","Pegasus"),("Per","Perseus"),("Phe","Phoenix"),("Pic","Pictor"),("Psc","Pisces"),("PsA","Piscis Austrinus"),("Pup","Puppis"),("Pyx","Pyxis"),("Ret","Reticulum"),("Sge","Sagitta"),("Sgr","Sagittarius"),("Sco","Scorpius"),("Scl","Sculptor"),("Sct","Scutum"),("Ser","Serpens"),("Sex","Sextans"),("Tau","Taurus"),("Tel","Telescopium"),("Tri","Triangulum"),("TrA","Triangulum Australe"),("Tuc","Tucana"),("UMa","Ursa Major"),("UMi","Ursa Minor"),("Vel","Vela"),("Vir","Virgo"),("Vol","Volans"),("Vul","Vulpecula")
]
def norm(s): return re.sub(r"[^A-Z]","",s.upper())
def source_key(abbr):
    # CSV sometimes uses different capitalization; match case-insensitively.
    for k in segments:
        if norm(k)==norm(abbr): return k
    return None

# Overrides currently encoded in Galaxy Viewer release JS.
cam_stars=[(33694,105.016033,76.977442),(29997,94.711583,69.320034),(22783,73.512544,66.342660),(23522,75.854572,60.442281),(23040,74.321752,53.752083),(17959,57.589483,71.332368),(17884,57.380356,65.526006),(16228,52.267227,59.940335)]
cam_edges=[(33694,29997),(29997,22783),(22783,23522),(23522,23040),(22783,17959),(17959,17884),(17884,16228)]
fornax_stars=[(9000001,"Dalim / Alpha Fornacis",48.018875,-28.9876111111),(9000002,"Beta Fornacis",42.2725833333,-32.4058888889),(9000003,"Nu Fornacis",31.1226666667,-29.2968055556)]
libra_stars=[(9000011,"Delta Librae",225.2967,-8.5197),(9000012,"Alpha Librae",222.7196,-16.0418),(9000013,"Sigma Librae",226.0176,-25.2819),(9000014,"Gamma Librae",233.8816,-14.7895),(9000015,"Upsilon Librae",234.2561,-28.1351),(9000016,"Beta Librae",229.2517,-9.3829)]
libra_edges=[(9000016,9000011),(9000011,9000012),(9000016,9000012),(9000012,9000013),(9000016,9000014),(9000014,9000015)]
custom = {
"Cam": ([(i,f"HIP {i}",ra,dec) for i,ra,dec in cam_stars], cam_edges),
"For": ([(i,n,ra,dec) for i,n,ra,dec in fornax_stars], [(9000001,9000002),(9000002,9000003)]),
"Lib": ([(i,n,ra,dec) for i,n,ra,dec in libra_stars], libra_edges),
}
# Direct official IAU / Sky & Telescope J2000 chart PDF endpoints.
iau_chart_urls={abbr:"https://iauarchive.eso.org/static/public/constellations/pdf/"+abbr.upper()+".pdf" for abbr,name in items}

W,H=landscape(A4)
c=canvas.Canvas(OUT,pagesize=(W,H))
navy=colors.HexColor("#0b1730"); blue=colors.HexColor("#176b87"); pale=colors.HexColor("#dbeafe")
def project(points):
    # Local gnomonic tangent-plane projection from the exact J2000 RA/Dec coordinates.
    # Reverse RA as on a conventional celestial chart; do not stretch RA and Dec independently.
    if not points: return {}
    ras=np.radians(np.array([p[1] for p in points],dtype=float))
    decs=np.radians(np.array([p[2] for p in points],dtype=float))
    ra0=float(np.mean(ras)); dec0=float(np.mean(decs)); dra=ras-ra0
    den=np.sin(dec0)*np.sin(decs)+np.cos(dec0)*np.cos(decs)*np.cos(dra)
    den=np.where(np.abs(den)<1e-9,1e-9,den)
    x=np.cos(decs)*np.sin(dra)/den
    y=(np.cos(dec0)*np.sin(decs)-np.sin(dec0)*np.cos(decs)*np.cos(dra))/den
    return {p[0]:(-float(x[i]),float(y[i])) for i,p in enumerate(points)}

def draw_diagram(x,y,w,h,rows,edges,title,source_label):
    c.setStrokeColor(colors.HexColor("#94a3b8")); c.roundRect(x,y,w,h,6,stroke=1,fill=0)
    c.setFillColor(navy); c.setFont("Helvetica-Bold",10); c.drawString(x+8,y+h-16,title)
    c.setFillColor(colors.HexColor("#475569")); c.setFont("Helvetica",7); c.drawString(x+8,y+h-28,source_label[:100])
    pts=[(r[0],r[2],r[3]) for r in rows]
    pos=project(pts)
    if not pos:
        c.setFont("Helvetica",9); c.drawCentredString(x+w/2,y+h/2,"No coordinate data found"); return
    px=x+18; py=y+18; pw=w-36; ph=h-58
    vals=list(pos.values()); xs=[v[0] for v in vals]; ys=[v[1] for v in vals]
    minx,maxx=min(xs),max(xs); miny,maxy=min(ys),max(ys)
    dx=max(maxx-minx,.01); dy=max(maxy-miny,.01)
    scale=min(pw/dx,ph/dy)
    ox=px+(pw-dx*scale)/2; oy=py+(ph-dy*scale)/2
    xy={i:(ox+(p[0]-minx)*scale,oy+(p[1]-miny)*scale) for i,p in pos.items()}
    c.setStrokeColor(colors.HexColor("#68a9c5")); c.setLineWidth(1.1)
    for a,b in edges:
        if a in xy and b in xy: c.line(*xy[a],*xy[b])
    c.setFillColor(colors.HexColor("#f59e0b"))
    for i,(sx,sy) in xy.items():
        c.circle(sx,sy,2.3,stroke=0,fill=1)
# Build left-hand diagrams from a source-derived edge register generated from the
# exact release JavaScript module plus its runtime line CSV. Do not retype custom edges here.
effective=defaultdict(list)
for row in csv.DictReader(io.StringIO(effective_edges_text)):
    abbr=row["constellation_abbr"]
    aid=row["endpoint_A_id"]; bid=row["endpoint_B_id"]
    a=(aid,row["endpoint_A_label"],float(row["endpoint_A_ra_deg"]),float(row["endpoint_A_dec_deg"]))
    b=(bid,row["endpoint_B_label"],float(row["endpoint_B_ra_deg"]),float(row["endpoint_B_dec_deg"]))
    effective[abbr].append((a,b,row["implementation"]))

def coords_rows(abbr):
    edges_data=effective.get(abbr,[])
    if not edges_data: return [],[]
    point_map={}
    edges=[]
    for a,b,implementation in edges_data:
        point_map[a[0]]=a
        point_map[b[0]]=b
        edges.append((a[0],b[0]))
    rows=[(pid,label,ra,dec) for pid,(pid,label,ra,dec) in point_map.items()]
    return rows,edges

def reference_rows(abbr):
    key=source_key(abbr)
    if not key: return [],[]
    rows,edges=coords_rows(abbr)
    # Reference wire diagram is the upstream Hipparcos constellation-line dataset.
    refedges=segments[key]
    refids=[]
    for a,b in refedges:
        if a not in refids: refids.append(a)
        if b not in refids: refids.append(b)
    refrows=[(i,f"HIP {i}",star[i][0],star[i][1]) for i in refids if i in star]
    return refrows,refedges
def draw_iau_chart(x,y,w,h,abbr,rows,edges):
    c.setStrokeColor(colors.HexColor("#94a3b8")); c.roundRect(x,y,w,h,6,stroke=1,fill=0)
    c.setFillColor(navy); c.setFont("Helvetica-Bold",10); c.drawString(x+8,y+h-16,"REFERENCE CHART / SOURCE WIRES")
    c.setFillColor(colors.HexColor("#475569")); c.setFont("Helvetica",7)
    c.drawString(x+8,y+h-28,"Official IAU / Sky & Telescope J2000 chart; fallback clearly marked if unavailable")
    chart_url=iau_chart_urls.get(abbr)
    if chart_url:
        try:
            import pymupdf as fitz
            from reportlab.lib.utils import ImageReader
            raw=get(chart_url)
            doc=fitz.open(stream=raw,filetype="pdf")
            if doc.page_count:
                pix=doc[0].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
                img=ImageReader(io.BytesIO(pix.tobytes("png")))
                iw,ih=img.getSize()
                bx=x+10; by=y+10; bw=w-20; bh=h-45
                scale=min(bw/iw,bh/ih)
                dw,dh=iw*scale,ih*scale
                c.drawImage(img,bx+(bw-dw)/2,by+(bh-dh)/2,width=dw,height=dh,preserveAspectRatio=True,mask="auto")
                doc.close()
                return
        except Exception as exc:
            print("IAU chart download/render failed",abbr,chart_url,repr(exc))
    c.setFillColor(colors.HexColor("#991b1b")); c.setFont("Helvetica-Bold",8)
    c.drawCentredString(x+w/2,y+h/2,"OFFICIAL IAU CHART UNAVAILABLE")
    c.setFont("Helvetica",7); c.drawCentredString(x+w/2,y+h/2-13,"Chart could not be retrieved; no substitute diagram shown")

def draw_header(title,subtitle,page):
    c.setFillColor(navy); c.rect(0,H-55,W,55,stroke=0,fill=1)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold",16); c.drawString(26,H-29,title)
    c.setFont("Helvetica",8); c.drawString(26,H-43,subtitle)
    c.setFillColor(colors.HexColor("#64748b")); c.setFont("Helvetica",7); c.drawRightString(W-26,15,f"Galaxy Viewer audit • page {page}")
page=0
for n,(abbr,name) in enumerate(items,1):
    rows,edges=coords_rows(abbr)
    refrows,refedges=reference_rows(abbr)
    page+=1
    draw_header(f"{n:02d}/88  {name} ({abbr}) — wire-diagram comparison",
                "Left: Galaxy Viewer release implementation • Right: upstream Hipparcos line dataset used by the overlay module",page)
    margin=25; gap=14; w=(W-2*margin-gap)/2; y=105; h=H-185
    draw_diagram(margin,y,w,h,rows,edges,"GALAXY VIEWER", "Exact release JS edges + runtime source CSV; custom overrides applied")
    draw_iau_chart(margin+w+gap,y,w,h,abbr,refrows,refedges)
    c.setFillColor(navy); c.setFont("Helvetica-Bold",8)
    c.drawString(28,82,"Review:  [ ] Correct   [ ] Incorrect   [ ] Needs review")
    c.drawString(28,65,"Missing / extra connections: ______________________________________________________________")
    c.setFillColor(colors.HexColor("#475569")); c.setFont("Helvetica",7)
    c.drawString(28,43,"Important: the IAU officially standardizes constellation boundaries and names, not one universal stick-figure line pattern.")
    c.showPage()
    page+=1
    draw_header(f"{n:02d}/88  {name} ({abbr}) — coordinate and segment register",
                "Coordinates are J2000 equatorial RA/Dec in decimal degrees, parsed from the catalog's HIP source table; custom points are labeled explicitly.",page)
    data=[["Point / HIP ID","RA (deg)","Dec (deg)","Connected to (star labels)"]]
    if rows:
        adjacency=defaultdict(list)
        label_by_id={row[0]:row[1] for row in rows}
        for a,b in edges:
            if a in label_by_id and b in label_by_id:
                adjacency[a].append(b); adjacency[b].append(a)
        for hip,label,ra,dec in rows:
            conn=", ".join(label_by_id[q] for q in adjacency[hip]) or "—"
            data.append([label, f"{ra:.6f}", f"{dec:+.6f}", conn])
    else: data.append(["NO COORDINATE ROWS FOUND","","",""])
    # split large tables across multiple pages while preserving every point
    usable_rows=31
    chunks=[data[0:1+usable_rows]]
    for start in range(1+usable_rows,len(data),usable_rows):
        chunks.append([data[0]]+data[start:start+usable_rows])
    for ci,chunk in enumerate(chunks):
        if ci>0:
            page+=1
            draw_header(f"{n:02d}/88  {name} ({abbr}) — coordinate register (continued)",
                        "Continuation of point coordinates and connections.",page)
        t=Table(chunk,colWidths=[180,90,90,220],repeatRows=1,rowHeights=[20]+[16]*(len(chunk)-1))
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),navy),("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),7),
            ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f1f5f9")]),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),5),
            ("RIGHTPADDING",(0,0),(-1,-1),5)
        ]))
        tw,th=t.wrapOn(c,W-50,H-100)
        t.drawOn(c,25,H-78-th)
        c.setFillColor(colors.HexColor("#475569")); c.setFont("Helvetica",7)
        c.drawString(27,32,f"Effective release edges: {len(edges)} • unique plotted points: {len(rows)} • source: release_effective_edges.csv")
        c.showPage()
c.save()
print(f"Created {OUT}; constellations={len(items)}; stars={len(star)}; source line groups={len(segments)}; IAU chart links found={len(iau_chart_urls)}")
