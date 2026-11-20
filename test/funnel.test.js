import test from 'node:test';
import assert from 'node:assert/strict';
import {calcularEmbudo} from '../src/analytics/funnel.js';

test('sin datos no simula métricas cero', () => {
 const m=calcularEmbudo({});
 assert.equal(m.ctr_pct,null);
 assert.equal(m.cpc_pen,null);
 assert.equal(m.coste_por_cita_pen,null);
 assert.equal(m.advertencias.length,3);
});

test('calcula el embudo sin inventar denominadores', () => {
 const m=calcularEmbudo({
   gasto_pen:120,impresiones:10000,clics_enlace:250,
   conversaciones_meta:50,conversaciones_webhook:45,
   leads_calificados:30,citas_confirmadas:15,citas_atendidas:12
 });
 assert.equal(m.ctr_pct,2.5);
 assert.equal(m.cpc_pen,0.48);
 assert.equal(m.coste_por_conversacion_meta_pen,2.4);
 assert.equal(m.tasa_webhook_vs_conversacion_pct,90);
 assert.equal(m.tasa_cita_sobre_lead_pct,50);
 assert.equal(m.coste_por_cita_pen,8);
 assert.equal(m.tasa_asistencia_pct,80);
});

test('cero confirmado como denominador no es dato calculable', () => {
 const m=calcularEmbudo({gasto_pen:0,impresiones:0,clics_enlace:0,citas_confirmadas:0});
 assert.equal(m.ctr_pct,null);
 assert.equal(m.cpc_pen,null);
});

test('rechaza negativos y tipos inválidos', () => {
 assert.throws(()=>calcularEmbudo({gasto_pen:-3}),TypeError);
 assert.throws(()=>calcularEmbudo({impresiones:'200'}),TypeError);
});
