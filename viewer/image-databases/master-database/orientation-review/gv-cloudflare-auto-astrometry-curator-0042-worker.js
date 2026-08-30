import {htmlResponse as baseHtmlResponse} from './gv0028-ui.js';
import {htmlResponse as gaiaHtmlResponse} from './gv0029-ui.js';
import {json,catalog,predictionsDisabled,predictionDiagnostics,image,solve,status,gaia} from './gv0029-api.js';

const REV='0042';
const BUILD_STAMP_COLOMBIA='2026-08-29 20:42:00 COT';

function scriptsOf(html){
  const out=[];let pos=0,i=0;
  while(true){
    const s=html.indexOf('<script',pos);if(s<0)break;
    const open=html.indexOf('>',s),e=html.indexOf('</script>',open);if(open<0||e<0)break;
    const code=html.slice(open+1,e);
    out.push({
      index:i++,length:code.length,
      markers:{
        predictions:/PREDICTIONS_URL/i.test(code),
        showCurrent:/showCurrent/i.test(code),currentRot:/currentRot/i.test(code),hardAim:/hardAim/i.test(code),
        boot:/boot\s*\(/i.test(code),analyzeBtn:/analyzeBtn/i.test(code),analyzeCurrent:/analyzeCurrent/i.test(code),
        applyState:/applyState/i.test(code),setRot:/setRot/i.test(code),machine:/MACHINE|PREDICTION/i.test(code)
      },
      head:code.slice(0,240),tail:code.slice(-240)
    });
    pos=e+9;
  }
  return out;
}
function snippets(html,terms){
  const out={};
  for(const term of terms){
    const re=new RegExp(term,'i'),m=re.exec(html);
    if(!m){out[term]=null;continue}
    const a=Math.max(0,m.index-220),b=Math.min(html.length,m.index+520);
    out[term]=html.slice(a,b);
  }
  return out;
}
async function debugCore(){
  const [br,gr]=await Promise.all([baseHtmlResponse(),gaiaHtmlResponse()]);
  const base=await br.text(),g=await gr.text();
  return json({ok:true,revision:REV,build_stamp_colombia:BUILD_STAMP_COLOMBIA,
    base:{length:base.length,doctype:base.slice(0,100),scripts:scriptsOf(base),snippets:snippets(base,['predictions','showCurrent','currentRot','hardAim','analyzeBtn','applyState','setRot','boot\\s*\\(','APPLY MACHINE'])},
    gaia:{length:g.length,scripts:scriptsOf(g),snippets:snippets(g,['oldShow29','analyze0029','GAIA STELLAR','analyzeBtn'])}
  });
}
async function page(){
  const r=await baseHtmlResponse();const h=await r.text();
  const headers=new Headers(r.headers);headers.set('cache-control','no-store');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-mode','diagnostic-baseline-0028');
  return new Response(h,{status:r.status,headers});
}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page();if(u.pathname==='/api/debug-core')return debugCore();if(u.pathname==='/api/health')return json({ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0042',build_stamp_colombia:BUILD_STAMP_COLOMBIA,mode:'diagnostic-baseline-0028',note:'page intentionally serves untouched decompressed 0028 while /api/debug-core reports actual runtime script structure'});if(u.pathname==='/api/catalog')return catalog(u);if(u.pathname==='/api/predictions')return predictionsDisabled();if(u.pathname==='/api/predictions-diagnostic')return predictionDiagnostics();if(u.pathname==='/api/image')return image(u,request);if(u.pathname==='/api/solve')return solve(request,env);if(u.pathname==='/api/status')return status(u);if(u.pathname==='/api/gaia')return gaia(u);return new Response('Not found',{status:404})}};
