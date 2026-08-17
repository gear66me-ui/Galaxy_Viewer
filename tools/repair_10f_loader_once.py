from pathlib import Path

p=Path('viewer/GV-beta-0010F.py')
s=p.read_text()
old_url="const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/gv-random-galaxy-0031.js?v=eaf76aa364853e1f997c5ec439bd8e0205a5e0c8';"
new_url="const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/1e6e2de79c24164003dd313132134b3866c2ca36/viewer/modules/gv-random-galaxy-0031.js?v=eaf76aa364853e1f997c5ec439bd8e0205a5e0c8';"
assert s.count(old_url)==1
s=s.replace(old_url,new_url)
old='''    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const existing=[...document.scripts].find(script=>script.src===url||script.dataset[datasetKey]==='true');
            if(existing){
                if(existing.dataset.gvLoaded==='true'){resolve(existing);return}
                existing.addEventListener('load',()=>resolve(existing),{once:true});
                existing.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
                return;
            }
            const script=document.createElement('script');
            script.src=url;
            script.charset='utf-8';
            script.dataset[datasetKey]='true';
            script.addEventListener('load',()=>{script.dataset.gvLoaded='true';resolve(script)},{once:true});
            script.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
            document.head.appendChild(script);
        });
    }
'''
new='''    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const existing=[...document.scripts].find(script=>script.src===url||script.dataset[datasetKey]==='true');
            if(existing){
                if(existing.dataset.gvLoaded==='true'){resolve(existing);return}
                existing.addEventListener('load',()=>resolve(existing),{once:true});
                existing.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
                return;
            }
            const script=document.createElement('script');
            script.charset='utf-8';
            script.dataset[datasetKey]='true';
            if(url.startsWith('https://raw.githubusercontent.com/')){
                fetch(url,{cache:'no-store'}).then(response=>{
                    if(!response.ok)throw new Error('SCRIPT FETCH RETURNED HTTP '+response.status+': '+url);
                    return response.text();
                }).then(source=>{
                    script.textContent=source;
                    document.head.appendChild(script);
                    script.dataset.gvLoaded='true';
                    resolve(script);
                }).catch(error=>reject(new Error('SCRIPT FAILED TO LOAD: '+url+' — '+String(error?.message||error))));
                return;
            }
            script.src=url;
            script.addEventListener('load',()=>{script.dataset.gvLoaded='true';resolve(script)},{once:true});
            script.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
            document.head.appendChild(script);
        });
    }
'''
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s)
