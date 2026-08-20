from IPython.display import HTML, Javascript, display

# GV-beta-0010AE3
# Surgical runtime wrapper pinned to the verified AE2 source commit.
# Authorized changes only: corrected Chandra catalog path + Chandra-first test queue + AE3 version labels.

display(HTML("""
<div id="gv-ae3-bootstrap" style="position:fixed;inset:0;background:#000;z-index:2147483647"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const AE2_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/8476dc286c55cb2a75801e1858292587c9146f29/viewer/GV-beta-0010AE2.py';
    const CHANDRA_OLD='viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001.json';
    const CHANDRA_NEW='viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001-FOV-updated.json';
    const OVERRIDE_OLD='chandraTestTotal=chandraTestQueue.length;\n        chandraTestOverrideActive=false;';
    const OVERRIDE_NEW='chandraTestTotal=chandraTestQueue.length;\n        chandraTestOverrideActive=chandraTestTotal>0;';

    function mountHtml(html){
        const template=document.createElement('template');
        template.innerHTML=html;
        for(const node of [...template.content.childNodes]){
            if(node.nodeName==='SCRIPT'){
                const script=document.createElement('script');
                for(const attr of [...node.attributes])script.setAttribute(attr.name,attr.value);
                script.textContent=node.textContent;
                document.body.appendChild(script);
            }else{
                document.body.appendChild(node);
            }
        }
    }

    const response=await fetch(AE2_URL+'?t='+Date.now(),{cache:'no-store'});
    if(!response.ok)throw new Error('AE3 BASELINE FETCH FAILED HTTP '+response.status);
    let source=await response.text();

    if(!source.includes(CHANDRA_OLD))throw new Error('AE3 CHANDRA CATALOG PATCH ANCHOR MISSING');
    if(!source.includes(OVERRIDE_OLD))throw new Error('AE3 CHANDRA-FIRST PATCH ANCHOR MISSING');

    source=source.replace(CHANDRA_OLD,CHANDRA_NEW);
    source=source.replace(OVERRIDE_OLD,OVERRIDE_NEW);
    source=source.replaceAll('10AE2','10AE3');

    const htmlMatch=source.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/);
    const jsMatches=[...source.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(!htmlMatch||!jsMatches.length)throw new Error('AE3 BASELINE EXTRACTION FAILED');

    document.getElementById('gv-ae3-bootstrap')?.remove();
    mountHtml(htmlMatch[1]);
    for(const match of jsMatches){
        const script=document.createElement('script');
        script.textContent=match[1];
        document.body.appendChild(script);
    }
})().catch(error=>{
    console.error('GALAXY VIEWER 10AE3 BOOTSTRAP FAILURE:',error);
    const box=document.getElementById('gv-ae3-bootstrap')||document.body.appendChild(document.createElement('div'));
    box.id='gv-ae3-bootstrap';
    Object.assign(box.style,{position:'fixed',inset:'0',zIndex:'2147483647',padding:'24px',boxSizing:'border-box',background:'#000',color:'#FFD166',whiteSpace:'pre-wrap',font:'14px/1.45 monospace'});
    box.textContent='GALAXY VIEWER 10AE3 FAILED TO LOAD\n\n'+String(error?.stack||error);
});
"""))

# GV-beta-0010AE3 staged
