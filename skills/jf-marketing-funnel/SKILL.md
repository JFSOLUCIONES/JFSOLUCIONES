---
name: jf-marketing-funnel
description: Guía de auditoría del embudo comercial en Meta Ads, WhatsApp, GA4 y JF CONNECT; sin acceso a secretos ni datos clínicos.
---

# JF SOLUCIONES — Auditoría objetiva de campañas y captación
**Versión inicial:** 2026-11-19. **Naturaleza:** skill documental de referencia; no está instalada automáticamente en ChatGPT.

## Disparadores
Usar cuando un cliente reporte «no llegaron clientes», «no recibo WhatsApp», «anuncios sin resultados», o se quiera instrumentar GA4/Meta Ads en su negocio.

## Flujo seguro
1. **Identificar cliente, canal y periodo.** Obtener permiso específico del titular y comprobar qué red social, cuenta publicitaria, WABA, teléfono, web y JF CONNECT corresponden al cliente. Nunca asumir que una propiedad GA4 de la agencia mide a su cliente.
2. **Separar cuatro evidencias:** (a) anuncios entregados/alcance/gasto; (b) intención por clic; (c) evento real de conversación/llamada; (d) cita/atención registrada. No equiparar ninguno de estos números.
3. **Leer Meta Ads Insights** con OAuth/permisos ads_read, filtrando account/campaign/ad del cliente; recopilar reach, impressions, spend, clicks, conversations_started si el resultado lo soporta. No usar claves de otros clientes.
4. **Comprobar WhatsApp sin envíos:** GET de datos de número/WABA y subscribed_apps, validar que Meta tenga la app y callback esperados; revisar webhook real con HMAC. Un estado de panel 'activo' o 'conectando' no confirma recepción.
5. **Probar de extremo a extremo** con mensaje originado desde un número de prueba autorizado por el titular. Registrar solo ID no sensible, hora, estado de llegada a n8n, creación de conversación, asignación a asesor y respuesta. No leer chats históricos salvo necesidad comercial específica, permiso y base jurídica.
6. **GA4**: solo cuando existe web/landing. Registrar `click_whatsapp` en CTA y `generate_lead` cuando el usuario efectivamente solicite información. No enviar teléfonos, nombres, condiciones médicas ni textos privados.
7. **Construir embudo por fecha/campaña:** impresiones -> clics -> conversaciones -> leads -> citas -> asistencia. Identificar el salto con mayor pérdida, indicar la incertidumbre y recomendar un experimento con una sola variable cambiada.
8. **Seguridad y auditoría:** secretos en gestor, permisos por cliente, consentimiento, conservación mínima, revisión humana de cualquier mensaje saliente, logs sin PII y trazabilidad de origen/fecha.

## Indicadores
- `CTR = clics_enlace / impresiones` cuando impresiones > 0.
- `CPC = gasto / clics_enlace` cuando clics > 0.
- `tasa_contacto = conversaciones_recibidas / clics_whatsapp` cuando ambos eventos estén correctamente identificados.
- `tasa_cita = citas_agendadas / leads_calificados` cuando leads > 0.
- `costo_por_cita = gasto / citas_agendadas` cuando citas > 0.
- Nunca sustituir 'sin dato' por cero. Documentar desfases de atribución, días, canales y permisos.

## Regla de decisión
- Poco alcance: revisar entrega, segmentación, presupuesto, configuración y rechazo.
- Alcance pero pocos clics: revisar creatividad, mensaje y llamado a acción.
- Clics pero pocas conversaciones: revisar enlace, destino, Meta/WhatsApp, webhook y experiencia móvil.
- Conversaciones pero pocas citas: revisar tiempo de respuesta, guion, disponibilidad y ubicación.
- Citas pero poca asistencia: confirmación, recordatorio permitido y barreras de acceso.

## Habilidades y herramientas sugeridas
- JF CONNECT n8n: orquestación, tablas de origen y comprobación diaria.
- Meta Graph APIs: estado de WABA y métricas Ads con permisos autorizados.
- GA4: medición web; Google Business Profile: interacciones locales cuando el titular comparte acceso.
- Chatwoot, DataEase, MaxKB y Uptime Kuma como pilotos sujetos a licencia y evaluación de seguridad.
- Referencia de investigación: `docs/jf-activos/CATALOGO_OPEN_SOURCE_ANALITICA_2026-11-19.md`.

**Prohibido:** campañas automáticas no consentidas, datos clínicos en reportes publicitarios, mezclar clientes, usar contraseñas copiadas en documentos, o afirmar que se ha registrado tráfico sin evidencia.
