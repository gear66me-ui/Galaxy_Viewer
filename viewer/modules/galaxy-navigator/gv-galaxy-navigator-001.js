/* Galaxy Viewer Galaxy Navigator 001
 * Presentation and user-intent module only.
 * Owns: navigation UI artwork, banner, Back/Random Galaxy/Forward controls, visual states.
 * Does NOT own: route planning, catalog selection, RA/Dec/FOV, Aladin camera, AVM image loading.
 */
(function(global){
'use strict';
const VERSION='001';
const FONT_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf';

function installStyle(){
    if(document.getElementById('gv-galaxy-navigator-001-style'))return;
    const style=document.createElement('style');
    style.id='gv-galaxy-navigator-001-style';
    style.textContent=`@font-face{font-family:"GV Space Age";src:url("${FONT_URL}") format("opentype");font-display:swap}
.gv-galaxy-navigator{display:grid;grid-template-columns:54px minmax(168px,1fr) 54px;align-items:center;justify-content:center;gap:7px;width:min(100%,390px);margin:0 auto}
.gv-galaxy-navigator button{position:relative;display:flex;align-items:center;justify-content:center;height:54px;padding:0;border:1px solid rgba(176,239,255,.92);border-radius:12px;background:linear-gradient(180deg,#12385f 0%,#071b34 20%,#041225 62%,#092a50 100%);box-shadow:0 0 5px rgba(72,192,255,.72),inset 0 2px 2px rgba(226,250,255,.34),inset 0 -2px 4px rgba(0,0,0,.72);color:#fff;overflow:hidden;transition:color .08s,text-shadow .08s,filter .08s,opacity .08s}
.gv-galaxy-navigator button::before{content:"";position:absolute;inset:3px;border:2px solid rgba(144,231,255,.82);border-radius:9px;box-shadow:0 0 5px rgba(70,194,255,.65),inset 0 0 7px rgba(34,133,230,.36);pointer-events:none}
.gv-galaxy-navigator button::after{content:"";position:absolute;left:10%;right:10%;top:5px;height:28%;border-radius:50%;background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,0));pointer-events:none}
.gv-galaxy-navigator .gv-nav-label{position:relative;z-index:1;font-family:"GV Space Age",sans-serif;font-size:16px;font-weight:400;letter-spacing:.7px;line-height:1;white-space:nowrap;color:currentColor;text-shadow:0 0 2px #fff,0 0 5px #fff,0 0 11px rgba(225,249,255,.98),0 0 18px rgba(116,215,255,.78)}
.gv-galaxy-navigator .gv-nav-chevron{position:relative;z-index:1;width:17px;height:17px;border-top:5px solid currentColor;border-right:5px solid currentColor;filter:drop-shadow(0 0 2px #fff) drop-shadow(0 0 6px rgba(230,250,255,.98)) drop-shadow(0 0 10px rgba(102,207,255,.72))}
.gv-galaxy-navigator [data-gv-nav="back"] .gv-nav-chevron{transform:rotate(-135deg);margin-left:5px}
.gv-galaxy-navigator [data-gv-nav="forward"] .gv-nav-chevron{transform:rotate(45deg);margin-right:5px}
.gv-galaxy-navigator button.gv-nav-pressed{color:#78FFAB}
.gv-galaxy-navigator button.gv-nav-pressed .gv-nav-label{text-shadow:0 0 2px #dffff0,0 0 5px #78FFAB,0 0 11px #38ff82,0 0 18px rgba(56,255,130,.82)}
.gv-galaxy-navigator button.gv-nav-pressed .gv-nav-chevron{filter:drop-shadow(0 0 2px #dffff0) drop-shadow(0 0 6px #78FFAB) drop-shadow(0 0 11px #38ff82)}
.gv-galaxy-navigator button:disabled{color:#68717a;filter:saturate(.18) brightness(.68);box-shadow:inset 0 1px 2px rgba(255,255,255,.08),inset 0 -2px 4px rgba(0,0,0,.82);opacity:.78}
.gv-galaxy-navigator button:disabled .gv-nav-label{text-shadow:none}
.gv-galaxy-navigator button:disabled .gv-nav-chevron{filter:none}
@media(max-width:420px){.gv-galaxy-navigator{grid-template-columns:50px minmax(160px,1fr) 50px;gap:6px}.gv-galaxy-navigator button{height:50px}.gv-galaxy-navigator .gv-nav-label{font-size:15px}.gv-galaxy-navigator .gv-nav-chevron{width:15px;height:15px;border-width:4px}}`;
    document.head.appendChild(style);
}

function mount(host,handlers={}){
    if(!(host instanceof Element))throw new Error('GALAXY NAVIGATOR HOST REQUIRED');
    installStyle();
    host.classList.add('gv-galaxy-navigator');
    host.innerHTML=
        '<button data-gv-nav="back" type="button" aria-label="Back"><span class="gv-nav-chevron" aria-hidden="true"></span></button>'+
        '<button data-gv-nav="random" type="button"><span class="gv-nav-label">RANDOM GALAXY</span></button>'+
        '<button data-gv-nav="forward" type="button" aria-label="Forward"><span class="gv-nav-chevron" aria-hidden="true"></span></button>';

    const back=host.querySelector('[data-gv-nav="back"]');
    const random=host.querySelector('[data-gv-nav="random"]');
    const forward=host.querySelector('[data-gv-nav="forward"]');

    const press=(button,handler)=>{
        if(button.disabled)return;
        button.classList.add('gv-nav-pressed');
        setTimeout(()=>button.classList.remove('gv-nav-pressed'),180);
        handler?.();
    };
    back.addEventListener('click',()=>press(back,handlers.onBack));
    random.addEventListener('click',()=>press(random,handlers.onRandom));
    forward.addEventListener('click',()=>press(forward,handlers.onForward));

    return Object.freeze({
        VERSION,
        host,
        back,
        random,
        forward,
        setEnabled({back:backEnabled=true,random:randomEnabled=true,forward:forwardEnabled=true}={}){
            back.disabled=!backEnabled;
            random.disabled=!randomEnabled;
            forward.disabled=!forwardEnabled;
        }
    });
}

global.GalaxyNavigator=Object.freeze({VERSION,mount});
})(typeof window!=='undefined'?window:globalThis);
