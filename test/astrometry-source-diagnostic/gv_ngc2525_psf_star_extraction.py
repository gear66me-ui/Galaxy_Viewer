#!/usr/bin/env python3
import json, math, shutil
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / 'test/astrometry-pairs/generated/PAIR-0001-heic2018b'
OUT = ROOT / 'test/astrometry-source-diagnostic/generated/NGC2525-psf'
OUT.mkdir(parents=True, exist_ok=True)

SIGMAS = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
MAX_STARS = 25
MIN_SEPARATION_PX = 95


def load_image():
    src = PAIR / '01_PROVIDER.jpg'
    if not src.exists():
        raise FileNotFoundError(src)
    dst = OUT / '01_PROVIDER.jpg'
    shutil.copy2(src, dst)
    im = cv2.imread(str(dst), cv2.IMREAD_COLOR)
    if im is None:
        raise RuntimeError('provider decode failed')
    return im


def gray01(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    p1, p999 = np.percentile(g, [1, 99.9])
    return np.ascontiguousarray(np.clip((g-p1)/max(1e-6,p999-p1), 0, 1), dtype=np.float32)


def mask_regions(h, w):
    yy, xx = np.mgrid[:h, :w]
    cx=(w-1)/2; cy=(h-1)/2
    # Exclude the bright galaxy body and the very outer edge only.
    central=((xx-cx)/(0.20*w))**2 + ((yy-cy)/(0.20*h))**2 <= 1.0
    edge=(xx<0.025*w)|(xx>0.975*w)|(yy<0.025*h)|(yy>0.975*h)
    return central | edge


def robust_threshold(response, valid):
    v=response[valid]
    if v.size == 0:
        return float('inf')
    med=float(np.median(v))
    mad=float(np.median(np.abs(v-med)))
    sigma=1.4826*mad
    # Strong local-contrast peaks only. Also require roughly the top 0.5%.
    return max(med + 6.0*max(sigma,1e-8), float(np.percentile(v,99.5)))


def weighted_centroid(img, x, y, radius):
    h,w=img.shape
    r=max(8,int(radius))
    x0=max(0,int(round(x))-r); x1=min(w,int(round(x))+r+1)
    y0=max(0,int(round(y))-r); y1=min(h,int(round(y))+r+1)
    patch=img[y0:y1,x0:x1].astype(np.float64)
    if patch.size == 0:
        return float(x),float(y),0.0
    bg=float(np.percentile(patch,20))
    wt=np.clip(patch-bg,0,None)
    # Suppress the outer wings so neighboring structure cannot drag the centroid.
    yy,xx=np.mgrid[y0:y1,x0:x1]
    rr2=(xx-x)**2+(yy-y)**2
    gate=np.exp(-0.5*rr2/max(4.0,(0.55*r)**2))
    wt*=gate
    s=float(wt.sum())
    if s<=0:
        return float(x),float(y),0.0
    cx=float((xx*wt).sum()/s); cy=float((yy*wt).sum()/s)
    return cx,cy,s


def psf_extract(base, mask, sigma):
    h,w=base.shape
    # Artificial defocus, followed by a much broader background estimate.
    fine=cv2.GaussianBlur(base,(0,0),sigmaX=sigma,sigmaY=sigma,borderType=cv2.BORDER_REPLICATE)
    broad_sigma=max(10.0, sigma*5.0)
    broad=cv2.GaussianBlur(base,(0,0),sigmaX=broad_sigma,sigmaY=broad_sigma,borderType=cv2.BORDER_REPLICATE)
    response=np.clip(fine-broad,0,None).astype(np.float32)
    response[mask]=0

    valid=~mask
    threshold=robust_threshold(response,valid)
    # Large local-max window prevents diffraction spikes/PSF lobes becoming multiple stars.
    k=max(31,int(round(12*sigma))|1)
    local=cv2.dilate(response,np.ones((k,k),np.uint8))
    peaks=(response>=local-1e-8)&(response>=threshold)&valid
    ys,xs=np.nonzero(peaks)
    candidates=[]
    for x,y in zip(xs,ys):
        score=float(response[y,x])
        # Refine against the deliberately blurred PSF, not the sharp source pixels.
        cx,cy,energy=weighted_centroid(fine,float(x),float(y),radius=max(14,7*sigma))
        if not (math.isfinite(cx) and math.isfinite(cy) and math.isfinite(energy)):
            continue
        # Bright, coherent defocused PSFs win. No size/npix/ellipticity rejection.
        candidates.append({'x':cx,'y':cy,'raw_x':float(x),'raw_y':float(y),
                           'response':score,'centroid_energy':energy,
                           'score':score*math.sqrt(max(energy,1e-12))})
    candidates.sort(key=lambda r:r['score'], reverse=True)

    # Global non-maximum suppression plus mild grid balance.
    chosen=[]; cells={}; gx=5; gy=5
    min2=MIN_SEPARATION_PX**2
    for r in candidates:
        if any((r['x']-q['x'])**2+(r['y']-q['y'])**2 < min2 for q in chosen):
            continue
        cell=(min(gx-1,max(0,int(r['x']/w*gx))),min(gy-1,max(0,int(r['y']/h*gy))))
        if cells.get(cell,0)>=2:
            continue
        chosen.append(r); cells[cell]=cells.get(cell,0)+1
        if len(chosen)>=MAX_STARS:
            break
    return fine,response,chosen,len(candidates),threshold


def draw(im, rows, sigma, out):
    canvas=im.copy(); h,w=canvas.shape[:2]
    for i,r in enumerate(rows,1):
        x=int(round(r['x'])); y=int(round(r['y']))
        rad=max(20,int(round(7*sigma)))
        cv2.circle(canvas,(x,y),rad,(0,255,0),3)
        cv2.drawMarker(canvas,(x,y),(0,0,255),cv2.MARKER_CROSS,16,2)
        cv2.putText(canvas,str(i),(x+rad+4,y),cv2.FONT_HERSHEY_SIMPLEX,0.72,(0,255,255),2,cv2.LINE_AA)
    cv2.rectangle(canvas,(0,0),(w-1,78),(0,0,0),-1)
    cv2.putText(canvas,f'PSF / DoG sigma={sigma:.1f}px — {len(rows)} selected',(18,50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),2,cv2.LINE_AA)
    cv2.imwrite(str(out),canvas,[cv2.IMWRITE_JPEG_QUALITY,92])


def main():
    im=load_image(); base=gray01(im); h,w=base.shape; mask=mask_regions(h,w)
    summary=[]
    for sigma in SIGMAS:
        fine,response,rows,ncand,threshold=psf_extract(base,mask,sigma)
        tag=str(sigma).replace('.','p')
        draw(im,rows,sigma,OUT/f'selected_psf_sigma_{tag}.jpg')
        cv2.imwrite(str(OUT/f'defocus_sigma_{tag}.jpg'),np.clip(fine*255,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,90])
        rmax=float(response.max()) if response.size else 0.0
        resp8=np.clip(response/max(rmax,1e-9)*255,0,255).astype(np.uint8)
        cv2.imwrite(str(OUT/f'response_sigma_{tag}.jpg'),resp8,[cv2.IMWRITE_JPEG_QUALITY,90])
        (OUT/f'sources_psf_sigma_{tag}.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
        summary.append({'sigma_px':sigma,'candidate_peaks':ncand,'selected_count':len(rows),
                        'threshold':threshold,'overlay':f'selected_psf_sigma_{tag}.jpg'})
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    cards=''.join(f'<div><h3>sigma {r["sigma_px"]:.1f}px — {r["selected_count"]} selected</h3><img src="{r["overlay"]}"></div>' for r in summary)
    html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NGC2525 PSF Star Extraction</title><style>body{{margin:0;background:#08111c;color:#eef;font-family:system-ui}}main{{padding:10px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}img{{width:100%;background:#000}}@media(max-width:850px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><main><h2>ASTROMETRY PSF STAR EXTRACTION — NGC 2525</h2><p>Artificial defocus + Difference-of-Gaussians peak detection + wide NMS + weighted PSF centroids. No astrometry solve.</p><div class="grid">{cards}</div></main></body></html>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
