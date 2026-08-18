from IPython.display import Javascript, display
from urllib.request import urlopen

# GV-beta-0010J — surgical HD archive + Galaxy Info repair.
# Derived directly from frozen 10H runtime while carrying forward only the authorized
# 10I controls: DOWNLOAD IMAGE remains removed; BACK TO VIEWER remains inside Galaxy Info.
# 10J restores the approved third-screenshot/10F archive-icon silhouette, adds a true
# lower-right text aperture, extends Galaxy Info downward, and opens each catalog record's
# exact sourceUrl directly in Android/browser context so iframe restrictions cannot block it.

_BASE='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0010H.py'
exec(compile(urlopen(_BASE).read().decode('utf-8'), _BASE, 'exec'), globals(), globals())

display(Javascript(r"""
(()=>{
    'use strict';
    const VERSION='10J';
    const TARGET_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/icon_target_vector.svg';

    const currentDestination=rg=>rg?.getState?.().activeDestination||rg?.activeDestination||null;
    const providerFor=destination=>destination?.provider==='JWST'?'JWST':'HUBBLE';

    function galaxyInfoText(destination){
        if(!destination)return '';
        const provider=providerFor(destination);
        const telescope=provider==='JWST'?'JAMES WEBB SPACE TELESCOPE':'HUBBLE SPACE TELESCOPE';
        const identity=String(destination.commonName||destination.designation||destination.name||'THIS GALAXY').trim().toUpperCase();
        const parts=[`${identity} — ${telescope} IMAGERY.`];
        if(destination.constellation)parts.push(`CONSTELLATION ${String(destination.constellation).trim().toUpperCase()}.`);
        const distance=Number(destination.distance);
        if(Number.isFinite(distance)&&distance>0)parts.push(`DISTANCE ${distance>=1000?(distance/1000).toFixed(2)+' BILLION':distance.toFixed(distance>=100?0:1)+' MILLION'} LIGHT-YEARS.`);
        if(destination.age)parts.push(`AGE ${String(destination.age).trim().toUpperCase()}.`);
        if(destination.imageType)parts.push(`${String(destination.imageType).trim().toUpperCase()} IMAGE.`);
        return parts.join(' ');
    }

    const apply=()=>{
        const rg=window.__gv10eRandomGalaxy;
        if(!rg)return false;

        // Visible revision identity only; no runtime architecture changes.
        const versionLabel=document.getElementById('gv-version-label');
        if(versionLabel){versionLabel.textContent='VERSION 10J';versionLabel.setAttribute('aria-label','GALAXY VIEWER VERSION 10J')}
        document.querySelectorAll('.gv-10e-version').forEach(el=>{el.textContent='VERSION 10J'});

        // DOWNLOAD IMAGE remains completely absent.
        if(rg.downloadButton){
            try{if(rg._downloadClick)rg.downloadButton.removeEventListener('click',rg._downloadClick)}catch(_){}
            try{rg.downloadButton.remove()}catch(_){}
            rg.downloadButton=null;
        }

        const infoPanel=document.getElementById('gv-hd-info-panel');
        const infoBody=document.getElementById('gv-hd-info-body');
        const backButton=rg.backButton;
        const archiveButton=document.getElementById('gv-hd-archive-button');
        const archiveIcon=archiveButton?.querySelector('img')||null;

        // BACK TO VIEWER: move the original already-bound module button, never clone it.
        if(infoPanel&&backButton){
            if(backButton.parentElement!==infoPanel)infoPanel.appendChild(backButton);
            backButton.setAttribute('aria-label','BACK TO VIEWER');
            const backLabel=backButton.lastElementChild;
            if(backLabel)backLabel.textContent='BACK TO VIEWER';
            Object.assign(infoPanel.style,{pointerEvents:'none',overflow:'hidden'});
            Object.assign(backButton.style,{
                position:'absolute',right:'12px',bottom:'12px',zIndex:'30',
                minWidth:'146px',height:'42px',margin:'0',padding:'0 14px',
                pointerEvents:'auto',touchAction:'manipulation',
                border:'2px solid #ABB3AA',borderRadius:'6px',
                background:'linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98))',
                color:'#E8FFF0',boxShadow:'none'
            });
        }

        // Approved third-screenshot source icon: green rounded frame, no orange redesign.
        if(archiveButton&&rg.hdViewport){
            if(archiveButton.parentElement!==rg.hdViewport)rg.hdViewport.appendChild(archiveButton);
            archiveButton.classList.remove('gvrg-hd-icon-button');
            Object.assign(archiveButton.style,{
                position:'absolute',right:'14px',bottom:'14px',zIndex:'40',
                width:'84px',height:'84px',margin:'0',padding:'5px',
                display:'inline-flex',alignItems:'center',justifyContent:'center',
                boxSizing:'border-box',pointerEvents:'auto',touchAction:'manipulation',
                border:'2px solid #78FFAB',borderRadius:'10px',
                background:'rgba(0,12,8,.72)',boxShadow:'none',filter:'none',overflow:'hidden'
            });
            if(archiveIcon)Object.assign(archiveIcon.style,{
                display:'block',width:'72px',height:'72px',maxWidth:'72px',maxHeight:'72px',
                objectFit:'contain',margin:'0',padding:'0',border:'0',borderRadius:'6px',boxShadow:'none'
            });
            if(!archiveButton.dataset.gv10jPointerGuard){
                archiveButton.dataset.gv10jPointerGuard='true';
                archiveButton.addEventListener('pointerdown',event=>event.stopPropagation(),true);
                archiveButton.addEventListener('pointerup',event=>event.stopPropagation(),true);
            }
            if(!archiveButton.dataset.gv10jArchiveBound){
                archiveButton.dataset.gv10jArchiveBound='true';
                archiveButton.addEventListener('click',event=>{
                    event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();
                    const destination=currentDestination(rg);
                    const sourceUrl=String(destination?.sourceUrl||'').trim();
                    if(!/^https:\/\//i.test(sourceUrl))return;
                    // Direct user-gesture navigation avoids ESA/Hubble/Webb iframe blocking.
                    const opened=window.open(sourceUrl,'_blank','noopener,noreferrer');
                    if(!opened){
                        const anchor=document.createElement('a');
                        anchor.href=sourceUrl;anchor.target='_blank';anchor.rel='noopener noreferrer';
                        document.body.appendChild(anchor);anchor.click();anchor.remove();
                    }
                },true);
            }
        }

        // Keep the embedded archive-return control styled correctly if an already-open overlay exists.
        const archiveBack=document.getElementById('gv-archive-back');
        if(archiveBack&&!archiveBack.dataset.gv10jStyled){
            archiveBack.dataset.gv10jStyled='true';
            archiveBack.innerHTML='';
            const arrow=document.createElement('span');arrow.textContent='←';arrow.setAttribute('aria-hidden','true');
            const mark=document.createElement('img');mark.src=TARGET_ICON_URL;mark.alt='';mark.setAttribute('aria-hidden','true');
            Object.assign(mark.style,{width:'23px',height:'23px',objectFit:'contain',display:'block',flex:'0 0 23px'});
            const label=document.createElement('span');label.textContent='BACK TO GALAXY VIEWER';
            archiveBack.append(arrow,mark,label);archiveBack.setAttribute('aria-label','BACK TO GALAXY VIEWER');
            Object.assign(archiveBack.style,{display:'inline-flex',alignItems:'center',justifyContent:'center',gap:'8px',height:'44px',padding:'0 16px',border:'2px solid #ABB3AA',borderRadius:'6px',background:'linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98))',color:'#E8FFF0',boxShadow:'none',touchAction:'manipulation',pointerEvents:'auto'});
        }

        function renderInfoWithAperture(){
            if(!infoPanel||!infoBody||!backButton)return;
            const destination=currentDestination(rg);if(!destination)return;
            const full=galaxyInfoText(destination);
            const words=full.split(/\s+/).filter(Boolean);
            const apertureWidth=Math.ceil(backButton.getBoundingClientRect().width)+18;
            const apertureHeight=Math.ceil(backButton.getBoundingClientRect().height)+8;
            const renderCount=count=>{
                infoBody.replaceChildren();
                const aperture=document.createElement('span');
                aperture.id='gv10j-back-aperture';
                Object.assign(aperture.style,{
                    float:'right',display:'block',width:`${apertureWidth}px`,height:`${apertureHeight}px`,
                    marginTop:`${Math.max(0,infoBody.clientHeight-apertureHeight)}px`,marginLeft:'10px',
                    pointerEvents:'none',visibility:'hidden'
                });
                infoBody.appendChild(aperture);
                infoBody.appendChild(document.createTextNode(words.slice(0,count).join(' ')+(count<words.length?' …':'')));
            };
            let lo=0,hi=words.length,best=0;
            while(lo<=hi){
                const mid=(lo+hi)>>1;renderCount(mid);
                if(infoBody.scrollHeight<=infoBody.clientHeight+1){best=mid;lo=mid+1}else hi=mid-1;
            }
            renderCount(best||words.length);
            infoBody.dataset.fittedWords=String(best||words.length);
        }

        function position10J(){
            if(!infoPanel||!rg.hdOverlay||!rg.hdViewport)return;
            const overlayRect=rg.hdOverlay.getBoundingClientRect();
            const viewportRect=rg.hdViewport.getBoundingClientRect();
            const nav=document.getElementById('gv-galaxy-nav');
            const navRect=nav?.getBoundingClientRect();
            if(!overlayRect.height||!viewportRect.height)return;
            const infoTop=Math.max(0,Math.round(viewportRect.bottom-overlayRect.top+6));
            const safeBottom=navRect?.top?Math.min(overlayRect.bottom-24,navRect.top-24):overlayRect.bottom-28;
            const targetBottom=Math.max(viewportRect.bottom+150,safeBottom);
            const infoHeight=Math.max(150,Math.floor(targetBottom-(overlayRect.top+infoTop)));
            infoPanel.style.setProperty('top',`${infoTop}px`,'important');
            infoPanel.style.setProperty('height',`${infoHeight}px`,'important');
            infoPanel.style.setProperty('max-height',`${infoHeight}px`,'important');
            infoPanel.style.setProperty('padding','9px 11px 10px','important');
            if(infoBody){
                infoBody.style.paddingRight='0';
                infoBody.style.boxSizing='border-box';
                infoBody.style.overflow='hidden';
            }
            renderInfoWithAperture();
        }

        // Re-run after every HD open/image settle without changing HD loading itself.
        if(!rg.dataset?.gv10jWrapped){
            try{
                const originalShow=rg.showHubbleHD.bind(rg);
                rg.showHubbleHD=function(){const result=originalShow();requestAnimationFrame(()=>requestAnimationFrame(position10J));return result};
            }catch(_){}
        }
        rg.viewHdButton?.addEventListener('click',()=>requestAnimationFrame(()=>requestAnimationFrame(position10J)),true);
        rg.hubbleIconButton?.addEventListener('click',()=>requestAnimationFrame(()=>requestAnimationFrame(position10J)),true);
        rg.hdImage?.addEventListener?.('load',()=>requestAnimationFrame(position10J));
        window.addEventListener('resize',()=>requestAnimationFrame(position10J));
        requestAnimationFrame(()=>requestAnimationFrame(position10J));
        return true;
    };

    if(!apply())document.addEventListener('gv-viewer-ready',apply,{once:true});
})();
"""))
