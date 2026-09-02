from IPython.display import HTML, Javascript, display
import hashlib, re, urllib.request

# ECO-20260902-12AR02-NAV-PERFORMANCE-001
# Create-only engineering derivative of verified GV-beta-0012AR-01.py.
BASE_URL = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0012AR-01.py'
EXPECTED_BLOB = '2844f67ece7701692f64e30c7c36ed6c8d55c6a2'

source = urllib.request.urlopen(BASE_URL, timeout=30).read()
actual = hashlib.sha1((f'blob {len(source)}\0').encode() + source).hexdigest()
if actual != EXPECTED_BLOB:
    raise RuntimeError(f'12AR-02 BASELINE DRIFT expected {EXPECTED_BLOB} got {actual}')
source = source.decode('utf-8')

source = source.replace("version.textContent='VERSION 12AR-01';", "version.textContent='VERSION 12AR-02';", 1)
source = source.replace("const VERSION='12AR-01';", "const VERSION='12AR-02';", 1)
source = source.replace("const DISPLAY_VERSION='12AR-01';", "const DISPLAY_VERSION='12AR-02';", 1)

benchmark = r'''    // ==================== 12AR-02 PHASE-TIMING FLIGHT RECORDER ====================
    const navBench={active:null,lastPayload:null};
    const navBenchPanel=document.createElement('div');navBenchPanel.id='gv-nav-benchmark-12ar02';
    navBenchPanel.innerHTML=`<div class="gv-nav-phase-row"><label>OUT <input data-phase="out" type="number" min="0.5" step="0.1" value="5.1"></label><label>MOVE <input data-phase="move" type="number" min="0.5" step="0.1" value="6.8"></label><label>IN <input data-phase="in" type="number" min="0.5" step="0.1" value="5.1"></label><button data-action="run">RUN</button></div><div class="gv-nav-benchmark-status">NAV RECORDER READY · TOTAL 17.0s</div>`;
    root.appendChild(navBenchPanel);
    const navBenchStatus=navBenchPanel.querySelector('.gv-nav-benchmark-status');
    const navBenchRun=navBenchPanel.querySelector('[data-action="run"]');
    const phaseInputs={out:navBenchPanel.querySelector('[data-phase="out"]'),move:navBenchPanel.querySelector('[data-phase="move"]'),in:navBenchPanel.querySelector('[data-phase="in"]')};
    const navBenchStyle=document.createElement('style');navBenchStyle.textContent='#gv-nav-benchmark-12ar02{position:absolute;right:8px;top:58px;z-index:7600;display:flex;flex-direction:column;align-items:flex-end;gap:4px;pointer-events:auto;font:700 9px/1.1 system-ui,sans-serif}.gv-nav-phase-row{display:flex;gap:4px;align-items:end;padding:4px;border:1px solid #1565C0;border-radius:7px;background:rgba(0,0,0,.84)}.gv-nav-phase-row label{display:flex;flex-direction:column;gap:2px;color:#9fd0ff;font:800 8px/1 system-ui,sans-serif}.gv-nav-phase-row input{width:45px;height:25px;box-sizing:border-box;border:1px solid #58bfff;border-radius:5px;background:#07111c;color:#fff;text-align:center;font:800 10px monospace}.gv-nav-phase-row button{height:25px;padding:0 8px;border:1px solid #78ffab;border-radius:5px;background:#07140c;color:#78ffab;font:800 9px system-ui,sans-serif}.gv-nav-phase-row button:disabled,.gv-nav-phase-row input:disabled{opacity:.4}#gv-nav-benchmark-12ar02 .gv-nav-benchmark-status{max-width:330px;padding:3px 5px;border-radius:4px;background:rgba(0,0,0,.72);color:#eee;font:700 8px/1.2 monospace;text-align:right}';document.head.appendChild(navBenchStyle);

    const nfinite=v=>{const n=Number(v);return Number.isFinite(n)?n:null};
    const norm180=v=>((Number(v)+180)%360+360)%360-180;
    const s7=v=>{const t=clamp01(v);return 35*t**4-84*t**5+70*t**6-20*t**7};
    const logMix=(a,b,p)=>Math.exp(Math.log(Math.max(1e-9,a))+(Math.log(Math.max(1e-9,b))-Math.log(Math.max(1e-9,a)))*p);
    const skySep=(a,b)=>{if(!a||!b)return null;const r=Math.PI/180,ra1=nfinite(a.ra),de1=nfinite(a.dec),ra2=nfinite(b.ra),de2=nfinite(b.dec);if([ra1,de1,ra2,de2].some(v=>v===null))return null;const c=Math.sin(de1*r)*Math.sin(de2*r)+Math.cos(de1*r)*Math.cos(de2*r)*Math.cos((ra1-ra2)*r);return Math.acos(Math.max(-1,Math.min(1,c)))/r};
    const phaseConfig=()=>{const out=Math.max(.5,nfinite(phaseInputs.out.value)||5.1),move=Math.max(.5,nfinite(phaseInputs.move.value)||6.8),zin=Math.max(.5,nfinite(phaseInputs.in.value)||5.1);return {zoomOutSeconds:out,translationSeconds:move,zoomInSeconds:zin,totalSeconds:out+move+zin}};
    const phaseAt=(elapsed,cfg)=>elapsed<cfg.zoomOutSeconds?'ZOOM_OUT':elapsed<cfg.zoomOutSeconds+cfg.translationSeconds?'TRANSLATION':elapsed<cfg.totalSeconds?'ZOOM_IN':'ARRIVED';
    const destinationKeyLocal=d=>{try{return destinationKey(d)}catch(_){return String(d?.key||d?.id||d?.designation||d?.name||'')}};
    const resolveTargetFov=d=>{const key=destinationKeyLocal(d);let receipt=null;try{receipt=preparationEngine?.getAladinPreparedReceipt?.(key)||null}catch(_){}for(const v of [receipt?.fov,receipt?.fieldOfView,d?.fov,d?.aladinFov,d?.fieldOfViewDegrees,parseFieldOfViewDegrees(d?.fieldOfView),parseFieldOfViewDegrees(d?.field_of_view)]){const n=nfinite(v);if(n!==null&&n>0)return n}return null};
    const getObserved=()=>{let rd=[null,null],fv=[null,null],rot=null;try{rd=aladin.getRaDec?.()||rd}catch(_){}try{fv=aladin.getFov?.()||fv}catch(_){}try{rot=typeof aladin.getRotation==='function'?aladin.getRotation():null}catch(_){}return {ra:nfinite(rd?.[0]),dec:nfinite(rd?.[1]),fov:nfinite(fv?.[0]),rotation:nfinite(rot)}};
    const getWindowState=()=>{try{return randomNavigationWindow?.getState?.()||{}}catch(_){return {}}};
    const headOf=state=>state?.future?.[0]||state?.future0||state?.pending||null;
    const readinessSnapshot=(label,destination=null)=>{const a=navBench.active;const state=getWindowState();const head=destination||headOf(state);const key=destinationKeyLocal(head);let hd=null,al=null,bg=null,prefetch=null;try{hd=key?Boolean(preparationEngine?.isHdPrepared?.(key)):null}catch(_){}try{al=key?Boolean(preparationEngine?.isAladinPrepared?.(key)):null}catch(_){}try{bg=Boolean(preparationEngine?.getBackgroundWorkSuspended?.())}catch(_){}try{prefetch=preparationEngine?.getPrefetchState?.()||null}catch(_){}const row={label,elapsedMs:a?performance.now()-a.startedAt:0,key,hdPrepared:hd,aladinPrepared:al,backgroundSuspended:bg,window:{current:destinationKeyLocal(state?.current),pending:destinationKeyLocal(state?.pending),future0:destinationKeyLocal(head),futureLength:Array.isArray(state?.future)?state.future.length:null},prefetch};if(a)a.readiness.push(row);return row};
    const navBenchDownload=payload=>{const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);const c=payload.configuration;link.download=`gv-nav-flight-${c.zoomOutSeconds}s-out-${c.translationSeconds}s-move-${c.zoomInSeconds}s-in-${Date.now()}.json`;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(link.href),1000)};
    const statsFor=frames=>{const vals=frames.map(x=>x.dtMs).filter(Number.isFinite).sort((a,b)=>a-b);const q=p=>vals.length?vals[Math.min(vals.length-1,Math.floor((vals.length-1)*p))]:null;const mean=vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:null;return {count:vals.length,meanMs:mean,medianMs:q(.5),p95Ms:q(.95),p99Ms:q(.99),maxMs:vals.length?vals[vals.length-1]:null,over25ms:vals.filter(x=>x>25).length,over50ms:vals.filter(x=>x>50).length,over100ms:vals.filter(x=>x>100).length,over250ms:vals.filter(x=>x>250).length}};
    const postProcess=active=>{for(let i=0;i<active.frames.length;i++){const row=active.frames[i];const prev=i?active.frames[i-1]:null;const dt=prev?(row.elapsedMs-prev.elapsedMs)/1000:null;row.instantaneousFps=row.dtMs>0?1000/row.dtMs:null;row.long25=row.dtMs>25;row.long50=row.dtMs>50;row.long100=row.dtMs>100;row.long250=row.dtMs>250;if(prev&&dt>0){row.fovVelocityDegPerSec=nfinite(row.observed?.fov)!==null&&nfinite(prev.observed?.fov)!==null?(row.observed.fov-prev.observed.fov)/dt:null;const sep=skySep(prev.observed,row.observed);row.skyVelocityDegPerSec=sep===null?null:sep/dt;const r1=nfinite(prev.observed?.rotation),r2=nfinite(row.observed?.rotation);row.rotationVelocityDegPerSec=r1!==null&&r2!==null?norm180(r2-r1)/dt:null}else{row.fovVelocityDegPerSec=null;row.skyVelocityDegPerSec=null;row.rotationVelocityDegPerSec=null}}const phases={};for(const p of ['ZOOM_OUT','TRANSLATION','ZOOM_IN'])phases[p]=statsFor(active.frames.filter(x=>x.phase===p));return {overall:statsFor(active.frames),phases}};

    const navBenchCommandState={ra:null,dec:null,fov:null,rotation:null};
    for(const method of ['gotoRaDec','setFov','setRotation']){
        const original=aladin[method];if(typeof original!=='function'||original.__gv12ar02Wrapped)continue;
        const wrapped=function(...args){const a=navBench.active;let applied=[...args];if(a){const elapsed=(performance.now()-a.startedAt)/1000;const phase=phaseAt(elapsed,a.configuration);if(method==='setFov'&&a.startState.fov!==null&&a.targetFov!==null){let fov;if(elapsed<=a.configuration.zoomOutSeconds){fov=logMix(a.startState.fov,237.6,s7(elapsed/a.configuration.zoomOutSeconds))}else if(elapsed<=a.configuration.zoomOutSeconds+a.configuration.translationSeconds){fov=237.6}else{fov=logMix(237.6,a.targetFov,s7((elapsed-a.configuration.zoomOutSeconds-a.configuration.translationSeconds)/a.configuration.zoomInSeconds))}applied=[fov];navBenchCommandState.fov=fov}else if(method==='gotoRaDec'){navBenchCommandState.ra=nfinite(args[0]);navBenchCommandState.dec=nfinite(args[1])}else if(method==='setRotation')navBenchCommandState.rotation=nfinite(args[0]);a.commands.push({elapsedMs:performance.now()-a.startedAt,phase,method,requestedArgs:[...args],appliedArgs:[...applied],commanded:{...navBenchCommandState}})}return original.apply(aladin,applied)};wrapped.__gv12ar02Wrapped=true;aladin[method]=wrapped;
    }

    async function runPhaseBenchmark(){
        if(navBench.active||randomGalaxy.busy)return;
        const cfg=phaseConfig();const stateBefore=getWindowState();const head=headOf(stateBefore);const startObs=getObserved();const targetFov=resolveTargetFov(head)||startObs.fov;
        randomGalaxy.options.travelSeconds=cfg.totalSeconds;randomGalaxy.options.translateStart=cfg.zoomOutSeconds/cfg.totalSeconds;randomGalaxy.options.turnPoint=cfg.zoomOutSeconds/cfg.totalSeconds;randomGalaxy.options.translate90=(cfg.zoomOutSeconds+cfg.translationSeconds)/cfg.totalSeconds;randomGalaxy.options.translationComplete=(cfg.zoomOutSeconds+cfg.translationSeconds)/cfg.totalSeconds;
        navBenchCommandState.ra=startObs.ra;navBenchCommandState.dec=startObs.dec;navBenchCommandState.fov=startObs.fov;navBenchCommandState.rotation=startObs.rotation;
        const current=stateBefore?.current||null;const routeEdge={fromKey:destinationKeyLocal(current),toKey:destinationKeyLocal(head),travelDeg:skySep(current,head),rotationDeg:(nfinite(current?.orientation??current?.aladinRotation)!==null&&nfinite(head?.orientation??head?.aladinRotation)!==null)?Math.abs(norm180(Number(head?.orientation??head?.aladinRotation)-Number(current?.orientation??current?.aladinRotation))):null};
        const active={schema:'GV-NAVIGATION-PERFORMANCE-TELEMETRY-0002',viewerVersion:VERSION,randomModuleVersion:window.GalaxyRandomGalaxy?.VERSION,generatedAt:new Date().toISOString(),startedAt:performance.now(),configuration:{...cfg,maxFovDeg:237.6,easing:'S7',sampling:'requestAnimationFrame'},startState:startObs,targetFov,routeEdge,destinationBefore:head,commands:[],frames:[],events:[],readiness:[],lastFrameAt:null,lastPhase:null,frameId:0,destination:null,error:null};navBench.active=active;
        for(const x of Object.values(phaseInputs))x.disabled=true;navBenchRun.disabled=true;navBenchStatus.textContent=`RUN ${cfg.zoomOutSeconds.toFixed(1)} OUT / ${cfg.translationSeconds.toFixed(1)} MOVE / ${cfg.zoomInSeconds.toFixed(1)} IN`;
        active.events.push({type:'NAVIGATION_START',elapsedMs:0});readinessSnapshot('BEFORE_CLAIM',head);
        const frame=now=>{if(navBench.active!==active)return;const elapsedMs=now-active.startedAt;const elapsed=elapsedMs/1000;const phase=phaseAt(elapsed,cfg);if(phase!==active.lastPhase){active.events.push({type:`${phase}_START`,elapsedMs});active.lastPhase=phase;readinessSnapshot(`PHASE_${phase}`,head)}const observed=getObserved();const dt=active.lastFrameAt===null?null:now-active.lastFrameAt;active.lastFrameAt=now;active.frames.push({frameIndex:active.frames.length,timestampMs:now,elapsedMs,dtMs:dt,phase,phaseElapsedMs:phase==='ZOOM_OUT'?elapsedMs:phase==='TRANSLATION'?elapsedMs-cfg.zoomOutSeconds*1000:phase==='ZOOM_IN'?elapsedMs-(cfg.zoomOutSeconds+cfg.translationSeconds)*1000:0,observed,commanded:{...navBenchCommandState}});active.frameId=requestAnimationFrame(frame)};active.frameId=requestAnimationFrame(frame);
        try{active.destination=await randomGalaxy.travelToRandom();active.events.push({type:'ARRIVAL',elapsedMs:performance.now()-active.startedAt})}catch(error){active.error={name:String(error?.name||'Error'),message:String(error?.message||error),stack:String(error?.stack||'')};active.events.push({type:'ERROR',elapsedMs:performance.now()-active.startedAt,message:active.error.message});console.error('12AR-02 NAV RECORDER FAILURE',error)}finally{cancelAnimationFrame(active.frameId);readinessSnapshot('AFTER_TRAVEL',active.destination||head);const endedAt=performance.now();const performanceSummary=postProcess(active);const payload={schema:active.schema,generatedAt:new Date().toISOString(),viewerVersion:active.viewerVersion,randomModuleVersion:active.randomModuleVersion,configuration:active.configuration,elapsedMs:endedAt-active.startedAt,startState:active.startState,targetFov:active.targetFov,routeEdge:active.routeEdge,destinationBefore:active.destinationBefore,destination:active.destination,error:active.error,performanceSummary,events:active.events,readiness:active.readiness,commands:active.commands,frames:active.frames};navBench.lastPayload=payload;navBench.active=null;for(const x of Object.values(phaseInputs))x.disabled=false;navBenchRun.disabled=false;const s=performanceSummary.overall;navBenchStatus.textContent=`DONE · P99 ${Number(s.p99Ms||0).toFixed(1)} ms · MAX ${Number(s.maxMs||0).toFixed(1)} ms · >50 ${s.over50ms} · DOWNLOADING`;navBenchDownload(payload)}
    }
    for(const input of Object.values(phaseInputs))input.addEventListener('input',()=>{const c=phaseConfig();navBenchStatus.textContent=`READY · TOTAL ${c.totalSeconds.toFixed(1)}s`});
    navBenchRun.addEventListener('click',runPhaseBenchmark);
    window.GalaxyViewerNavigationBenchmark=Object.freeze({run:runPhaseBenchmark,get active(){return navBench.active},get lastPayload(){return navBench.lastPayload},get configuration(){return phaseConfig()}});

    window.addEventListener('beforeunload' '''

pattern = re.compile(r"    // ==================== 12AR-01 LOADED NAVIGATION BENCHMARK ====================[\s\S]*?\n    window\.addEventListener\('beforeunload'", re.M)
source, count = pattern.subn(benchmark, source, count=1)
if count != 1:
    raise RuntimeError(f'12AR-02 benchmark replacement count {count}, expected 1')

# Execute exact derivative in the current notebook context.
exec(compile(source, 'GV-beta-0012AR-02-derived.py', 'exec'))
