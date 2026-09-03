const SOURCE = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/orientation-review/gv-triangle-consensus-sandbox-0006.html';
const BASE_SOURCE = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/fcf413428accb443b7d29ddb880493252bf98729/viewer/image-databases/master-database/orientation-review/gv-astrometry-sandbox-0010.html';
const OLD_WORKER = 'https://gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev';

function corsHeaders(extra = {}) {
  return {
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'GET,HEAD,OPTIONS',
    'access-control-allow-headers': '*',
    ...extra
  };
}

function patchTriangleHtml(input, origin) {
  let html = input;
  let solvePatched = false;
  let gatePatched = false;

  const solveRe = /function solveTriangles\(S,T\)\{[\s\S]*?return\{best,tests,candidates,sourceTriangles:ST\.length,targetTriangles:TT\.length\}\}/;
  const newSolve = `function solveTriangles(S,T){
const ST=triangles(S),TT=triangles(T),bins=new Map();
for(const t of TT){const key=Math.round(t.r1*100)+'|'+Math.round(t.r2*100);if(!bins.has(key))bins.set(key,[]);bins.get(key).push(t)}
let tests=0,candidates=0;const pool=[];
for(const s of ST){const a=Math.round(s.r1*100),b=Math.round(s.r2*100);for(let da=-1;da<=1;da++)for(let db=-1;db<=1;db++){const L=bins.get((a+da)+'|'+(b+db));if(!L)continue;for(const t of L){if(Math.abs(s.r1-t.r1)>.012||Math.abs(s.r2-t.r2)>.012||s.hand!==t.hand)continue;candidates++;const so=s.order,to=t.order,tr=tr2(S[so[0]],S[so[1]],T[to[0]],T[to[1]]);if(!tr)continue;const third=dist(ap(tr,S[so[2]]),T[to[2]]);if(third>3.5)continue;tests++;const ev=evalCandidate(tr,S,T,so,to,7);pool.push({...tr,...ev,defS:so,defT:to,triResidual:third,srcTri:s,tgtTri:t,rotDeg:norm180(tr.rot*180/Math.PI)})}}}
function ad(a,b){let d=Math.abs(a-b)%360;return d>180?360-d:d}
let best=null,bestClusterScore=-Infinity;
for(const seed of pool){const group=pool.filter(c=>ad(c.rotDeg,seed.rotDeg)<=2&&Math.abs(c.scale/seed.scale-1)<=.03);if(group.length<3)continue;
 const srcKeys=new Set(),tgtKeys=new Set(),pairVotes=new Map();let maxRot=0,minScale=Infinity,maxScale=-Infinity;
 for(const c of group){srcKeys.add([...c.defS].sort((x,y)=>x-y).join(','));tgtKeys.add([...c.defT].sort((x,y)=>x-y).join(','));maxRot=Math.max(maxRot,ad(c.rotDeg,seed.rotDeg));minScale=Math.min(minScale,c.scale);maxScale=Math.max(maxScale,c.scale);for(let n=0;n<c.defS.length;n++){const k=c.defS[n]+'>'+c.defT[n];pairVotes.set(k,(pairVotes.get(k)||0)+1)}}
 const supportTriangles=Math.min(srcKeys.size,tgtKeys.size),consensusPairs=[...pairVotes.values()].filter(v=>v>=2).length,scaleSpreadFrac=(maxScale-minScale)/Math.max(1e-9,seed.scale);
 if(supportTriangles<3||consensusPairs<4||maxRot>2||scaleSpreadFrac>.03)continue;
 const rep=[...group].sort((x,y)=>y.score-x.score)[0],clusterScore=supportTriangles*100000+consensusPairs*20000+rep.score-maxRot*500-scaleSpreadFrac*50000;
 if(clusterScore>bestClusterScore){bestClusterScore=clusterScore;best={...rep,supportTriangles,consensusPairs,rotationSpreadDeg:maxRot,scaleSpreadFrac,clusterSize:group.length,clusterScore}}
}
return{best,tests,candidates,sourceTriangles:ST.length,targetTriangles:TT.length}}`;
  if (solveRe.test(html)) { html = html.replace(solveRe, newSolve); solvePatched = true; }

  const gateRe = /function passGate\(b,post=false\)\{if\(!b\)return false;return b\.holdout>=3&&b\.holdRms<=\(post\?4:4\.5\)&&b\.recFrac>=\.80&&b\.triResidual<=3\.5&&b\.matches\.length>=6\}/;
  const newGate = `function passGate(b,post=false){if(!b)return false;return b.holdout>=3&&b.holdRms<=(post?4:4.5)&&b.recFrac>=.80&&b.triResidual<=3.5&&b.matches.length>=6&&b.supportTriangles>=3&&b.consensusPairs>=4&&b.rotationSpreadDeg<=2&&b.scaleSpreadFrac<=.03}`;
  if (gateRe.test(html)) { html = html.replace(gateRe, newGate); gatePatched = true; }

  html = html.split(BASE_SOURCE).join(origin + '/base');
  html = html.split(OLD_WORKER).join(origin);

  if (!solvePatched || !gatePatched) {
    throw new Error('ECO-072 patch seam missing: solve='+solvePatched+' gate='+gatePatched);
  }
  return html;
}

function patchBaseHtml(input, origin) {
  let html = input;
  const surveyOld = "currentSurveyId=override||surveyRanking[0]?.id||'P/DSS2/color';";
  const surveyNew = "currentSurveyId=override||'P/DSS2/color';";
  if (!html.includes(surveyOld)) throw new Error('ECO-072 base DSS2 seam missing');
  html = html.replace(surveyOld, surveyNew);
  html = html.split(OLD_WORKER).join(origin);
  return html;
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (url.pathname === '/api/image') {
      const target = url.searchParams.get('url');
      if (!target || !/^https?:\/\//i.test(target)) {
        return new Response('Missing or invalid image url', { status: 400, headers: corsHeaders({ 'content-type': 'text/plain; charset=utf-8' }) });
      }
      try {
        const upstream = await fetch(target, { redirect: 'follow', headers: { 'User-Agent': 'Galaxy-Viewer-Triangle-Consensus-0006', 'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' } });
        if (!upstream.ok) return new Response('Image upstream HTTP ' + upstream.status, { status: 502, headers: corsHeaders({ 'content-type': 'text/plain; charset=utf-8' }) });
        return new Response(upstream.body, { status: 200, headers: corsHeaders({ 'content-type': upstream.headers.get('content-type') || 'application/octet-stream', 'cache-control': 'public, max-age=3600', 'x-gv-image-proxy': 'triangle-consensus-0006' }) });
      } catch (err) {
        return new Response('Image proxy fetch failed: ' + String(err?.message || err), { status: 502, headers: corsHeaders({ 'content-type': 'text/plain; charset=utf-8' }) });
      }
    }

    if (url.pathname === '/base') {
      try {
        const upstream = await fetch(BASE_SOURCE, { cf: { cacheTtl: 60, cacheEverything: true }, headers: { 'User-Agent': 'Galaxy-Viewer-Triangle-Consensus-0006' } });
        if (!upstream.ok) throw new Error('base HTTP ' + upstream.status);
        const html = patchBaseHtml(await upstream.text(), url.origin);
        return new Response(html, { status: 200, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store, max-age=0', 'x-gv-base': '0010-dss2' } });
      } catch (err) {
        return new Response('Triangle Consensus base patch failed: ' + String(err?.message || err), { status: 500, headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store' } });
      }
    }

    if (url.pathname !== '/' && url.pathname !== '/index.html') return new Response('Not Found', { status: 404 });

    const upstream = await fetch(SOURCE, { cf: { cacheTtl: 60, cacheEverything: true }, headers: { 'User-Agent': 'Galaxy-Viewer-Triangle-Consensus-0006' } });
    if (!upstream.ok) return new Response('Triangle Consensus Sandbox source unavailable: HTTP ' + upstream.status, { status: 502, headers: { 'content-type': 'text/plain; charset=utf-8' } });

    try {
      const html = patchTriangleHtml(await upstream.text(), url.origin);
      return new Response(html, { status: 200, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store, max-age=0', 'x-gv-sandbox': 'triangle-consensus-0006', 'x-gv-image-proxy': 'same-origin', 'x-gv-eco': 'ECO-072-multi-triangle-consensus-dss2-base' } });
    } catch (err) {
      return new Response('Triangle Consensus ECO-072 patch failed: ' + String(err?.message || err), { status: 500, headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store' } });
    }
  }
};
