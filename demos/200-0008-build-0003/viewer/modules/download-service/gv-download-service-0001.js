/* Galaxy Viewer Download Service 0001 */
(function(global){
  "use strict";
  const existing=global.GalaxyViewerDownloads;
  if(existing&&typeof existing.saveJson==="function")return;
  const api=existing&&typeof existing==="object"?existing:{};
  api.saveJson=function(filename,json){
    const safe=String(filename||"galaxy-viewer.json").replace(/[\\/:*?"<>|]+/g,"_");
    const blob=new Blob([String(json??"")],{type:"application/json"});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;
    a.download=safe;
    a.style.display="none";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    return true;
  };
  global.GalaxyViewerDownloads=api;
})(window);
