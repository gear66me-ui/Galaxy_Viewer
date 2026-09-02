/*
GALAXY VIEWER RANDOM GALAXY 0086-01 — CONTROLLED NAVIGATION BENCHMARK DERIVATIVE
ECO-ID: ECO-20260902-12AR01-NAV-BENCH-001
BASELINE: viewer/modules/random-galaxy/gv-random-galaxy-0086.js
BASELINE GIT BLOB: 04876b77875684115c7e4c0a7e61fe8dec336503

This engineering-test derivative leaves 0086 untouched. It synchronously loads the
exact authorized 0086 baseline, verifies the Git blob SHA, applies only the
navigation-law replacements declared below, then executes the verified result.
*/
(function(){
  'use strict';

  const SOURCE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/random-galaxy/gv-random-galaxy-0086.js?v=04876b77875684115c7e4c0a7e61fe8dec336503';
  const EXPECTED_BLOB='04876b77875684115c7e4c0a7e61fe8dec336503';

  function rol(value,bits){return ((value<<bits)|(value>>>(32-bits)))>>>0}
  function sha1Bytes(bytes){
    const originalLength=bytes.length;
    const bitLength=originalLength*8;
    const paddedLength=(((originalLength+9+63)>>6)<<6);
    const data=new Uint8Array(paddedLength);
    data.set(bytes);
    data[originalLength]=0x80;
    const view=new DataView(data.buffer);
    const high=Math.floor(bitLength/0x100000000);
    const low=bitLength>>>0;
    view.setUint32(paddedLength-8,high,false);
    view.setUint32(paddedLength-4,low,false);
    let h0=0x67452301,h1=0xEFCDAB89,h2=0x98BADCFE,h3=0x10325476,h4=0xC3D2E1F0;
    const w=new Uint32Array(80);
    for(let offset=0;offset<paddedLength;offset+=64){
      for(let i=0;i<16;i++)w[i]=view.getUint32(offset+i*4,false);
      for(let i=16;i<80;i++)w[i]=rol(w[i-3]^w[i-8]^w[i-14]^w[i-16],1);
      let a=h0,b=h1,c=h2,d=h3,e=h4;
      for(let i=0;i<80;i++){
        let f,k;
        if(i<20){f=(b&c)|((~b)&d);k=0x5A827999}
        else if(i<40){f=b^c^d;k=0x6ED9EBA1}
        else if(i<60){f=(b&c)|(b&d)|(c&d);k=0x8F1BBCDC}
        else{f=b^c^d;k=0xCA62C1D6}
        const temp=(rol(a,5)+(f>>>0)+e+k+w[i])>>>0;
        e=d;d=c;c=rol(b,30);b=a;a=temp;
      }
      h0=(h0+a)>>>0;h1=(h1+b)>>>0;h2=(h2+c)>>>0;h3=(h3+d)>>>0;h4=(h4+e)>>>0;
    }
    return [h0,h1,h2,h3,h4].map(v=>v.toString(16).padStart(8,'0')).join('');
  }

  function gitBlobSha(text){
    const body=new TextEncoder().encode(text);
    const head=new TextEncoder().encode(`blob ${body.length}\0`);
    const all=new Uint8Array(head.length+body.length);
    all.set(head);all.set(body,head.length);
    return sha1Bytes(all);
  }

  function replaceOnce(source,needle,replacement,label){
    const first=source.indexOf(needle);
    const last=source.lastIndexOf(needle);
    if(first<0||first!==last)throw new Error(`0086-01 ${label}: expected exactly one baseline occurrence`);
    return source.slice(0,first)+replacement+source.slice(first+needle.length);
  }

  function replaceRegexOnce(source,re,replacement,label){
    const flags=re.flags.includes('g')?re.flags:re.flags+'g';
    const probe=new RegExp(re.source,flags);
    const matches=[...source.matchAll(probe)];
    if(matches.length!==1)throw new Error(`0086-01 ${label}: expected one match, got ${matches.length}`);
    return source.replace(re,replacement);
  }

  const xhr=new XMLHttpRequest();
  xhr.open('GET',SOURCE_URL,false);
  xhr.send(null);
  if(xhr.status<200||xhr.status>=300)throw new Error(`0086-01 baseline fetch failed HTTP ${xhr.status}`);
  let source=xhr.responseText;
  const actualBlob=gitBlobSha(source);
  if(actualBlob!==EXPECTED_BLOB)throw new Error(`0086-01 BASELINE DRIFT expected ${EXPECTED_BLOB} got ${actualBlob}`);

  source=replaceOnce(source,"const VERSION='0086';","const VERSION='0086-01';",'VERSION');
  source=replaceOnce(source,'    translateStart: 0.34,','    translateStart: 0.30,','translateStart');
  source=replaceOnce(source,'    turnPoint: 0.46,','    turnPoint: 0.50,','turnPoint');
  source=replaceOnce(source,'    translate90: 0.58,','    translate90: 0.70,','translate90');
  source=replaceOnce(source,'    translationComplete: 0.68,','    translationComplete: 0.70,','translationComplete');

  source=replaceOnce(
    source,
    "  function smootherstep(value) {\n    const t = clamp01(value);\n    return t * t * t * (t * (t * 6 - 15) + 10);\n  }",
    "  function smootherstep(value) {\n    const t = clamp01(value);\n    return t * t * t * (t * (t * 6 - 15) + 10);\n  }\n  function navigationSmootherstep(value) {\n    const t = clamp01(value);\n    return 35*t*t*t*t - 84*t*t*t*t*t + 70*t*t*t*t*t*t - 20*t*t*t*t*t*t*t;\n  }",
    'navigation S7 insertion'
  );

  source=replaceRegexOnce(
    source,
    /    #translationProgress\(t, immediate = false\) \{[\s\S]*?\n    \}\n    #fovAt\(t, startFov, destinationFov, immediate = false\) \{/,
    "    #translationProgress(t, immediate = false) {\n      if (immediate) return clamp01(t);\n      const start = Number(this.options.translateStart);\n      const complete = Number(this.options.translationComplete);\n      if (t <= start) return 0;\n      if (t >= complete) return 1;\n      return navigationSmootherstep((t - start) / (complete - start));\n    }\n    #fovAt(t, startFov, destinationFov, immediate = false) {",
    'translation profile'
  );

  source=replaceOnce(source,'        const progress = smootherstep(t / turn);','        const progress = navigationSmootherstep(t / turn);','FOV outbound S7');
  source=replaceOnce(source,'      const progress = smootherstep((t - turn) / (1 - turn));','      const progress = navigationSmootherstep((t - turn) / (1 - turn));','FOV inbound S7');

  source=replaceRegexOnce(
    source,
    /    #distanceProgress\(t\) \{[\s\S]*?\n    \}\n    #showDistance\(/,
    "    #distanceProgress(t) {\n      return navigationSmootherstep(t);\n    }\n    #showDistance(",
    'distance progress S7'
  );

  source=replaceRegexOnce(
    source,
    /    #travelHudProgress\(t\) \{[\s\S]*?\n    \}\n\n    #formatTravelHudDistance/,
    "    #travelHudProgress(t) {\n      return navigationSmootherstep(t);\n    }\n\n    #formatTravelHudDistance",
    'travel HUD S7'
  );

  source=replaceOnce(source,'        const baseDestinationRA=finiteNumber(destination.framingBaseRa)??Number(destination.ra);','        const baseDestinationRA=Number(destination.ra);','no-tail RA target');
  source=replaceOnce(source,'        const baseDestinationDec=finiteNumber(destination.framingBaseDec)??Number(destination.dec);','        const baseDestinationDec=Number(destination.dec);','no-tail Dec target');
  source=replaceOnce(source,'        const baseDestinationFov=finiteNumber(destination.framingBaseFov)??destinationFov;','        const baseDestinationFov=destinationFov;','no-tail FOV target');

  source=replaceOnce(
    source,
    '        const turnPoint=Number(this.options.turnPoint);\n        const alignmentStart=Math.max(turnPoint,.76);',
    '        const turnPoint=Number(this.options.turnPoint);\n        const rotationStartPoint=firstHomeTrip?turnPoint:Number(this.options.translateStart);\n        const alignmentStart=firstHomeTrip?Math.max(turnPoint,.76):Number(this.options.translationComplete);',
    'rotation window setup'
  );
  source=replaceOnce(source,'                t>=turnPoint &&\n                t<alignmentStart &&','                t>=rotationStartPoint &&\n                t<alignmentStart &&','rotation start condition');
  source=replaceOnce(
    source,
    '                const rotationProgress=smootherstep(\n                  (t-turnPoint)/(alignmentStart-turnPoint)\n                );',
    '                const rotationProgress=(firstHomeTrip?smootherstep:navigationSmootherstep)(\n                  (t-rotationStartPoint)/(alignmentStart-rotationStartPoint)\n                );',
    'rotation S7 progress'
  );

  source += '\n//# sourceURL=gv-random-galaxy-0086-01-derived.js';
  (0,eval)(source);

  if(window.GalaxyRandomGalaxy?.VERSION!=='0086-01')
    throw new Error('RANDOM GALAXY 0086-01 EXPORT MISSING AFTER CONTROLLED DERIVATION');
})();
