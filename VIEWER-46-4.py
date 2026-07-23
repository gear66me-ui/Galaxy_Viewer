from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-46-4 — corrected final audit
# Immutable baseline: VIEWER-45 commit a9002326395ea21b6aab0e3968b77c30fcd80741.
# Authorized changes only: preserve the working viewer/Get Info path; combine
# Angular Size / Physical Size immediately after Morphological Type; remove
# Interest Score; and normalize Galaxy Age and Redshift fonts while retaining yellow.

display(Javascript(r'''
(() => {
  window['viewer42-bridge12-patch'] = true;
  window['viewer43-size-row-patch'] = true;
  window['viewer44-age-font-patch'] = true;
  window['viewer45-remove-interest-score'] = true;
  window.viewer46FinalTitle = 'Galaxy Viewer — VIEWER-46';
})();
'''))

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a9002326395ea21b6aab0e3968b77c30fcd80741/VIEWER-45.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-45-immutable-base.py", "exec"))


display(Javascript(r'''
(() => {
  if(window.viewer46Observer){
    try{ window.viewer46Observer.disconnect(); }catch(_){ }
    window.viewer46Observer = null;
  }
  if(window.viewer46Guard){
    clearInterval(window.viewer46Guard);
    window.viewer46Guard = null;
  }
  if(window.viewer46ApplyTimer){
    clearTimeout(window.viewer46ApplyTimer);
    window.viewer46ApplyTimer = null;
  }

  const YELLOW = '#ffd84d';

  function clean(v){ return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function status(){ return document.getElementById('viewer14Status'); }
  function rows(){ return [...(status()?.querySelectorAll('tr') || [])]; }
  function label(row){ return clean(row?.querySelector('th')?.textContent); }
  function rowBy(...names){
    const wanted = names.map(x => clean(x).toLowerCase());
    return rows().find(row => wanted.includes(label(row).toLowerCase()));
  }

  function installTitle(){
    const title = window.viewer46FinalTitle || 'Galaxy Viewer — VIEWER-46';
    let style = document.getElementById('viewer46TitleStyle');
    if(!style){
      style = document.createElement('style');
      style.id = 'viewer46TitleStyle';
      document.head.appendChild(style);
    }
    const css = `#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"${title}";font-size:22px!important;color:#35c6ff!important}`;
    if(style.textContent !== css) style.textContent = css;
  }

  function conciseAge(text){
    const value = clean(text);
    const match = value.match(/approximately\s+([0-9]+(?:\.[0-9]+)?)\s+billion\s+years/i);
    return match ? `Approximately ${match[1]} billion years` : value;
  }

  function normalFontSize(){
    const normal = rows().find(row => {
      const name = label(row).toLowerCase();
      return name && !['galaxy age','redshift (z) / distance','redshift / distance'].includes(name);
    });
    const cell = normal?.querySelector('td') || normal?.querySelector('th');
    return cell ? getComputedStyle(cell).fontSize : '16px';
  }

  function angularFirst(text){
    let value = clean(text);
    value = value.replace(/arcminutes?/gi, 'arcmin').replace(/arcsecs?/gi, 'arcsec');
    return value;
  }

  function physicalMillionLy(text){
    let value = clean(text);
    const thousand = value.match(/^([0-9.]+)\s*[×x]\s*([0-9.]+)\s*thousand\s*(?:light[- ]?years?|ly)(.*)$/i);
    if(thousand){
      const major = Number(thousand[1]) / 1000;
      const minor = Number(thousand[2]) / 1000;
      const suffix = clean(thousand[3]);
      return `${major.toFixed(4).replace(/0+$/,'').replace(/\.$/,'')} × ${minor.toFixed(4).replace(/0+$/,'').replace(/\.$/,'')} million ly${suffix ? ` ${suffix}` : ''}`;
    }
    value = value.replace(/million\s*(?:light[- ]?years?|ly)/gi, 'million ly');
    return value;
  }

  function combineSizeRows(){
    const angular = rowBy('Angular size');
    const physical = rowBy('Physical size');
    let combined = rowBy('Angular size / Physical size','Angular / physical size','Physical size / Angular size','Physical / angular size');
    const morphology = rowBy('Morphological type','Morphology');

    if(!combined && (angular || physical)) combined = angular || physical;
    if(!combined) return;

    const th = combined.querySelector('th');
    const td = combined.querySelector('td');
    const angularText = angularFirst(angular?.querySelector('td')?.textContent || (label(combined).toLowerCase().startsWith('angular') ? td?.textContent : ''));
    const physicalText = physicalMillionLy(physical?.querySelector('td')?.textContent || (label(combined).toLowerCase().startsWith('physical') ? td?.textContent : ''));

    if(th) th.textContent = 'Angular size / Physical size';
    if(td){
      const parts = [];
      if(angularText) parts.push(angularText);
      if(physicalText) parts.push(physicalText);
      if(parts.length) td.textContent = parts.join(' / ');
    }

    if(angular && angular !== combined) angular.remove();
    if(physical && physical !== combined) physical.remove();
    if(morphology && morphology.nextElementSibling !== combined){
      morphology.parentNode.insertBefore(combined, morphology.nextElementSibling);
    }
  }

  function apply(){
    const table = status();
    if(!table){ installTitle(); return false; }

    rows().forEach(row => {
      if(label(row).toLowerCase() === 'interest score') row.remove();
    });

    combineSizeRows();

    const age = rowBy('Galaxy age');
    const ageCell = age?.querySelector('td');
    if(ageCell){
      const next = conciseAge(ageCell.textContent);
      if(next && clean(ageCell.textContent) !== next) ageCell.textContent = next;
    }

    const size = normalFontSize();
    ['Galaxy age','Redshift (z) / Distance','Redshift / Distance'].forEach(name => {
      const row = rowBy(name);
      if(!row) return;
      row.classList.remove('emphasis');
      [row.querySelector('th'), row.querySelector('td')].forEach(cell => {
        if(!cell) return;
        cell.style.setProperty('color', YELLOW, 'important');
        cell.style.setProperty('font-size', size, 'important');
        cell.style.setProperty('font-family', 'inherit', 'important');
        cell.style.setProperty('font-weight', 'inherit', 'important');
        cell.style.setProperty('line-height', 'normal', 'important');
      });
    });

    installTitle();
    return true;
  }

  apply();
  const target = status();
  if(target){
    const observer = new MutationObserver(() => {
      clearTimeout(window.viewer46ApplyTimer);
      window.viewer46ApplyTimer = setTimeout(apply, 80);
    });
    observer.observe(target, {childList:true, subtree:true, characterData:true});
    window.viewer46Observer = observer;
  }
  window.viewer46Guard = setInterval(apply, 500);
})();
'''))
