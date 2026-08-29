import {htmlResponse} from './gv0029-ui.js';
import {REV,json,catalog,predictionsDisabled,predictionDiagnostics,image,solve,status,gaia} from './gv0029-api.js';

export default {async fetch(request,env){
  const u=new URL(request.url);
  if(u.pathname==='/'||u.pathname==='/index.html') return htmlResponse();
  if(u.pathname==='/api/health') return json({
    ok:true,
    revision:REV,
    service:'gv-cloudflare-auto-astrometry-curator-0029',
    key_source:'server-secret',
    key_configured:Boolean(String(env?.ASTROMETRY_API_KEY||'').trim()),
    architecture:'gaia-stellar-gated',
    fail_closed:true,
    thresholds:{min_stellar_inliers:15,min_inlier_ratio:.60,max_rms_px:2.5,max_centroid_residual_px:2.0,max_rotation_disagreement_deg:5,max_fov_relative_disagreement:.15,max_center_disagreement_fraction_of_fov:.10},
    features:['standalone-0029','catalog-navigation','source-and-live-data','manual-rotation','legacy-sift-automation-disabled','point-source-detection','gaia-dr3-vizier','triangle-asterism-ransac','mandatory-stellar-validation-gate','astrometry-independent-cross-check','fail-closed-disagreement','match-circles-and-ids-no-lines','human-gold-curation','diagnostics']
  });
  if(u.pathname==='/api/catalog') return catalog(u);
  if(u.pathname==='/api/predictions') return predictionsDisabled();
  if(u.pathname==='/api/predictions-diagnostic') return predictionDiagnostics();
  if(u.pathname==='/api/image') return image(u,request);
  if(u.pathname==='/api/solve') return solve(request,env);
  if(u.pathname==='/api/status') return status(u);
  if(u.pathname==='/api/gaia') return gaia(u);
  return new Response('Not found',{status:404});
}};
