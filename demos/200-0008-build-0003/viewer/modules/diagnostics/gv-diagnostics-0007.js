/* Galaxy Viewer automatic analytics diagnostics 0005. Collection starts immediately and never pauses. */
(() => {
  'use strict';
  const VERSION='0007',POLL_MS=1000,MAX_SNAPSHOTS=3600,MAX_ERRORS=500,MAX_EVENTS=12000;
  const startedAt=performance.now();
  const errors=[],snapshots=[],localEvents=[];
  let panel=null,statusEl=null,bodyEl=null,navEl=null,queueEl=null,eventEl=null,timer=0,enabled=true;
  const nowIso=()=>new Date().toISOString();
  const elapsed=()=>Math.round(performance.now()-startedAt);
  const pad=n=>String(n).padStart(2,'0');
  const stamp=()=>{const d=new Date();return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}_${pad(d.getHours())}-${pad(d.getMinutes())}-${pad(d.getSeconds())}`};
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const push=(array,value,max)=>{array.push(value);if(array.length>max)array.splice(0,array.length-max)};
  const audit=()=>window.__GV_ANALYTICS_AUDIT__||null;
  const core=()=>window.GalaxyViewerCore||window.GalaxyRandomGalaxy?.prefetchRuntime?.core||null;
  const telemetry=()=>{try{return window.GalaxyRandomGalaxy?.getPrefetchTelemetry?.()||null}catch(error){recordError('TELEMETRY',error);return null}};
  const compactUrl=value=>{try{const u=new URL(String(value||''),location.href);return `${u.host}${u.pathname}${u.search}`.slice(-220)}catch(_){return String(value||'').slice(-220)}};
  function emit(type,detail={}){
    const entry=Object.freeze({at:nowIso(),elapsedMs:elapsed(),type:String(type||'EVENT'),detail});
    push(localEvents,entry,MAX_EVENTS);
    try{audit()?.emit?.('DIAG_'+type,detail)}catch(_){}
    return entry;
  }
  function recordError(type,value){
    const message=value?.error?.stack||value?.reason?.stack||value?.message||value?.reason||value?.error||value;
    push(errors,Object.freeze({at:nowIso(),elapsedMs:elapsed(),type:String(type||'ERROR'),message:String(message||'UNKNOWN ERROR')}),MAX_ERRORS);
  }
  window.addEventListener('error',event=>recordError('ERROR',event),true);
  window.addEventListener('unhandledrejection',event=>recordError('PROMISE',event),true);

  // 0006 — capture exceptions deliberately caught and sent to console.error.
  const gvNativeConsoleError=console.error.bind(console);
  console.error=(...args)=>{
    try{
      const message=args.map(value=>{
        if(value instanceof Error)
          return value.stack||value.message||String(value);
        if(typeof value==='string')return value;
        try{return JSON.stringify(value)}
        catch(_){return String(value)}
      }).join(' ');
      recordError('CONSOLE_ERROR',message);
    }catch(_){}
    return gvNativeConsoleError(...args);
  };

  function preparedFor(c,row){
    try{return c?.getHdPreparedResource?.(row?.key)||null}catch(error){recordError('HD_RESOURCE',error);return null}
  }
  const normKey=value=>String(value||'').trim().toLowerCase();
  function ledKind(kind,data={}){
    const state=String(data?.state||'').trim().toUpperCase();
    const expected=normKey(data?.expectedKey);
    const stateKey=normKey(data?.stateKey);
    const resourceKey=normKey(data?.resourceKey);
    const receiptKey=normKey(data?.receiptKey);
    const activeKey=normKey(data?.activeKey);

    if(kind==='hd'){
      if((stateKey&&expected&&stateKey!==expected)||(resourceKey&&expected&&resourceKey!==expected))return 'blue';
      if(state==='READY')return data?.identityMatch===true&&resourceKey===expected?'green':'blue';
      if(state==='DOWNLOADING'||state==='DECODING')return !stateKey||stateKey===expected?'yellow':'blue';
      return 'red';
    }

    if(kind==='aladin'){
      if(receiptKey&&expected&&receiptKey!==expected)return 'blue';
      if(state==='READY')return data?.identityMatch===true&&receiptKey===expected?'green':'blue';
      if(state==='PREPARING')return activeKey===expected?'yellow':'blue';
      return 'red';
    }

    if(kind==='web'){
      if(stateKey&&expected&&stateKey!==expected)return 'blue';
      if(state==='READY')return data?.identityMatch===true&&stateKey===expected?'green':'blue';
      if(state==='DOWNLOADING')return activeKey===expected?'yellow':'blue';
      return 'red';
    }

    return 'red';
  }
  const ledGlyph=kind=>({green:'🟢',yellow:'🟡',red:'🔴',blue:'🔵'}[kind]||'🔴');

  function queueRow(row,index,c){
    const destination=row?.destination||{};
    const key=normKey(row?.key);
    const hd=row?.hd||{},aladin=row?.aladin||{},web=row?.web||{};

    const hdDetail=[
      `KEY ${key||'—'}`,
      `STATE ${String(hd.state||'—')}`,
      `STATE KEY ${String(hd.stateKey||'—')}`,
      `RESOURCE KEY ${String(hd.resourceKey||'—')}`,
      `SOURCE ${String(hd.detail||'—')}`,
      `URL ${compactUrl(hd.resourceUrl||destination.selectedImageUrl||destination.githubImageUrl||'')||'—'}`
    ].join(' · ');

    const aladinDetail=[
      `KEY ${key||'—'}`,
      `STATE ${String(aladin.state||'—')}`,
      `RECEIPT ${String(aladin.receiptKey||'—')}`,
      `ACTIVE ${String(aladin.activeKey||'—')}`,
      `RA ${aladin.ra??destination.ra??'—'}`,
      `DEC ${aladin.dec??destination.dec??'—'}`,
      `FOV ${aladin.fov??destination.fov??'—'}`,
      `ROT ${aladin.rotation??destination.rotation??'—'}`,
      `RECEIPT RA ${aladin.receiptRa??'—'}`,
      `RECEIPT DEC ${aladin.receiptDec??'—'}`,
      `RECEIPT FOV ${aladin.receiptFov??'—'}`,
      `RECEIPT ROT ${aladin.receiptRotation??'—'}`
    ].join(' · ');

    const webDetail=[
      `KEY ${key||'—'}`,
      `STATE ${String(web.state||'—')}`,
      `STATE KEY ${String(web.stateKey||'—')}`,
      `ACTIVE ${String(web.activeKey||'—')}`,
      `URL ${compactUrl(web.sourceUrl||'')||'—'}`,
      `EXPECTED ${compactUrl(web.expectedSourceUrl||destination.sourceUrl||'')||'—'}`
    ].join(' · ');

    const hdLed=ledKind('hd',hd);
    const aladinLed=ledKind('aladin',aladin);
    const webLed=ledKind('web',web);

    return Object.freeze({
      slot:Number(row?.slot||index+1),
      key,
      name:String(row?.name||key||''),
      provider:String(row?.provider||''),
      destination:Object.freeze({
        ra:destination?.ra??null,
        dec:destination?.dec??null,
        fov:destination?.fov??null,
        rotation:destination?.rotation??null
      }),
      hd:Object.freeze({...hd,led:hdLed,title:hdDetail}),
      aladin:Object.freeze({...aladin,led:aladinLed,title:aladinDetail}),
      web:Object.freeze({...web,led:webLed,title:webDetail})
    });
  }
  function imageStates(){
    return [...document.images].slice(0,160).map((img,index)=>Object.freeze({
      index, id:String(img.id||''), alt:String(img.alt||''), src:compactUrl(img.currentSrc||img.src||''),
      complete:Boolean(img.complete), width:Number(img.naturalWidth||0), height:Number(img.naturalHeight||0),
      state:img.complete?(img.naturalWidth>0?'LOADED':'FAILED_OR_EMPTY'):'LOADING'
    }));
  }
  function nativeAudit(){
    try{const raw=window.GalaxyViewerNativeAudit?.getNativeAudit?.();return raw?JSON.parse(raw):null}catch(error){recordError('NATIVE_AUDIT',error);return null}
  }
  function summary(){
    const c=core(),t=telemetry(),rows=Array.isArray(t?.rows)?t.rows:[],random=c?.randomGalaxy?.getState?.()||{};
    const queue=rows.map((row,index)=>queueRow(row,index,c));
    const count=key=>queue.filter(row=>String(row[key]?.led||'')==='green').length;
    const a=audit();
    const resources=a?.resources||[];
    const recentResources=resources.filter(r=>Number(r.elapsedMs||0)>=Math.max(0,elapsed()-1100)).slice(-80);
    const navigation=t?.navigation||{};
    return Object.freeze({
      at:nowIso(),elapsedMs:elapsed(),second:Math.floor(elapsed()/1000),viewer:String(c?.displayVersion||document.querySelector('[aria-label^="GALAXY VIEWER VERSION"]')?.textContent||''),
      randomVersion:String(window.GalaxyRandomGalaxy?.VERSION||''),telemetryApi:typeof window.GalaxyRandomGalaxy?.getPrefetchTelemetry==='function'?'READY':'MISSING',
      mode:random.busy?'TRAVELING':random.hdOpen?'HD_OPEN':'READY',backgroundSuspended:Boolean(c?.getBackgroundWorkSuspended?.()||t?.suspended),
      future:queue.length,next:queue[0]?.name||'',active:String(t?.active?.name||''),navigation,
      catalog:Number(c?.eligibleCatalogCount||0),
      hdReady:count('hd'),aladinReady:count('aladin'),webReady:count('web'),queue,
      images:imageStates(),recentResources,canvasCount:document.querySelectorAll('canvas').length,
      aladinCanvas:Boolean(document.querySelector('#aladin-cosmic-command-test canvas')),
      nativeEventCount:Number(nativeAudit()?.events?.length||0),auditEventCount:Number(a?.events?.length||0),auditResourceCount:Number(resources.length||0)
    });
  }
  function collect(){
    const snapshot=summary();push(snapshots,snapshot,MAX_SNAPSHOTS);emit('SECOND',{second:snapshot.second,future:snapshot.future,next:snapshot.next,hdReady:snapshot.hdReady,aladinReady:snapshot.aladinReady,webReady:snapshot.webReady,images:snapshot.images.length,canvas:snapshot.canvasCount});
    render(snapshot);
  }
  function start(){
    if(timer)return false;
    enabled=true;
    collect();
    timer=setInterval(collect,POLL_MS);
    return true;
  }
  function stop(){
    if(timer){clearInterval(timer);timer=0}
    enabled=false;
    render();
    return true;
  }
  function toggle(){return enabled?stop():start()}
  function ensureStyle(){
    if(document.getElementById('gv-diagnostics-0006-style'))return;
    const style=document.createElement('style');style.id='gv-diagnostics-0006-style';style.textContent=`
#gv-diagnostics-0006{position:fixed;right:5px;top:56px;z-index:2147483200;width:min(355px,calc(100vw - 10px));max-height:52vh;overflow:auto;padding:5px;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,rgba(5,20,45,.97),rgba(10,48,112,.95));color:#DDF8FF;font:7px/1.16 monospace;box-shadow:0 0 10px rgba(88,191,255,.35)}
#gv-diagnostics-0006 *{box-sizing:border-box}
#gv-diagnostics-0006 header{display:flex;align-items:center;justify-content:space-between;gap:4px;color:#9BE5FF;font-weight:700;margin-bottom:3px}
#gv-diagnostics-0006 button{padding:2px 4px;border:1px solid #7CCBFF;border-radius:3px;background:#081B3A;color:#EAF8FF;font:6.5px monospace}
#gv-diagnostics-0006 table{width:100%;border-collapse:collapse;table-layout:fixed}
#gv-diagnostics-0006 td,#gv-diagnostics-0006 th{padding:1.5px 2px;border:1px solid rgba(124,203,255,.23);text-align:left;vertical-align:top;overflow-wrap:anywhere}
#gv-diagnostics-0006 th{color:#9BE5FF;background:#081B3A}
#gv-diagnostics-0006 .s{color:#9BE5FF;margin:3px 0 2px;font-weight:700}
#gv-diagnostics-0006 .status{color:#78FFAB;margin-bottom:3px}
#gv-diagnostics-0006 .nav{margin:2px 0;color:#DDF8FF;white-space:normal}
#gv-diagnostics-0006 .led{font-size:10px;line-height:1;display:inline-block;min-width:12px;text-align:center}
#gv-diagnostics-0006 .target{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:170px}`;
    document.head.appendChild(style);
  }
  function render(s=snapshots.at(-1)||summary()){
    if(!panel)return;
    statusEl.textContent=enabled
      ? `ON — COLLECTING · ${s.second}s · ${snapshots.length} SNAPSHOTS`
      : `OFF — COLLECTION PAUSED · ${s.second}s · ${snapshots.length} SNAPSHOTS`;
    const toggleButton=panel.querySelector('[data-a="toggle"]');
    if(toggleButton)toggleButton.textContent=enabled?'ON':'OFF';
    bodyEl.innerHTML=[
      ['VIEWER',s.viewer||'—',`RANDOM ${s.randomVersion||'—'}`],
      ['MODE',s.mode,s.backgroundSuspended?'SUSPENDED':'RUNNING'],
      ['FUTURE',s.future,`NEXT ${s.next||'—'}`],
      ['READY',`HD ${s.hdReady}/${s.future}`,`AL ${s.aladinReady}/${s.future} WEB ${s.webReady}/${s.future}`],
      ['IMAGES',s.images.length,`CANVAS ${s.canvasCount}`],
      ['EVENTS',s.auditEventCount,`RES ${s.auditResourceCount}`]
    ].map(r=>`<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td></tr>`).join('');

    const nav=s.navigation||{};
    navEl.textContent=[
      `CURRENT ${nav.current?.name||nav.current?.key||'—'}`,
      `LOCKED ${nav.locked?.name||nav.locked?.key||'—'}`,
      `PENDING ${nav.pending?.name||nav.pending?.key||'—'}`,
      `FUTURE[0] ${nav.future0?.name||nav.future0?.key||'—'}`
    ].join(' · ');

    const navKeys={
      current:normKey(nav.current?.key),
      locked:normKey(nav.locked?.key),
      pending:normKey(nav.pending?.key),
      future0:normKey(nav.future0?.key)
    };

    queueEl.innerHTML=s.queue.map(r=>{
      const marks=[];
      if(r.key&&r.key===navKeys.current)marks.push('C');
      if(r.key&&r.key===navKeys.locked)marks.push('L');
      if(r.key&&r.key===navKeys.pending)marks.push('P');
      if(r.key&&r.key===navKeys.future0)marks.push('0');
      const marker=marks.length?` [${marks.join('')}]`:'';
      return `<tr>
<td>${r.slot}</td>
<td class="target" title="${esc(r.key)}">${esc((r.name||r.key||'—')+marker)}</td>
<td><span class="led" title="${esc(r.hd.title||'')}">${ledGlyph(r.hd.led)}</span></td>
<td><span class="led" title="${esc(r.aladin.title||'')}">${ledGlyph(r.aladin.led)}</span></td>
<td><span class="led" title="${esc(r.web.title||'')}">${ledGlyph(r.web.led)}</span></td>
</tr>`;
    }).join('')||'<tr><td colspan="5">QUEUE NOT AVAILABLE YET</td></tr>';

    const all=[...(audit()?.events||[]),...localEvents]
      .sort((a,b)=>Number(a.elapsedMs||0)-Number(b.elapsedMs||0))
      .slice(-12).reverse();

    eventEl.innerHTML=all.map(e=>`<tr><td>${(Number(e.elapsedMs||0)/1000).toFixed(1)}</td><td>${esc(e.type)}</td><td>${esc(typeof e.detail==='string'?e.detail:JSON.stringify(e.detail||{}))}</td></tr>`).join('')||'<tr><td colspan="3">NO EVENTS YET</td></tr>';
  }
  function ensurePanel(){
    ensureStyle();
    if(panel)return panel;
    panel=document.createElement('section');
    panel.id='gv-diagnostics-0006';
    panel.innerHTML=`<header><span>DIAGNOSTICS 0006 · AUTO</span><span><button data-a="toggle">ON</button><button data-a="download">DOWNLOAD</button><button data-a="close">X</button></span></header><div class="status"></div><table><tbody class="body"></tbody></table><div class="nav"></div><div class="s">LIVE 10-SLOT QUEUE · C=CURRENT L=LOCKED P=PENDING 0=FUTURE[0]</div><table><thead><tr><th>#</th><th>TARGET</th><th>HD</th><th>AL</th><th>WEB</th></tr></thead><tbody class="queue"></tbody></table><div class="s">LED: 🟢 READY · 🟡 ACTIVE · 🔴 IDLE/FAILED · 🔵 STALE/MISMATCH</div><div class="s">RECENT EVENTS</div><table><thead><tr><th>s</th><th>TYPE</th><th>DETAIL</th></tr></thead><tbody class="events"></tbody></table>`;
    statusEl=panel.querySelector('.status');
    bodyEl=panel.querySelector('.body');
    navEl=panel.querySelector('.nav');
    queueEl=panel.querySelector('.queue');
    eventEl=panel.querySelector('.events');
    panel.addEventListener('click',event=>{
      const a=event.target?.dataset?.a;
      if(a==='download')download();
      else if(a==='toggle')toggle();
      else if(a==='close')panel.style.display='none';
    });
    document.body.appendChild(panel);
    render();
    return panel;
  }
  function exportData(){
    const trace=window.__GV_RANDOM_EXEC_TRACE__||null;
    const traceEvents=Array.isArray(trace?.events)?[...trace.events]:[];
    let largestExecutionGapMs=0;
    let largestExecutionGapEvent=null;
    for(let i=1;i<traceEvents.length;i++){
      const gap=
        Number(traceEvents[i]?.elapsedMs||0)-
        Number(traceEvents[i-1]?.elapsedMs||0);
      if(gap>largestExecutionGapMs){
        largestExecutionGapMs=gap;
        largestExecutionGapEvent=traceEvents[i];
      }
    }
    const randomExecutionTrace=trace?{
      version:String(trace.version||''),
      source:String(trace.source||''),
      eventCount:traceEvents.length,
      lastExecutedStep:trace.last||traceEvents.at(-1)||null,
      largestExecutionGapMs,
      largestExecutionGapEvent,
      events:traceEvents
    }:null;
    return {
      module:'GalaxyViewerDiagnostics',
      version:VERSION,
      autoStarted:true,
      exportedAt:nowIso(),
      elapsedMs:elapsed(),
      errors:[...errors],
      snapshots:[...snapshots],
      events:[...localEvents],
      randomExecutionTrace,
      bootAudit:audit()?.exportData?.()||audit()||null,
      nativeAudit:nativeAudit()
    };
  }
  function download(){
    const filename=`Galaxy-Viewer-Diagnostics-${stamp()}.json`,json=JSON.stringify(exportData(),null,2);
    if(window.GalaxyViewerDownloads?.saveJson){window.GalaxyViewerDownloads.saveJson(filename,json);return true}
    console.error('DIAGNOSTICS 0006 DOWNLOAD BRIDGE MISSING',filename);return false;
  }
  function open(){ensurePanel().style.display='block';render()}function close(){if(panel)panel.style.display='none'}
  emit('AUTO_START',{version:VERSION});start();
  window.GalaxyViewerDiagnostics=Object.freeze({VERSION,open,close,start,stop,toggle,download,exportData,getState:()=>Object.freeze({enabled,autoStarted:true,errors:errors.length,snapshots:snapshots.length,events:localEvents.length})});
})();
