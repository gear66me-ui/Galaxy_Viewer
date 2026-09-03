#!/usr/bin/env python3
import json, math, os, shutil, subprocess, time
from pathlib import Path

import cv2
import numpy as np
import requests
import sep
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / 'test/astrometry-pairs/generated/PAIR-0001-heic2018b'
OUT = ROOT / 'test/astrometry-source-diagnostic/generated/NGC2525'
OUT.mkdir(parents=True, exist_ok=True)

PROVIDER_URL = 'https://cdn.esahubble.org/archives/images/large/heic2018b.jpg'
RA = 121.4072916667
DEC = -11.4265944444
CATALOG_FOV = 0.043167
MAX_STARS = 50


def get_provider():
    local = PAIR / '01_PROVIDER.jpg'
    dst = OUT / '01_PROVIDER.jpg'
    if local.exists():
        shutil.copy2(local, dst)
    else:
        r = requests.get(PROVIDER_URL, timeout=90, headers={'User-Agent':'GalaxyViewer/astrometry-source-diagnostic'})
        r.raise_for_status(); dst.write_bytes(r.content)
    im = cv2.imread(str(dst), cv2.IMREAD_COLOR)
    if im is None: raise RuntimeError('provider image decode failed')
    return im


def gray_float(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    p1, p99 = np.percentile(g, [1,99.8])
    g = np.clip((g-p1)/(max(1e-6,p99-p1)), 0, 1)
    return np.ascontiguousarray(g.astype(np.float32))


def exclusion_mask(h,w):
    yy,xx=np.mgrid[:h,:w]
    cx=(w-1)/2; cy=(h-1)/2
    rx=0.27*w; ry=0.27*h
    central=((xx-cx)/rx)**2+((yy-cy)/ry)**2 <= 1.0
    edge=(xx<0.025*w)|(xx>0.975*w)|(yy<0.025*h)|(yy>0.975*h)
    return central|edge


def uniformize(rows,w,h,maxn=MAX_STARS):
    if not rows: return []
    rows=sorted(rows,key=lambda r:r['rank'],reverse=True)
    chosen=[]; cells={}; gx=5; gy=5
    for r in rows:
        cell=(min(gx-1,int(r['x']/w*gx)), min(gy-1,int(r['y']/h*gy)))
        if cells.get(cell,0)>=3: continue
        chosen.append(r); cells[cell]=cells.get(cell,0)+1
        if len(chosen)>=maxn: break
    return chosen


def sep_sources(g,mask):
    bkg=sep.Background(g, mask=mask.astype(np.uint8))
    data=np.ascontiguousarray(g-bkg.back(), dtype=np.float32)
    objs=sep.extract(data, 4.0, err=bkg.globalrms, mask=mask.astype(np.uint8), minarea=7,
                     deblend_nthresh=32, deblend_cont=0.005, clean=True)
    h,w=g.shape; rows=[]
    for o in objs:
        x=float(o['x']); y=float(o['y']); a=float(o['a']); b=float(o['b'])
        flux=float(o['flux']); peak=float(o['peak']); npix=int(o['npix'])
        if not all(map(math.isfinite,[x,y,a,b,flux,peak])) or flux<=0 or b<=0: continue
        ell=1.0-b/max(a,1e-6)
        if a<1.0 or a>35 or b<0.8 or ell>0.62 or npix<7 or npix>1800: continue
        if mask[int(np.clip(round(y),0,h-1)),int(np.clip(round(x),0,w-1))]: continue
        compact=1.0/(1.0+2.2*ell+0.015*npix)
        rows.append({'x':x,'y':y,'flux':flux,'a':a,'b':b,'ellipticity':ell,'npix':npix,'peak':peak,'rank':flux*compact})
    return uniformize(rows,w,h)


def dao_sources(g,mask):
    arr=g.copy(); arr[mask]=np.nan
    _,med,std=sigma_clipped_stats(arr, sigma=3.0, maxiters=5)
    finder=DAOStarFinder(fwhm=5.0, threshold=5.0*std, sharplo=0.05, sharphi=1.5, roundlo=-1.0, roundhi=1.0)
    tbl=finder(np.nan_to_num(g-med, nan=0.0))
    h,w=g.shape; rows=[]
    if tbl is None: return []
    names=list(getattr(tbl,'colnames',[]) or [])
    xkey=next((k for k in ('xcentroid','x_centroid','x','xcen') if k in names),None)
    ykey=next((k for k in ('ycentroid','y_centroid','y','ycen') if k in names),None)
    fkey=next((k for k in ('flux','peak','flux_fit') if k in names),None)
    if not xkey or not ykey:
        print('DAO SKIPPED — unsupported Photutils columns:', names)
        return []
    for row in tbl:
        try:
            x=float(row[xkey]); y=float(row[ykey]); flux=float(row[fkey]) if fkey else 1.0
        except Exception:
            continue
        if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(flux)): continue
        if mask[int(np.clip(round(y),0,h-1)),int(np.clip(round(x),0,w-1))]: continue
        rows.append({'x':x,'y':y,'flux':flux,'rank':flux})
    return uniformize(rows,w,h)


def image2xy_sources(provider_path,w,h):
    exe=shutil.which('image2xy')
    if not exe: return [], 'image2xy not installed'
    xyls=OUT/'image2xy.xyls'
    cmd=[exe,'-O','-o',str(xyls),str(provider_path)]
    try:
        p=subprocess.run(cmd, capture_output=True, text=False, timeout=120)
        if p.returncode!=0:
            raw=(p.stderr or p.stdout or b'')[-4000:]
            return [], raw.decode('utf-8','replace')
        with fits.open(xyls) as hdul:
            tab=hdul[1].data
            names=[n.upper() for n in tab.names]
            xn=tab.names[names.index('X')] if 'X' in names else tab.names[0]
            yn=tab.names[names.index('Y')] if 'Y' in names else tab.names[1]
            fn=None
            for candidate in ('FLUX','BACKGROUND','MAG'):
                if candidate in names: fn=tab.names[names.index(candidate)]; break
            rows=[]
            for i in range(min(len(tab),500)):
                x=float(tab[xn][i])-1.0; y=float(tab[yn][i])-1.0
                if not (0<=x<w and 0<=y<h): continue
                flux=float(tab[fn][i]) if fn else float(len(tab)-i)
                if not math.isfinite(flux): flux=float(len(tab)-i)
                rows.append({'x':x,'y':y,'flux':flux,'rank':flux})
            return uniformize(rows,w,h), None
    except Exception as e:
        return [], f'{type(e).__name__}: {e}'


def draw(im,rows,label,out):
    canvas=im.copy(); h,w=canvas.shape[:2]
    scale=max(0.6,min(1.2,w/3600))
    for i,r in enumerate(rows,1):
        x=int(round(r['x'])); y=int(round(r['y']))
        rad=max(10,int(min(h,w)*0.004))
        cv2.circle(canvas,(x,y),rad,(0,255,0),max(2,int(scale*2)))
        cv2.putText(canvas,str(i),(x+rad+2,y),cv2.FONT_HERSHEY_SIMPLEX,0.55*scale,(0,255,255),max(1,int(scale*2)),cv2.LINE_AA)
    cv2.rectangle(canvas,(0,0),(w-1,max(50,int(0.045*h))),(0,0,0),-1)
    cv2.putText(canvas,f'{label}: {len(rows)} selected compact sources',(14,max(34,int(0.032*h))),cv2.FONT_HERSHEY_SIMPLEX,0.9*scale,(255,255,255),max(2,int(scale*2)),cv2.LINE_AA)
    cv2.imwrite(str(out),canvas,[cv2.IMWRITE_JPEG_QUALITY,90])


def write_csv(rows,path):
    keys=['rank','x','y','flux','a','b','ellipticity','npix','peak']
    with open(path,'w',encoding='utf-8') as f:
        f.write(','.join(keys)+'\n')
        for r in rows:
            f.write(','.join(str(r.get(k,'')) for k in keys)+'\n')


def write_xyls(rows,w,h,path,flip_y=False):
    x=np.array([r['x']+1.0 for r in rows],dtype=np.float64)
    if flip_y:
        y=np.array([h-r['y'] for r in rows],dtype=np.float64)
    else:
        y=np.array([r['y']+1.0 for r in rows],dtype=np.float64)
    flux=np.array([r['flux'] for r in rows],dtype=np.float64)
    order=np.argsort(-flux); x=x[order]; y=y[order]; flux=flux[order]
    cols=[fits.Column(name='X',format='D',array=x),fits.Column(name='Y',format='D',array=y),fits.Column(name='FLUX',format='D',array=flux)]
    hdu=fits.BinTableHDU.from_columns(cols); hdu.header['IMAGEW']=w; hdu.header['IMAGEH']=h
    fits.HDUList([fits.PrimaryHDU(),hdu]).writeto(path,overwrite=True)


def api_post(url,payload,files=None):
    data={'request-json':json.dumps(payload)}
    r=requests.post(url,data=data,files=files,timeout=90); r.raise_for_status()
    try: return r.json()
    except Exception: raise RuntimeError(f'non-json response: {r.text[:500]}')


def solve_astrometry(xyls,w,h,label):
    key=os.environ.get('ASTROMETRY_API_KEY','').strip()
    if not key: return {'status':'NO_API_KEY'}
    login=api_post('https://nova.astrometry.net/api/login',{'apikey':key})
    if login.get('status')!='success': return {'status':'LOGIN_FAIL','login':login}
    req={
      'session':login['session'],'publicly_visible':'n','allow_modifications':'d','allow_commercial_use':'d',
      'scale_units':'degwidth','scale_type':'ul','scale_lower':CATALOG_FOV*0.65,'scale_upper':CATALOG_FOV*1.45,
      'center_ra':RA,'center_dec':DEC,'radius':0.12,'image_width':w,'image_height':h,
      'positional_error':2.0,'tweak_order':2,'crpix_center':True
    }
    with open(xyls,'rb') as fh:
        sub=api_post('https://nova.astrometry.net/api/upload',req,files={'file':(f'ngc2525_{label}.xyls',fh,'application/octet-stream')})
    result={'status':'SUBMITTED','submission':sub,'request':{k:v for k,v in req.items() if k!='session'}}
    subid=sub.get('subid')
    if not subid: return result|{'status':'SUBMIT_FAIL'}
    job=None; deadline=time.time()+240
    while time.time()<deadline:
        s=requests.get(f'https://nova.astrometry.net/api/submissions/{subid}',timeout=30).json()
        jobs=[j for j in (s.get('jobs') or []) if j]
        if jobs: job=jobs[0]; break
        time.sleep(4)
    if not job: return result|{'status':'TIMEOUT_WAITING_JOB'}
    result['job_id']=job
    while time.time()<deadline:
        j=requests.get(f'https://nova.astrometry.net/api/jobs/{job}',timeout=30).json()
        if j.get('status') in ('success','failure'):
            result['job_status']=j; break
        time.sleep(4)
    if result.get('job_status',{}).get('status')!='success': return result|{'status':'SOLVE_FAIL'}
    cal=requests.get(f'https://nova.astrometry.net/api/jobs/{job}/calibration/',timeout=30).json()
    result.update({'status':'SOLVED','calibration':cal})
    return result


def make_html(matrix,counts):
    solved=[(k,v) for k,v in matrix.items() if v.get('status')=='SOLVED']
    winner=solved[0][1] if solved else {}
    cal=winner.get('calibration') or {}
    ra=cal.get('ra',RA); dec=cal.get('dec',DEC); orient=cal.get('orientation',0)
    radius=cal.get('radius',CATALOG_FOV/2); fov=max(CATALOG_FOV,2*float(radius or CATALOG_FOV/2))
    rows=''.join(f'<tr><td>{k}</td><td>{v.get("status")}</td><td>{v.get("job_id","")}</td></tr>' for k,v in matrix.items())
    html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NGC 2525 Five-Way Solve Matrix</title>
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.min.css"><script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"></script>
<style>body{{margin:0;background:#07101b;color:#eef;font-family:system-ui}}main{{padding:10px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}img{{width:100%;background:#000}}#aladin{{height:65vh}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #456;padding:6px}}.card{{background:#101b29;border:1px solid #345;border-radius:10px;padding:10px;margin:8px 0}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><main>
<h2>ASTROMETRY SOURCE DIAGNOSTIC — NGC 2525 FIVE-WAY MATRIX</h2><div class="card">SEP {counts['sep']} · DAO {counts['dao']} · image2xy {counts['image2xy']}<table><tr><th>Variant</th><th>Status</th><th>Job</th></tr>{rows}</table></div>
<div class="grid"><div><h3>SEP</h3><img src="02_SEP_SELECTED.jpg"></div><div><h3>DAOStarFinder</h3><img src="03_DAO_SELECTED.jpg"></div><div><h3>Astrometry image2xy</h3><img src="04_IMAGE2XY_SELECTED.jpg"></div><div><h3>Live Aladin at first solved variant</h3><div id="aladin"></div></div></div>
<script>A.init.then(()=>{{const a=A.aladin('#aladin',{{survey:'P/DSS2/color',target:'{ra} {dec}',fov:{fov},cooFrame:'ICRSd',showReticle:true,showCooGridControl:true,showLayersControl:true}}); if(typeof a.setRotation==='function') a.setRotation({orient});}});</script></main></body></html>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')


def main():
    t0=time.time(); im=get_provider(); h,w=im.shape[:2]; g=gray_float(im); mask=exclusion_mask(h,w)
    sep_rows=sep_sources(g,mask); dao_rows=dao_sources(g,mask); img_rows,img_err=image2xy_sources(OUT/'01_PROVIDER.jpg',w,h)
    draw(im,sep_rows,'SEP FILTERED',OUT/'02_SEP_SELECTED.jpg'); draw(im,dao_rows,'DAOStarFinder',OUT/'03_DAO_SELECTED.jpg'); draw(im,img_rows,'ASTROMETRY image2xy',OUT/'04_IMAGE2XY_SELECTED.jpg')
    write_csv(sep_rows,OUT/'sep_sources.csv'); write_csv(dao_rows,OUT/'dao_sources.csv'); write_csv(img_rows,OUT/'image2xy_sources.csv')

    variants={
      'sep_native':(sep_rows,False),
      'sep_yflip':(sep_rows,True),
      'dao_native':(dao_rows,False),
      'dao_yflip':(dao_rows,True),
      'image2xy_native':(img_rows,False),
    }
    matrix={}
    for label,(rows,flip_y) in variants.items():
        if len(rows)<4:
            matrix[label]={'status':'SKIPPED_TOO_FEW_SOURCES','count':len(rows)}
            continue
        xyls=OUT/f'{label}.xyls'; write_xyls(rows,w,h,xyls,flip_y=flip_y)
        print(f'=== SOLVING {label} ({len(rows)} sources, flip_y={flip_y}) ===', flush=True)
        matrix[label]=solve_astrometry(xyls,w,h,label)
        (OUT/f'{label}_result.json').write_text(json.dumps(matrix[label],indent=2),encoding='utf-8')

    payload={'schema':'gv-ngc2525-source-diagnostic-0002','elapsed_s':round(time.time()-t0,2),'image':{'width':w,'height':h},'catalog_hint':{'ra':RA,'dec':DEC,'fov_deg':CATALOG_FOV},'counts':{'sep':len(sep_rows),'dao':len(dao_rows),'image2xy':len(img_rows)},'image2xy_error':img_err,'solve_matrix':matrix}
    (OUT/'result.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    make_html(matrix,payload['counts'])
    print(json.dumps(payload,indent=2))

if __name__=='__main__': main()
