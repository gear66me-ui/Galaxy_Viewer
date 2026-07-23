from IPython.display import HTML, display

# GALAXY-VIEWER-CORE-04
# Standalone finished widget: futuristic Galaxy Viewer header + unchanged live Aladin viewer.
# Reticle disabled. No status text. No catalog, bridge, table, or extra controls.

HTML_CONTENT = r'''
<div id="gvcore04-root">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&display=swap');

    #gvcore04-root{
      width:100%;max-width:1180px;margin:0 auto;padding:14px;box-sizing:border-box;
      background:#000;color:#dff8ff;font-family:Arial,Helvetica,sans-serif;
      border:1px solid #164c6b;border-radius:12px;
      box-shadow:0 0 26px rgba(53,198,255,.20),inset 0 0 30px rgba(14,78,112,.10)
    }
    #gvcore04-root .gvcore04-header{
      position:relative;height:118px;margin-bottom:14px;overflow:hidden;border-radius:10px;
      border:1px solid #1b6d96;
      background:
        radial-gradient(circle at 77% 42%,rgba(255,255,255,.95) 0 1.2%,rgba(255,233,205,.75) 2.2%,rgba(180,205,222,.22) 7%,transparent 17%),
        radial-gradient(ellipse at 79% 47%,rgba(236,236,224,.72) 0 7%,rgba(126,159,178,.22) 17%,transparent 39%),
        radial-gradient(circle at 12% 25%,rgba(255,255,255,.85) 0 1px,transparent 1.5px),
        radial-gradient(circle at 34% 66%,rgba(93,191,255,.72) 0 1px,transparent 1.7px),
        linear-gradient(108deg,#01050a 0%,#020a12 42%,#07111a 70%,#000 100%);
      background-size:auto,auto,86px 86px,127px 127px,auto;
      box-shadow:inset 0 0 42px rgba(0,0,0,.72)
    }
    #gvcore04-root .gvcore04-header::before{
      content:"";position:absolute;right:1.5%;top:-14%;width:45%;height:142%;
      background:
        radial-gradient(ellipse at 60% 50%,rgba(255,247,225,.94) 0 9%,rgba(213,219,214,.62) 14%,rgba(116,143,160,.28) 31%,transparent 58%);
      transform:rotate(-10deg);filter:blur(.3px);opacity:.95
    }
    #gvcore04-root .gvcore04-header::after{
      content:"";position:absolute;right:18%;top:17%;width:27%;height:8px;border-radius:999px;
      background:linear-gradient(90deg,transparent,rgba(99,178,235,.18),rgba(215,244,255,.66),#fff);
      filter:blur(2px);transform:rotate(-7deg);opacity:.72
    }
    #gvcore04-root .gvcore04-title{
      position:absolute;z-index:3;left:34px;top:50%;transform:translateY(-50%);
      font-family:"Michroma","Eurostile","Bank Gothic",sans-serif;
      font-size:clamp(28px,5vw,54px);font-weight:400;letter-spacing:.14em;white-space:nowrap;
      color:#ecfbff;text-shadow:0 0 5px #8bdfff,0 0 13px #35c6ff,0 0 28px rgba(53,198,255,.75)
    }
    #gvcore04-root .gvcore04-shell{
      background:#000;border:1px solid #1b6d96;border-radius:10px;overflow:hidden;
      box-shadow:0 0 18px rgba(53,198,255,.12)
    }
    #gvcore04-aladin{width:100%;height:560px;background:#000}

    @media(max-width:700px){
      #gvcore04-root .gvcore04-header{height:90px}
      #gvcore04-root .gvcore04-title{left:18px;letter-spacing:.08em}
      #gvcore04-root .gvcore04-header::before{width:52%;right:-4%}
    }
  </style>

  <div class="gvcore04-header">
    <div class="gvcore04-title">GALAXY VIEWER</div>
  </div>

  <div class="gvcore04-shell">
    <div id="gvcore04-aladin"></div>
  </div>
</div>

<script>
(async()=>{
  try{
    if(!window.A||!A.init){
      const css=document.createElement('link');
      css.rel='stylesheet';
      css.href='https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.min.css';
      document.head.appendChild(css);
      await new Promise((resolve,reject)=>{
        const script=document.createElement('script');
        script.src='https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js';
        script.onload=resolve;
        script.onerror=()=>reject(new Error('Aladin library failed to load.'));
        document.head.appendChild(script);
      });
    }
    await A.init;
    window.gvcore04Aladin=A.aladin('#gvcore04-aladin',{
      target:'M31',survey:'P/DSS2/color',fov:1,cooFrame:'ICRS',
      showReticle:false,
      showZoomControl:true,
      showFullscreenControl:true,
      showLayersControl:true,
      showGotoControl:true,
      showCooGridControl:true,
      showSimbadPointerControl:true
    });
  }catch(error){console.error('GALAXY-VIEWER-CORE-04 failed:',error)}
})();
</script>
'''

display(HTML(HTML_CONTENT))
