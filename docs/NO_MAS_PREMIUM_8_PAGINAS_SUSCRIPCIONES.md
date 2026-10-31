# NO+ Premium — Modelo de negocio y flujo de lectores (31-10-2026)

## Producto
- Marca: Periódico NO MÁS — NO+ Premium.
- Precio propuesto: **S/ 10 por 30 días**, por confirmar en lanzamiento.
- Prestación: **edición de 8 páginas en PDF** entregada a lectores con acceso vigente por WhatsApp, junto con acceso web privado a sus ediciones.
- Complementos: alertas, boletines y solicitudes de información personalizada mediante capacidad editorial/IA, con límites claros de uso y revisión humana.
- **No confundir** con un servicio de investigación privada ilimitada: el equipo editorial prioriza, contrasta y aprueba los informes. El sistema no promete trabajos periodísticos exclusivos por cada consulta.

## Flujo de conversión
1. Facebook/Instagram/TikTok: fragmento periodístico original + titular + llamada a leer en `https://periodiconomas.space`.
2. Web: artículo público resumido, portada de edición premium, índice y convocatoria de suscripción. La publicidad debe estar claramente identificada.
3. Registro: teléfono, nombre de contacto, aceptación de términos y consentimiento separado para recibir comunicaciones por WhatsApp.
4. DNI: **no solicitar por chat como condición general**. Solo recopilar documento de identidad si existe una finalidad legítima y necesidad justificada (p. ej. facturación/validación reglamentaria), mediante formulario HTTPS de acceso restringido, minimización y retención definida.
5. Pago: proveedor de pagos autorizado; no admitir pagos por captura o mensaje como prueba suficiente. Confirmar transacción consultando API server-to-server después de notificación firmada.
6. Activar: `starts_at = paid_at`, `expires_at = paid_at + 30 days`; estados `pending`, `active`, `expired`, `cancelled`, `refunded`. No activar ante duplicados ni pagos pendientes.
7. Entrega: número verificado + opt-in + acceso activo. Fuera de ventana de atención de 24 horas, utilizar plantillas WhatsApp aprobadas y considerar costos de mensajería.
8. Al vencer: cortar acceso inmediatamente al PDF premium, detener envíos, ofrecer renovación sin cobros sorpresivos.
9. Retiro/rectificaciones: versiones, historial, fecha y correcciones visibles; documentos privados no públicos.

## Estructura editorial recomendada — edición PDF 8 páginas

| Página | Contenido |
|---|---|
| 1 | Portada: titular investigativo, fotografía auténtica, edición, fecha y marca NO+ |
| 2 | Investigación principal: contexto, hechos probados y preguntas públicas |
| 3 | Lambayeque y gobiernos locales |
| 4 | Noticias del Perú y fiscalización |
| 5 | Economía, salud y servicios |
| 6 | Mundo, tecnología y tendencias |
| 7 | Entrevistas, cultura y Radio NO MÁS (cuando esté operativa) |
| 8 | Opinión identificada, correcciones, guía de suscripción y anuncios claramente etiquetados |

- PDF legible en celular, edición con folio y enlace de validación; versión web accesible.
- Todas las fotos con licencias y créditos pertinentes. Diferenciar editoriales, reportajes, publicidad y opinión.
- No saturar: regla 70% visual/30% texto aplica a **flyers publicitarios**, no al periódico de 8 páginas que requiere densidad editorial legible.

## Modelo de datos mínimo

`readers(id, name, phone_e164, phone_verified_at, consent_whatsapp_at, status)`
`subscriptions(id, reader_id, amount_pen, starts_at, expires_at, payment_reference, status)`
`payments(id, provider, transaction_id UNIQUE, status, amount, verified_at)`
`editions(id, issue_date, issue_no, pdf_storage_key, sha256, editorial_status, approved_by, approved_at)`
`deliveries(id, edition_id, subscription_id, whatsapp_message_id, status, sent_at, error_code)`
`articles(id, section, headline, sources_private, editor_status, version)`

Nunca guardar contraseñas de pago, tokens o documentos identificatorios en GitHub. Cifrar campos necesarios, limitar acceso, registrar auditoría y diseñar eliminación de datos.

## Requisitos normativos y comerciales antes del lanzamiento

- Términos de suscripción, disponibilidad de ediciones, política de renovación y reembolso.
- Privacidad y cumplimiento del Reglamento de Protección de Datos Personales (DS 016-2024-JUS) y Ley 29733.
- Meta: plantilla aprobada para entrega proactiva y consentimiento del usuario.
- Proveedor de pagos: webhook verificado con consulta del estado definitivo del cobro.
- Derechos de autor: redacción original, fotos autorizadas y atribución cuando corresponda.
- Ingresos: S/ 10 es importe bruto antes de comisión de pagos, mensajería, impuestos, soporte, diseño y tecnología.

## Estado al 31-10-2026

- WhatsApp NO+ en producción con menú informativo y **prelanzamiento** de NO+ Premium.
- El pago, la identidad segura, acceso PDF y vencimiento automático no están implementados ni operativos.
- No cobrar ni prometer entrega automática hasta completar pruebas end-to-end.
- Publicaciones de redes: borradores de 9 piezas; aprobaciones y difusión manual pendientes.
