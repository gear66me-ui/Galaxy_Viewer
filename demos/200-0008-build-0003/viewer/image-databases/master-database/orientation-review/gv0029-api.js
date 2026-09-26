import * as base from './gv0028-api.js';
export const REV='0029';
export const json=base.json;

async function retag(response){
  const ct=(response.headers.get('content-type')||'').toLowerCase();
  if(!ct.includes('application/json')) return response;
  let body;
  try{body=await response.json()}catch{return response}
  if(body&&typeof body==='object'){
    body.revision=REV;
    if(body.result&&typeof body.result==='object') body.result.revision=REV;
  }
  const headers=new Headers(response.headers);
  headers.set('content-type','application/json; charset=utf-8');
  headers.set('cache-control','no-store');
  return new Response(JSON.stringify(body),{status:response.status,headers});
}

export async function catalog(u){return retag(await base.catalog(u))}
export async function image(u,request){return base.image(u,request)}
export async function solve(request,env){return retag(await base.solve(request,env))}
export async function status(u){return retag(await base.status(u))}
export async function gaia(u){return retag(await base.gaia(u))}

export function predictionsDisabled(){
  return json({ok:true,revision:REV,predictions:[],automation:false,reason:'Legacy SIFT/RANSAC predictions are prohibited from driving Aladin in 0029.'});
}

export async function predictionDiagnostics(){
  const r=await base.predictions();
  let body={};
  try{body=await r.json()}catch{}
  return json({
    ok:r.ok,
    revision:REV,
    diagnostic_only:true,
    automation:false,
    method:'legacy-sift-ransac',
    warning:'Diagnostic evidence only. This endpoint is never an acceptance source and must never move Aladin.',
    predictions:Array.isArray(body.predictions)?body.predictions:[],
    upstream_error:body.error||null
  },r.ok?200:r.status);
}
