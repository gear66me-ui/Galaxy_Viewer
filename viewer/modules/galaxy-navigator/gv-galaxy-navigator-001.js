/* Galaxy Viewer Galaxy Navigator 001
 * Presentation and user-intent module only.
 * Owns: navigation UI artwork, banner, Back/Random Galaxy/Forward controls, visual states.
 * Does NOT own: route planning, catalog selection, RA/Dec/FOV, Aladin camera, AVM image loading.
 */
(function(global){
'use strict';
const VERSION='001';

function mount(host,handlers={}){
    if(!(host instanceof Element))throw new Error('GALAXY NAVIGATOR HOST REQUIRED');
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
