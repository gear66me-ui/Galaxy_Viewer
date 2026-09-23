/*
AVM 0053-BG HOTFIX LOADER — NAVIGATION CAMERA AUTHORITY FENCE
- Loads the restored real AVM 0053 source from fixed commit c5472d4889be2f4851e4d6e776722689cf3d8e0e.
- Keeps GalaxyViewerAvmOverlayLab.VERSION === "0053" for existing BD viewer compatibility.
- Suppresses AVM camera writers only: prepared authority camera, callback RA/Dec camera, and AVM camera roll.
- AVM may still stage/display the overlay; Navigation remains sole owner of Aladin center/FOV/rotation.
*/
(()=>{
  'use strict';
  const RAW_0053_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/c5472d4889be2f4851e4d6e776722689cf3d8e0e/viewer/modules/lab/gv-avm-overlay-lab-0053.js?bg=nav-camera-authority-20260923';
  const trace=(code,detail={})=>{try{globalThis.GalaxyViewerDiagnostics?.recordAvm?.(code,detail)}catch(_){}};
  function fail(message){trace('AVM_0053BG_HOTFIX_FAIL',{message:String(message||'')});throw new Error(String(message||'AVM 0053-BG HOTFIX FAILED'));}
  function replaceOne(source,pattern,replacement,label){
    const next=source.replace(pattern,replacement);
    if(next===source)fail('PATCH MISS: '+label);
    trace('AVM_0053BG_PATCH_OK',{label});
    return next;
  }
  function patch(source){
    let s=String(source||'');
    if(!/const VERSION=\"0053\"/.test(s)&&!/const VERSION='0053'/.test(s))fail('VERSION MARKER MISSING');

    s=replaceOne(
      s,
      /function applyPreparedAuthorityCamera\(d,key\)\{[\s\S]*?\}function catalogSummary\(d\)\{/,
      `function applyPreparedAuthorityCamera(d,key){const before=cameraSnapshot('before-prepared-authority-camera-suppressed',d);const camera=finiteValue(d?.avmCameraRotation);trace('AVM_0053BG_PREPARED_AUTHORITY_CAMERA_SUPPRESSED',{key,camera,applied:false,before,catalog:catalogSummary(d)});return {source:'avmCameraRotation',camera,applied:false,before,after:before,suppressed:true}}function catalogSummary(d){`,
      'applyPreparedAuthorityCamera'
    );

    s=replaceOne(
      s,
      /function applyAvmCallbackCamera\(ra,dec,fov,d,key\)\{[\s\S]*?\}function applyAvmCameraRoll\(d,key\)\{/,
      `function applyAvmCallbackCamera(ra,dec,fov,d,key){const before=cameraSnapshot('before-callback-camera-suppressed',d);const callbackFov=finiteValue(fov);const catalog=catalogSummary(d);const cra=finiteValue(catalog.ra),cdec=finiteValue(catalog.dec),ara=finiteValue(ra),adec=finiteValue(dec);let deltaDeg=null;if(cra!==null&&cdec!==null&&ara!==null&&adec!==null){const R=Math.PI/180,a1=cra*R,a2=ara*R,b1=cdec*R,b2=adec*R;const cos=Math.sin(b1)*Math.sin(b2)+Math.cos(b1)*Math.cos(b2)*Math.cos(a1-a2);deltaDeg=Math.acos(Math.max(-1,Math.min(1,cos)))/R}trace('AVM_0053BG_CALLBACK_CAMERA_SUPPRESSED',{key,ra:ara,dec:adec,fov:callbackFov,catalogRa:cra,catalogDec:cdec,deltaDeg,didCenter:false,didFov:false,before,catalog});return {didCenter:false,didFov:false,callbackFov,before,after:before,suppressed:true,deltaDeg}}function applyAvmCameraRoll(d,key){`,
      'applyAvmCallbackCamera'
    );

    s=replaceOne(
      s,
      /function applyAvmCameraRoll\(d,key\)\{[\s\S]*?\}let interactionDiagnosticInstalled=/,
      `function applyAvmCameraRoll(d,key){const rot=avmRotationSource(d);const before=cameraSnapshot('before-avm-camera-roll-suppressed',d);trace('AVM_0053BG_CAMERA_ROLL_SUPPRESSED',{key,source:rot.source,avmRotation:rot.value,camera:rot.camera,applied:false,before,catalog:catalogSummary(d)});return {source:rot.source,avmRotation:rot.value,camera:rot.camera,applied:false,before,after:before,suppressed:true}}let interactionDiagnosticInstalled=`,
      'applyAvmCameraRoll'
    );

    s=s.replace(
      `trace("AVM_LAB_BOOT",{version:VERSION});`,
      `trace("AVM_LAB_BOOT",{version:VERSION,hotfix:'0053-BG-navigation-camera-authority-fence'});trace('AVM_0053BG_HOTFIX_ACTIVE',{version:VERSION});`
    );

    return s;
  }

  trace('AVM_0053BG_RAW_FETCH_START',{url:RAW_0053_URL});
  fetch(RAW_0053_URL,{cache:'no-store'})
    .then(response=>{
      if(!response.ok)throw new Error('RAW AVM 0053 HTTP '+response.status);
      return response.text();
    })
    .then(source=>{
      const patched=patch(source);
      trace('AVM_0053BG_PATCHED_EVAL_START',{bytes:patched.length});
      (0,eval)(patched+'\n//# sourceURL=gv-avm-overlay-lab-0053-bg-hotfix-eval.js');
      trace('AVM_0053BG_PATCHED_EVAL_OK',{version:String(globalThis.GalaxyViewerAvmOverlayLab?.VERSION||'')});
    })
    .catch(error=>{
      trace('AVM_0053BG_LOAD_FAIL',{message:String(error?.message||error||'')});
      console.error('AVM 0053-BG hotfix load failure',error);
    });
})();
