from IPython.display import Javascript, display
from urllib.request import urlopen

# GV-beta-0010I — surgical restoration layer over frozen 10H.
# Authorized scope: restore the 10F source-icon location/role and remove DOWNLOAD IMAGE only.

_BASE='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0010H.py'
exec(compile(urlopen(_BASE).read().decode('utf-8'), _BASE, 'exec'), globals(), globals())

display(Javascript(r"""
(()=>{
    'use strict';
    const apply=()=>{
        const rg=window.__gv10eRandomGalaxy;
        if(!rg)return false;

        // Remove the visible DOWNLOAD IMAGE control and its bound click handler.
        if(rg.downloadButton){
            try{if(rg._downloadClick)rg.downloadButton.removeEventListener('click',rg._downloadClick)}catch(_){}
            try{rg.downloadButton.remove()}catch(_){}
            rg.downloadButton=null;
        }

        // Remove the incorrectly added HD-footer source icon. 10F's source icon lives
        // in the arrival card as rg.hubbleIconButton; leave that geometry untouched.
        const wrongHdArchiveButton=document.getElementById('gv-hd-archive-button');
        if(wrongHdArchiveButton)wrongHdArchiveButton.remove();

        const sourceButton=rg.hubbleIconButton;
        if(sourceButton&&!sourceButton.dataset.gv10iSourceBound){
            // 10F position/dimensions/classes are preserved. Only its action is changed
            // from the redundant HD-open shortcut to the originating archive page.
            try{if(rg._hdClick)sourceButton.removeEventListener('click',rg._hdClick)}catch(_){}
            sourceButton.dataset.gv10iSourceBound='true';
            sourceButton.addEventListener('click',event=>{
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                const destination=rg.getState?.().activeDestination||rg.activeDestination||null;
                const sourceUrl=String(destination?.sourceUrl||'').trim();
                if(!sourceUrl)return;
                const frame=document.getElementById('gv-archive-frame');
                const overlay=document.getElementById('gv-archive-overlay');
                if(frame&&overlay){frame.src=sourceUrl;overlay.classList.add('gv-open')}
                else window.open(sourceUrl,'_blank','noopener,noreferrer');
            },true);
        }

        return true;
    };

    if(!apply())document.addEventListener('gv-viewer-ready',apply,{once:true});
})();
"""))
