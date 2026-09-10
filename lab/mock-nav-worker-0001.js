'use strict';

const fs=require('fs');
const path=require('path');
const {Worker}=require('worker_threads');

const navPath=path.resolve(process.argv[2]);
const workerPath=path.resolve(process.argv[3]);

if(!fs.existsSync(navPath)) throw new Error('NAV0004 MISSING');
if(!fs.existsSync(workerPath)) throw new Error('WORKER0001 MISSING');

const catalog=Array.from({length:130},(_,i)=>({
  provider:'MOCK',
  id:`MOCK-${i}`,
  name:`Mock ${i}`,
  ra:(i*360/130)%360,
  dec:0,
  fovDegrees:1,
  aladinRotation:0
}));

const anchor={
  provider:'MOCK',
  id:'ANCHOR',
  name:'Anchor',
  ra:180,
  dec:0,
  fovDegrees:1,
  aladinRotation:0
};

const bootstrap=`
'use strict';
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const {parentPort,workerData}=require('worker_threads');

global.self=globalThis;
self.postMessage=message=>parentPort.postMessage(message);
global.importScripts=(...urls)=>{
  for(const url of urls){
    const target=path.resolve(path.dirname(workerData.workerPath),url);
    const source=fs.readFileSync(target,'utf8');
    vm.runInThisContext(source,{filename:target});
  }
};

const workerSource=fs.readFileSync(workerData.workerPath,'utf8');
vm.runInThisContext(workerSource,{filename:workerData.workerPath});

parentPort.on('message',data=>{
  if(typeof self.onmessage!=='function')
    throw new Error('WORKER onmessage NOT INSTALLED');
  self.onmessage({data});
});
`;

const thread=new Worker(bootstrap,{
  eval:true,
  workerData:{workerPath}
});

let resultReceived=false;
let heartbeatTicks=0;

const heartbeat=setInterval(()=>{
  heartbeatTicks++;
},1);

const resultPromise=new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>{
    reject(new Error('MOCK WORKER TIMEOUT'));
  },60000);

  thread.once('error',error=>{
    clearTimeout(timer);
    reject(error);
  });

  thread.on('message',data=>{
    if(data?.type!=='PLAN_RESULT') return;
    resultReceived=true;
    clearTimeout(timer);
    resolve(data);
  });
});

thread.postMessage({
  type:'PLAN',
  id:'mock-nav-worker-0001',
  catalog,
  anchorRecord:anchor
});

(async()=>{
  try{
    await new Promise(resolve=>setTimeout(resolve,5));
    const heartbeatBeforeResult=!resultReceived && heartbeatTicks>0;

    const result=await resultPromise;
    clearInterval(heartbeat);
    await thread.terminate();

    console.log('WORKER RESPONSE RECEIVED: PASS');
    console.log('WORKER OK:',result.ok===true?'PASS':'FAIL');
    console.log('WORKER VERSION:',result.workerVersion);
    console.log('NAVIGATION VERSION:',result.navigationVersion);
    console.log('POOL SIZE:',result.poolSize);
    console.log('ROUTE LENGTH:',result.routeLength);
    console.log('ROUTE KEYS:',Array.isArray(result.routeKeys)?result.routeKeys.length:0);
    console.log('DISCARDED KEYS:',Array.isArray(result.discardedKeys)?result.discardedKeys.length:0);
    console.log('SOLVE TIME MS:',result.solveTimeMs);
    console.log('MAIN THREAD HEARTBEAT TICKS:',heartbeatTicks);
    console.log('MAIN THREAD HEARTBEAT BEFORE RESULT:',heartbeatBeforeResult?'PASS':'FAIL');

    if(result.ok!==true) throw new Error(result.error||'WORKER RESULT NOT OK');
    if(result.workerVersion!=='0001') throw new Error('WORKER VERSION MISMATCH');
    if(result.navigationVersion!=='0004') throw new Error('NAVIGATION VERSION MISMATCH');
    if(result.poolSize!==130) throw new Error('POOL SIZE MISMATCH');
    if(result.routeLength!==100) throw new Error('ROUTE LENGTH MISMATCH');
    if(!Array.isArray(result.routeKeys)||result.routeKeys.length!==100)
      throw new Error('ROUTE KEYS LENGTH MISMATCH');
    if(new Set(result.routeKeys).size!==100)
      throw new Error('ROUTE KEYS NOT UNIQUE');
    if(!heartbeatBeforeResult)
      throw new Error('MAIN THREAD HEARTBEAT DID NOT RUN BEFORE RESULT');

    console.log('130->100 ROUTE VALIDATION: PASS');
    console.log('OFF-MAIN-THREAD RESPONSIVENESS: PASS');
    console.log('ACTUAL WORKER MOCK: PASS');
  }catch(error){
    clearInterval(heartbeat);
    try{await thread.terminate();}catch(_){}
    console.error('ACTUAL WORKER MOCK: FAIL');
    console.error(String(error?.stack||error));
    process.exitCode=1;
  }
})();
