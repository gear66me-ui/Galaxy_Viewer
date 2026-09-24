/* Galaxy Viewer Galaxy Navigator 001
 * Presentation and user-intent module only.
 * Owns: navigation UI artwork, banner, Back/Random Galaxy/Forward controls, visual states.
 * Does NOT own: route planning, catalog selection, RA/Dec/FOV, Aladin camera, AVM image loading.
 */
(function(global){
'use strict';
const VERSION='001';

const GalaxyNavigator=Object.freeze({
    VERSION
});

global.GalaxyNavigator=GalaxyNavigator;
})(typeof window!=='undefined'?window:globalThis);
