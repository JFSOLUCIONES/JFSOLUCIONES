# Despliegue NO+ por etapas — procedimientos controlados

**No ejecutado en VPS aún.** Ejecutar preflight ANTES de instalar cualquier software adicional.

## Paso 0: lectura de capacidad

En servidor Linux (SSH, NO PowerShell de Windows):
```bash
curl -fsSL https://raw.githubusercontent.com/JFSOLUCIONES/JFSOLUCIONES/main/ops/preflight-no-mas.sh -o /tmp/preflight-no-mas.sh
sed -n '1,160p' /tmp/preflight-no-mas.sh
bash /tmp/preflight-no-mas.sh
```
El script solo muestra recursos, contenedores, puertos y estados HTTP. No toma ni muestra tokens.

## CMS — Payload (prioridad uno)

- Evaluar memoria y recursos del VPS compartido; no instalar antes del resultado.
- Elegir plantilla **website** oficial con `npx create-payload-app -n no-mas-cms -t website` y base PostgreSQL propia, siguiendo los pasos compatibles de la versión fijada.
- Configurar Node/Next y Payload según versión compatible y construir la app **en un directorio separado**, nunca sobre `/var/www/periodiconomas.space`.
- Archivo ejemplo `ops/cms/docker-compose.cms.yml` proporciona **topología de aislamiento**: Postgres interno + aplicación CMS en localhost:3401. No ejecutar este Compose hasta que exista `./app/Dockerfile`, el proyecto Payload real y secretos locales.
- Copiar y ajustar secrets `.env.cms` fuera de Git; permisos `chmod 600`; revisar escaping si contraseñas contienen caracteres especiales.
- Caddy: agregar `redaccion.periodiconomas.space` tras configurar DNS, con `reverse_proxy 127.0.0.1:3401`; validar `caddy validate` y recargar, sin reiniciar.
- Importante: **no se debe abrir el panel administrativo a internet sin protección y MFA/roles**; desplegar en staging primero.
- Crear colecciones: Noticias (draft/published), Expedientes, Fuentes, Medios, Rectificaciones, Aprobaciones y Usuarios por rol.
- Flujo: n8n envía expediente al CMS vía API autenticada; editor revisa; publicación al portal tras aprobación humana. El bot de WhatsApp NO publica.

## Revive Adserver — publicidad

- PHP 8.1+ y extensiones compatibles; MySQL/Postgres separado.
- Obtener **paquete oficial** desde https://www.revive-adserver.com/download/; verificar SHA256 del paquete con referencia vigente.
- No desplegar ZIP de desarrollo de GitHub ni auto-installer no oficial.
- Subdominio privado de gestión publicitaria, segmentación y consentimiento de cookies, backups y gestión de permisos.

## Radio NO+ — AzuraCast

- Instalar solo después de auditoría del VPS y programación/régimen de licencias.
- AzuraCast recomienda mínimo 2 GB RAM/20GB disco; recomienda 4 CPU, 4GB RAM/40GB para unas estaciones.
- La instalación oficial es Docker. **Evitar instalador automático en VPS compartido** antes de auditar puertos 80/443, radio y red Docker; podría interferir con Caddy.
- Considerar VPS aislado para radio si el host actual se acerca a los límites.
- Streaming público solo tras derechos y licencias para música, locuciones y material de terceros.

## Criterio de cierre

1. CMS autenticado en staging, noticias en borrador, roles y bitácora.
2. API JF CONNECT → expediente NO+ probado con mensajes sintéticos y sin datos reales.
3. 1 publicación aprobada por humano visible en web; corrección editorial probada.
4. Publicidad: campaña de demostración y métricas sin datos personales.
5. Radio: reproducción con audio original/licenciado, sin interrupción de los servicios JF.
6. Backups y rollback probados antes de declararlo producción.
