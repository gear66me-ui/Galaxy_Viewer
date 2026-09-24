/* Galaxy Viewer Galaxy Route Engine 001
 * Clean-room runtime authority for master catalog loading and 130 -> 100 + 30 planning.
 * Owns: catalog normalization, candidate sampling, route solve, reserve bank, exclusion set.
 * Does NOT own: Aladin camera, travel choreography, Random Galaxy UI, AVM, image decode, HD viewport.
 */
(function(global){'use strict';
const VERSION='0001';
const MASTER='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
const ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
const C=Object.freeze({CANDIDATE_POOL_SIZE:130,ROUTE_LENGTH:100,RESERVE_SIZE:30,TRANSLATION_TARGET_DEG:95,TRANSLATION_MIN_DEG:65,TRANSLATION_MAX_DEG:125,MAX_FOV_OCTAVES:5,ROUTE_RESTARTS:128,MAX_SAMPLE_ATTEMPTS:100});
const log=(m,x)=>{console.info('[GV011]',m,x??'');const e=document.getElementById('gv011log');if(e)e.textContent+=m+(x===undefined?'':' '+JSON.stringify(x))+'\n'};
const finite=v=>{const n=Number(v);return Number.isFinite(n)?n:null},clean=v=>String(v??'').replace(/\s+/g,' ').trim();
function key(r){const p=clean(r?.provider??r?.source??r?.catalogKey).toLowerCase(),d=clean(r?.archiveId??r?.id??r?.key).toLowerCase(),ra=finite(r?.ra),dc=finite(r?.dec);if(d)return p?`${p}|${d}`:`${d}|${ra??''}|${dc??''}`;const n=clean(r?.name??r?.title).toLowerCase();return n&&ra!==null&&dc!==null?`${p}|${n}|${ra}|${dc}`:''}
function norm(r){const k=key(r),ra=finite(r?.ra),dec=finite(r?.dec),fov=finite(r?.fovDegrees??r?.fieldOfViewDegrees);return k&&ra!==null&&ra>=0&&ra<360&&dec!==null&&dec>=-90&&dec<=90&&fov!==null&&fov>0?{key:k,ra,dec,fov,record:r}:null}
function eligible(a){const m=new Map;for(const r of a){const x=norm(r);if(x&&!m.has(x.key))m.set(x.key,x)}return [...m.values()]}
function gc(a,b){const d=Math.PI/180,r1=a.ra*d,e1=a.dec*d,r2=b.ra*d,e2=b.dec*d,c=Math.sin(e1)*Math.sin(e2)+Math.cos(e1)*Math.cos(e2)*Math.cos(r1-r2);return Math.acos(Math.max(-1,Math.min(1,c)))/d}
function compat(a,b){const travelDeg=gc(a,b),fovDeltaOctaves=Math.abs(Math.log2(a.fov/b.fov));return {compatible:travelDeg>=C.TRANSLATION_MIN_DEG&&travelDeg<=C.TRANSLATION_MAX_DEG&&fovDeltaOctaves<=C.MAX_FOV_OCTAVES,travelDeg,fovDeltaOctaves}}
function shuffle(v){const a=[...v];for(let i=a.length-1;i;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function graph(nodes){const n=nodes.length,N=Array.from({length:n},()=>[]),E=new Map;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){const e=compat(nodes[i],nodes[j]);E.set(`${i}:${j}`,e);if(e.compatible){N[i].push(j);N[j].push(i)}}return {nodes,N,E}}
const edge=(g,a,b)=>g.E.get(a<b?`${a}:${b}`:`${b}:${a}`);function degree(g,i,u){let n=0;for(const x of g.N[i])if(!u.has(x))n++;return n}
function solve(g){const starts=g.nodes.map((_,i)=>i).filter(i=>g.N[i].length);for(let attempt=1;attempt<=C.ROUTE_RESTARTS;attempt++){const ranked=shuffle(starts).sort((a,b)=>g.N[a].length-g.N[b].length),band=ranked.slice(0,Math.max(1,Math.ceil(ranked.length*.35))),start=band[Math.floor(Math.random()*band.length)],path=[start],used=new Set(path);while(path.length<C.ROUTE_LENGTH){const cur=path.at(-1),cand=g.N[cur].filter(i=>!used.has(i));if(!cand.length)break;const s=cand.map(next=>{const e=edge(g,cur,next);return {next,target:Math.abs(e.travelDeg-C.TRANSLATION_TARGET_DEG),fov:e.fovDeltaOctaves,remain:degree(g,next,used),tie:Math.random()}}).sort((a,b)=>a.target-b.target||a.fov-b.fov||b.remain-a.remain||a.tie-b.tie);path.push(s[0].next);used.add(s[0].next)}if(path.length===C.ROUTE_LENGTH)return {path,attempt}}return null}
function validate(route){if(route.length!==100||new Set(route.map(x=>x.key)).size!==100)return false;for(let i=1;i<route.length;i++)if(!compat(route[i-1],route[i]).compatible)return false;return true}
function plan(records){const e=eligible(records);if(e.length<130)throw Error(`ELIGIBLE CATALOG TOO SMALL ${e.length}`);const t=performance.now();for(let sampleAttempt=1;sampleAttempt<=100;sampleAttempt++){const sample=shuffle(e).slice(0,130),s=solve(graph(sample));if(!s)continue;const route=s.path.map(i=>sample[i]);if(!validate(route))continue;const used=new Set(route.map(x=>x.key)),reserve=sample.filter(x=>!used.has(x.key));if(reserve.length!==30)throw Error(`RESERVE ${reserve.length}`);return {sample:sample.map(x=>x.record),route:route.map(x=>x.record),reserve:reserve.map(x=>x.record),sampleAttempt,solverAttempt:s.attempt,solveTimeMs:performance.now()-t}}throw Error('130->100 FAILED')}
function imageUrl(r){const a=[...(Array.isArray(r?.jpegCandidates)?r.jpegCandidates:[]),r?.selectedImageUrl,r?.hdUrl].map(clean).filter(Boolean);return a.find(x=>/\/screen\//i.test(x))||a[0]||''}
function normalizeRaw(r,i,catalogKey,meta){return Object.freeze({provider:clean(r?.provider??meta.provider??catalogKey).toUpperCase(),source:clean(r?.source??meta.source??catalogKey),archiveId:clean(r?.archiveId??r?.id),name:clean(r?.name??r?.title??r?.displayName??r?.archiveId),ra:finite(r?.ra),dec:finite(r?.dec),fovDegrees:finite(r?.fovDegrees??r?.fieldOfViewDegrees),aladinRotation:finite(r?.aladinRotation),imageUrl:imageUrl(r),catalogKey,catalogIndex:i})}
async function json(url){const r=await fetch(url,{cache:'no-cache'});if(!r.ok)throw Error(`HTTP ${r.status} ${url}`);return r.json()}
async function catalogs(){const m=await json(MASTER);if(!m?.catalogs)throw Error('MASTER POINTER MAP MISSING');const records=[],counts={};for(const [k,p] of Object.entries(m.catalogs)){const x=await json(new URL(String(p),ROOT).href);if(!Array.isArray(x?.entries))throw Error(`${k} ENTRIES MISSING`);const meta={provider:x.provider,source:x.source};records.push(...x.entries.map((r,i)=>normalizeRaw(r,i,k,meta)));counts[k]=x.entries.length}return {version:m.version,records,counts}}

const Runtime={
 VERSION,CONSTANTS:C,phase:'IDLE',catalog:null,active:null,exclusion:new Set(),
 async initialize(){
  this.phase='CATALOG';this.catalog=await catalogs();
  this.phase='MONTE_CARLO';this.active=plan(this.catalog.records);
  this.exclusion.clear();for(const r of this.active.sample){const k=key(r);if(k)this.exclusion.add(k)}
  this.phase='READY';return this.snapshot();
 },
 snapshot(){return Object.freeze({runtime:VERSION,phase:this.phase,catalog:this.catalog?.records.length??0,active:this.active?.route.length??0,reserve:this.active?.reserve.length??0,excluded:this.exclusion.size,solveTimeMs:this.active?.solveTimeMs??null,sampleAttempt:this.active?.sampleAttempt??null,solverAttempt:this.active?.solverAttempt??null})}
};
global.GalaxyRouteEngine=Runtime;
})(typeof window!=='undefined'?window:globalThis);
