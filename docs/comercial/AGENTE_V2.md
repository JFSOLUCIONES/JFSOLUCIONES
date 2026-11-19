# JF SOLUCIONES · Agente Comercial IA V2 (laboratorio)

**Estado:** prototipo en rama de desarrollo. No conecta aún el número WhatsApp de JF SOLUCIONES a Meta; no genera envíos, cobros, publicaciones ni mensajes al propietario.

## Objetivo
Atender con cordialidad, diagnosticar la necesidad, recomendar el servicio adecuado, generar propuestas **borrador**, conservar el contexto autorizado, facilitar derivación humana y medir conversión real.

## Infraestructura encontrada el 19/11/2026
- [JF CONNECT WhatsApp Central](https://n8n.jfconnect.online/workflow/iEvozsVNjK5g2Dgg), activo, multicliente: NO modificar sin revisión de verificación de firma HMAC, tokens y aislamiento por cliente.
- [JF COMERCIAL simulador](https://n8n.jfconnect.online/workflow/qId8vwjr2r6sN5T8), manual, seis escenarios probados, sin envíos.
- n8n data tables: `JF_COMERCIAL_CRM_V1` y `JF_COMERCIAL_CATALOGO_SERVICIOS_V1`.
- [JF Academy](https://jfconnect.online/academia.html): guías gratuitas, cursos de pago todavía no publicados.

## Diseño de la conversación
1. Identificación transparente: "Soy el asistente virtual de JF SOLUCIONES"; bienvenida empática sin suplantar humanos.
2. Diagnóstico conversacional progresivo: negocio, etapa, problema, objetivo, plazo y alcance. Presupuesto solo si el interesado acepta compartirlo.
3. Valorización de oportunidad por necesidades expresadas y encaje, **no por patrimonio presunto, tipo de RUC ni datos privados**.
4. Ofrecer una sola solución prioritaria y un complemento pertinente: diseño → página de aterrizaje → captación → automatización, solo si tiene sentido.
5. Cotización **preliminar** basada en tarifario interno aprobado, alcance y horas; aprobación humana necesaria antes de oferta vinculante/contrato/pago.
6. Si envía logo con permiso, preparar un brief de marca y una muestra en entorno de diseño controlado; no enviar artefactos generados sin validación de calidad ni atribuirle al cliente propiedad que no tiene.
7. Si tiene interés y consiente el seguimiento, registrar siguiente acción; si no quiere, terminar sin presionar.
8. Alerta al responsable mediante credencial de canal privada configurable `JF_OWNER_ALERT_PHONE`, después de aprobar qué datos se comparten y validar canal de envío. No incluir el número privado ni datos de personas en este repositorio público.

## Integración de orígenes
Preferir enlace voluntario con código de campaña o formulario con fuente UTM y aviso de privacidad; el cliente inicia chat. **No decir "sé que visitaste tal página"** a partir de cookies, pixel o inferencias. No reutilizar datos de otros clientes o proyectos.

## Consulta SUNAT
Pedir número de RUC solo cuando ayude a identificar una organización que el cliente declara representar; explicar propósito y solicitar autorización para consultar datos de empresa en [SUNAT](https://www.gob.pe/institucion/sunat/pages/565-consultar-el-estado-del-ruc). Prefijos 10/20 NO verifican identidad ni solvencia. No se hará búsqueda inversa de teléfonos, scraping de perfiles personales, historial crediticio ni inferencias de ingreso diario. No usar RUC para discriminar precios: dimensionar costo por alcance, esfuerzo y nivel de soporte.

## Condiciones de WhatsApp
Enviar mediante **Cloud API oficial** solamente tras número y WABA verificados, firma de webhook, idempotencia, consentimiento, ventanas de atención, plantillas permitidas, opt-out, rate limits y pruebas. Meta permite respuestas libres en ventana de atención de 24 h; fuera de ella usa plantillas aprobadas según condiciones aplicables. [Política oficial](https://whatsappbusiness.com/policy/). Auditoría de datos personales: [Reglamento peruano DS 016-2024-JUS](https://www.gob.pe/institucion/anpd/campa%C3%B1as/128319-nuevo-reglamento-de-proteccion-de-datos-personales).

## Open source seleccionado (no instalado ni copiado)
| Proyecto | GitHub | Uso | Nota |
| --- | --- | --- | --- |
| Chatwoot | https://github.com/chatwoot/chatwoot | Bandeja compartida, derivación a humanos y SLA | Núcleo MIT; revisar enterprise/ y recursos VPS antes de instalar |
| Langfuse | https://github.com/langfuse/langfuse | QA de conversaciones, trazas, análisis de fallos y prompts | Núcleo MIT; revisar carpetas EE, autohospedaje y anonimización |
| LangChain JS | https://github.com/langchain-ai/langchainjs | Herramientas de razonamiento/orquestación cuando n8n resulte insuficiente | MIT |
| Qdrant | https://github.com/qdrant/qdrant | Búsqueda semántica de servicios y documentación autorizada | Apache-2.0; no necesaria en la primera fase |

No copiar plataformas enteras a un repo público. Evaluar seguridad, CVE, dependencias, licencias y costo operativo; alojar aisladas antes de usarlas.

## Pruebas y puerta a producción
`node --test test/sales_agent.test.js` (Node >=20, sin paquetes). Separación de tenants, replay, falsos webhooks, duplicados, stop, falta de RUC, precios sin aprobar, ausencia de logo, carga, horarios, pérdida de Meta, permisos de adjuntos y alerta a propietario. Requiere revisión independiente y pruebas end-to-end antes de habilitar mensajes.
