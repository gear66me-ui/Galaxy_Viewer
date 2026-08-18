from IPython.display import Javascript, display
from urllib.request import urlopen

# GV-beta-0010I — surgical HD navigation/source-control repair over frozen 10H.
# Authorized scope: keep DOWNLOAD IMAGE removed; move BACK TO VIEWER into the lower
# Galaxy Info panel; restore the active Hubble/JWST archive icon to the lower-right
# corner of the HD image; preserve record-specific archive navigation; keep the
# archive-overlay BACK TO GALAXY VIEWER control and give it the GV target mark.

_BASE='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0010H.py'
exec(compile(urlopen(_BASE).read().decode('utf-8'), _BASE, 'exec'), globals(), globals())

display(Javascript(r"""
(()=>{
    'use strict';
    const TARGET_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/icon_target_vector.svg';

    const apply=()=>{
        const rg=window.__gv10eRandomGalaxy;
        if(!rg)return false;

        // DOWNLOAD IMAGE stays deleted, including its bound click handler.
        if(rg.downloadButton){
            try{if(rg._downloadClick)rg.downloadButton.removeEventListener('click',rg._downloadClick)}catch(_){}
            try{rg.downloadButton.remove()}catch(_){}
            rg.downloadButton=null;
        }

        const infoPanel=document.getElementById('gv-hd-info-panel');
        const infoBody=document.getElementById('gv-hd-info-body');
        const backButton=rg.backButton;
        if(infoPanel&&backButton){
            // The module's backToSky() is synchronous; the observed hesitation came from
            // the control living in the separate footer/pointer layer. Put the original
            // bound button directly in the visible lower panel and make it a direct hit target.
            if(backButton.parentElement!==infoPanel)infoPanel.appendChild(backButton);
            backButton.setAttribute('aria-label','BACK TO VIEWER');
            const backLabel=backButton.lastElementChild;
            if(backLabel)backLabel.textContent='BACK TO VIEWER';
            Object.assign(infoPanel.style,{position:'absolute',pointerEvents:'none'});
            if(infoBody){
                infoBody.style.paddingRight='154px';
                infoBody.style.boxSizing='border-box';
            }
            Object.assign(backButton.style,{
                position:'absolute',
                right:'12px',
                bottom:'10px',
                zIndex:'12',
                minWidth:'132px',
                height:'38px',
                margin:'0',
                padding:'0 12px',
                pointerEvents:'auto',
                touchAction:'manipulation',
                border:'2px solid #ABB3AA',
                borderRadius:'6px',
                background:'linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98))',
                color:'#E8FFF0',
                boxShadow:'none'
            });
        }

        // Restore the provider-specific source control to the HD image lower-right corner.
        // 10H already owns provider switching and the record-specific sourceUrl action.
        const archiveButton=document.getElementById('gv-hd-archive-button');
        if(archiveButton&&rg.hdViewport){
            if(archiveButton.parentElement!==rg.hdViewport)rg.hdViewport.appendChild(archiveButton);
            Object.assign(archiveButton.style,{
                position:'absolute',
                right:'12px',
                bottom:'12px',
                zIndex:'20',
                width:'46px',
                height:'40px',
                margin:'0',
                padding:'2px 4px',
                pointerEvents:'auto',
                touchAction:'manipulation'
            });
            // Prevent the HD pan gesture from swallowing a source-icon tap.
            if(!archiveButton.dataset.gv10iPointerGuard){
                archiveButton.dataset.gv10iPointerGuard='true';
                archiveButton.addEventListener('pointerdown',event=>event.stopPropagation(),true);
                archiveButton.addEventListener('pointerup',event=>event.stopPropagation(),true);
            }
        }

        // Keep the original arrival-card provider icon doing exactly what it did in 10H:
        // open the HD view. The archive/source icon is the one over the HD image.

        // Archive website overlay: retain its separate BACK TO GALAXY VIEWER control,
        // using the Galaxy Viewer green/gray button language, a left arrow and GV target mark.
        const archiveBack=document.getElementById('gv-archive-back');
        if(archiveBack){
            archiveBack.innerHTML='';
            const arrow=document.createElement('span');
            arrow.textContent='←';
            arrow.setAttribute('aria-hidden','true');
            const mark=document.createElement('img');
            mark.src=TARGET_ICON_URL;
            mark.alt='';
            mark.setAttribute('aria-hidden','true');
            Object.assign(mark.style,{width:'23px',height:'23px',objectFit:'contain',display:'block',flex:'0 0 23px'});
            const label=document.createElement('span');
            label.textContent='BACK TO GALAXY VIEWER';
            archiveBack.append(arrow,mark,label);
            archiveBack.setAttribute('aria-label','BACK TO GALAXY VIEWER');
            Object.assign(archiveBack.style,{
                display:'inline-flex',
                alignItems:'center',
                justifyContent:'center',
                gap:'8px',
                height:'44px',
                padding:'0 16px',
                border:'2px solid #ABB3AA',
                borderRadius:'6px',
                background:'linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98))',
                color:'#E8FFF0',
                boxShadow:'none',
                touchAction:'manipulation',
                pointerEvents:'auto'
            });
        }

        return true;
    };

    if(!apply())document.addEventListener('gv-viewer-ready',apply,{once:true});
})();
"""))
