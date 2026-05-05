import re

with open('/Users/boss/Downloads/index (5).html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the IndexedDB section
original = """// ════════════════════════════════════════════════════════
//  IndexedDB — Database layer (thay thế MySQL)
// ════════════════════════════════════════════════════════
function openDB(){
  return new Promise((resolve,reject)=>{
    const req=indexedDB.open('TokyoLifeWMS',1);
    req.onupgradeneeded=e=>{
      const db=e.target.result;
      ['users','suppliers','products','imports','exports'].forEach(store=>{
        if(!db.objectStoreNames.contains(store)){
          db.createObjectStore(store,{keyPath:'id'});
        }
      });
    };
    req.onsuccess=e=>resolve(e.target.result);
    req.onerror=e=>reject(e);
  });
}

function dbGetAll(store){
  return new Promise((resolve,reject)=>{
    const tx=DB.transaction(store,'readonly');
    const req=tx.objectStore(store).getAll();
    req.onsuccess=e=>resolve(e.target.result);
    req.onerror=e=>reject(e);
  });
}
function dbGet(store,id){
  return new Promise((resolve,reject)=>{
    const tx=DB.transaction(store,'readonly');
    const req=tx.objectStore(store).get(id);
    req.onsuccess=e=>resolve(e.target.result);
    req.onerror=e=>reject(e);
  });
}
function dbPut(store,obj){
  return new Promise((resolve,reject)=>{
    const tx=DB.transaction(store,'readwrite');
    const req=tx.objectStore(store).put(obj);
    req.onsuccess=e=>resolve(e.target.result);
    req.onerror=e=>reject(e);
  });
}
function dbDelete(store,id){
  return new Promise((resolve,reject)=>{
    const tx=DB.transaction(store,'readwrite');
    const req=tx.objectStore(store).delete(id);
    req.onsuccess=e=>resolve(e.target.result);
    req.onerror=e=>reject(e);
  });
}"""

replacement = """// ════════════════════════════════════════════════════════
//  API Call — Database layer (kết nối với Node.js Backend)
// ════════════════════════════════════════════════════════
async function openDB(){
  return true; // Không cần khởi tạo IndexedDB nữa
}

async function dbGetAll(store){
  const res = await fetch('/api/' + store);
  return res.json();
}
async function dbGet(store,id){
  const res = await fetch('/api/' + store + '/' + id);
  return res.json();
}
async function dbPut(store,obj){
  const res = await fetch('/api/' + store, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(obj)
  });
  return res.json();
}
async function dbDelete(store,id){
  const res = await fetch('/api/' + store + '/' + id, { method: 'DELETE' });
  return res.json();
}"""

if original in content:
    content = content.replace(original, replacement)
    print("Replaced IndexedDB functions successfully")
else:
    print("Could not find exact IndexedDB match, attempting regex replacement")
    # regex fallback if there are slight whitespace differences
    pattern = re.compile(r"// \u2550{56}\n//  IndexedDB.*?function dbDelete\(store,id\)\{.*?\n\}", re.DOTALL)
    content = re.sub(pattern, replacement, content)
    
with open('/Users/boss/.gemini/antigravity/scratch/tokyolife-wms/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
