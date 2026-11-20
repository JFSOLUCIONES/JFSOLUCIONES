# JF SPORTS EDGE — Puerta de despliegue controlado

**Estado al 2026-11-19: NO DESPLEGADO.**

## Procedimiento de habilitación
1. Administrador de VPS1 crea una cuenta SSH técnica con autenticación por clave y permisos restringidos al servicio `jf-sports-edge-core`; sin shell root ni grupos Docker generales.
2. Aprovisionar comando de wrapper de instalación de alcance fijo, hash verificable, repositorio privado y rollback; revisar con equipo responsable antes de activar.
3. Registrar credencial n8n `JF SPORTS EDGE - DEPLOY STAGING` (sin revelar su clave).
4. Preparar contenedor Docker independiente, red y volumen propios, acceso interno solamente; no reutilizar claves/volúmenes de Gestión 360.
5. Conceder acceso de solo lectura a vistas deportivas filtradas de PostgreSQL o, preferentemente, una API autenticada y específica; no acceso irrestricto a la base.
6. Vincular API-Football en el gestor de credenciales y comprobar plan, cuota, fuentes y permisos de redistribución.
7. Ejecutar ingestión limitada, pruebas de modelo y backtesting cronológico. Publicar únicamente cuando QA, calibración y condiciones legales estén aprobadas.
8. Integrar frontend por API autenticada con multiusuario, rate limits, logs sanitizados y estado de indisponibilidad.
9. Verificar salud real, registrar fecha/ejecución y mantener rollback operativo.

## Guardias obligatorias
- Ningún cambio a `jfgestion360-web-1`, `jfgestion360-db-1` o servicios ajenos.
- Sin credenciales, datos de cliente ni copias de base de datos en GitHub público.
- No usar el SSH restringido de auditoría para escalar privilegios o saltar controles.
- No presentar resultados de cuotas o probabilidades como garantía de ganancias.
