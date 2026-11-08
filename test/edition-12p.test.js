import test from "node:test";
import assert from "node:assert/strict";
import {createEditionDraft,validateEdition} from "../src/editorial/edition-12p.js";
const article=()=>({
 title:"Titular de prueba",body:"Borrador con contenido verificable, no publicable desde este test.",
 eventDate:"2026-11-07",sourcePublicationDate:"2026-11-07",
 sources:[{url:"https://example.org/fuente",publisher:"Fuente de prueba",checkedAt:"2026-11-07T16:00:00-05:00"}],
 verifiedBy:"editor-prueba",visual:{type:"none"},sensitiveAllegation:false,
 approval:{editorId:"director-prueba",approvedAt:"2026-11-07T18:00:00-05:00"}
});
const filled=()=>{const e=createEditionDraft("2026-11-07");for(const p of e.pages)for(const s of p.slots)s.article=article();return e};
test("crea 12 páginas y 36 huecos, todos bloqueados",()=>{
 const e=createEditionDraft("2026-11-07");
 assert.equal(e.pages.length,12);
 assert.equal(e.pages[0].slots.length,0);
 assert.equal(e.pages[1].slots.length,4);
 assert.equal(e.pages[11].slots.length,3);
 assert.equal(e.pages.flatMap(p=>p.slots).length,36);
 assert.equal(e.autoPublish,false);
 assert.equal(validateEdition(e).ready,false);
});
test("36 expedientes con trazabilidad formal superan solo validación de esquema",()=>{
 const e=filled(),r=validateEdition(e);
 assert.equal(r.ready,true,JSON.stringify(r.issues));
 assert.equal(r.count,36);
 assert.equal(e.autoPublish,false);
});
test("no aprueba una noticia sin fuente ni derechos de foto",()=>{
 const e=filled();
 e.pages[0].slots[0].article.sources=[];
 e.pages[1].slots[0].article.visual={type:"photo"};
 assert.equal(validateEdition(e).ready,false);
});
test("denuncia sensible requiere auditoría legal y registro del descargo",()=>{
 const e=filled();
 e.pages[0].slots[0].article.sensitiveAllegation=true;
 assert.equal(validateEdition(e).ready,false);
});
test("activar autoPublish bloquea la edición",()=>{
 const e=filled();e.autoPublish=true;
 assert.equal(validateEdition(e).ready,false);
});
