# AM-Medic — Automatización de WhatsApp: control de activación
**Fecha de control:** 2026-11-19 (hora de Lima)  
**Propiedad:** JF SOLUCIONES · uso interno del equipo de implementación.  
**Importante:** esta documentación no acredita WhatsApp en producción y no contiene tokens ni conversaciones reales.

## Evidencias
- JF CONNECT — WhatsApp Central está activo en n8n. En el momento de la revisión las últimas ejecuciones visibles eran del 7 de noviembre de 2026.
- Meta Graph API pudo leer la ficha de la línea y una aplicación suscrita llamada AM-MEDIC Connect; esto no prueba que el webhook reciba un mensaje.
- El monitor comercial registra estado `conectando` y fecha de última actividad ausente.
- Workflow n8n **AM-MEDIC | QA asistente WhatsApp - SOLO SIMULACION** (`wVici5w7OqxMQ08Z`), ejecución **964**: **12 escenarios superados, 0 fallidos, 0 mensajes enviados**. El flujo quedó INACTIVO para producción.
- No se modificó el flujo de otros clientes ni se emitieron campañas de WhatsApp.

## Activación segura, en orden
1. Obtener consentimiento verificable del titular del WhatsApp Business y autorización de automatización y tratamiento comercial de datos.
2. Confirmar el método de vinculación: Cloud API, Business App o coexistencia; preservar funcionamiento y acceso del titular.
3. **Auditar el POST del webhook de producción y validar firma X-Hub-Signature-256 (HMAC) antes de aceptar payloads como auténticos**. Revisar idempotencia, fuente de evento, manejo de errores, reintentos y separación por cliente. En la inspección de nodos del flujo central no se encontró un paso explícito de validación HMAC; esto requiere revisión de infraestructura antes de afirmar protección.
4. Desde un teléfono de prueba autorizado, mandar mensaje real al WhatsApp comercial; observar evento de Meta, ejecución n8n, identificación del número del cliente, creación de conversación y recepción humana. No registrar contenido sensible.
5. Probar categorías licencia nueva, revalidación, recategorización, ubicación, horarios, citas, precios y derivación humana; jamás indicar precios no aprobados ni prometer citas sin cupos.
6. Comprobar bajas/no-contacto, horarios de atención, límites y plantillas aprobadas por Meta. Respuestas únicamente según las reglas vigentes y la conversación iniciada por el usuario; revisar la ventana de atención.
7. Cuando los controles estén aprobados, habilitar primero un mensaje de bienvenida informativo con opción de asesor y supervisar la primera semana. Mensajes masivos y campañas proactivas quedan fuera del alcance inicial.

## Indicadores para Gestión 360
- Mensajes entrantes recibidos por Meta (verificados).
- Eventos válidos entregados al webhook.
- Conversaciones únicas en JF Connect.
- Tiempo de primera respuesta.
- Casos en espera de asesor.
- Citas confirmadas y atenciones reportadas.
- Alertas del canal y última actividad comprobada.

Separar eventos de conversación, llamadas de WhatsApp (si la Calling API corresponde) y llamadas convencionales. Sin prueba de fuente, mostrar **SIN DATOS VERIFICADOS**, nunca cero. No subir nombres, DNI, números de pacientes, historias clínicas ni secretos a este repositorio público.

## Guion base candidato (no habilitado)
> ¡Hola! Gracias por comunicarte con Policlínico AM-Medic. Estamos en Av. Perú 2714, segundo piso, San Martín de Porres. ¿Tu consulta es por licencia nueva, revalidación, recategorización o una cita? Te ayudaremos a comunicarte con recepción para confirmar los requisitos y la disponibilidad.

No publicar el guion como respuesta automatizada sin validación de recepción, aprobación del titular y pruebas técnicas.


## Auditoría adicional: Webhook 19/11/2026, 22:18 (Lima)
- Capturas de Meta Developers muestran callback `https://n8n.jfconnect.online/webhook/meta-whatsapp` y campo `messages` **suscrito** en v26.0. No alterar esta configuración sin diagnóstico adicional.
- La aplicación **AM-MEDIC Connect** del panel coincide con la aplicación registrada en la suscripción de la WABA consultada por Graph API.
- GET de pertenencia de teléfonos WABA en n8n, ejecución **1013**: el identificador técnico del teléfono de AM-Medic corresponde a esa WABA. Esto no confirma su entrega al webhook.
- Ejecuciones nuevas **998–1004** del webhook central, observadas el 19/11 aproximadamente a las 21:55–21:56 Perú: **todas corresponden al número del periódico NO+, ninguna a AM-Medic**. Se verificó por metadato de número receptor, sin registrar datos de remitentes ni contenido.
- El usuario confirmó que su mensaje de prueba a AM-Medic mostró **dos checks grises**. Esto acredita entrega en WhatsApp, no entrega de webhook a JF CONNECT.
- Estado operativo: **AM-MEDIC SIN EVENTO ENTRANTE VERIFICADO**. Próximas comprobaciones: modo Live/Development de la aplicación, registro y modalidad Cloud API / Business App / coexistencia y logs de entrega de Meta, incluyendo overrides por teléfono.
- El flujo de otros clientes no se alteró. El webhook central no presenta una validación HMAC explícita en el grafo inspeccionado; **antes de activar respuestas automáticas** se requiere control de autenticidad y pruebas de extremo a extremo supervisadas.
