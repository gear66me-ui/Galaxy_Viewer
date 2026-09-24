/*
RANDOM GALAXY 0240
PRESENTATION-ONLY RESET BASELINE.
No sky-motion, geometry, image-registration, route, queue, or preparation authority.
This module owns only Random Galaxy / HD banner presentation artwork.
*/
(function(global){
  'use strict';

  const VERSION='0240';
  const instances=new WeakMap();

  const FONT_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf';
  const PROVIDER_ICON_URLS=Object.freeze({
    chandra:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Chandra/Chandra.jpg',
    eso:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/ESO/ESO.jpg',
    euclid:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Euclid/Euclid.jpg',
    galex:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/GALEX/GALEX.jpg',
    herschel:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Herschel/Herschel.jpg',
    hubble:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble.jpg',
    jwst:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/JWST/JWST.jpg',
    nrao:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NRAO/NRAO.jpg',
    noirlab:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NoirLabs/NOIRLab.jpg',
    nustar:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NuSTAR/NuSTAR.jpg',
    spitzer:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Spitzer/Spitzer.jpg'
  });

  function clean(value){
    return String(value==null?'':value).replace(/\s+/g,' ').trim();
  }

  function providerKey(value){
    const text=clean(value).toLowerCase();
    if(/noir|gemini|noao/.test(text))return 'noirlab';
    if(/hubble|hst/.test(text))return 'hubble';
    if(/james webb|webb|jwst/.test(text))return 'jwst';
    for(const key of Object.keys(PROVIDER_ICON_URLS)){
      if(text.includes(key))return key;
    }
    return '';
  }

  function styleElement(){
    const style=document.createElement('style');
    style.textContent=`
@font-face{font-family:"GV Space";src:url("${FONT_URL}") format("opentype");font-display:swap}
.gvrg-root,.gvrg-root *{box-sizing:border-box}
.gvrg-root{position:absolute;inset:0;z-index:9990;pointer-events:none;font-family:"GV Space",sans-serif;color:#eefaff}
.gvrg-card{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);width:min(94vw,720px);padding:10px 12px;border:1px solid rgba(124,203,255,.72);border-radius:10px;background:linear-gradient(145deg,rgba(4,17,43,.94),rgba(8,39,74,.94));box-shadow:0 0 18px rgba(64,165,255,.24);opacity:0;visibility:hidden;transition:opacity .18s ease;pointer-events:auto}
.gvrg-card.gvrg-visible{opacity:1;visibility:visible}
.gvrg-title{text-align:center;font-size:15px;letter-spacing:1.3px;color:#eaf8ff;text-shadow:0 0 7px rgba(124,203,255,.5)}
.gvrg-info{margin-top:7px;text-align:center;font:10px/1.45 system-ui,sans-serif;color:#cfeeff}
.gvrg-actions{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:9px}
.gvrg-button{border:1px solid rgba(124,203,255,.8);border-radius:7px;background:linear-gradient(145deg,#0a2a55,#12457d);color:#f3fbff;padding:8px 12px;font-family:"GV Space",sans-serif;letter-spacing:.7px}
.gvrg-provider{width:42px;height:42px;padding:2px;overflow:hidden}
.gvrg-provider img{display:block;width:100%;height:100%;border-radius:5px;object-fit:cover}
.gvrg-hd{position:absolute;inset:0;z-index:10020;display:none;background:#020711;pointer-events:auto}
.gvrg-hd.gvrg-visible{display:flex;flex-direction:column}
.gvrg-hd-banner{flex:0 0 auto;min-height:94px;padding:12px;border-bottom:1px solid rgba(124,203,255,.5);background:linear-gradient(145deg,#06162e,#0a315b);text-align:center}
.gvrg-hd-title{font-size:17px;letter-spacing:1.4px}
.gvrg-hd-info{margin-top:7px;font:11px/1.45 system-ui,sans-serif;color:#d9f1ff}
.gvrg-hd-image{position:relative;flex:1;min-height:0;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#000}
.gvrg-hd-image img{display:block;max-width:100%;max-height:100%;object-fit:contain}
.gvrg-hd-footer{display:flex;justify-content:center;gap:10px;padding:10px;background:linear-gradient(145deg,#06162e,#0a315b)}
`;
    return style;
  }

  class GalaxyRandomGalaxy{
    constructor(options={}){
      if(!(options.host instanceof Element))
        throw new TypeError('GalaxyRandomGalaxy requires a DOM Element host.');
      if(instances.has(options.host))
        throw new Error('GalaxyRandomGalaxy is already mounted on this host.');

      this.host=options.host;
      this.destroyed=false;
      this.root=this.#build();
      this.host.appendChild(this.root);
      instances.set(this.host,this);
    }

    #build(){
      const root=document.createElement('div');
      root.className='gvrg-root';
      root.dataset.gvrgVersion=VERSION;
      root.appendChild(styleElement());

      const card=document.createElement('section');
      card.className='gvrg-card';
      this.card=card;

      const title=document.createElement('div');
      title.className='gvrg-title';
      this.title=title;

      const info=document.createElement('div');
      info.className='gvrg-info';
      this.info=info;

      const actions=document.createElement('div');
      actions.className='gvrg-actions';

      const view=document.createElement('button');
      view.type='button';
      view.className='gvrg-button';
      view.textContent='VIEW HD IMAGE';
      this.viewHdButton=view;

      const provider=document.createElement('button');
      provider.type='button';
      provider.className='gvrg-button gvrg-provider';
      provider.setAttribute('aria-label','VIEW HD IMAGE');
      const providerImage=document.createElement('img');
      providerImage.alt='';
      provider.appendChild(providerImage);
      this.providerImage=providerImage;

      actions.append(view,provider);
      card.append(title,info,actions);

      const hd=document.createElement('section');
      hd.className='gvrg-hd';
      this.hd=hd;

      const hdBanner=document.createElement('div');
      hdBanner.className='gvrg-hd-banner';
      const hdTitle=document.createElement('div');
      hdTitle.className='gvrg-hd-title';
      this.hdTitle=hdTitle;
      const hdInfo=document.createElement('div');
      hdInfo.className='gvrg-hd-info';
      this.hdInfo=hdInfo;
      hdBanner.append(hdTitle,hdInfo);

      const imageHost=document.createElement('div');
      imageHost.className='gvrg-hd-image';
      const image=document.createElement('img');
      image.alt='';
      this.hdImage=image;
      imageHost.appendChild(image);

      const footer=document.createElement('div');
      footer.className='gvrg-hd-footer';
      const back=document.createElement('button');
      back.type='button';
      back.className='gvrg-button';
      back.textContent='BACK TO SKY';
      this.backButton=back;
      footer.appendChild(back);

      hd.append(hdBanner,imageHost,footer);
      root.append(card,hd);

      view.addEventListener('click',()=>this.showHD());
      provider.addEventListener('click',()=>this.showHD());
      back.addEventListener('click',()=>this.backToSky());
      return root;
    }

    setBanner(data={}){
      const name=clean(data.name||data.commonName||data.designation||'GALAXY');
      const info=clean(data.info||'');
      this.title.textContent=name.toUpperCase();
      this.hdTitle.textContent=name.toUpperCase();
      this.info.textContent=info;
      this.hdInfo.textContent=info;

      const key=providerKey(data.provider||data.telescope);
      const icon=PROVIDER_ICON_URLS[key]||'';
      this.providerImage.src=icon;
      this.providerImage.hidden=!icon;

      const image=clean(data.imageUrl||data.hdUrl);
      if(image)this.hdImage.src=image;
      else this.hdImage.removeAttribute('src');

      this.card.classList.add('gvrg-visible');
      return this;
    }

    clearBanner(){
      this.card.classList.remove('gvrg-visible');
      this.backToSky();
      this.hdImage.removeAttribute('src');
      return this;
    }

    showHD(){
      this.hd.classList.add('gvrg-visible');
      return this;
    }

    backToSky(){
      this.hd.classList.remove('gvrg-visible');
      return this;
    }

    destroy(){
      if(this.destroyed)return;
      this.destroyed=true;
      this.root.remove();
      instances.delete(this.host);
    }

    static mount(host,options={}){
      const existing=instances.get(host);
      if(existing&&!existing.destroyed)return existing;
      return new GalaxyRandomGalaxy({...options,host});
    }
  }

  GalaxyRandomGalaxy.VERSION=VERSION;
  GalaxyRandomGalaxy.PROVIDER_ICON_URLS=PROVIDER_ICON_URLS;
  global.GalaxyRandomGalaxy=GalaxyRandomGalaxy;
})(window);
