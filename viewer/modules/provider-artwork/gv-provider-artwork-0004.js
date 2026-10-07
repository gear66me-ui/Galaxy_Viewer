(()=>{'use strict';
const VERSION='0004';
const ART='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/artwork/';
const ICONS=Object.freeze({
  HUBBLE:'Hubble/Hubble.jpg',
  JWST:'JWST/JWST.jpeg',
  CHANDRA:'Chandra/Chandra.jpg',
  ESO:'ESO/ESO.jpg',
  NOIRLAB:'NoirLabs/NOIRLab.jpg',
  SPITZER:'Spitzer/Spitzer.jpg'
});
const icon=provider=>{
  const key=String(provider||'').trim().toUpperCase();
  const path=ICONS[key];
  return path?ART+path:'';
};
globalThis.GVProviderArtwork=Object.freeze({VERSION,icon,icons:Object.freeze({...ICONS})});
})();