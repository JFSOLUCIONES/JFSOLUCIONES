# Puerta de integración con JF Gestión360

## Dato confirmado
El módulo existe en Gestión360 en `https://gestion360.jfconnect.online/admin/sistemas/jf-geoplan-360/`; su ficha lo presenta como desarrollo v0.1. El inventario de VPS1 del 21-11-2026, ejecución n8n N° 1770, detectó contenedores `jfgestion360-web-1`, `jfgestion360-db-1`, `jfconnect-n8n` y `jfconnect-postgres` (el inventario no prueba funcionalidad integral). Contexto histórico ubica el código productivo en `/opt/jfgestion360` como Django/PostgreSQL.

## Bloqueo verificado
El 21-11-2026, workflow `wuFsT1YP9Wiv58aW`, ejecución 1773, al ejecutar una SONDA DE EXISTENCIA de rutas vía credencial **JF CONTROL AI - VPS1**, recibió `code 126`, stderr: `DENIED: only jf-audit or jf-inventory is permitted for this SSH key`. Es un control correcto; no intentar evadirlo.

## Paso del administrador para preparar staging
- Crear usuario de desarrollo específico `jf_geoplan_dev` sin root/sudo general ni permisos de escritura en producción.
- Instalar comando de inspección fijo con lista blanca de rutas dentro de `/opt/jfgestion360` (solo nombres de directorio, hashes de fuentes no sensibles y metadatos), sin lectura de `.env`, backups, llaves ni bases.
- Entregar archivo fuente por canal seguro a un repositorio PRIVADO de JF SOLUCIONES; datos reales y secretos fuera de Git.
- Crear clon de staging con base sintética, respaldos, checks de restauración, migración reversible y CI. No apagar ni modificar tenants productivos.
- Integrar el módulo en `system_hub` reutilizando autenticación/organizaciones/roles existentes. Evaluar microservicio sólo para geometría intensiva, no duplicar usuarios.
- Regla de liberación: tests unitarios, integración 2 tenants, QA profesional, seguridad de facturación, prueba de recuperación y autorización explícita de cambio con rollback.

## VPS1/VPS2
El sistema no debe instalar GIS/BIM pesados, Blender o render en VPS productivo sin medición de RAM/CPU/SSD y reservas de recursos. PostGIS necesita migración ensayada y respaldo. El usuario informa dos VPS, pero inventarios completos y capacidad disponible siguen pendientes de auditoría actual.

## Continuidad empresarial
Cuentas nominales y administrativas distintas (MFA), política de acceso legal de sucesor, custodia cifrada fuera del VPS, actualización de dominios, inventario de claves en bóveda sin ponerlas en el panel, roles mínimos, demostración de restauración trimestral en entorno aislado.
