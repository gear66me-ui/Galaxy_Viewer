#!/usr/bin/env python3
import csv, io, json, math, os, re, statistics, time, urllib.error, urllib.parse, urllib.request
from collections import Counter
from pathlib import Path
from PIL import Image

CAT=Path('viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0019.json')
OUT=Path('test'); TIMEOUT=int(os.getenv('HUBBLE_IV_TIMEOUT','25')); MAX=8*1024*1024
UA='GalaxyViewer-HubbleIV-Audit/1.0'

def txt(v): return '' if v is None else str(v).strip()
def num(v):
    try: return None if isinstance(v,bool) or txt(v)=='' else float(v)
    except: return None

def records():
    d=json.loads(CAT.read_text(encoding='utf-8'))
    if isinstance(d,list): return d
    if isinstance(d,dict):
        for k in ('galaxies','items','records','entries','data'):
            if isinstance(d.get(k),list): return d[k]
    raise RuntimeError('unrecognized Catalog 0019 root')

def fetch(url, head=False, limit=None):
    if not url.startswith(('http://','https://')): return {'ok':False,'status':None,'type':'','length':None,'ms':0,'body':b'','error':'missing/malformed URL'}
    h={'User-Agent':UA,'Cache-Control':'no-cache','Pragma':'no-cache'}
    req=urllib.request.Request(url,method='HEAD' if head else 'GET',headers=h); t=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
            body=b'' if head else r.read((limit or MAX)+1)
            if limit and len(body)>limit: raise ValueError(f'preview exceeds {limit} bytes')
            l=r.headers.get('Content-Length','')
            return {'ok':200<=getattr(r,'status',200)<400,'status':getattr(r,'status',200),'type':r.headers.get('Content-Type',''),'length':int(l) if l.isdigit() else None,'ms':round((time.monotonic()-t)*1000),'body':body,'error':''}
    except urllib.error.HTTPError as e: return {'ok':False,'status':e.code,'type':e.headers.get('Content-Type','') if e.headers else '','length':None,'ms':round((time.monotonic()-t)*1000),'body':b'','error':f'HTTP {e.code}'}
    except Exception as e: return {'ok':False,'status':None,'type':'','length':None,'ms':round((time.monotonic()-t)*1000),'body':b'','error':str(e)}

def active(url):
    r=fetch(url,head=True)
    if r['ok']: return r
    h={'User-Agent':UA,'Range':'bytes=0-32767','Cache-Control':'no-cache'}; t=time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=TIMEOUT) as q:
            q.read(32768); l=q.headers.get('Content-Length','')
            return {'ok':200<=getattr(q,'status',200)<400,'status':getattr(q,'status',200),'type':q.headers.get('Content-Type',''),'length':int(l) if l.isdigit() else None,'ms':round((time.monotonic()-t)*1000),'body':b'','error':''}
    except urllib.error.HTTPError as e: return {'ok':False,'status':e.code,'type':'','length':None,'ms':round((time.monotonic()-t)*1000),'body':b'','error':f'HTTP {e.code}'}
    except Exception as e: return {'ok':False,'status':None,'type':'','length':None,'ms':round((time.monotonic()-t)*1000),'body':b'','error':str(e)}

def preview(url,aid):
    p=urllib.parse.urlparse(url); name=Path(p.path).name
    if p.netloc.lower().endswith('esahubble.org') and re.search(r'\.(jpe?g|png|webp)$',name,re.I): return f'https://cdn.esahubble.org/archives/images/screen/{name}'
    return f'https://cdn.esahubble.org/archives/images/screen/{aid}.jpg' if aid else url

def metrics(blob):
    with Image.open(io.BytesIO(blob)) as im:
        im=im.convert('RGB'); im.thumbnail((512,512)); w,h=im.size; px=list(im.getdata()); n=len(px)
        lum=[]; sat=[]; rg=[]; yb=[]; dark=black=white=0
        for r,g,b in px:
            mx=max(r,g,b); mn=min(r,g,b); y=.2126*r+.7152*g+.0722*b
            lum.append(y); sat.append(0 if mx==0 else (mx-mn)/mx); rg.append(r-g); yb.append(.5*(r+g)-b)
            dark+=y<12; black+=mx<=3; white+=mn>=252
        s=sorted(lum); p05=s[int((n-1)*.05)]; p95=s[int((n-1)*.95)]
        cf=math.sqrt(statistics.pvariance(rg)+statistics.pvariance(yb))+.3*math.sqrt(statistics.fmean(rg)**2+statistics.fmean(yb)**2)
        g=im.convert('L'); a=list(g.getdata()); bw=[]; inside=[]
        for y in range(h):
            row=y*w
            for x in range(1,w):
                d=abs(a[row+x]-a[row+x-1]); (bw if x%8==0 else inside).append(d)
        block=(statistics.fmean(bw)/(statistics.fmean(inside)+1e-6)) if bw and inside else 1
        return {'width':w,'height':h,'meanLuma':round(statistics.fmean(lum),2),'dynamicRangeP90':round(p95-p05,2),'meanSaturation':round(statistics.fmean(sat),4),'colorfulness':round(cf,2),'darkPixelFraction':round(dark/n,4),'blackClipFraction':round(black/n,4),'whiteClipFraction':round(white/n,4),'blockinessRatio':round(block,3)}

def visual_flags(m):
    f=[]
    if m['meanSaturation']<.035 and m['colorfulness']<8: f.append('NEAR_GRAYSCALE')
    if m['dynamicRangeP90']<42: f.append('LOW_DYNAMIC_RANGE')
    if m['darkPixelFraction']>.82: f.append('EXCESSIVE_BLACK_BACKGROUND')
    if m['meanLuma']<22: f.append('VERY_DARK')
    if m['width']<320 or m['height']<240: f.append('LOW_PREVIEW_RESOLUTION')
    if m['blockinessRatio']>1.85: f.append('PIXELATED_OR_BLOCKY')
    return f

def structural(rec):
    f=[]; fv=num(rec.get('fieldOfView')); ori=num(rec.get('orientation'))
    if fv is None: f.append('FOV_MALFORMED_OR_MISSING')
    elif not .002<=fv<=20: f.append('FOV_EXTREME')
    if ori is None: f.append('ORIENTATION_MALFORMED_OR_MISSING')
    elif not -360<=ori<=360: f.append('ORIENTATION_EXTREME')
    return fv,ori,f

def normname(s): return re.sub(r'[^a-z0-9]+','',txt(s).lower())
def sep(a,b):
    ra1,dc1,ra2,dc2=map(num,(a.get('ra'),a.get('dec'),b.get('ra'),b.get('dec')))
    if None in (ra1,dc1,ra2,dc2): return 999
    x=math.radians(ra1-ra2)*math.cos(math.radians((dc1+dc2)/2)); y=math.radians(dc1-dc2)
    return math.degrees(math.sqrt(x*x+y*y))

def candidate_replacements(rows):
    for r in rows:
        if not any(x in r['flags'] for x in ('NEAR_GRAYSCALE','LOW_DYNAMIC_RANGE','EXCESSIVE_BLACK_BACKGROUND','VERY_DARK','LOW_PREVIEW_RESOLUTION','PIXELATED_OR_BLOCKY')): continue
        keys={normname(r.get(k,'')) for k in ('archiveId','name','designation') if normname(r.get(k,''))}
        cand=[]
        for q in rows:
            if q is r or not q.get('metrics') or q.get('activeHttpStatus') not in (200,206): continue
            qkeys={normname(q.get(k,'')) for k in ('archiveId','name','designation') if normname(q.get(k,''))}
            same=bool(keys & qkeys) or sep(r,q)<=.03
            if not same: continue
            bad=sum(x in q['flags'] for x in ('NEAR_GRAYSCALE','LOW_DYNAMIC_RANGE','EXCESSIVE_BLACK_BACKGROUND','VERY_DARK','LOW_PREVIEW_RESOLUTION','PIXELATED_OR_BLOCKY'))
            score=100*bad-q['metrics']['colorfulness']-.2*q['metrics']['dynamicRangeP90']
            cand.append((score,q))
        r['candidateReplacements']=[{'archiveId':q['archiveId'],'name':q['name'],'selectedImageUrl':q['selectedImageUrl'],'sourceUrl':q['sourceUrl']} for _,q in sorted(cand,key=lambda x:x[0])[:3]]

def main():
    src=records(); rows=[]; print(f'Hubble IV: {len(src)} records')
    for i,rec in enumerate(src,1):
        aid=txt(rec.get('archiveId') or rec.get('id')); name=txt(rec.get('displayName') or rec.get('name') or rec.get('title')); url=txt(rec.get('selectedImageUrl')); source=txt(rec.get('sourceUrl'))
        fv,ori,sf=structural(rec); ah=active(url); af=[]
        if not ah['ok']: af.append('STALE_ACTIVE_LINK' if ah['status'] in (404,410) else 'ACTIVE_LINK_FAILURE')
        elif ah['type'] and not ah['type'].lower().startswith('image/'): af.append('ACTIVE_LINK_NOT_IMAGE')
        if ah['length'] is not None and ah['length']<10000: af.append('ACTIVE_IMAGE_UNEXPECTEDLY_TINY')
        pu=preview(url,aid); pr=fetch(pu,limit=MAX); m=None; vf=[]
        if pr['ok'] and pr['body']:
            try: m=metrics(pr['body']); vf=visual_flags(m)
            except Exception as e: vf=['PREVIEW_DECODE_FAILURE']; pr['error']=str(e)
        else: vf=['PREVIEW_UNAVAILABLE']
        flags=af+vf+sf; groups=[]
        if vf: groups.append('BAD IMAGE')
        if af: groups.append('STALE ACTIVE LINK')
        if any(x.startswith('FOV_') for x in sf): groups.append('FOV')
        if any(x.startswith('ORIENTATION_') for x in sf): groups.append('ORIENTATION')
        if len(groups)>1: groups.append('MULTIPLE PROBLEMS')
        rows.append({'index':i,'archiveId':aid,'name':name,'designation':txt(rec.get('designation')),'ra':rec.get('ra'),'dec':rec.get('dec'),'selectedImageUrl':url,'sourceUrl':source,'previewUrl':pu,'fieldOfView':rec.get('fieldOfView'),'fieldOfViewNumeric':fv,'orientation':rec.get('orientation'),'orientationNumeric':ori,'activeHttpStatus':ah['status'],'activeContentType':ah['type'],'activeContentLength':ah['length'],'activeElapsedMs':ah['ms'],'activeError':ah['error'],'previewHttpStatus':pr['status'],'previewError':pr['error'],'metrics':m,'flags':flags,'groups':groups,'candidateReplacements':[]})
        if i%50==0 or i==len(src): print(f'Progress {i}/{len(src)}')
    candidate_replacements(rows)
    gc=Counter(g for r in rows for g in r['groups']); fc=Counter(f for r in rows for f in r['flags']); bad=[r for r in rows if r['flags']]
    summary={'catalogPath':str(CAT),'recordCount':len(rows),'recordsWithAnyFlag':len(bad),'groupCounts':dict(gc),'flagCounts':dict(fc),'recordsWithReplacementCandidates':sum(bool(r['candidateReplacements']) for r in rows),'method':{'activeLink':'actual selectedImageUrl; HEAD with GET fallback','visual':'screen-sized rendition of same selected ESA asset; RGB saturation/colorfulness/dynamic-range/darkness/blockiness metrics','replacementCandidates':'other healthy Catalog 0019 Hubble records with matching normalized identity or <=0.03 degree coordinates, ranked for visual quality','fov':'numeric presence + conservative 0.002..20 degree plausibility','orientation':'numeric presence + conservative -360..360 degree plausibility','note':'flags are review candidates, never automatic repair authority'}}
    (OUT/'HUBBLE-IV-REPORT.json').write_text(json.dumps({'summary':summary,'results':rows},indent=2,ensure_ascii=False),encoding='utf-8')
    cols=['index','archiveId','name','groups','flags','fieldOfView','orientation','activeHttpStatus','activeContentLength','selectedImageUrl','previewUrl','candidateReplacements','sourceUrl']
    with (OUT/'HUBBLE-IV-REPORT.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for r in rows: w.writerow({k:(';'.join(x['archiveId'] for x in r[k]) if k=='candidateReplacements' else ';'.join(r[k]) if k in ('groups','flags') else r.get(k,'')) for k in cols})
    md=['# Hubble IV — Catalog 0019 Quality Audit','',f'- Catalog records: **{len(rows)}**',f'- Flagged records: **{len(bad)}**',f"- Flagged records with same-object replacement candidates: **{summary['recordsWithReplacementCandidates']}**",'','## Category counts','']+[f'- {k}: **{v}**' for k,v in sorted(gc.items())]+['','## Flagged records','','| # | ID | Name | Categories | Flags | Candidates |','|---:|---|---|---|---|---|']
    for r in bad: md.append(f"| {r['index']} | {r['archiveId']} | {r['name'].replace('|','/')} | {', '.join(r['groups'])} | {', '.join(r['flags'])} | {', '.join(x['archiveId'] for x in r['candidateReplacements']) or '—'} |")
    md+=['','## Method','', '- Active link checks target `selectedImageUrl`, not fallback candidates.', '- Visual flags use a lower-resolution rendition of the same selected ESA asset where possible.', '- Replacement candidates, when available, are other healthy Hubble Catalog 0019 records matching identity or sky position.', '- FOV/orientation flags identify records requiring review; they do not silently rewrite values.','']
    (OUT/'HUBBLE-IV-REPORT.md').write_text('\n'.join(md),encoding='utf-8')
    html_rows=''.join(f"<tr><td>{r['index']}</td><td>{r['archiveId']}</td><td>{r['name']}</td><td>{', '.join(r['groups'])}</td><td>{', '.join(r['flags'])}</td><td><a href='{r['selectedImageUrl']}'>active</a></td><td><a href='{r['previewUrl']}'>preview</a></td><td><a href='{r['sourceUrl']}'>source</a></td></tr>" for r in bad)
    html=f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Hubble IV Audit</title><style>body{{font-family:system-ui;background:#07111d;color:#eef7ff;margin:18px}}a{{color:#7cc9ff}}table{{border-collapse:collapse;width:100%;font-size:12px}}td,th{{padding:6px;border-bottom:1px solid #29445d;text-align:left}}</style><h1>Hubble IV — Catalog 0019 Audit</h1><p>Records {len(rows)} · Flagged {len(bad)}</p><table><tr><th>#</th><th>ID</th><th>Name</th><th>Categories</th><th>Flags</th><th>Active</th><th>Preview</th><th>Source</th></tr>{html_rows}</table>"
    (OUT/'HUBBLE-IV-REPORT.html').write_text(html,encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
