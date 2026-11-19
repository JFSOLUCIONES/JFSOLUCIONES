# Puerta de producción · JF SALES V2

No confundir "workflow activo" con "número WhatsApp corporativo habilitado". Antes de lanzar:

- [ ] Número oficial de JF SOLUCIONES y WABA verificadas para el negocio correcto (sin reutilizar credencial de otros clientes).
- [ ] Webhook GET verify token desde secreto rotado; POST con firma HMAC SHA256 sobre cuerpo original, comparación constante, protección contra replay, idempotencia por message_id.
- [ ] Controles de 24 horas, plantillas fuera de ventana, consentimiento y supresión de contactos que rechazaron mensajes; límites de frecuencia y monitoreo.
- [ ] Política de privacidad para web/WhatsApp según Ley 29733/DS 016-2024-JUS; RUC opcional con permiso, sin búsquedas inversas del móvil ni perfilamiento financiero.
- [ ] Modelo tiene acceso solo al catálogo vigente, guía de producto y contexto mínimo del lead; no a clientes cruzados; evaluación de prompt injection.
- [ ] Tarifario interno, matriz de descuentos y cotizaciones borrador aprobados por propietario; contratos/pagos firmados por humano.
- [ ] Alerta privada a responsable: verificar canal de envío, configurarlo como secreto, minimizar datos y ensayar alerta con destinatario y caso ficticio; no enviar chats completos ni datos personales a dispositivos no autorizados.
- [ ] Logo: permiso específico de uso, procesamiento de imagen en herramienta autorizada, revisión de diseño y entrega con mensaje validado.
- [ ] Backup de workflow, entorno de ensayo y rollback. No modificar central WhatsApp multicliente hasta superar pruebas.
- [ ] Pruebas E2E de Meta con 2 números de ensayo, escenarios de error, duplicidad, silencio, opt-out, adjuntos peligrosos y caída de proveedor.
- [ ] Dashboard comercial GA4/CRM con eventos: inicio consulta, diagnóstico completo, cotización aprobada, pago confirmado y trabajo iniciado (no inventar conversiones).

## Flujos existentes
- Central: `iEvozsVNjK5g2Dgg` (activo; auditoría halló riesgo de firma de webhook no evidente y token incrustado; revisar y rotar).
- Motor funcional QA: `YEqUYo7N3a6chnYm`; ejecución N° 902, 11/11 simulaciones sin envíos.
- IA de atención QA: `bw0laHVYcRkWPKy0`; ejecución N° 905, respuesta de prueba completada; no recibe mensajes reales.
- Simulador/CRM: `qId8vwjr2r6sN5T8`.

## Arquitectura de referencia
Meta Cloud API -> HMAC + idempotencia + control ventana -> contexto mínimo/CRM consentido -> LLM (prompt versionado) -> validador de tarifa y reglas -> respuesta borrador -> (Meta reply condicionado) o (aprobación humana) -> CRM -> métricas. Notificación propietaria por canal privado aprobado. Diseño de muestras en rama aparte con permiso y revisión.
