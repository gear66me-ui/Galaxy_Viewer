/* Galaxy Viewer Galaxy Route Engine 002
 * Revision 002: restore the complete catalog science/presentation metadata contract on normalized destination records.
 * Navigation/route-solving behavior is unchanged from 001.
 * Clean-room runtime authority for master catalog loading and 130 -> 100 + 30 planning.
 * Owns: catalog normalization, candidate sampling, route solve, reserve bank, exclusion set.
 * Does NOT own: Aladin camera, travel choreography, Random Galaxy UI, AVM, image decode, HD viewport.
 */
(function(global){'use strict';
const VERSION='0002';
const MASTER='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
const ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
const C=Object.freeze({CANDIDATE_POOL_SIZE:130,ROUTE_LENGTH:100,RESERVE_SIZE:30,TRANSLATION_TARGET_DEG:95,TRANSLATION_MIN_DEG:65,TRANSLATION_MAX_DEG:125,MAX_FOV_OCTAVES:5,ROUTE_RESTARTS:128,MAX_SAMPLE_ATTEMPTS:100,URL_RETRY_LIMIT:3,URL_RETRY_DELAY_MS:350,QUARANTINE_RECHECK_MS:300000,REPLENISH_AT:10,VALIDATION_WORKERS:12});
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
function normalizeRaw(r,i,catalogKey,meta){
 const science=(r?.science&&typeof r.science==='object')?r.science:{};
 const distanceDisplay=clean(science.distanceDisplay??r?.distance);
 const distanceMatch=distanceDisplay.match(/([0-9]+(?:\.[0-9]+)?)\s*(billion|million|thousand)\s+light\s*-?\s*years?/i);
 const distanceScale=distanceMatch?(distanceMatch[2].toLowerCase()==='billion'?1000:distanceMatch[2].toLowerCase()==='thousand'?0.001:1):null;
 const distanceMly=finite(science.distanceMly??r?.distanceMly??r?.distance_mly)??(distanceMatch?Number(distanceMatch[1])*distanceScale:null);
 const ageGyr=finite(science.ageGyr??r?.ageGyr);
 const ageYears=finite(r?.ageYears)??(ageGyr!==null?ageGyr*1e9:null);
 const sizeKly=Array.isArray(science.sizeKly)?science.sizeKly.map(finite).filter(v=>v!==null):[];
 const physicalSizeLy=finite(r?.physicalSizeLy)??(sizeKly.length?Math.max(...sizeKly)*1000:null);
 const commonName=clean(r?.commonName??r?.common_name??r?.displayName??r?.title??r?.name);
 return Object.freeze({
  provider:clean(r?.provider??meta.provider??catalogKey).toUpperCase(),
  providerLabel:clean(r?.providerLabel??meta.provider??r?.provider??catalogKey),
  source:clean(r?.source??meta.source??catalogKey),
  archiveId:clean(r?.archiveId??r?.id),
  name:clean(r?.name??r?.title??r?.displayName??r?.archiveId),
  designation:clean(r?.designation),
  commonName,
  pseudonym:clean(r?.pseudonym??r?.pseudo??r?.alias??r?.alternateName??commonName),
  ra:finite(r?.ra),dec:finite(r?.dec),
  distance:distanceDisplay,
  distanceMly,
  distanceMethod:clean(science.distanceMethod),
  distanceEstimated:science.distanceEstimated??null,
  constellation:clean(r?.constellation),
  constellationMethod:clean(r?.constellationMethod),
  age:clean(science.ageDisplay??r?.age??r?.ageEstimate??r?.age_estimate),
  ageGyr,ageYears,
  ageEstimated:science.ageEstimated??null,
  ageMethod:clean(science.ageMethod),
  size:clean(science.sizeDisplay??r?.size),
  sizeKly:Object.freeze(sizeKly),
  physicalSizeLy,
  sizeEstimated:science.sizeEstimated??null,
  sizeMethod:clean(science.sizeMethod),
  redshift:finite(science.redshift??r?.redshift),
  redshiftDisplay:clean(science.redshiftDisplay),
  description:clean(r?.description),
  credit:clean(r?.credit),
  imageType:clean(r?.imageType),
  category:clean(r?.category),
  telescope:clean(r?.telescope),
  facility:Object.freeze(Array.isArray(r?.facility)?r.facility.map(clean).filter(Boolean):[]),
  instrument:Object.freeze(Array.isArray(r?.instrument)?r.instrument.map(clean).filter(Boolean):[]),
  sourceUrl:clean(r?.sourceUrl),
  hdUrl:clean(r?.hdUrl),
  githubImageUrl:clean(r?.githubImageUrl),
  sha256:clean(r?.sha256),
  fovDegrees:finite(r?.fovDegrees??r?.fieldOfViewDegrees),
  avmHorizontalFovDegrees:finite(r?.avmHorizontalFovDegrees),
  avmVerticalFovDegrees:finite(r?.avmVerticalFovDegrees),
  avmRotation:finite(r?.avmRotation),
  aladinRotation:finite(r?.aladinRotation),
  avmReferenceRa:finite(r?.avmReferenceRa),
  avmReferenceDec:finite(r?.avmReferenceDec),
  avmWcsQuality:clean(r?.avmWcsQuality),
  fovAuthority:clean(r?.fovAuthority),
  rotationAuthority:clean(r?.rotationAuthority),
  coordinateAuthority:clean(r?.coordinateAuthority),
  imageUrl:imageUrl(r),
  catalogKey,catalogIndex:i
 })
}
async function json(url){const r=await fetch(url,{cache:'no-cache'});if(!r.ok)throw Error(`HTTP ${r.status} ${url}`);return r.json()}
async function catalogs(){const m=await json(MASTER);if(!m?.catalogs)throw Error('MASTER POINTER MAP MISSING');const records=[],counts={};for(const [k,p] of Object.entries(m.catalogs)){const x=await json(new URL(String(p),ROOT).href);if(!Array.isArray(x?.entries))throw Error(`${k} ENTRIES MISSING`);const meta={provider:x.provider,source:x.source};records.push(...x.entries.map((r,i)=>normalizeRaw(r,i,k,meta)));counts[k]=x.entries.length}return {version:m.version,records,counts}}

const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
function avmUrl(r){return clean(r?.imageUrl??imageUrl(r))}
async function urlAlive(r){
 const url=avmUrl(r);if(!/^https?:\/\//i.test(url))return {ok:false,reason:'AVM_URL_MISSING',url};
 let last='';for(let attempt=1;attempt<=C.URL_RETRY_LIMIT;attempt++){try{const q=url+(url.includes('?')?'&':'?')+'gv_avm_probe='+Date.now();const response=await fetch(q,{method:'GET',headers:{Range:'bytes=0-0'},cache:'no-store'});if(response.ok||response.status===206)return {ok:true,url,attempt,status:response.status};last='HTTP_'+response.status}catch(error){last=clean(error?.message)||'FETCH_FAILED'}if(attempt<C.URL_RETRY_LIMIT)await wait(C.URL_RETRY_DELAY_MS)}
 return {ok:false,reason:last||'AVM_URL_DEAD',url,attempt:C.URL_RETRY_LIMIT}
}


async function validatedPlan(records,runtime){
 const candidates=shuffle(eligible(records).map(x=>x.record)).filter(r=>!runtime.quarantine.has(key(r)));
 const healthy=[];let cursor=0;
 async function worker(){
  while(healthy.length<C.CANDIDATE_POOL_SIZE&&cursor<candidates.length){
   const r=candidates[cursor++],probe=await runtime.validateAvm(r);
   if(probe.ok)healthy.push(r);
  }
 }
 while(healthy.length<C.CANDIDATE_POOL_SIZE&&cursor<candidates.length){
  await Promise.all(Array.from({length:C.VALIDATION_WORKERS},()=>worker()));
 }
 if(healthy.length<C.CANDIDATE_POOL_SIZE)throw Error(`VALIDATED CATALOG TOO SMALL ${healthy.length}`);
 return plan(healthy.slice(0,C.CANDIDATE_POOL_SIZE));
}

const Runtime={
 VERSION,CONSTANTS:C,phase:'IDLE',catalog:null,active:null,exclusion:new Set(),quarantine:new Map(),routeCursor:0,reserveCursor:0,generation:0,nextGeneration:null,recheckTimer:null,
 async initialize(){
  this.phase='CATALOG';this.catalog=await catalogs();
  this.phase='MONTE_CARLO';this.active=plan(this.catalog.records);this.generation=1;this.routeCursor=0;this.reserveCursor=0;this.nextGeneration=null;
  this.exclusion.clear();for(const r of this.active.sample){const k=key(r);if(k)this.exclusion.add(k)}
  this.phase='READY';this.startQuarantineRecheck();return this.snapshot();
 },
 quarantineRecord(r,probe){const k=key(r);if(!k)return;const prior=this.quarantine.get(k);this.quarantine.set(k,{record:r,reason:probe?.reason||'AVM_URL_DEAD',failureCount:(prior?.failureCount||0)+1,lastChecked:Date.now(),nextCheck:Date.now()+C.QUARANTINE_RECHECK_MS})},
 async validateAvm(r){const probe=await urlAlive(r);if(!probe.ok)this.quarantineRecord(r,probe);return probe},
 async takeReserve(previous){
  while(this.reserveCursor<this.active.reserve.length){const r=this.active.reserve[this.reserveCursor++],k=key(r);if(this.quarantine.has(k))continue;if(previous&&!compat(norm(previous),norm(r)).compatible)continue;return r}
  return null
 },
 async nextDestination(){
  if(!this.active)throw Error('ROUTE ENGINE NOT INITIALIZED');
  let previous=null;
  if(this.routeCursor>0)previous=this.active.route[this.routeCursor-1];
  while(this.routeCursor<this.active.route.length){
   const r=this.active.route[this.routeCursor++],k=key(r);if(this.quarantine.has(k)){const replacement=await this.takeReserve(previous);if(replacement){this.maybePrepareNext();return replacement}continue}
   this.maybePrepareNext();return r
  }
  await this.promoteNext();
  return this.nextDestination()
 },
 maybePrepareNext(){
  const remaining=this.active.route.length-this.routeCursor;
  if(remaining<=C.REPLENISH_AT&&!this.nextGeneration){const eligibleRecords=this.catalog.records.filter(r=>!this.quarantine.has(key(r)));this.nextGeneration=Promise.resolve(plan(eligibleRecords))}
 },
 async promoteNext(){
  if(!this.nextGeneration)this.maybePrepareNext();
  if(!this.nextGeneration){const eligibleRecords=this.catalog.records.filter(r=>!this.quarantine.has(key(r)));this.nextGeneration=Promise.resolve(plan(eligibleRecords))}
  this.phase='MONTE_CARLO';this.active=await this.nextGeneration;this.nextGeneration=null;this.generation++;this.routeCursor=0;this.reserveCursor=0;
  this.exclusion.clear();for(const r of this.active.sample){const k=key(r);if(k)this.exclusion.add(k)}
  this.phase='READY'
 },
 async recheckQuarantine(){
  const now=Date.now();for(const [k,q] of [...this.quarantine]){if(q.nextCheck>now)continue;const probe=await urlAlive(q.record);if(probe.ok)this.quarantine.delete(k);else this.quarantine.set(k,{...q,reason:probe.reason,failureCount:q.failureCount+1,lastChecked:now,nextCheck:now+C.QUARANTINE_RECHECK_MS})}
 },
 startQuarantineRecheck(){if(this.recheckTimer)return;this.recheckTimer=setInterval(()=>this.recheckQuarantine().catch(error=>log('QUARANTINE RECHECK FAILED',clean(error?.message))),C.QUARANTINE_RECHECK_MS)},
 snapshot(){return Object.freeze({runtime:VERSION,phase:this.phase,catalog:this.catalog?.records.length??0,active:this.active?.route.length??0,activeRemaining:Math.max(0,(this.active?.route.length??0)-this.routeCursor),reserve:this.active?.reserve.length??0,reserveRemaining:Math.max(0,(this.active?.reserve.length??0)-this.reserveCursor),generation:this.generation,quarantined:this.quarantine.size,excluded:this.exclusion.size,nextGenerationPending:Boolean(this.nextGeneration),solveTimeMs:this.active?.solveTimeMs??null,sampleAttempt:this.active?.sampleAttempt??null,solverAttempt:this.active?.solverAttempt??null})}
};
global.GalaxyRouteEngine=Runtime;
})(typeof window!=='undefined'?window:globalThis);
