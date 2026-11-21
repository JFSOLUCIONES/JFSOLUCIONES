# JF DIRECTOR 360 — Control operacional seguro de ecosistema JF SOLUCIONES
**21/11/2026 · Diseño, sin ejecutar cambios de permisos en el VPS.**

## Hechos verificados de conexión

- Auditoría n8n VPS1, ejecución `1490`, SSH `code=0`, resultado `AUDIT_COMPLETE`; Docker activo, contenedor Gestión360 arriba, disco 50% utilizado, memoria ~4.3 GiB disponibles. Auditoría **no es** despliegue.
- Auditoría de capacidades de usuario de desarrollo SPORTS EDGE, ejecución n8n `1491`, `code=0`, `verified=true`, `USER=jf_sports_dev`; Docker CLI instalado pero socket restringido; `sudo -n -l` permite al menos alguna elevación no interactiva; carpetas productivas inspeccionadas sin escritura.
- Workflow existente de despliegue antiguo usa `sudo -n /usr/local/sbin/jf-edge-ops-v2 deploy-v048`. Esto demuestra un **patrón de comando aprobado**; no confiere permiso para despliegues arbitrarios v0.5.x.
- Los flujos no introducen secretos en ChatGPT; claves SSH permanecen en n8n.

## Requisito: dejar de solicitar contraseñas por cambios rutinarios

El problema es de **modelo de permisos**, no de capacidad de ChatGPT. Diseñar y aprovisionar un canal de despliegue acotado a cada servicio:

1. Una sola revisión inicial por administrador del VPS: crear o ampliar un wrapper propio `/usr/local/sbin/jf-approved-deploy`, propiedad de root, sin escritura para usuario SSH y con allowlist de subcomandos.
2. Usar usuario de despliegue sin login interactivo, autenticación mediante credencial SSH de n8n, y **sudoers único** para ejecutar solo ese wrapper; sin `NOPASSWD: ALL`, shell, Docker socket ni `bash -c` arbitrarios. No dejar que los nombres de archivo de usuario se conviertan en rutas arbitrarias o shell.
3. Cada operación recibirá release-id y SHA256/commit, previamente aprobados y almacenados en un manifiesto controlado por root. Descargar o recibir artefacto desde canal autorizado con verificación de integridad y procedencia. Nunca aceptar scripts cambiados en una rama mutable como autoridad de despliegue.
4. El wrapper permite `status`, `preflight`, `staging-test`, `deploy-approved <release-id>`, `rollback-approved <release-id>` y `logs-sanitized`. Desplegar solo stack Sports Edge permitido; no tocar contenedores ni datos de otros clientes.
5. Implementar workflow n8n con disparo manual para ChatGPT: validar operación, ejecutar SSH con credencial existente, sanitizar salida, almacenar execution-id y bitácora, leer resultado. Al despliegue, autorizar release específico antes de ejecutarlo; registrar quién solicitó y aprobó.
6. Pruebas de seguridad: usuario sin acceso general a Docker; no puede suministrar comandos arbitrarios; ruta fuera de allowlist bloqueada; SHA incorrecto bloqueado; rollback probado; sin duplicados si se reintenta.
7. Publicar solo después de backup verificado (incluida recuperación). Cambios en servicios ajenos requieren autorización propia.

## Fases propuestas

- **A. Ejecutada:** auditoría mediante n8n; no introducir contraseña para leer estado.
- **B. Pendiente:** preparar wrapper y configurarlo una sola vez con autorización root. Un administrador debe validar el alcance; no se ha realizado todavía.
- **C. Pendiente:** workflow n8n para acciones permitidas y pruebas de despliegue en staging.
- **D. Pendiente:** conexión operativa desde JF Director 360 AI a n8n con artefactos versionados, auditoría y aprobaciones.

## JF Director 360 AI

Plugin privado de ChatGPT `jf-director-360-ai` v0.1.0 con cuatro habilidades: dirección, operaciones VPS, radar de innovación y Sports Edge. Creación confirmada, pero la disponibilidad futura de los conectores depende de instalación y permisos del usuario. Un plugin de habilidades no puede por sí solo conectarse a root, autoentrenar modelos ni efectuar cambios sin disparar tools autorizadas.

## Radar de innovación

El usuario solicita identificación diaria de herramientas y oportunidades nuevas. Una automatización nueva de ChatGPT no se creó porque la cuenta alcanzó el límite de cinco tareas programadas. No se pausó ni modificó ninguna tarea existente. Alternativas: sustituir con consentimiento una tarea ya vencida o crear un workflow n8n con publicación diaria y persistencia en repositorio/Drive.

## Política de repositorio

Este repositorio es público: no agregar host IP, topología sensible, claves, credenciales, contenido de clientes, comandos sudo con rutas privadas o datos de backup. La arquitectura aquí es genérica; detalles operativos y manifiestos de release deben estar bajo control privado.
