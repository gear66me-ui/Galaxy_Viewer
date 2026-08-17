/*
 * Galaxy Viewer Hamburger / Projection Menu Module 0002
 * Standalone UI component extracted from the approved Galaxy Viewer menu lineage.
 * Owns only hamburger/menu DOM, geometry, projection artwork, visual state, and callbacks.
 */
(() => {
  "use strict";

  const MODULE_VERSION = "0002";
  const STYLE_ID = "gv-hamburger-menu-0002-style";
  const DEFAULT_ROOT_CLASS = "gv-hamburger-module-root";
  const FONT_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001";
  const ROW_HEIGHT = 36;
  const TILE_GAP = 2;
  const LEFT_INSET = 12;
  const TOP_INSET = 12;
  const MENU_TOP = 50;
  const CYCLE = 3000;
  const EASING = "cubic-bezier(.42,0,.18,1)";
  const MENU_FADE_MS = 1000;

  const LEFT_LABELS = ["PROJECTION", "LAYERS", "GRID", "SURVEY", "RETICLE ON/OFF"];
  const PROJECTION_LABELS = ["MOLLWEIDE", "SPHERICAL", "ORTHO", "TANGENTIAL", "SINUSOIDAL"];
  const PROJECTION_CODES = Object.freeze({
    MOLLWEIDE: "MOL",
    SPHERICAL: "SIN",
    ORTHO: "SIN",
    TANGENTIAL: "TAN",
    SINUSOIDAL: "SFL"
  });

  const PROJECTION_MAIN_SVG = `<svg viewBox="0 0 64 64" aria-hidden="true"><g><circle class="gv-proj-sphere" cx="23" cy="31" r="14.5"/><ellipse class="gv-proj-sphere" cx="23" cy="31" rx="6" ry="14.5"/><ellipse class="gv-proj-sphere" cx="23" cy="31" rx="14.5" ry="6"/><path class="gv-proj-sphere" d="M10.5 24.5c7.7 3.9 17.3 3.9 25 0M10.5 37.5c7.7-3.9 17.3-3.9 25 0"/><path class="gv-proj-bridge" d="M35.5 23.5L43 18M37.5 31L47 31M35.5 38.5L43 44"/><path class="gv-proj-grid" d="M43 18L57 22L57 40L43 44Z"/><path class="gv-proj-grid" d="M47.7 19.35V42.65M52.4 20.7V41.3M43 24.5L57 27M43 31L57 31M43 37.5L57 35"/><circle class="gv-proj-node" cx="47" cy="31" r="1.5"/></g></svg>`;

  const MOLLWEIDE_SVG = `<svg viewBox="0 0 64 64" aria-hidden="true"><ellipse class="gv-mol-outline gv-sub-cyan" cx="32" cy="32" rx="25.5" ry="16.5"/><path class="gv-mol-grid gv-sub-purple" d="M12 32H52"/><path class="gv-mol-grid gv-sub-purple" d="M14 25.5C22 22.3 42 22.3 50 25.5"/><path class="gv-mol-grid gv-sub-purple" d="M14 38.5C22 41.7 42 41.7 50 38.5"/><path class="gv-mol-grid gv-sub-purple" d="M32 18.5V45.5"/><path class="gv-mol-grid gv-sub-purple" d="M25 19.2C21 24.2 21 39.8 25 44.8"/><path class="gv-mol-grid gv-sub-purple" d="M39 19.2C43 24.2 43 39.8 39 44.8"/><path class="gv-mol-grid gv-sub-purple" d="M19.5 21.2C15.2 26.5 15.2 37.5 19.5 42.8"/><path class="gv-mol-grid gv-sub-purple" d="M44.5 21.2C48.8 26.5 48.8 37.5 44.5 42.8"/></svg>`;

  const SPHERICAL_SVG = `<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><circle class="gv-sub-cyan" cx="32" cy="32" r="22" stroke="#8feaff" stroke-width="2.75"/><ellipse class="gv-sub-purple" cx="32" cy="32" rx="8.5" ry="19.5" stroke="#9d7cff" stroke-width="1.86"/><ellipse cx="32" cy="32" rx="16" ry="22" stroke="#4fa6ff" stroke-width="1.05" opacity=".8"/><ellipse class="gv-sub-purple" cx="32" cy="32" rx="19.5" ry="8.5" stroke="#9d7cff" stroke-width="1.74"/><path d="M13 21.2C22.4 26 41.6 26 51 21.2M13 42.8C22.4 38 41.6 38 51 42.8" stroke="#4fa6ff" stroke-width="1.15" opacity=".9"/><path class="gv-sub-cyan" d="M10.5 32H53.5" stroke="#8feaff" stroke-width="1.6875"/><circle cx="32" cy="32" r="2" fill="#4fa6ff" stroke="none"/></g></svg>`;

  const ORTHO_SVG = `<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><circle class="gv-sub-cyan" cx="32" cy="32" r="22" stroke="#8feaff" stroke-width="2.875"/><path class="gv-sub-purple" d="M15 22.5C23 26.2 41 26.2 49 22.5M12.5 32H51.5M15 41.5C23 37.8 41 37.8 49 41.5" stroke="#9d7cff" stroke-width="1.62"/><path d="M32 10C23.5 18 23.5 46 32 54M32 10C40.5 18 40.5 46 32 54" stroke="#4fa6ff" stroke-width="1.45"/><path class="gv-sub-cyan" d="M32 13V51M13 32H51" stroke="#8feaff" stroke-width="1" opacity=".75"/><circle cx="32" cy="32" r="3.1" stroke="#4fa6ff" stroke-width="1.6"/><circle class="gv-sub-purple-fill" cx="32" cy="32" r="1.25" fill="#9d7cff" stroke="none"/></g></svg>`;

  const TANGENTIAL_SVG = `<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path class="gv-sub-cyan" d="M10 18C18 12 27 11 34 13M10 32C18 27 27 26 34 27M10 46C18 42 27 42 34 43" stroke="#8feaff" stroke-width="1.8125"/><path class="gv-sub-purple" d="M16.5 13C20 21 21 37 17.5 51M27 12C29.5 21 29.5 43 27 52" stroke="#9d7cff" stroke-width="1.5" opacity=".92"/><circle cx="34" cy="32" r="2.5" fill="#4fa6ff" stroke="none"/><path d="M36.5 25L44 18M36.8 32H45M36.5 39L44 46" stroke="#4fa6ff" stroke-width="1.7"/><path class="gv-sub-cyan" d="M44 18L56 21.5L56 42.5L44 46Z" stroke="#8feaff" stroke-width="2.5"/><path class="gv-sub-purple" d="M48 22V42M52 23V41M47 25.8L53 27.4M47 32H53M47 38.2L53 36.6" stroke="#9d7cff" stroke-width="1.38"/></g></svg>`;

  const SINUSOIDAL_SVG = `<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path class="gv-sub-cyan" d="M32 9C22 11 13 20 9 32C13 44 22 53 32 55C42 53 51 44 55 32C51 20 42 11 32 9Z" stroke="#8feaff" stroke-width="2.8125"/><path d="M9 32H55" stroke="#4fa6ff" stroke-width="1.65"/><path class="gv-sub-purple" d="M15.5 22H48.5M15.5 42H48.5" stroke="#9d7cff" stroke-width="1.62"/><path class="gv-sub-purple" d="M32 12V52M22.5 14.5C26.5 23 26.5 41 22.5 49.5M41.5 14.5C37.5 23 37.5 41 41.5 49.5M16.5 19C21.5 26 21.5 38 16.5 45M47.5 19C42.5 26 42.5 38 47.5 45" stroke="#9d7cff" stroke-width="1.5"/><path d="M17 15.5C24 23 24 41 17 48.5M47 15.5C40 23 40 41 47 48.5" stroke="#4fa6ff" stroke-width=".9" opacity=".68"/><circle cx="32" cy="32" r="1.6" fill="#4fa6ff" stroke="none"/></g></svg>`;

  const PROJECTION_SVGS = Object.freeze({
    MOLLWEIDE: MOLLWEIDE_SVG,
    SPHERICAL: SPHERICAL_SVG,
    ORTHO: ORTHO_SVG,
    TANGENTIAL: TANGENTIAL_SVG,
    SINUSOIDAL: SINUSOIDAL_SVG
  });

  const ICON_FRAMES = [
    { offset: 0, opacity: .82, filter: "brightness(1.08) saturate(1.06) drop-shadow(0 0 2px rgba(143,234,255,.42)) drop-shadow(0 0 5px rgba(79,166,255,.22))" },
    { offset: .24, opacity: .94, filter: "brightness(1.22) saturate(1.12) drop-shadow(0 0 3px rgba(224,252,255,.72)) drop-shadow(0 0 7px rgba(98,216,255,.68)) drop-shadow(0 0 11px rgba(157,124,255,.34))" },
    { offset: .52, opacity: 1, filter: "brightness(1.48) saturate(1.18) drop-shadow(0 0 5px rgba(255,255,255,1)) drop-shadow(0 0 10px rgba(143,234,255,1)) drop-shadow(0 0 16px rgba(79,166,255,.98)) drop-shadow(0 0 22px rgba(157,124,255,.72))" },
    { offset: .76, opacity: .94, filter: "brightness(1.24) saturate(1.12) drop-shadow(0 0 3px rgba(224,252,255,.76)) drop-shadow(0 0 7px rgba(98,216,255,.70)) drop-shadow(0 0 11px rgba(157,124,255,.36))" },
    { offset: 1, opacity: .82, filter: "brightness(1.08) saturate(1.06) drop-shadow(0 0 2px rgba(143,234,255,.42)) drop-shadow(0 0 5px rgba(79,166,255,.22))" }
  ];
  const SELECTED_FRAME = ICON_FRAMES[2];

  function installStyles() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
@font-face{font-family:"Space Age";src:url("${FONT_URL}") format("opentype");font-style:normal;font-weight:400;font-display:block}
.${DEFAULT_ROOT_CLASS}{position:relative;width:100%;height:100%;min-height:100%;overflow:hidden;background:transparent;font-family:"Space Age",sans-serif;text-transform:uppercase}
.${DEFAULT_ROOT_CLASS} *{box-sizing:border-box;font-family:"Space Age",sans-serif;text-transform:uppercase}
.${DEFAULT_ROOT_CLASS} .gv-space-age-glyph{display:inline-block;transform:scaleY(1.5);transform-origin:center}
.${DEFAULT_ROOT_CLASS} button{font:inherit}
.${DEFAULT_ROOT_CLASS} .gv-menu-proxy{appearance:none;-webkit-appearance:none;position:absolute;left:${LEFT_INSET}px;top:${TOP_INSET}px;display:flex;align-items:center;justify-content:center;width:${ROW_HEIGHT}px;height:${ROW_HEIGHT}px;margin:0;padding:0;overflow:hidden;background:rgba(0,0,0,.82);border:1px solid #D7F4FF;border-radius:6px;cursor:pointer;touch-action:manipulation;outline:none;box-shadow:0 0 10px rgba(98,216,255,.38);z-index:20}
.${DEFAULT_ROOT_CLASS} .gv-menu-stack{position:absolute;left:50%;top:50%;width:18px;height:16px;transform:translate(-50%,-50%);pointer-events:none}
.${DEFAULT_ROOT_CLASS} .gv-menu-track{position:absolute;left:0;width:18px;height:2px;border-radius:2px;background:#D7F3FF;box-shadow:none;filter:none}
.${DEFAULT_ROOT_CLASS} .gv-menu-track:nth-child(1){top:0}.${DEFAULT_ROOT_CLASS} .gv-menu-track:nth-child(2){top:7px}.${DEFAULT_ROOT_CLASS} .gv-menu-track:nth-child(3){top:14px}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu,.${DEFAULT_ROOT_CLASS} .gv-projection-submenu{position:absolute;top:${MENU_TOP}px;display:flex;visibility:hidden;opacity:0;pointer-events:none;flex-direction:column;align-items:flex-start;gap:${TILE_GAP}px;margin:0;padding:0;transform:translateY(-4px);transition:opacity .18s ease,transform .18s ease,visibility 0s linear .18s;z-index:15}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu{left:${LEFT_INSET}px}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu.gv-open,.${DEFAULT_ROOT_CLASS} .gv-projection-submenu.gv-open{visibility:visible;opacity:1;pointer-events:auto;transform:translateY(0);transition:opacity .18s ease,transform .18s ease}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-row,.${DEFAULT_ROOT_CLASS} .gv-projection-option-row{display:grid;align-items:center;height:${ROW_HEIGHT}px;margin:0;padding:0;isolation:isolate}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-label,.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-icon,.${DEFAULT_ROOT_CLASS} .gv-projection-option-label,.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon{appearance:none;-webkit-appearance:none;position:relative;display:flex;visibility:visible;opacity:1;align-items:center;height:${ROW_HEIGHT}px;min-height:${ROW_HEIGHT}px;max-height:${ROW_HEIGHT}px;margin:0;border:1px solid #D7F4FF;border-radius:6px;background:rgba(0,0,0,.90);color:#D7F3FF;cursor:pointer;touch-action:manipulation;outline:none;transition:background .22s ease,filter .22s ease,opacity .22s ease}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-label,.${DEFAULT_ROOT_CLASS} .gv-projection-option-label{justify-content:flex-start;padding:0 10px;font:400 12px/1.15 "Space Age",sans-serif;letter-spacing:.55px;text-shadow:0 0 2px rgba(234,248,255,.58);text-align:left;white-space:nowrap;overflow:hidden;box-shadow:none}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-icon,.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon{width:${ROW_HEIGHT}px;min-width:${ROW_HEIGHT}px;max-width:${ROW_HEIGHT}px;justify-content:center;padding:0;overflow:hidden;box-shadow:0 0 10px rgba(98,216,255,.38);isolation:isolate}
.${DEFAULT_ROOT_CLASS} .gv-static-inset{position:absolute;inset:2px;border-radius:6px;pointer-events:none;z-index:0;opacity:1;background:rgba(5,18,32,.10);box-shadow:inset 0 0 0 1px rgba(143,234,255,.28),inset 0 0 6px rgba(98,216,255,.18),inset 0 0 10px rgba(157,124,255,.10)}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-icon>svg,.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon>svg{position:relative;z-index:2;display:block;overflow:visible;pointer-events:none;margin:0}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-icon.gv-projection-icon>svg{width:30px;height:30px}
.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon>svg{width:24px;height:24px}
.${DEFAULT_ROOT_CLASS} .gv-proj-sphere,.${DEFAULT_ROOT_CLASS} .gv-proj-grid,.${DEFAULT_ROOT_CLASS} .gv-proj-bridge{fill:none;stroke-linecap:round;stroke-linejoin:round}
.${DEFAULT_ROOT_CLASS} .gv-proj-sphere{stroke:#8FEAFF;stroke-width:1.55}.${DEFAULT_ROOT_CLASS} .gv-proj-grid{stroke:#9D7CFF;stroke-width:1.45}.${DEFAULT_ROOT_CLASS} .gv-proj-bridge{stroke:#4FA6FF;stroke-width:1.3;opacity:.9}.${DEFAULT_ROOT_CLASS} .gv-proj-node{fill:#4FA6FF}
.${DEFAULT_ROOT_CLASS} .gv-mol-outline,.${DEFAULT_ROOT_CLASS} .gv-mol-grid{fill:none;stroke-linecap:round;stroke-linejoin:round}.${DEFAULT_ROOT_CLASS} .gv-mol-outline{stroke:#8FEAFF;stroke-width:2.25}.${DEFAULT_ROOT_CLASS} .gv-mol-grid{stroke:#9D7CFF;stroke-width:1.38;opacity:.96}
.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon .gv-sub-cyan{filter:brightness(1.18) drop-shadow(0 0 .75px rgba(143,234,255,.72))}
.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon .gv-sub-purple,.${DEFAULT_ROOT_CLASS} .gv-projection-option-icon .gv-sub-purple-fill{filter:brightness(1.25) drop-shadow(0 0 .65px rgba(157,124,255,.55))}
.${DEFAULT_ROOT_CLASS}.gv-projection-mode .gv-viewer-menu>.gv-viewer-menu-row:not(:first-child) .gv-viewer-menu-label,.${DEFAULT_ROOT_CLASS}.gv-projection-mode .gv-viewer-menu>.gv-viewer-menu-row:not(:first-child) .gv-viewer-menu-icon{opacity:.42;filter:grayscale(1) saturate(.12) brightness(.58);box-shadow:0 0 4px rgba(120,150,165,.10)}
.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-row.gv-selected .gv-viewer-menu-label,.${DEFAULT_ROOT_CLASS} .gv-viewer-menu-row.gv-selected .gv-viewer-menu-icon,.${DEFAULT_ROOT_CLASS} .gv-projection-option-row.gv-active .gv-projection-option-label{background:rgba(35,31,70,.96)}
.${DEFAULT_ROOT_CLASS} .gv-projection-option-row.gv-active .gv-projection-option-icon{background:rgba(18,24,52,.96)}
@media (prefers-reduced-motion:reduce){.${DEFAULT_ROOT_CLASS} .gv-viewer-menu,.${DEFAULT_ROOT_CLASS} .gv-projection-submenu{transition:none}}
`;
    document.head.appendChild(style);
  }

  function glyph(text) {
    const span = document.createElement("span");
    span.className = "gv-space-age-glyph";
    span.textContent = text;
    return span;
  }

  function addStaticInset(tile) {
    const layer = document.createElement("span");
    layer.className = "gv-static-inset";
    layer.setAttribute("aria-hidden", "true");
    tile.appendChild(layer);
    return layer;
  }

  function createIconButton(className, ariaLabel, svgMarkup = "") {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.setAttribute("aria-label", ariaLabel);
    addStaticInset(button);
    if (svgMarkup) button.insertAdjacentHTML("beforeend", svgMarkup);
    return button;
  }

  function cancelAnimation(animation) {
    try { animation.cancel(); } catch (_) { }
  }

  function createInstance(options = {}) {
    installStyles();
    const host = options.host || document.body;
    if (!(host instanceof Element)) throw new TypeError("GalaxyViewerHamburgerMenu.init requires an Element host");

    const root = document.createElement("div");
    root.className = DEFAULT_ROOT_CLASS;
    root.dataset.gvHamburgerMenuVersion = MODULE_VERSION;
    host.appendChild(root);

    const menuButton = document.createElement("button");
    menuButton.type = "button";
    menuButton.className = "gv-menu-proxy";
    menuButton.title = "VIEWER MENU";
    menuButton.setAttribute("aria-label", "VIEWER MENU");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.innerHTML = '<span class="gv-menu-stack" aria-hidden="true"><span class="gv-menu-track"></span><span class="gv-menu-track"></span><span class="gv-menu-track"></span></span>';
    root.appendChild(menuButton);

    const leftMenu = document.createElement("div");
    leftMenu.className = "gv-viewer-menu";
    leftMenu.setAttribute("role", "menu");
    leftMenu.setAttribute("aria-label", "VIEWER OPTIONS");
    root.appendChild(leftMenu);

    const leftRows = LEFT_LABELS.map((name, index) => {
      const row = document.createElement("div");
      row.className = "gv-viewer-menu-row";
      row.dataset.gvMenuAction = name;
      row.setAttribute("role", "none");

      const label = document.createElement("button");
      label.type = "button";
      label.className = "gv-viewer-menu-label";
      label.setAttribute("role", "menuitem");
      label.appendChild(glyph(name));

      const icon = createIconButton("gv-viewer-menu-icon" + (index === 0 ? " gv-projection-icon" : ""), name, index === 0 ? PROJECTION_MAIN_SVG : "");
      icon.setAttribute("role", "menuitem");

      row.append(label, icon);
      leftMenu.appendChild(row);
      return { row, label, icon };
    });

    const rightMenu = document.createElement("div");
    rightMenu.className = "gv-projection-submenu";
    rightMenu.setAttribute("role", "menu");
    rightMenu.setAttribute("aria-label", "PROJECTION OPTIONS");
    root.appendChild(rightMenu);

    const projectionRows = PROJECTION_LABELS.map(name => {
      const row = document.createElement("div");
      row.className = "gv-projection-option-row";
      row.dataset.gvProjection = name;
      row.setAttribute("role", "none");

      const label = document.createElement("button");
      label.type = "button";
      label.className = "gv-projection-option-label";
      label.setAttribute("role", "menuitemradio");
      label.setAttribute("aria-checked", "false");
      label.appendChild(glyph(name));

      const icon = createIconButton("gv-projection-option-icon", `${name} PROJECTION`, PROJECTION_SVGS[name]);
      icon.setAttribute("role", "menuitemradio");
      icon.setAttribute("aria-checked", "false");

      row.append(label, icon);
      rightMenu.appendChild(row);
      return { name, row, label, icon };
    });

    let selectedProjection = null;
    let fadeTimer = 0;
    let sharedPulseStart = null;
    const iconAnimations = new Map();
    const listeners = [];
    let destroyed = false;

    function listen(element, type, handler, opts) {
      element.addEventListener(type, handler, opts);
      listeners.push(() => element.removeEventListener(type, handler, opts));
    }

    function emit(type, detail) {
      root.dispatchEvent(new CustomEvent(type, { bubbles: true, detail }));
    }

    function stopBreathing(svg) {
      const animation = iconAnimations.get(svg);
      if (animation) cancelAnimation(animation);
      iconAnimations.delete(svg);
      svg.getAnimations?.().forEach(cancelAnimation);
      svg.style.animation = "none";
    }

    function startBreathing(svg) {
      if (!svg || window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) return;
      stopBreathing(svg);
      svg.style.removeProperty("opacity");
      svg.style.removeProperty("filter");
      const animation = svg.animate(ICON_FRAMES, { duration: CYCLE, iterations: Infinity, easing: EASING, fill: "both" });
      if (sharedPulseStart === null) sharedPulseStart = document.timeline.currentTime ?? performance.now();
      animation.startTime = sharedPulseStart;
      iconAnimations.set(svg, animation);
    }

    function makeSelectedSteady(svg) {
      if (!svg) return;
      stopBreathing(svg);
      svg.style.setProperty("opacity", String(SELECTED_FRAME.opacity));
      svg.style.setProperty("filter", SELECTED_FRAME.filter);
    }

    function refreshProjectionVisuals() {
      const leftOpen = leftMenu.classList.contains("gv-open");
      const projectionOpen = rightMenu.classList.contains("gv-open");
      const mainSvg = leftRows[0].icon.querySelector("svg");
      if (leftOpen) startBreathing(mainSvg); else stopBreathing(mainSvg);
      projectionRows.forEach(item => {
        const selected = item.name === selectedProjection;
        item.row.classList.toggle("gv-active", selected);
        item.label.setAttribute("aria-checked", selected ? "true" : "false");
        item.icon.setAttribute("aria-checked", selected ? "true" : "false");
        const svg = item.icon.querySelector("svg");
        if (!projectionOpen) {
          stopBreathing(svg);
          if (!selected) { svg.style.removeProperty("opacity"); svg.style.removeProperty("filter"); }
        } else if (selected) makeSelectedSteady(svg);
        else startBreathing(svg);
      });
    }

    function centerPaintedSvg(tile, svg) {
      if (!tile || !svg || typeof svg.getBBox !== "function") return null;
      svg.style.removeProperty("left");
      svg.style.removeProperty("top");
      svg.style.setProperty("position", "relative");
      void svg.getBoundingClientRect();
      let box;
      try { box = svg.getBBox({ fill: true, stroke: true, markers: true }); }
      catch (_) { box = svg.getBBox(); }
      const matrix = svg.getScreenCTM?.();
      if (!matrix || !box) return null;
      const point = svg.createSVGPoint();
      point.x = box.x + box.width / 2;
      point.y = box.y + box.height / 2;
      const painted = point.matrixTransform(matrix);
      const tileRect = tile.getBoundingClientRect();
      const errorX = tileRect.left + tileRect.width / 2 - painted.x;
      const errorY = tileRect.top + tileRect.height / 2 - painted.y;
      svg.style.setProperty("left", `${errorX.toFixed(3)}px`);
      svg.style.setProperty("top", `${errorY.toFixed(3)}px`);
      return { errorX, errorY };
    }

    function centerProjectionArtwork() {
      projectionRows.forEach(item => centerPaintedSvg(item.icon, item.icon.querySelector("svg")));
    }

    function applyGeometry() {
      if (destroyed) return;
      const width = root.getBoundingClientRect().width || root.clientWidth || window.innerWidth || 390;
      const S = ROW_HEIGHT;
      const G = TILE_GAP;
      const C = G;
      const A = Math.max(0, width - (LEFT_INSET * 2));
      const W = Math.max(72, (A - (2 * S) - (2 * G) - C) / 2);
      const groupWidth = W + G + S;
      const rightLeft = LEFT_INSET + groupWidth + C;

      leftMenu.style.width = `${groupWidth.toFixed(3)}px`;
      rightMenu.style.left = `${rightLeft.toFixed(3)}px`;
      rightMenu.style.width = `${groupWidth.toFixed(3)}px`;

      [...leftRows, ...projectionRows].forEach(item => {
        item.row.style.gridTemplateColumns = `${W.toFixed(3)}px ${S.toFixed(3)}px`;
        item.row.style.columnGap = `${G.toFixed(3)}px`;
        item.row.style.width = `${groupWidth.toFixed(3)}px`;
        item.label.style.width = `${W.toFixed(3)}px`;
        item.label.style.minWidth = `${W.toFixed(3)}px`;
        item.label.style.maxWidth = `${W.toFixed(3)}px`;
      });

      return { width, A, S, G, C, W, groupWidth, leftStart: LEFT_INSET, rightLeft, rightBoundary: width - LEFT_INSET };
    }

    function closeProjection() {
      rightMenu.classList.remove("gv-open");
      leftRows[0].row.classList.remove("gv-selected");
      leftRows[0].label.setAttribute("aria-expanded", "false");
      leftRows[0].icon.setAttribute("aria-expanded", "false");
      root.classList.remove("gv-projection-mode");
      refreshProjectionVisuals();
    }

    function closeAll() {
      clearTimeout(fadeTimer);
      leftMenu.classList.remove("gv-open");
      closeProjection();
      menuButton.setAttribute("aria-expanded", "false");
      [leftMenu, rightMenu].forEach(el => {
        el.style.removeProperty("transition");
        el.style.removeProperty("opacity");
        el.style.removeProperty("visibility");
        el.style.removeProperty("pointer-events");
      });
    }

    function openLeft() {
      clearTimeout(fadeTimer);
      leftMenu.style.removeProperty("transition");
      leftMenu.style.removeProperty("opacity");
      leftMenu.style.removeProperty("visibility");
      leftMenu.style.removeProperty("pointer-events");
      leftMenu.classList.add("gv-open");
      menuButton.setAttribute("aria-expanded", "true");
      applyGeometry();
      centerProjectionArtwork();
      refreshProjectionVisuals();
    }

    function toggleLeft(event) {
      event?.preventDefault?.();
      event?.stopPropagation?.();
      if (leftMenu.classList.contains("gv-open")) closeAll(); else openLeft();
      emit("gv-menu-toggle", { open: leftMenu.classList.contains("gv-open") });
    }

    function toggleProjection(event) {
      event?.preventDefault?.();
      event?.stopPropagation?.();
      if (!leftMenu.classList.contains("gv-open")) openLeft();
      const open = !rightMenu.classList.contains("gv-open");
      rightMenu.classList.toggle("gv-open", open);
      leftRows[0].row.classList.toggle("gv-selected", open);
      leftRows[0].label.setAttribute("aria-haspopup", "menu");
      leftRows[0].icon.setAttribute("aria-haspopup", "menu");
      leftRows[0].label.setAttribute("aria-expanded", open ? "true" : "false");
      leftRows[0].icon.setAttribute("aria-expanded", open ? "true" : "false");
      root.classList.toggle("gv-projection-mode", open);
      applyGeometry();
      centerProjectionArtwork();
      refreshProjectionVisuals();
      emit("gv-projection-menu-toggle", { open });
    }

    function flashRow(item) {
      item.row.classList.add("gv-selected");
      clearTimeout(item.row.__gvSelectionTimer);
      item.row.__gvSelectionTimer = setTimeout(() => item.row.classList.remove("gv-selected"), 700);
    }

    function activateMenuAction(item, event) {
      event.preventDefault();
      event.stopPropagation();
      if (item === leftRows[0]) return toggleProjection(event);
      flashRow(item);
      const action = item.row.dataset.gvMenuAction;
      options.onMenuAction?.(action, { sourceEvent: event, root });
      emit("gv-menu-action", { action });
    }

    function fadePanelsAfterSelection() {
      const panels = [leftMenu, rightMenu];
      panels.forEach(panel => {
        panel.style.setProperty("transition", `opacity ${MENU_FADE_MS}ms ease`);
        panel.style.setProperty("opacity", "1");
        panel.style.setProperty("visibility", "visible");
        panel.style.setProperty("pointer-events", "none");
      });
      void leftMenu.offsetWidth;
      requestAnimationFrame(() => panels.forEach(panel => panel.style.setProperty("opacity", "0")));
      clearTimeout(fadeTimer);
      fadeTimer = setTimeout(() => {
        leftMenu.classList.remove("gv-open");
        closeProjection();
        menuButton.setAttribute("aria-expanded", "false");
        panels.forEach(panel => {
          panel.style.removeProperty("transition");
          panel.style.removeProperty("opacity");
          panel.style.removeProperty("visibility");
          panel.style.removeProperty("pointer-events");
        });
        refreshProjectionVisuals();
      }, MENU_FADE_MS + 40);
    }

    function activateProjection(item, event) {
      event.preventDefault();
      event.stopPropagation();
      selectedProjection = item.name;
      refreshProjectionVisuals();
      const detail = { name: item.name, code: PROJECTION_CODES[item.name] };
      options.onProjectionSelected?.(item.name, detail);
      emit("gv-projection-selected", detail);
      fadePanelsAfterSelection();
    }

    listen(menuButton, "click", toggleLeft);
    leftRows.forEach(item => {
      listen(item.label, "click", event => activateMenuAction(item, event));
      listen(item.icon, "click", event => activateMenuAction(item, event));
    });
    projectionRows.forEach(item => {
      listen(item.label, "click", event => activateProjection(item, event));
      listen(item.icon, "click", event => activateProjection(item, event));
    });

    const resizeObserver = typeof ResizeObserver === "function" ? new ResizeObserver(applyGeometry) : null;
    resizeObserver?.observe(root);
    listen(window, "resize", applyGeometry, { passive: true });

    applyGeometry();
    centerProjectionArtwork();
    refreshProjectionVisuals();

    const api = {
      version: MODULE_VERSION,
      root,
      menuButton,
      leftMenu,
      projectionMenu: rightMenu,
      get selectedProjection() { return selectedProjection; },
      get geometry() { return applyGeometry(); },
      open: openLeft,
      close: closeAll,
      openProjectionMenu() { openLeft(); if (!rightMenu.classList.contains("gv-open")) toggleProjection(); },
      selectProjection(name) {
        const item = projectionRows.find(row => row.name === String(name).toUpperCase());
        if (!item) throw new RangeError(`Unknown projection: ${name}`);
        selectedProjection = item.name;
        refreshProjectionVisuals();
        const detail = { name: item.name, code: PROJECTION_CODES[item.name] };
        options.onProjectionSelected?.(item.name, detail);
        emit("gv-projection-selected", detail);
        return detail;
      },
      destroy() {
        if (destroyed) return;
        destroyed = true;
        clearTimeout(fadeTimer);
        resizeObserver?.disconnect();
        listeners.splice(0).forEach(dispose => dispose());
        iconAnimations.forEach(cancelAnimation);
        iconAnimations.clear();
        root.remove();
      }
    };

    root.__gvHamburgerMenu = api;
    return api;
  }

  window.GalaxyViewerHamburgerMenu = Object.freeze({
    version: MODULE_VERSION,
    init: createInstance,
    labels: Object.freeze({ left: [...LEFT_LABELS], projections: [...PROJECTION_LABELS] }),
    projectionCodes: PROJECTION_CODES
  });
})();
