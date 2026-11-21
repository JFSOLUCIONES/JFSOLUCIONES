# JF Gestión360 · Registro seguro de enlaces MASTER / clientes

Propuesta técnica v0.1 (21-11-2026). Aislada de producción, sin secretos ni datos reales de clientes.

## Estado verificado
La tabla n8n `JF_CONTROL_AI_CATALOGO_MAESTRO_ACTIVOS` tiene 25 activos. Reporte 1766: 7 campos MASTER no vacíos, 2 cliente y 15 operativos, pero ninguno contiene una URL simple aprobable por validador estricto. Los campos pueden guardar texto descriptivo, pendiente o mezclas; no generar botones a partir de esos valores.

## Contrato de API propuesto
- GET `/api/master/catalog/links`: autorización por sesión del lado del servidor, permite a MASTER corporativo consultar sólo enlaces de activos autorizados.
- GET `/api/organizations/:tenantId/catalog/links`: lista exclusiva del tenant en sesión, sin confiar en `tenantId` del frontend.
- Un sucesor legal **no** recibe acceso por parentesco o por nombre: requiere designación legal, activación empresarial autorizada, cuenta independiente, 2FA y auditoría.
- Registrar fecha/fuente/verificación de cada URL y separar `disponible`, `pendiente`, `bloqueado`.
- Enlaces a paneles externos no sustituyen la autorización en cada aplicación.

## Pruebas locales
`node --test registry.test.mjs`: 9 pruebas.

## Producción / sin ejecutar
Alinear con esquema real de Gestión360, aplicar migración aditiva de acceso a clientes/organizaciones, RLS por tenant, backup de DB, staging y reversión. Este prototipo no concede permisos, no crea herederos y no cambia el portal productivo.
