from IPython.display import HTML, Javascript, display

# GV-beta-0010AE4
# Surgical diagnostic wrapper derived from the exact current AE3 runtime behavior.
# Authorized change only: visible HD + ALDN preload status instrumentation.

display(HTML("""
<div id="gv-ae4-bootstrap" style="position:fixed;inset:0;background:#000;z-index:2147483647"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const AE3_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0010AE3.py';

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

    const response=await fetch(AE3_URL+'?t='+Date.now(),{cache:'no-store'});
    if(!response.ok)throw new Error('AE4 BASELINE FETCH FAILED HTTP '+response.status);
    let source=await response.text();
    source=source.replaceAll('10AE3','10AE4');

    const htmlMatch=source.match(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/);
    const jsMatches=[...source.matchAll(/display\(Javascript\(r?\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(!htmlMatch||!jsMatches.length)throw new Error('AE4 BASELINE EXTRACTION FAILED');

    document.getElementById('gv-ae4-bootstrap')?.remove();
    mountHtml(htmlMatch[1]);
    for(const match of jsMatches){
        const script=document.createElement('script');
        script.textContent=match[1];
        document.body.appendChild(script);
    }

    function installDiagnostics(){
        if(document.getElementById('gv-ae4-preload-diagnostics'))return;
        const root=document.getElementById('aladin-cosmic-command-test');
        if(!root||!window.GV10E)return;

        const style=document.createElement('style');
        style.textContent=`
#gv-ae4-preload-diagnostics{position:absolute;right:8px;bottom:64px;z-index:7600;display:flex;align-items:flex-end;gap:6px;pointer-events:none;font-family:monospace;color:#DFFFEA;text-shadow:0 0 3px #000}
#gv-ae4-hd-panel,#gv-ae4-aldn-panel{box-sizing:border-box;border:1px solid rgba(120,255,171,.72);border-radius:5px;background:rgba(0,10,7,.80);box-shadow:0 0 7px rgba(87,255,147,.18)}
#gv-ae4-hd-panel{width:178px;padding:4px 5px 5px}
#gv-ae4-aldn-panel{width:76px;padding:4px 5px 5px}
.gv-ae4-title{height:11px;margin-bottom:3px;color:#78FFAB;font:700 8px/11px monospace;letter-spacing:.8px;text-align:center}
.gv-ae4-row{display:grid;grid-template-columns:12px 1fr 52px;align-items:center;gap:3px;height:12px;margin:1px 0;font:7px/10px monospace;white-space:nowrap}
.gv-ae4-num{color:#B7FFD0;text-align:right}.gv-ae4-state{overflow:hidden;text-overflow:ellipsis}.gv-ae4-track{position:relative;height:4px;border:1px solid rgba(120,255,171,.38);border-radius:3px;background:rgba(8,30,18,.76);overflow:hidden}.gv-ae4-fill{height:100%;width:0%;background:linear-gradient(90deg,#1C7D47,#78FFAB);transition:width .18s linear}.gv-ae4-row.gv-fail .gv-ae4-fill{background:linear-gradient(90deg,#8E1E1E,#FF6363)}.gv-ae4-row.gv-ready .gv-ae4-state{color:#9CFFBB}.gv-ae4-row.gv-fail .gv-ae4-state{color:#FF8D8D}
#gv-ae4-aldn-label{height:22px;overflow:hidden;text-overflow:ellipsis;font:7px/10px monospace;text-align:center;color:#CFFFE0;white-space:normal}#gv-ae4-aldn-state{margin-top:3px;font:7px/9px monospace;text-align:center;color:#9CFFBB}#gv-ae4-aldn-track{height:6px;margin-top:3px;border:1px solid rgba(120,255,171,.38);border-radius:3px;background:rgba(8,30,18,.76);overflow:hidden}#gv-ae4-aldn-fill{height:100%;width:0%;background:linear-gradient(90deg,#1C7D47,#78FFAB);transition:width .18s linear}
`;
        document.head.appendChild(style);

        const panel=document.createElement('div');
        panel.id='gv-ae4-preload-diagnostics';
        const hd=document.createElement('div');
        hd.id='gv-ae4-hd-panel';
        hd.innerHTML='<div class="gv-ae4-title">HD</div>';
        for(let i=1;i<=10;i++){
            const row=document.createElement('div');
            row.className='gv-ae4-row';
            row.dataset.slot=String(i);
            row.innerHTML=`<span class="gv-ae4-num">${i}</span><span class="gv-ae4-state">WAIT</span><span class="gv-ae4-track"><span class="gv-ae4-fill"></span></span>`;
            hd.appendChild(row);
        }
        const aldn=document.createElement('div');
        aldn.id='gv-ae4-aldn-panel';
        aldn.innerHTML='<div class="gv-ae4-title">ALDN</div><div id="gv-ae4-aldn-label">WAIT</div><div id="gv-ae4-aldn-track"><div id="gv-ae4-aldn-fill"></div></div><div id="gv-ae4-aldn-state">0/10</div>';
        panel.append(hd,aldn);
        root.appendChild(panel);

        const stagePercent=state=>{
            const s=String(state||'').toUpperCase();
            if(s==='READY')return 100;
            if(s==='DECODING')return 82;
            if(s==='DOWNLOADING')return 48;
            if(s==='QUEUED')return 14;
            if(s==='SUSPENDED')return 24;
            if(s==='RETRY-WAIT')return 100;
            return 4;
        };
        const stageLabel=item=>{
            const s=String(item?.state||'WAIT').toUpperCase();
            const name=String(item?.name||'').trim();
            const short=name.length>12?name.slice(0,11)+'…':name;
            if(s==='READY')return '✓ '+short;
            if(s==='RETRY-WAIT')return 'FAIL '+short;
            return (s||'WAIT')+(short?' '+short:'');
        };

        const render=()=>{
            const api=window.GV10E;
            if(!api)return;
            let downloads=[];
            try{downloads=[...(api.getHubbleDownloadStatus?.()||[])]}catch(_){}
            downloads.sort((a,b)=>Number(b.updatedAt||0)-Number(a.updatedAt||0));
            const live=downloads.filter(item=>['QUEUED','DOWNLOADING','DECODING','READY','RETRY-WAIT','SUSPENDED'].includes(String(item?.state||'').toUpperCase())).slice(0,10);
            const rows=[...hd.querySelectorAll('.gv-ae4-row')];
            rows.forEach((row,index)=>{
                const item=live[index]||null;
                const state=String(item?.state||'WAIT').toUpperCase();
                row.classList.toggle('gv-ready',state==='READY');
                row.classList.toggle('gv-fail',state==='RETRY-WAIT');
                row.querySelector('.gv-ae4-state').textContent=item?stageLabel(item):'WAIT';
                row.querySelector('.gv-ae4-fill').style.width=(item?stagePercent(state):0)+'%';
            });

            let a={targetReady:10,cachedCount:0,activeKey:'',queuedDestinations:[]};
            try{a=api.getAladinPrewarmState?.()||a}catch(_){}
            const target=Math.max(1,Number(a.targetReady)||10);
            const cached=Math.max(0,Number(a.cachedCount)||0);
            const pct=Math.max(0,Math.min(100,cached/target*100));
            const label=document.getElementById('gv-ae4-aldn-label');
            const fill=document.getElementById('gv-ae4-aldn-fill');
            const state=document.getElementById('gv-ae4-aldn-state');
            if(label)label.textContent=a.activeKey?'PRELOAD '+String(a.activeKey).slice(0,12):cached>=target?'✓ READY':'CACHE';
            if(fill)fill.style.width=pct+'%';
            if(state)state.textContent=`${Math.min(cached,target)}/${target}`;
        };
        render();
        const timer=setInterval(render,200);
        window.addEventListener('beforeunload',()=>clearInterval(timer),{once:true});
    }

    let attempts=0;
    const wait=setInterval(()=>{
        attempts++;
        if(window.GV10E){clearInterval(wait);installDiagnostics();return}
        if(attempts>300){clearInterval(wait);console.error('GV-10AE4 DIAGNOSTICS COULD NOT FIND GV10E')}
    },100);
})().catch(error=>{
    console.error('GALAXY VIEWER 10AE4 BOOTSTRAP FAILURE:',error);
    const box=document.getElementById('gv-ae4-bootstrap')||document.body.appendChild(document.createElement('div'));
    box.id='gv-ae4-bootstrap';
    Object.assign(box.style,{position:'fixed',inset:'0',zIndex:2147483647,padding:'24px',boxSizing:'border-box',background:'#000',color:'#FFD166',whiteSpace:'pre-wrap',font:'14px/1.45 monospace'});
    box.textContent='GALAXY VIEWER 10AE4 FAILED TO LOAD\n\n'+String(error?.stack||error);
});
"""))

# GV-beta-0010AE4 staged
