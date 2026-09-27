(()=>{'use strict';
const ORIGINAL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/destination-presentation/gv-destination-presentation.js';
const bust=url=>url+(url.includes('?')?'&':'?')+'gvdp0049hotfix='+Date.now().toString(36);
function fetchOriginal(url){
  const x=new XMLHttpRequest();
  x.open('GET',bust(url),false);
  x.send(null);
  if(x.status<200||x.status>=300)throw new Error('DESTINATION PRESENTATION HOTFIX FETCH FAILED: HTTP '+x.status);
  return x.responseText;
}
let s=fetchOriginal(ORIGINAL);
const handlerStart="archiveButton.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();const url=clean(destination?.sourceUrl);if(!/^https:\\/\\//i.test(url))return;";
const handlerEnd="},true);archiveBack.addEventListener";
const handlerAt=s.indexOf(handlerStart);
const handlerEndAt=handlerAt<0?-1:s.indexOf(handlerEnd,handlerAt);
if(handlerAt<0||handlerEndAt<0)throw new Error('DESTINATION PRESENTATION HOTFIX SIGNATURE MISSING: archive handler');
const directHandler="archiveButton.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();const url=clean(destination?.sourceUrl);if(!/^https:\\/\\//i.test(url))return;archiveButton.classList.add('gvdp-green');try{window.open(url,'_blank','noopener,noreferrer')}finally{setTimeout(()=>archiveButton.classList.remove('gvdp-green'),220)}},true);archiveBack.addEventListener";
s=s.slice(0,handlerAt)+directHandler+s.slice(handlerEndAt+handlerEnd.length);
const resizeOld="window.addEventListener('resize',()=>{if(hd.classList.contains('gvdp-open'))requestAnimationFrame(updateScale)});";
const resizeNew="const healHd=()=>{if(!hd.classList.contains('gvdp-open'))return;requestAnimationFrame(()=>{clampTransform();applyTransform();updateScale(false)})};window.addEventListener('resize',healHd);window.addEventListener('focus',healHd);window.addEventListener('pageshow',healHd);document.addEventListener('visibilitychange',()=>{if(!document.hidden)healHd()});";
if(!s.includes(resizeOld))throw new Error('DESTINATION PRESENTATION HOTFIX SIGNATURE MISSING: resize handler');
s=s.replace(resizeOld,resizeNew);
(0,eval)(s);
})();
