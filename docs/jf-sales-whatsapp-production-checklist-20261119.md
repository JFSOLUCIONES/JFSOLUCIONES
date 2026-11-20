# JF SALES — Checklist de activación de WhatsApp (2026-11-19)
Estado: NO APTO PARA ACTIVAR ENVÍO AUTÓNOMO.

## Evidencia comprobada
- Central n8n activa: workflow iEvozsVNjK5g2Dgg; su POST meta-whatsapp recibe eventos de varios clientes.
- Workflow guarda un token de verificación GET en un condicional; ROTAR ese token y usar un secret manager, sin publicarlo en logs/repositorios.
- En POST no se observó validación HMAC de X-Hub-Signature-256 previa a clasificación. Recalcular HMAC SHA-256 sobre bytes exactos del raw body con Meta App Secret y comparación constante.
- Laboratorio bWORRkXGEGxZzZvZ usa un webhook raw separado y ruta HMAC; revisar credencial/secret y comprobar su funcionamiento real antes de copiar el patrón.
- Últimas ejecuciones visibles de la central: 2026-11-07; no demuestran recepción actual.
- Identificador del teléfono comercial de JF todavía no vinculado a una entrada empresarial verificada de Meta. No inferirlo desde el número personal del propietario ni utilizar números de NO+ o AM-MEDIC.
- Recursos aislados n8n: JF_SALES_ORDERS_V2, JF_SALES_MUSIC_CAPACITY_V2, JF_SALES_PRICE_APPROVALS_V2; laboratorio 486VJnO1IPruGL2v, ejecución 940 exitosa sin envíos.

## Procedimiento
1. Verificar en Meta WhatsApp Manager la WABA y phone_number_id de JF; comprobar relación con panel interno sin copiar tokens.
2. Lista permitida exclusiva para phone_number_id confirmado de JF SALES; preservar el enrutamiento NO+ y AM-MEDIC.
3. Verificar HMAC con bytes originales al ingreso, antes de clasificar, almacenar o contestar. Rechazar sin firma o inválida; no filtrar secretos a logs.
4. Rotar el token GET expuesto coordinando Meta y backend y validar challenge sin interrumpir mensajes.
5. Probar sintéticos firmados, alterados, sin firma, duplicados y otros clientes. Ningún mensaje no autorizado debe llegar a IA, CRM o envío.
6. Probar un evento real autorizado de línea JF, recepción, respuesta, CRM, aislamiento, latencia, ventana 24 horas.
7. Aprobar tarifas, impuestos, costos, medios de pago, licencias musicales y cupos de descargas. Promoción febrero 2027 sigue borrador.
8. Conectar subflujo ventas con aislamiento tenant; impedir cobros/entregas sin autorizaciones. Alertar al 901 170 429 únicamente mediante canal privado autorizado.
9. Activar progresivamente solo para JF, con monitorización y rollback preparado.

## Criterios de aceptación
- Ningún mensaje con HMAC inválido llega al flujo de atención.
- No se cruzan mensajes de JF con NO+/AM-MEDIC.
- Repetidos no producen respuestas ni ventas duplicadas.
- Cotizaciones no autorizadas, capturas de pago, licencias no verificadas y falta de cupo se bloquean.
- Se registra auditoría sin divulgar datos personales ni credenciales.
