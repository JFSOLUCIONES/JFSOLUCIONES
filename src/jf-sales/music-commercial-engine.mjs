/**
 * JF SALES V2 — módulo piloto de cotización y orden musical.
 * No tiene red, credenciales, cobros, ni envíos. No autoriza precios al cliente.
 * Para producción: persistir pedidos, reservas y claves idempotentes en una BD transaccional.
 */
export const MUSIC_CATALOG = Object.freeze({
  song_personal: {label:"Canción personalizada para uso personal", basePen:80, discountable:true},
  jingle_business: {label:"Jingle para negocio con usos comerciales verificados", basePen:200, discountable:true},
});
export const MUSIC_CAMPAIGNS = Object.freeze({
  love_2027: {
    label:"Mes del Amor 2027", starts:"2027-02-01", ends:"2027-02-28",
    discountPercent:50, status:"DRAFT", // no activar sin aprobación administrativa
  },
});

const money = n => Math.round((n + Number.EPSILON) * 100) / 100;
const validDate = s => /^\d{4}-\d{2}-\d{2}$/.test(s) && !Number.isNaN(Date.parse(s+"T00:00:00Z"));
export function quoteMusic({sku, now, campaignId=null, policy={}, costPen, taxRate=0, downloadUnits=1}) {
  const item = MUSIC_CATALOG[sku];
  if (!item) throw new Error("SKU desconocido");
  if (!validDate(now)) throw new Error("Fecha YYYY-MM-DD requerida");
  if (!Number.isFinite(costPen) || costPen<0) throw new Error("Costo de producción inválido");
  if (!Number.isFinite(taxRate) || taxRate<0 || taxRate>1) throw new Error("Tasa de impuestos inválida");
  if (!Number.isInteger(downloadUnits) || downloadUnits<1) throw new Error("Descargas requeridas inválidas");
  const {approved=false, marginMin=0.35, maxRevisions=2} = policy;
  if (!(marginMin>=0 && marginMin<1)) throw new Error("Margen mínimo inválido");
  if (!Number.isInteger(maxRevisions) || maxRevisions<0) throw new Error("Revisiones inválidas");
  const campaign = campaignId ? MUSIC_CAMPAIGNS[campaignId] : null;
  if (campaignId && !campaign) throw new Error("Campaña desconocida");
  const isInPeriod = campaign && now>=campaign.starts && now<=campaign.ends;
  const campaignAllowed = Boolean(campaign && campaign.status==="ACTIVE" && approved && item.discountable && isInPeriod);
  const netBase = item.basePen;
  const netOffered = money(netBase * (campaignAllowed ? (1-campaign.discountPercent/100) : 1));
  const netFloor = money(costPen/(1-marginMin));
  const viable = netOffered >= netFloor;
  return {
    sku, label:item.label, campaignId, campaignApplied:campaignAllowed,
    basePen:netBase, netPen:netOffered, taxPen:money(netOffered*taxRate),
    totalPen:money(netOffered*(1+taxRate)), costPen:money(costPen),
    floorPen:netFloor, viable, maxRevisions, downloadUnits,
    decision: !approved ? "HUMAN_REVIEW" : viable ? "QUOTE_ALLOWED" : "REPRICE_OR_HUMAN_REVIEW",
    message: !approved ? "Tarifario pendiente de autorización" : viable ? "Cotización viable" : "Precio inferior al margen mínimo",
  };
}

/** Solo genera un paquete interno, no manda WhatsApp ni descarga canciones. */
export function musicProductionHandoff({orderId, customerRef, sku, acceptance, payment, requirements, approvedSongRef, deliveredDownloads=0, monthlyLimit=20, requestedDownloads=1}) {
  if (!/^[A-Za-z0-9_-]{4,64}$/.test(orderId||"")) throw new Error("Orden inválida");
  if (!customerRef || typeof customerRef!=="string") throw new Error("Referencia CRM requerida");
  if (!MUSIC_CATALOG[sku]) throw new Error("SKU desconocido");
  if (!Number.isInteger(deliveredDownloads) || deliveredDownloads<0 || !Number.isInteger(monthlyLimit) || monthlyLimit<1) throw new Error("Capacidad inválida");
  if (!Number.isInteger(requestedDownloads) || requestedDownloads<1) throw new Error("Descargas inválidas");
  const blockers=[];
  if (acceptance!==true) blockers.push("PENDIENTE_ACEPTACION");
  if (payment!=="VERIFIED") blockers.push("PENDIENTE_VERIFICACION_PAGO");
  if (!requirements?.complete) blockers.push("BRIEF_INCOMPLETO");
  if (!approvedSongRef || !/^https:\/\//.test(approvedSongRef)) blockers.push("CANCION_NO_APROBADA");
  if (!requirements?.rightsVerified) blockers.push("DERECHOS_NO_VERIFICADOS");
  if (deliveredDownloads+requestedDownloads>monthlyLimit) blockers.push("CUPO_DESCARGAS_INSUFICIENTE");
  return {
    orderId, customerRef, sku, state:blockers.length ? "BLOCKED" : "READY_FOR_PRODUCTION",
    blockers,
    downloadReserved:false, // solo una BD con reserva atómica puede confirmar un cupo
    dispatchEnabled:false, // enviar al 901 170 429 solo cuando el canal privado esté validado
    destination:"OWNER_INTERNAL_QUEUE",
    approvedSongRef: approvedSongRef || null,
    instruction:blockers.length ? "Resolver bloqueos antes de descargar o enviar" : "Aprobar reserva transaccional y generar orden interna",
  };
}
