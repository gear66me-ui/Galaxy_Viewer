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
.gv-galaxy-navigator{display:flex;align-items:center;justify-content:center;gap:7px}
.gv-galaxy-navigator button{min-width:62px;height:38px;padding:0 12px;border:1px solid rgba(238,250,255,.92);border-radius:8px;background:linear-gradient(180deg,#29323b,#090d12 58%,#151b22);box-shadow:0 0 7px rgba(230,248,255,.72),0 0 15px rgba(190,230,255,.30),inset 0 1px 1px rgba(255,255,255,.42),inset 0 -2px 3px rgba(0,0,0,.75);color:#F4FCFF;text-shadow:0 0 6px rgba(225,247,255,.95);font-family:"GV Space Age",sans-serif;font-size:10px;letter-spacing:.6px;text-transform:uppercase;white-space:nowrap;transition:border-color .06s,box-shadow .06s,color .06s,text-shadow .06s,filter .06s}
.gv-galaxy-navigator button[data-gv-nav="random"]{min-width:132px;height:42px}
.gv-galaxy-navigator button.gv-nav-pressed{border-color:#78FFAB;color:#CFFFF0;box-shadow:0 0 8px rgba(120,255,171,.98),0 0 20px rgba(120,255,171,.72),0 0 34px rgba(120,255,171,.38),inset 0 1px 2px rgba(220,255,235,.48);text-shadow:0 0 7px rgba(120,255,171,1);filter:brightness(1.16)}
.gv-galaxy-navigator button:disabled{border-color:#303840;color:#59636c;box-shadow:inset 0 1px 1px rgba(255,255,255,.08),inset 0 -2px 3px rgba(0,0,0,.8);text-shadow:none;opacity:.72}`;
    document.head.appendChild(style);
}

function mount(host,handlers={}){
    if(!(host instanceof Element))throw new Error('GALAXY NAVIGATOR HOST REQUIRED');
    installStyle();
    host.classList.add('gv-galaxy-navigator');
    host.innerHTML=
        '<button data-gv-nav="back" type="button">BACK</button>'+
        '<button data-gv-nav="random" type="button">RANDOM GALAXY</button>'+
        '<button data-gv-nav="forward" type="button">FORWARD</button>';

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
