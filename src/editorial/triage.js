/**
 * NO+ — clasificador de preingreso editorial.
 * Prototipo sin dependencias, sin APIs, sin secretos, sin publicación.
 * No determina veracidad ni culpabilidad.
 */
export const CATEGORY = Object.freeze({
  DENUNCIA: 'denuncia',
  NOTICIA: 'noticia',
  PUBLICIDAD: 'publicidad',
  CONSULTA: 'consulta',
  REVISION: 'revision_manual',
});

const patterns = [
  [CATEGORY.DENUNCIA, /\b(denuncia|corrupci[oó]n|soborno|nepotismo|malversaci[oó]n|irregularidad|presunto|presunta|abuso)\b/iu],
  [CATEGORY.PUBLICIDAD, /\b(publicidad|anuncio|tarifa|auspicio|promocionar|spot|paquete publicitario)\b/iu],
  [CATEGORY.NOTICIA, /\b(noticia|informaci[oó]n|accidente|incendio|municipalidad|hospital|obra|suceso|reportaje)\b/iu],
  [CATEGORY.CONSULTA, /\b(hola|buenas|gracias|horario|consulta|contacto|ayuda)\b/iu],
];

function cleanText(value) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, 10000);
}

/**
 * @param {{message?: string, channel?: string, sourceId?: string}} input
 * @returns {object} expediente preliminar; no constituye verificación periodística
 */
export function triage(input = {}) {
  const message = cleanText(input.message);
  const hits = patterns.filter(([, regex]) => regex.test(message));
  const category = hits.length === 1 ? hits[0][0] : CATEGORY.REVISION;
  const priority = /\b(urgente|peligro|amenaza|riesgo inmediato)\b/iu.test(message)
    ? 'alta_sujeta_a_revision'
    : 'normal';

  return {
    channel: input.channel === 'whatsapp' ? 'whatsapp' : 'manual',
    category,
    priority,
    status: 'pendiente_revision_humana',
    verified: false,
    publicationApproved: false,
    autoPublish: false,
    evidenceRequired: true,
    ambiguous: hits.length > 1,
    message,
    sourceId: typeof input.sourceId === 'string' ? input.sourceId.slice(0, 128) : null,
    note: 'Clasificación preliminar. Verificar datos, fuentes y derecho de respuesta antes de publicar.',
  };
}
