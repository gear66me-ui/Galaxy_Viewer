#!/usr/bin/env python3
import json, math, shutil
from pathlib import Path

import cv2
import numpy as np
import sep

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / 'test/astrometry-pairs/generated/PAIR-0001-heic2018b'
OUT = ROOT / 'test/astrometry-source-diagnostic/generated/NGC2525-defocus'
OUT.mkdir(parents=True, exist_ok=True)

SIGMAS = [0.0, 1.0, 1.5, 2.0, 2.5, 3.0]
MAX_STARS = 30


def load_image():
    src = PAIR / '01_PROVIDER.jpg'
    if not src.exists():
        raise FileNotFoundError(src)
    dst = OUT / '01_PROVIDER.jpg'
    shutil.copy2(src, dst)
    im = cv2.imread(str(dst), cv2.IMREAD_COLOR)
    if im is None:
        raise RuntimeError('decode failed')
    return im


def gray01(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    p1, p999 = np.percentile(g, [1, 99.9])
    return np.ascontiguousarray(np.clip((g-p1)/max(1e-6,p999-p1),0,1), dtype=np.float32)


def mask_regions(h,w):
    yy,xx=np.mgrid[:h,:w]
    cx=(w-1)/2; cy=(h-1)/2
    central=((xx-cx)/(0.24*w))**2 + ((yy-cy)/(0.24*h))**2 <= 1
    edge=(xx<0.03*w)|(xx>0.97*w)|(yy<0.03*h)|(yy>0.97*h)
    return central|edge


def weighted_centroid(img,x,y,r=8):
    h,w=img.shape
    x0=max(0,int(round(x))-r); x1=min(w,int(round(x))+r+1)
    y0=max(0,int(round(y))-r); y1=min(h,int(round(y))+r+1)
    patch=img[y0:y1,x0:x1].astype(np.float64)
    if patch.size==0: return x,y
    bg=np.percentile(patch,25)
    wt=np.clip(patch-bg,0,None)
    s=wt.sum()
    if s<=0: return x,y
    yy,xx=np.mgrid[y0:y1,x0:x1]
    return float((xx*wt).sum()/s), float((yy*wt).sum()/s)


def extract(base,mask,sigma):
    if sigma>0:
        g=cv2.GaussianBlur(base,(0,0),sigmaX=sigma,sigmaY=sigma,borderType=cv2.BORDER_REPLICATE)
    else:
        g=base.copy()
    bkg=sep.Background(g,mask=mask.astype(np.uint8))
    data=np.ascontiguousarray(g-bkg.back(),dtype=np.float32)
    objs=sep.extract(data,4.5,err=bkg.globalrms,mask=mask.astype(np.uint8),minarea=8,
                     deblend_nthresh=32,deblend_cont=0.003,clean=True)
    h,w=g.shape
    candidates=[]
    for o in objs:
        x=float(o['x']); y=float(o['y']); a=float(o['a']); b=float(o['b'])
        flux=float(o['flux']); peak=float(o['peak']); npix=int(o['npix'])
        if not all(map(math.isfinite,[x,y,a,b,flux,peak])) or flux<=0 or peak<=0 or b<=0: continue
        ell=1-b/max(a,1e-6)
        # Deliberately target defocused-but-still-stellar blobs, not huge galaxy structures.
        if a<1.2 or a>7.5 or b<1.0 or ell>0.28 or npix<10 or npix>380: continue
        if mask[int(np.clip(round(y),0,h-1)),int(np.clip(round(x),0,w-1))]: continue
        cx,cy=weighted_centroid(g,x,y,r=max(6,int(round(2.5*max(a,b)))))
        circularity=max(0.0,1.0-ell)
        compact=1.0/(1.0+0.010*npix)
        # Peak/SNR dominate; integrated flux no longer rewards giant diffuse blobs.
        score=(peak**1.8)*(circularity**2.0)*compact
        candidates.append(dict(x=cx,y=cy,raw_x=x,raw_y=y,a=a,b=b,ellipticity=ell,
                               npix=npix,peak=peak,flux=flux,score=score))
    candidates.sort(key=lambda r:r['score'],reverse=True)
    # Spatial uniformization: at most 2 stars per 5x5 cell.
    chosen=[]; cells={}; gx=5; gy=5
    for r in candidates:
        cell=(min(gx-1,int(r['x']/w*gx)),min(gy-1,int(r['y']/h*gy)))
        if cells.get(cell,0)>=2: continue
        chosen.append(r); cells[cell]=cells.get(cell,0)+1
        if len(chosen)>=MAX_STARS: break
    return g,chosen,len(candidates)


def draw(im,rows,sigma,out):
    canvas=im.copy(); h,w=canvas.shape[:2]
    for i,r in enumerate(rows,1):
        x=int(round(r['x'])); y=int(round(r['y']))
        rad=max(14,int(round(3*max(r['a'],r['b']))))
        cv2.circle(canvas,(x,y),rad,(0,255,0),3)
        cv2.putText(canvas,str(i),(x+rad+3,y),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,255),2,cv2.LINE_AA)
    cv2.rectangle(canvas,(0,0),(w-1,70),(0,0,0),-1)
    cv2.putText(canvas,f'DEFOCUS sigma={sigma:.1f}px — {len(rows)} selected',(18,46),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),2,cv2.LINE_AA)
    cv2.imwrite(str(out),canvas,[cv2.IMWRITE_JPEG_QUALITY,90])


def main():
    im=load_image(); h,w=im.shape[:2]; base=gray01(im); mask=mask_regions(h,w)
    summary=[]
    for sigma in SIGMAS:
        g,rows,ncand=extract(base,mask,sigma)
        tag=str(sigma).replace('.','p')
        cv2.imwrite(str(OUT/f'blur_sigma_{tag}.jpg'),np.clip(g*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,90])
        draw(im,rows,sigma,OUT/f'selected_sigma_{tag}.jpg')
        (OUT/f'sources_sigma_{tag}.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
        summary.append({'sigma_px':sigma,'candidate_count':ncand,'selected_count':len(rows),'overlay':f'selected_sigma_{tag}.jpg'})
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    cards=''.join(f'<div><h3>sigma {r["sigma_px"]:.1f}px — {r["selected_count"]} stars</h3><img src="{r["overlay"]}"></div>' for r in summary)
    html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NGC2525 Defocus Star Extraction</title><style>body{{margin:0;background:#08111c;color:#eef;font-family:system-ui}}main{{padding:10px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}img{{width:100%;background:#000}}@media(max-width:850px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><main><h2>NGC 2525 — DEFOCUS STAR EXTRACTION</h2><p>No astrometry solve. Select the blur level whose numbered circles land on real stars most consistently.</p><div class="grid">{cards}</div></main></body></html>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
