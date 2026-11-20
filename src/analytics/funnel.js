/**
 * JF SOLUCIONES — cálculo de indicadores comerciales sin datos personales.
 * No obtiene datos de cuentas ni envía mensajes. Los campos ausentes siguen siendo null.
 */
const metrics = ['gasto_pen','impresiones','clics_enlace','conversaciones_meta','conversaciones_webhook','leads_calificados','citas_confirmadas','citas_atendidas'];

function asMetric(value, name) {
  if (value === undefined || value === null || value === '') return null;
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0)
    throw new TypeError(`Métrica inválida en ${name}: se espera número finito no negativo o null`);
  return value;
}
function divide(a, b) {
  if (a === null || b === null || b === 0) return null;
  return Number((a / b).toFixed(4));
}
function pct(a, b) {
  const ratio=divide(a,b);
  return ratio === null ? null : Number((ratio*100).toFixed(2));
}

/** Devuelve null si no hay datos suficientes; cero queda reservado para medición verificada. */
export function calcularEmbudo(registro) {
  if (!registro || typeof registro !== 'object' || Array.isArray(registro)) throw new TypeError('Se espera registro');
  const m=Object.fromEntries(metrics.map(k=>[k,asMetric(registro[k],k)]));
  return {
    ctr_pct: pct(m.clics_enlace,m.impresiones),
    cpc_pen: divide(m.gasto_pen,m.clics_enlace),
    coste_por_conversacion_meta_pen: divide(m.gasto_pen,m.conversaciones_meta),
    tasa_webhook_vs_conversacion_pct: pct(m.conversaciones_webhook,m.conversaciones_meta),
    tasa_cita_sobre_lead_pct: pct(m.citas_confirmadas,m.leads_calificados),
    coste_por_cita_pen: divide(m.gasto_pen,m.citas_confirmadas),
    tasa_asistencia_pct: pct(m.citas_atendidas,m.citas_confirmadas),
    advertencias: [
      ...(m.conversaciones_meta===null? ['No hay conversaciones Meta verificadas; no inferir cero.'] : []),
      ...(m.conversaciones_webhook===null? ['No hay eventos webhook verificados; no inferir cero.'] : []),
      ...(m.citas_confirmadas===null? ['No hay agenda confirmada; no inferir cero.'] : [])
    ]
  };
}
