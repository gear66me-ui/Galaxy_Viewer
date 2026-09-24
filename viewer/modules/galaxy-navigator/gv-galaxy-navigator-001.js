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
.gv-galaxy-navigator button{min-width:62px;height:38px;padding:0 12px;border:1px solid rgba(124,203,255,.78);border-radius:8px;background:linear-gradient(180deg,rgba(11,49,119,.94),rgba(3,19,54,.96));box-shadow:0 0 9px rgba(65,168,255,.22),inset 0 1px 0 rgba(255,255,255,.13);color:#DDF8FF;font-family:"GV Space Age",sans-serif;font-size:10px;letter-spacing:.6px;text-transform:uppercase;white-space:nowrap}
.gv-galaxy-navigator button[data-gv-nav="random"]{min-width:132px;height:42px;border-color:#78FFAB;box-shadow:0 0 12px rgba(120,255,171,.25),inset 0 1px 0 rgba(255,255,255,.13)}
.gv-galaxy-navigator button:active{transform:translateY(1px);filter:brightness(1.18)}
.gv-galaxy-navigator button:disabled{opacity:.38}`;
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

    back.addEventListener('click',()=>handlers.onBack?.());
    random.addEventListener('click',()=>handlers.onRandom?.());
    forward.addEventListener('click',()=>handlers.onForward?.());

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
