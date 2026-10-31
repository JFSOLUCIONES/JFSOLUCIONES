import fs from 'node:fs';
import { triage } from './triage.js';

const path = process.argv[2] || 'editorial/2026-10-31/9-publicaciones.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const issues=[];
const seen=new Set();
if(data.posts.length!==9) issues.push('El lote debe contener exactamente 9 publicaciones');
for(const p of data.posts){
 const tag='Post '+p.numero;
 if(!/^https:\/\//.test(p.url||'')) issues.push(tag+': falta URL de fuente');
 if(!/^2026-10-(29|30|31)$/.test(p.fecha_fuente||'')) issues.push(tag+': fecha de fuente sin verificar');
 if(!p.copy?.includes('periodiconomas.space') || !p.copy?.includes('+51 906 605 712')) issues.push(tag+': faltan web y contacto publico');
 if(p.estado!=='BORRADOR_PARA_APROBACION'||p.autopublicacion!==false) issues.push(tag+': requiere revisión humana');
 if(!p.riesgo || !p.fuente) issues.push(tag+': falta ficha documental o cautela editorial');
 if(!p.logo || p.logo!=='NO+') issues.push(tag+': logo incorrecto');
 if(seen.has(p.titular)) issues.push(tag+': titular duplicado');
 seen.add(p.titular);
 const r=triage({message:p.copy});
 if(r.autoPublish!==false||r.publicationApproved!==false) issues.push(tag+': clasificador no bloquea publicación automática');
}
console.log(JSON.stringify({fecha:data.fecha_programacion,posts:data.posts.length,passed:issues.length===0,issues},null,2));
if(issues.length) process.exitCode=1;
