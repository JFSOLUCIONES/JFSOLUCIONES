# JF SOLUCIONES — Catálogo de herramientas abiertas para analítica y operación
**Corte de evaluación:** 19-11-2026 · **Estado:** investigación documentada, NO instalación ni autorización para usar datos de clientes.
**Propósito:** preservar referencias técnicas y criterios de evaluación para un centro maestro de sistemas. No contiene tokens, IDs de cuentas, datos personales, accesos ni configuración real.

## Prioridades de negocio
1. **Meta Ads / Instagram / Facebook Insights**: inversión, entrega, clics y conversaciones iniciadas; consultar mediante permisos y API oficial o conector autorizado. NO confundir clics con pacientes.
2. **JF CONNECT + n8n**: recepción realmente verificada de mensajes, tiempo de respuesta, prospectos válidos, citas y atenciones. Un bot registrado como activo NO demuestra conexión.
3. **GA4**: solo instrumentar páginas web o landing pages propiedad/autorizadas del cliente. El evento `click_whatsapp` mide intención, no conversación; `generate_lead` solo cuando exista una solicitud verificable.
4. **Gestión 360**: vista por cliente y por campaña con fuente/fecha, auditorías, obligaciones y acceso RBAC. Nulos y 'pendiente de conexión' son preferibles a fabricar ceros.

## Herramientas evaluadas
| Herramienta | Repositorio oficial | Función propuesta | Licencia verificada en repo (2026-11-19) | Adopción |
| --- | --- | --- | --- | --- |
| **Chatwoot** | https://github.com/chatwoot/chatwoot | Bandeja compartida con WhatsApp, IG, FB y asignación humana | Núcleo MIT/Expat; directorio enterprise tiene licencia propia | Piloto aislado cuando el canal Meta esté verificado. No duplicar JF CONNECT sin razón. |
| **DataEase** (ecosistema FIT2CLOUD, China) | https://github.com/dataease/dataease | BI y visualización de métricas | GPLv3 modificado: obliga preservar logo/copyright, consultar restricciones adicionales | Prioridad media para dashboard de prueba, no despliegue en VPS productivo. |
| **MaxKB** (1Panel, China) | https://github.com/1Panel-dev/MaxKB | Base documental e IA para FAQs y atención asistida | GPLv3 | Prioridad media-baja: no sustituye analítica ni autorización Meta. |
| **1Panel** (China) | https://github.com/1Panel-dev/1Panel | Panel de administración de servidores | GPLv3 | Estudiar solo con RBAC, sin exponer root en Gestión 360. |
| **Uptime Kuma** (proyecto de Louis Lam) | https://github.com/louislam/uptime-kuma | Disponibilidad de webs y webhooks | MIT | Complemento de infraestructura; nunca prueba conversión comercial. |
| **NocoBase** | https://github.com/nocobase/nocobase | Constructor de aplicaciones y fichas RBAC | Versión 3: acuerdo propio NocoBase con condiciones comerciales; NO asumir licencia OSI sin revisar | Solo revisión legal/licencia; no clonar ni incorporar código a producto vendible sin evaluación. |

## Diseño mínimo del embudo verificable
- Fuente de gasto y resultados: `date, client_key, ad_account_key, campaign_id, ad_id, spend, impressions, reach, clicks, conversations_started_meta`.
- Fuente de recepción: `timestamp, client_key, channel, message_event_id, source_campaign_if_available, conversation_status, first_response_s` (sin textos de chats ni teléfonos visibles en el tablero).
- Operación comercial: `lead_id_pseudonym, qualified, appointment_booked, appointment_attended, outcome`.
- Reconciliación por cuenta/campaña/fecha, con diferencias visibles: `click -> started conversation -> webhook delivered -> lead -> appointment -> attended`.
- Reportes: CTR, CPC, costo por conversación, tasa de respuesta, costo por cita, asistencia; solo publicar valores si hay denominador válido, consentimiento y datos confirmados.

## Reglas de seguridad y producto
- No clonar ni subir código de terceros al repositorio JFSOLUCIONES sin respetar la licencia; conservar URL, versión, copyright y atribuciones.
- No registrar secretos, datos clínicos, correos de pacientes, teléfonos o backups en GitHub público, GA4 o herramientas de seguimiento.
- Meta OAuth y permisos por cliente; titular conserva control y puede revocar. Separar directorios y datos de cada cliente.
- Cambios de ads, envíos, automatizaciones de WhatsApp y publicación requieren aprobación por cuenta y prueba en entorno aislado.
- Nuevos proyectos OSS: verificar licencia en versión exacta, actividad, CVEs, costos de VPS y soporte antes de instalarlos.

## Política de despliegue
Primero aprovechar JF CONNECT + n8n existentes. No instalar herramientas extras en producción sin ensayo de staging, backup restaurable, roles, seguridad de webhook y procedimiento rollback.

## Lecturas oficiales
- GA4 events: https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- WhatsApp Meta subscribed apps: https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account/subscribed_apps/
- Licencias upstream: consultar `LICENSE` y `LICENSE.txt` de cada repositorio y el texto de la versión desplegada.

Este documento contiene únicamente investigación pública reutilizable. No representa conexión, compra, instalación, autorización ni operación activa.
