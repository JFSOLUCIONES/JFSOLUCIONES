# Arquitectura objetivo NO+ — etapas, no despliegue existente

## Principio de aislamiento

- **JF CONNECT WhatsApp Central** es compartido por clientes. No sustituir, duplicar webhooks ni cambiar credenciales ajenas.
- **NO+ Editorial** debe tener su propia lógica, registros, permisos y aprobaciones.
- **Panel JF CONNECT** seguirá como control operativo; el estado del bot debe resultar de una prueba de salud real, no solo de un selector manual.
- **Periodiconomas.space** ofrece la experiencia pública; el CMS editorial puede instalarse en un subdominio y servicio/container distintos.
- Colas y archivos de denunciantes en almacenamiento privado con controles de acceso; nunca en repositorios públicos.

## Flujo editorial recomendado

WhatsApp / formulario web / correo de redacción / radar RSS
→ normalización y deduplicación
→ clasificación con reglas; IA opcional para casos ambiguos
→ expediente con fuentes y adjuntos
→ investigación documental y contraste de fuentes
→ evaluación de riesgos y revisión legal cuando corresponda
→ edición por periodista
→ aprobación humana de publicación
→ CMS (Payload, por evaluar)
→ portal y plataformas de difusión.

Estados del expediente: recibido → clasificación → investigación → contrastación → redacción → revisión → aprobado / descartado / rectificación.

## Servicios y orden

**Fase A (actual):** acuse Meta/n8n probado, prototipo de clasificación y registro del bot en panel. Queda pendiente integrar IA al bot; `ai_client_id` no estaba asociado en auditoría.

**Fase B:** servicio NO+ editorial dedicado y API autenticada de ingreso de mensajes; idempotencia por message_id; protección de PII; auditoría y encriptación de evidencias.

**Fase C:** CMS Payload con colecciones News, Sources, EditorialCases, Corrections, Users y ApprovalEvents; publicaciones públicas solo después de aprobación.

**Fase D:** radar RSS verificable y herramientas OSINT; separación explícita entre hallazgo, hipótesis y hecho corroborado.

**Fase E:** Revive Adserver para campañas, AzuraCast para radio con stream y derechos de emisión; ambos aislados y tras medición de capacidad.

## Seguridad técnica mínima

- Webhook firmado (validación HMAC SHA-256) y deduplicación de eventos.
- Secretos en gestor de credenciales; jamás variables expuestas a frontend o GitHub.
- Roles `reportero`, `verificador`, `editor`, `director`.
- Publicación requiere aprobación explícita registrada; los agentes IA solo generan borradores.
- Backups cifrados; restauraciones probadas; observabilidad y alertas de fallas.
- Plan de retención limitado para datos personales y tratamiento de denuncias.
- Revisar DNS/HTTPS/Caddy, uso de RAM, CPU, almacenamiento y ancho de banda ANTES de nuevas instalaciones.

## No asumir

Este documento NO instala Payload, AzuraCast, Revive, Aleph, OpenSanctions ni cambia la infraestructura productiva.
