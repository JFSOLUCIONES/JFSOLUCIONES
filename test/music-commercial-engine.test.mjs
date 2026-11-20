import test from "node:test";
import assert from "node:assert/strict";
import {quoteMusic, musicProductionHandoff} from "../src/jf-sales/music-commercial-engine.mjs";

test("campaña febrero no aplica antes de 2027",()=>{
 const q=quoteMusic({sku:"song_personal",now:"2026-11-19",campaignId:"love_2027",costPen:15,policy:{approved:true}});
 assert.equal(q.campaignApplied,false);assert.equal(q.netPen,80);
});
test("campaña borrador no aplica aun en febrero",()=>{
 const q=quoteMusic({sku:"song_personal",now:"2027-02-14",campaignId:"love_2027",costPen:15,policy:{approved:true}});
 assert.equal(q.campaignApplied,false);
});
test("sin costos validos no cotiza",()=>assert.throws(()=>quoteMusic({sku:"song_personal",now:"2026-11-19",costPen:NaN})));
test("precio bajo el margen minimo bloquea oferta",()=>{
 const q=quoteMusic({sku:"song_personal",now:"2026-11-19",costPen:60,policy:{approved:true,marginMin:0.35}});
 assert.equal(q.viable,false);assert.equal(q.decision,"REPRICE_OR_HUMAN_REVIEW");
});
test("tarifario sin autorizar exige revisión",()=>{
 const q=quoteMusic({sku:"song_personal",now:"2026-11-19",costPen:10});
 assert.equal(q.decision,"HUMAN_REVIEW");
});
test("cotizacion autorizada calcula impuesto",()=>{
 const q=quoteMusic({sku:"jingle_business",now:"2026-11-19",costPen:20,taxRate:0.18,policy:{approved:true}});
 assert.equal(q.totalPen,236);assert.equal(q.decision,"QUOTE_ALLOWED");
});
const base={orderId:"JF_1001",customerRef:"CRM_01",sku:"song_personal",acceptance:true,payment:"VERIFIED",requirements:{complete:true,rightsVerified:true},approvedSongRef:"https://suno.com/s/ejemplo",deliveredDownloads:18,monthlyLimit:20,requestedDownloads:1};
test("pedido listo permanece sin despacho ni descarga automatica",()=>{
 const r=musicProductionHandoff(base);assert.equal(r.state,"READY_FOR_PRODUCTION");assert.equal(r.downloadReserved,false);assert.equal(r.dispatchEnabled,false);
});
test("sin pago verificado se bloquea",()=>{
 const r=musicProductionHandoff({...base,payment:"SCREENSHOT"});assert.ok(r.blockers.includes("PENDIENTE_VERIFICACION_PAGO"));
});
test("sin aprobacion version musical se bloquea",()=>{
 const r=musicProductionHandoff({...base,approvedSongRef:null});assert.ok(r.blockers.includes("CANCION_NO_APROBADA"));
});
test("sin licencia validada se bloquea",()=>{
 const r=musicProductionHandoff({...base,requirements:{complete:true,rightsVerified:false}});assert.ok(r.blockers.includes("DERECHOS_NO_VERIFICADOS"));
});
test("sin capacidad mensual se bloquea",()=>{
 const r=musicProductionHandoff({...base,deliveredDownloads:20});assert.ok(r.blockers.includes("CUPO_DESCARGAS_INSUFICIENTE"));
});
test("no permitir una orden sin identificador CRM",()=>assert.throws(()=>musicProductionHandoff({...base,customerRef:""})));
