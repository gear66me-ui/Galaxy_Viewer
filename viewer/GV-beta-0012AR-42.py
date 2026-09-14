from IPython.display import HTML, Javascript, display

# GV 12AR-42 — ICRSd restoration / rotation-frame fix.
# Mobile-compatible bootstrap: generic-app.html can extract these literal
# HTML/Javascript blocks, then this loader imports AR-41 in-browser and applies
# only the ICRSd frame changes before executing it.

display(HTML("""
<div id="gv-ar42-bootstrap" style="display:none"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const BASE='../../viewer/GV-beta-0012AR-41.py';
    const response=await fetch(BASE+'?t='+Date.now(),{cache:'no-store'});
    if(!response.ok)throw new Error('AR-42 BASE LOAD FAILED HTTP '+response.status);
    let source=await response.text();

    const replaceOnce=(oldValue,newValue,label)=>{
        const count=source.split(oldValue).length-1;
        if(count!==1)throw new Error('AR-42 PATCH DRIFT '+label+' expected 1 found '+count);
        source=source.replace(oldValue,newValue);
    };

    source=source.replaceAll('12AR-41','12AR-42');
    replaceOnce("cooFrame:'galactic',","cooFrame:'ICRSd',",'ALADIN COOFRAME');
    replaceOnce("let frame='GAL',latestRa=HOME.ra,latestDec=HOME.dec;","let frame='ICRSD',latestRa=HOME.ra,latestDec=HOME.dec;",'COORDINATE DEFAULT');
    replaceOnce(
      '#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}',
      '#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:none}',
      'COORDINATE LOCK'
    );

    const oldCallback=`coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
        renderCoordinates();
    }});`;
    const newCallback=`coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(){
        frame='ICRSD';
        try{if(typeof aladin.setFrame==='function')aladin.setFrame('ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
        coordinate?.setFrame('ICRSD');
        renderCoordinates();
    }});`;
    replaceOnce(oldCallback,newCallback,'FRAME CALLBACK');

    if(source.includes("cooFrame:'galactic'"))throw new Error('AR-42 ICRSD GUARD FAILED: GALACTIC ALADIN FRAME REMAINS');
    if(source.includes("let frame='GAL'"))throw new Error('AR-42 ICRSD GUARD FAILED: GALACTIC DEFAULT REMAINS');

    const htmlMatch=source.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/);
    const jsMatches=[...source.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(!htmlMatch||!jsMatches.length)throw new Error('AR-42 BASE EXTRACTION FAILED');

    const template=document.createElement('template');
    template.innerHTML=htmlMatch[1];
    for(const node of [...template.content.childNodes]){
        if(node.nodeName==='SCRIPT'){
            const script=document.createElement('script');
            for(const attr of [...node.attributes])script.setAttribute(attr.name,attr.value);
            script.textContent=node.textContent;
            document.body.appendChild(script);
        }else document.body.appendChild(node);
    }
    for(const match of jsMatches){
        const script=document.createElement('script');
        script.textContent=match[1];
        document.body.appendChild(script);
    }
})().catch(error=>{
    console.error('GALAXY VIEWER AR-42 BOOTSTRAP FAILED',error);
    const box=document.createElement('pre');
    box.style.cssText='position:fixed;inset:0;z-index:2147483647;margin:0;padding:20px;background:#000;color:#FFD166;white-space:pre-wrap;font:14px/1.4 monospace';
    box.textContent='GALAXY VIEWER AR-42 FAILED\n\n'+String(error?.stack||error);
    document.body.appendChild(box);
});
"""))
