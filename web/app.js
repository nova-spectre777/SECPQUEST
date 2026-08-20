const $=id=>document.getElementById(id);const post=async(path,data)=>{const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});return await r.json()};const pretty=x=>JSON.stringify(x,null,2);let puzzles=[];
async function loadFeatures(){const r=await fetch('/api/features');$('featuresOut').textContent=pretty(await r.json())}
async function init(){const r=await fetch('/api/puzzles');const d=await r.json();puzzles=d.puzzles;for(const p of puzzles){const o=document.createElement('option');o.value=p.id;o.textContent=p.title;$('puzzle').appendChild(o)}showPuzzle();loadFeatures();const secs=[...document.querySelectorAll('section[data-title]')];$('nav').innerHTML=secs.map(s=>`<a href="#${s.id}">${s.dataset.title}</a>`).join('');$('filter').oninput=e=>{const q=e.target.value.toLowerCase();secs.forEach(s=>s.style.display=s.dataset.title.toLowerCase().includes(q)?'block':'none')}}
function selected(){return $('puzzle').value}function showPuzzle(){const p=puzzles.find(x=>x.id===selected());$('puzzleOut').textContent=pretty(p)}
async function plan(){$('planOut').textContent=pretty(await post('/api/plan',{puzzle:selected(),shards:+$('shards').value,index:+$('shardIndex').value}))}
async function runSearch(){$('searchOut').textContent='Searching…';$('searchOut').textContent=pretty(await post('/api/search',{puzzle:selected(),start:$('searchStart').value||null,max_keys:+$('maxKeys').value}))}
async function verifyCandidate(){$('verifyOut').textContent=pretty(await post('/api/verify',{puzzle:selected(),candidate:$('candidate').value}))}
async function point(){$('pointOut').textContent=pretty(await post('/api/point',{scalar:$('scalar').value}))}
async function hashIt(){$('hashOut').textContent=pretty(await post('/api/hash',{data:$('hashData').value,mode:'text'}))}
async function h160(){$('h160Out').textContent=pretty(await post('/api/hash160-addresses',{hash160:$('h160in').value}))}
async function scriptAddr(){$('scriptOut').textContent=pretty(await post('/api/script-addresses',{script:$('scriptIn').value}))}
async function der(){$('derOut').textContent=pretty(await post('/api/der',{signature:$('derIn').value}))}
async function tx(){$('txOut').textContent=pretty(await post('/api/tx/decode',{hex:$('txIn').value}))}init();