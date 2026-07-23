from IPython.display import HTML, display

# GALAXY-VIEWER-CORE-02
# Scope locked: title/header styling only. Live Aladin viewer settings preserved from CORE-01.

HTML_CONTENT = r'''
<div id="gvcore02-root">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&display=swap');

    #gvcore02-root {
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

    #gvcore02-root .gvcore02-title {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      min-height: 82px;
      margin: 0 0 12px;
      padding: 12px 18px;
      border: 1px solid #137aa3;
      border-radius: 9px;
      background:
        radial-gradient(circle at 78% 32%, rgba(53,198,255,.14), transparent 25%),
        radial-gradient(circle at 18% 75%, rgba(138,79,212,.12), transparent 28%),
        linear-gradient(90deg, #01050a, #020b12 58%, #000);
      overflow: hidden;
    }

    #gvcore02-root .gvcore02-title::before {
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      background-image:
        radial-gradient(circle, rgba(255,255,255,.85) 0 1px, transparent 1.4px),
        radial-gradient(circle, rgba(53,198,255,.65) 0 1px, transparent 1.4px);
      background-size: 92px 92px, 137px 137px;
      background-position: 17px 12px, 55px 31px;
      opacity: .34;
    }

    #gvcore02-root .gvcore02-title-text {
      position: relative;
      z-index: 2;
      display: inline-flex;
      align-items: baseline;
      font-family: "Michroma", "Eurostile", "Bank Gothic", sans-serif;
      font-size: clamp(23px, 4vw, 42px);
      font-weight: 400;
      letter-spacing: .16em;
      line-height: 1;
      color: #eafcff;
      text-shadow:
        0 0 5px #35c6ff,
        0 0 14px rgba(53,198,255,.76),
        0 0 28px rgba(53,198,255,.28);
      white-space: nowrap;
    }

    #gvcore02-root .gvcore02-viewer-word {
      position: relative;
      display: inline-block;
    }

    #gvcore02-root .gvcore02-dust {
      position: absolute;
      left: 58%;
      right: -3%;
      top: 70%;
      height: 86px;
      pointer-events: none;
      z-index: 1;
    }

    #gvcore02-root .gvcore02-dust span {
      position: absolute;
      display: block;
      width: 3px;
      height: 3px;
      border-radius: 50%;
      background: #dff9ff;
      box-shadow: 0 0 5px #35c6ff;
      opacity: 0;
      animation: gvcore02-fall 4.8s linear infinite;
    }

    #gvcore02-root .gvcore02-dust span:nth-child(1){left:8%;animation-delay:.1s}
    #gvcore02-root .gvcore02-dust span:nth-child(2){left:18%;animation-delay:.8s;width:2px;height:2px}
    #gvcore02-root .gvcore02-dust span:nth-child(3){left:30%;animation-delay:1.5s}
    #gvcore02-root .gvcore02-dust span:nth-child(4){left:42%;animation-delay:2.2s;width:2px;height:2px}
    #gvcore02-root .gvcore02-dust span:nth-child(5){left:55%;animation-delay:2.9s}
    #gvcore02-root .gvcore02-dust span:nth-child(6){left:66%;animation-delay:3.6s;width:2px;height:2px}
    #gvcore02-root .gvcore02-dust span:nth-child(7){left:78%;animation-delay:4.1s}
    #gvcore02-root .gvcore02-dust span:nth-child(8){left:90%;animation-delay:1.9s;width:2px;height:2px}
    #gvcore02-root .gvcore02-dust span:nth-child(9){left:96%;animation-delay:3.2s}

    @keyframes gvcore02-fall {
      0%   { transform: translate3d(0,-4px,0) scale(1); opacity: 0; }
      10%  { opacity: .95; }
      55%  { opacity: .72; }
      100% { transform: translate3d(13px,72px,0) scale(.18); opacity: 0; }
    }

    #gvcore02-root .gvcore02-comet {
      position: relative;
      z-index: 2;
      width: 128px;
      height: 42px;
      flex: 0 0 128px;
    }

    #gvcore02-root .gvcore02-comet-tail {
      position: absolute;
      left: 0;
      right: 22px;
      top: 15px;
      height: 12px;
      border-radius: 999px;
      background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(138,79,212,.08) 18%,
        rgba(138,79,212,.28) 42%,
        rgba(53,198,255,.62) 70%,
        rgba(223,249,255,.96) 100%
      );
      filter: blur(1.4px);
      transform: skewX(-20deg);
    }

    #gvcore02-root .gvcore02-comet-tail::before,
    #gvcore02-root .gvcore02-comet-tail::after {
      content: "";
      position: absolute;
      right: 0;
      width: 88%;
      height: 5px;
      border-radius: 999px;
      background: linear-gradient(90deg, transparent, rgba(53,198,255,.38), rgba(255,255,255,.82));
      filter: blur(1px);
    }

    #gvcore02-root .gvcore02-comet-tail::before {
      top: -7px;
      transform: rotate(-5deg);
    }

    #gvcore02-root .gvcore02-comet-tail::after {
      top: 13px;
      transform: rotate(5deg);
    }

    #gvcore02-root .gvcore02-comet-head {
      position: absolute;
      right: 2px;
      top: 7px;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: radial-gradient(circle at 34% 34%, #fff 0 16%, #dff9ff 24%, #7FDBFF 42%, #35c6ff 58%, #0a6f98 76%, transparent 78%);
      box-shadow:
        0 0 10px #fff,
        0 0 20px #35c6ff,
        0 0 34px rgba(53,198,255,.72);
    }

    #gvcore02-root .gvcore02-shell {
      background: #000;
      border: 1px solid #137aa3;
      border-radius: 8px;
      overflow: hidden;
    }

    #gvcore02-aladin {
      width: 100%;
      height: 560px;
      background: #000;
    }

    @media (max-width: 680px) {
      #gvcore02-root .gvcore02-title {
        min-height: 72px;
        padding: 10px 12px;
      }
      #gvcore02-root .gvcore02-comet {
        width: 90px;
        flex-basis: 90px;
      }
      #gvcore02-root .gvcore02-title-text {
        letter-spacing: .09em;
      }
    }
  </style>

  <div class="gvcore02-title">
    <div class="gvcore02-title-text">
      <span>GALAXY&nbsp;</span>
      <span class="gvcore02-viewer-word">VIEWER
        <span class="gvcore02-dust" aria-hidden="true">
          <span></span><span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span>
        </span>
      </span>
    </div>

    <div class="gvcore02-comet" aria-hidden="true">
      <div class="gvcore02-comet-tail"></div>
      <div class="gvcore02-comet-head"></div>
    </div>
  </div>

  <div class="gvcore02-shell">
    <div id="gvcore02-aladin"></div>
  </div>
</div>

<script>
(async () => {
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
    window.gvcore02Aladin = A.aladin('#gvcore02-aladin', {
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
  } catch (error) {
    console.error('GALAXY-VIEWER-CORE-02 failed:', error);
  }
})();
</script>
'''

display(HTML(HTML_CONTENT))
