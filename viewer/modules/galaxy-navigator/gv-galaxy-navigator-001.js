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
.gv-galaxy-navigator{display:grid;grid-template-columns:58px minmax(190px,1fr) 58px;align-items:center;justify-content:center;gap:7px;width:min(100%,430px);margin:0 auto}
.gv-galaxy-navigator button{position:relative;display:flex;align-items:center;justify-content:center;height:58px;padding:0;border:2px solid #8ceaff;border-radius:13px;background:linear-gradient(180deg,#12497a 0%,#082b52 14%,#03172d 48%,#041426 72%,#0a3765 100%);box-shadow:0 0 5px rgba(52,190,255,.88),0 0 10px rgba(25,139,255,.48),inset 0 2px 3px rgba(235,253,255,.50),inset 0 -3px 5px rgba(0,0,0,.78);color:#fff;overflow:hidden;transition:color .08s,text-shadow .08s,filter .08s,opacity .08s}
.gv-galaxy-navigator button::before{content:"";position:absolute;inset:3px;border:2px solid rgba(180,244,255,.94);border-radius:9px;box-shadow:0 0 4px #bff7ff,0 0 8px rgba(48,192,255,.70),inset 0 0 8px rgba(30,135,235,.38);pointer-events:none}
.gv-galaxy-navigator button::after{content:"";position:absolute;left:8%;right:8%;top:5px;height:25%;border-radius:50%;background:linear-gradient(180deg,rgba(255,255,255,.20),rgba(255,255,255,0));pointer-events:none}
.gv-galaxy-navigator .gv-nav-label{position:relative;z-index:1;font-family:"GV Space Age";font-size:21px;font-weight:400;letter-spacing:.5px;line-height:1;white-space:nowrap;color:currentColor;text-shadow:0 0 2px #fff,0 0 5px #fff,0 0 10px #e8fbff,0 0 17px rgba(88,204,255,.95)}
.gv-galaxy-navigator .gv-nav-chevron{position:relative;z-index:1;width:16px;height:16px;border-top:4px solid currentColor;border-right:4px solid currentColor;filter:drop-shadow(0 0 2px #fff) drop-shadow(0 0 5px #fff) drop-shadow(0 0 9px rgba(115,220,255,.92))}
.gv-galaxy-navigator [data-gv-nav="back"] .gv-nav-chevron{transform:rotate(-135deg);margin-left:5px}
.gv-galaxy-navigator [data-gv-nav="forward"] .gv-nav-chevron{transform:rotate(45deg);margin-right:5px}
.gv-galaxy-navigator button.gv-nav-pressed{color:#78FFAB}
.gv-galaxy-navigator button.gv-nav-pressed .gv-nav-label{text-shadow:0 0 2px #eafff2,0 0 5px #78FFAB,0 0 10px #38ff82,0 0 17px rgba(56,255,130,.90)}
.gv-galaxy-navigator button.gv-nav-pressed .gv-nav-chevron{filter:drop-shadow(0 0 2px #eafff2) drop-shadow(0 0 5px #78FFAB) drop-shadow(0 0 10px #38ff82)}
.gv-galaxy-navigator button:disabled{color:#626b73;filter:saturate(.15) brightness(.62);box-shadow:inset 0 1px 2px rgba(255,255,255,.07),inset 0 -2px 4px rgba(0,0,0,.85);opacity:.76}
.gv-galaxy-navigator button:disabled::before{border-color:#68737c;box-shadow:none}
.gv-galaxy-navigator button:disabled .gv-nav-label{text-shadow:none}
.gv-galaxy-navigator button:disabled .gv-nav-chevron{filter:none}
@media(max-width:420px){.gv-galaxy-navigator{grid-template-columns:52px minmax(180px,1fr) 52px;gap:6px}.gv-galaxy-navigator button{height:52px}.gv-galaxy-navigator .gv-nav-label{font-size:18px}.gv-galaxy-navigator .gv-nav-chevron{width:14px;height:14px;border-width:4px}}`
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
