(function(global){
  'use strict';

  const VERSION='0002';
  const GEOMETRY=Object.freeze({
    width:290,height:36,icrsdLeft:9,galLeft:19,dividerCenterX:64.5,
    xFieldLeft:78,xDecimalFromFieldLeft:37.5,lambdaCenterX:179.5,
    yFieldLeft:191,yDecimalFromFieldLeft:34.5
  });
  const FONT_URLS={
    spaceAge:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001',
    digits:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0004.otf?v=7K-centered-coordinate-digits-0004'
  };
  const instances=new WeakMap();

  function clamp(v,min,max){return Math.max(min,Math.min(max,Number(v)))}
  function formatLongitude(v){const [integer,fraction]=clamp(v,0,359.9999).toFixed(4).split('.');return {integer,fraction}}
  function formatLatitude(v){const n=clamp(v,-90,90),[integer,fraction]=Math.abs(n).toFixed(4).split('.');return {sign:n<0?'-':'',integer,fraction}}
  function createMeasureCanvas(){const c=document.createElement('canvas');c.width=1024;c.height=256;c.hidden=true;return c}
  function scan(ctx,canvas,text,font,size){
    const S=4,W=1024,H=256;canvas.width=W;canvas.height=H;ctx.clearRect(0,0,W,H);
    ctx.save();ctx.scale(S,S);ctx.font=`400 ${size}px "${font}"`;ctx.textBaseline='alphabetic';ctx.fillStyle='#fff';ctx.fillText(text,32,48);ctx.restore();
    const d=ctx.getImageData(0,0,W,H).data;let min=W,max=-1;
    for(let y=0;y<H;y++)for(let x=0;x<W;x++)if(d[(y*W+x)*4+3]>24){if(x<min)min=x;if(x>max)max=x}
    return max<min?0:(max-min+1)/S;
  }

  class GalaxyCoordinateOverlay{
    constructor(container,options={}){
      if(!(container instanceof Element))throw new TypeError('GalaxyCoordinateOverlay requires a DOM Element container.');
      if(container.shadowRoot)throw new Error('GalaxyCoordinateOverlay host already has a ShadowRoot.');
      this.container=container;this.frame='ICRSD';this.longitude=359.9999;this.latitude=-90;this.destroyed=false;
      this.onFrameChange=typeof options.onFrameChange==='function'?options.onFrameChange:null;
      this.shadow=container.attachShadow({mode:'open'});
      this.canvas=createMeasureCanvas();this.ctx=this.canvas.getContext('2d',{willReadFrequently:true});
      this.metrics=null;this.root=this.#build();
      this.shadow.append(this.#style(),this.root,this.canvas);
      this.ready=this.#init();
    }
    #style(){
      const style=document.createElement('style');
      style.textContent=`
@font-face{font-family:"GV Space Age";src:url("${FONT_URLS.spaceAge}") format("opentype");font-display:block}
@font-face{font-family:"GV Coordinate Digits";src:url("${FONT_URLS.digits}") format("opentype");font-display:block}
:host{display:block;width:${GEOMETRY.width}px;height:${GEOMETRY.height}px;contain:layout style paint;}
*,*::before,*::after{box-sizing:border-box;text-transform:none}
.gvco-root{position:relative;width:${GEOMETRY.width}px;height:${GEOMETRY.height}px;overflow:hidden;background:rgba(0,0,0,.86);border:1px solid #D7F4FF;border-radius:6px;box-shadow:0 0 10px rgba(98,216,255,.44);color:#72A7E8;user-select:none;-webkit-user-select:none}
.gvco-frame{position:absolute;top:50%;display:inline-flex;align-items:baseline;gap:.8px;font:400 12.5px/1 "GV Space Age",sans-serif;white-space:nowrap;transform:translateY(-50%) scaleY(1.1);transform-origin:left center;cursor:pointer;touch-action:manipulation}
.gvco-frame .gvco-small-d{font-size:60%;line-height:1;transform-origin:left bottom}
.gvco-divider{position:absolute;left:${GEOMETRY.dividerCenterX}px;top:50%;width:1px;height:15px;background:rgba(114,167,232,.75);transform:translate(-.5px,-50%)}
.gvco-number{position:absolute;top:3px;height:30px;font:400 20px/30px "GV Coordinate Digits",sans-serif;white-space:nowrap}
.gvco-cell{position:absolute;top:0;height:30px;display:flex;align-items:center;justify-content:center;line-height:30px;font-family:"GV Coordinate Digits",sans-serif;transform:scaleY(1.15);transform-origin:center}
.gvco-lambda{position:absolute;left:${GEOMETRY.lambdaCenterX}px;top:50%;width:9px;height:30px;font:400 9px/30px Arial,sans-serif;transform:translate(-50%,-50%);display:flex;align-items:center;justify-content:center}
`;
      return style;
    }
    #build(){
      const root=document.createElement('div');root.className='gvco-root';root.setAttribute('role','group');root.setAttribute('aria-label','Galaxy Viewer coordinates');
      root.innerHTML='<span class="gvco-frame" role="button" tabindex="0" title="Tap to switch coordinate frame"></span><span class="gvco-divider"></span><div class="gvco-number gvco-x"></div><span class="gvco-lambda">Λ</span><div class="gvco-number gvco-y"></div>';
      this.frameEl=root.querySelector('.gvco-frame');this.xEl=root.querySelector('.gvco-x');this.yEl=root.querySelector('.gvco-y');
      this.xEl.style.left=`${GEOMETRY.xFieldLeft}px`;this.xEl.style.width='87px';this.yEl.style.left=`${GEOMETRY.yFieldLeft}px`;this.yEl.style.width='82px';
      this.activateFrame=e=>{e.preventDefault();if(this.destroyed)return;this.setFrame(this.frame==='ICRSD'?'GAL':'ICRSD');this.onFrameChange?.(this.frame)};
      this.frameEl.addEventListener('click',this.activateFrame);this.frameEl.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '||e.key==='Spacebar')this.activateFrame(e)});
      return root;
    }
    async #init(){
      await Promise.all([document.fonts.load('400 12.5px "GV Space Age"'),document.fonts.load('400 20px "GV Coordinate Digits"')]);
      await document.fonts.ready;if(this.destroyed)return this;
      let widest=0;for(const c of '0123456789')widest=Math.max(widest,scan(this.ctx,this.canvas,c,'GV Coordinate Digits',20));
      this.metrics={digit:Math.ceil(widest),decimal:Math.ceil(scan(this.ctx,this.canvas,'.','GV Coordinate Digits',20)),minus:Math.ceil(scan(this.ctx,this.canvas,'-','GV Coordinate Digits',20))};
      this.#render();return this;
    }
    #cell(parent,char,left,width){const s=document.createElement('span');s.className='gvco-cell';s.textContent=char;s.style.left=`${left}px`;s.style.width=`${width}px`;parent.appendChild(s)}
    #renderNumber(parent,value,anchor,integerSlots,signWidth){if(!this.metrics)return;const {digit,decimal}=this.metrics;parent.textContent='';const dl=anchor-decimal/2;this.#cell(parent,'.',dl,decimal);let cursor=dl,integer=value.integer.padStart(integerSlots,' ');for(let i=integer.length-1;i>=0;i--){cursor-=digit;if(integer[i]!==' ')this.#cell(parent,integer[i],cursor,digit)}if(signWidth){cursor-=signWidth;this.#cell(parent,value.sign,cursor,signWidth)}cursor=dl+decimal;for(const c of value.fraction){this.#cell(parent,c,cursor,digit);cursor+=digit}}
    #renderFrame(){this.frameEl.style.left=`${this.frame==='GAL'?GEOMETRY.galLeft:GEOMETRY.icrsdLeft}px`;this.frameEl.replaceChildren();for(const [i,c] of [...this.frame].entries()){const s=document.createElement('span');s.textContent=c;if(this.frame==='ICRSD'&&i===4)s.className='gvco-small-d';this.frameEl.appendChild(s)}this.frameEl.setAttribute('aria-label',`Coordinate frame ${this.frame}. Tap to switch.`)}
    #render(){if(this.destroyed||!this.metrics)return;this.#renderFrame();this.#renderNumber(this.xEl,formatLongitude(this.longitude),GEOMETRY.xDecimalFromFieldLeft,3,0);this.#renderNumber(this.yEl,formatLatitude(this.latitude),GEOMETRY.yDecimalFromFieldLeft,2,this.metrics.minus)}
    update(longitude,latitude){if(this.destroyed)return this;this.longitude=clamp(longitude,0,359.9999);this.latitude=clamp(latitude,-90,90);this.#render();return this}
    setFrame(frame){if(this.destroyed)return this;this.frame=String(frame).toUpperCase().includes('GAL')?'GAL':'ICRSD';this.#render();return this}
    getState(){return {version:VERSION,frame:this.frame,longitude:this.longitude,latitude:this.latitude,destroyed:this.destroyed}}
    getMeasurements(){const r=this.root.getBoundingClientRect();return {...GEOMETRY,renderedWidth:r.width,renderedHeight:r.height,...this.getState()}}
    destroy(){if(this.destroyed)return;this.destroyed=true;this.frameEl.removeEventListener('click',this.activateFrame);this.shadow.replaceChildren();instances.delete(this.container)}
    static mount(container,options){const existing=instances.get(container);if(existing&&!existing.destroyed)return existing;const instance=new GalaxyCoordinateOverlay(container,options);instances.set(container,instance);return instance}
  }

  GalaxyCoordinateOverlay.VERSION=VERSION;
  GalaxyCoordinateOverlay.GEOMETRY=GEOMETRY;
  global.GalaxyCoordinateOverlay=GalaxyCoordinateOverlay;
})(window);
