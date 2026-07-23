from IPython.display import HTML, display

# GALAXY-VIEWER-CORE-01
# Standalone interface block: title + live Aladin viewer only.

HTML_CONTENT = r'''
<div id="gvcore01-root">
  <style>
    #gvcore01-root {
      width: 100%;
      max-width: 1180px;
      margin: 0 auto;
      padding: 14px;
      box-sizing: border-box;
      background: #000;
      color: #7FDBFF;
      font-family: Arial, Helvetica, sans-serif;
      border: 1px solid #0b4f6c;
      border-radius: 10px;
      box-shadow: 0 0 18px rgba(0,174,239,.18);
    }
    #gvcore01-root .gvcore01-title {
      display: flex;
      align-items: center;
      gap: 14px;
      margin: 0 0 12px;
      padding: 10px 12px;
      border: 1px solid #137aa3;
      border-radius: 9px;
      background:
        radial-gradient(circle at 18% 35%, rgba(53,198,255,.25), transparent 28%),
        linear-gradient(90deg, #01050a, #020b12 55%, #000);
      overflow: hidden;
    }
    #gvcore01-root .gvcore01-comet {
      position: relative;
      width: 74px;
      height: 34px;
      flex: 0 0 74px;
    }
    #gvcore01-root .gvcore01-comet::before {
      content: "";
      position: absolute;
      right: 5px;
      top: 7px;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: radial-gradient(circle at 35% 35%, #fff 0 18%, #7FDBFF 30%, #35c6ff 52%, #086b94 76%, transparent 78%);
      box-shadow: 0 0 12px #35c6ff, 0 0 24px rgba(53,198,255,.8);
    }
    #gvcore01-root .gvcore01-comet::after {
      content: "";
      position: absolute;
      left: 0;
      top: 12px;
      width: 58px;
      height: 10px;
      border-radius: 999px;
      background: linear-gradient(90deg, transparent, rgba(138,79,212,.25), rgba(53,198,255,.8), #fff);
      filter: blur(1px);
      transform: skewX(-18deg);
    }
    #gvcore01-root .gvcore01-title-text {
      font-family: "Courier New", Consolas, monospace;
      font-size: clamp(26px, 4vw, 44px);
      font-weight: 800;
      letter-spacing: .12em;
      line-height: 1;
      color: #dff8ff;
      text-shadow: 0 0 5px #35c6ff, 0 0 14px rgba(53,198,255,.85);
      white-space: nowrap;
    }
    #gvcore01-root .gvcore01-shell {
      background: #000;
      border: 1px solid #137aa3;
      border-radius: 8px;
      overflow: hidden;
    }
    #gvcore01-aladin {
      width: 100%;
      height: 560px;
      background: #000;
    }
    #gvcore01-status {
      margin-top: 10px;
      padding: 9px 11px;
      border: 1px solid #0d668a;
      border-radius: 7px;
      background: #02080d;
      color: #8be0ff;
      font-family: monospace;
      white-space: pre-wrap;
    }
  </style>

  <div class="gvcore01-title">
    <div class="gvcore01-comet" aria-hidden="true"></div>
    <div class="gvcore01-title-text">GALAXY VIEWER</div>
  </div>

  <div class="gvcore01-shell">
    <div id="gvcore01-aladin"></div>
  </div>

  <div id="gvcore01-status">Loading live Aladin viewer…</div>
</div>

<script>
(async () => {
  const status = document.getElementById('gvcore01-status');
  try {
    if (!window.A || !A.init) {
      const css = document.createElement('link');
      css.rel = 'stylesheet';
      css.href = 'https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.min.css';
      document.head.appendChild(css);

      await new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js';
        script.onload = resolve;
        script.onerror = () => reject(new Error('Aladin library failed to load.'));
        document.head.appendChild(script);
      });
    }

    await A.init;
    window.gvcore01Aladin = A.aladin('#gvcore01-aladin', {
      target: 'M31',
      survey: 'P/DSS2/color',
      fov: 1,
      cooFrame: 'ICRS',
      showReticle: true,
      showZoomControl: true,
      showFullscreenControl: true,
      showLayersControl: true,
      showGotoControl: true,
      showCooGridControl: true,
      showSimbadPointerControl: true
    });
    status.textContent = 'Galaxy Viewer core loaded.';
  } catch (error) {
    status.textContent = 'Viewer initialization failed: ' + String(error?.message || error);
  }
})();
</script>
'''

display(HTML(HTML_CONTENT))
