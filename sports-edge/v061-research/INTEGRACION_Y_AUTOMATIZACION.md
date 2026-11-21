# JF SPORTS EDGE AI — Contratos v0.6.1 y automatización segura

**Auditoría:** 21 de noviembre de 2026. **Estado:** candidato local, NO producción, NO apuestas automáticas.

## Evidencia de trabajo ejecutado
- Monitor CORE y Django por n8n: workflow `fAGr63LuklTmnJOr`, ejecución `1501`, CORE HTTP 200, Django 302.
- Control de staging creado y **ejecutado realmente** desde ChatGPT: n8n `bErjrDUVo4e0JWxp`, ejecución `1510`, vía SSH `jf_sports_dev`. `sudo -n /usr/local/sbin/jf-edge-ops-v2 status`: CORE 200, Django 302, base de datos staging healthy, imagen staging-v048. No tocó producción.
- CORE v0.6.1 candidato aislado: 27 pruebas unitarias de los contratos (incluidos mercados, calibración temporal, proveedor, ledger e integridad de 0-0) aprobadas en contenedor local.
- Artefacto ZIP de conversación `JF_SPORTS_EDGE_V061_CIERRE.zip`, SHA256 `71f3d7428af4fea961e2e44e96aa5c72cd9e3da2f1dc04fcc4adfb27721c2212`. **El ZIP completo todavía no se ha añadido a GitHub**; esta ficha no equivale a un respaldo de fuente en el repositorio.
- El complemento privado `JF Director 360 AI` pasó de v0.1.0 a v0.1.1 con una habilidad de gate de release JF SPORTS EDGE y una guía estadística corregida. Conserva las habilidades anteriores.

## Contratos del nuevo motor investigativo
1. `learn_offline.py`: parser OpenFootball CC0 con bug 0-0 corregido y evaluación cronológica.
2. `market_math.py`: distribución Poisson homogénea para 1X2, ambos anotan, más de 1.5 y 2.5 goles.
3. `multimarket.py`: utiliza **el mismo estimador de tasas de goles** en test histórico y preview de tres partidos; calibración 2024/25, holdout 2025/26 por mercado. No calcula cuota para combinadas sin validación.
4. `provider_api_football.py`: adaptador de solo lectura a API-Football v3 con endpoints permitidos, llave por variable de entorno, límites de respuesta, validación de cobertura y ausencia de paginación incompleta. **No hay llave conectada aún**.
5. `quality_gate.py`: bloquea prepartidos sin fuente actual, métricas por mercado, snapshots o cuotas verificadas; nunca habilita apuestas automáticas.
6. `ledger.py`: investigación SQLite inmutable por organización, con idempotencia, snapshot anterior al kickoff y liquidación posterior al resultado oficial. PostgreSQL de producción no modificado.

## Despliegue sin contraseña reiterada — etapa permitida
El ZIP incluye dos scripts preparados, **no instalados**:
- `deploy/bootstrap_once_v061.sh`: requiere autorización de un administrador root una sola vez, valida pruebas y crea archivos de propiedad root.
- `deploy/jf-edge-research-v061`: operaciones fijas `status`, `qa`, `validate` ejecutables con usuario `jf_sports_dev` por sudoers allowlist. No abre shell root, no escribe en Gestión360 ni habilita deploy de producción.

**No ejecutar** comandos de despliegue en producción hasta autorización humana específica, backup verificable, imagen aprobada, tests de integración y capacidad de rollback.

## Bloqueos pendientes
- Integrar proveedor con licencia contractual y tokens gestionados exclusivamente en servidor: lesiones, lineups, estadísticas de jugadores y odds reales.
- Realizar evaluación real de BTTS/goles 1.5/2.5 en los 306 encuentros del holdout y repetir sobre múltiples temporadas, con métricas y rangos de confianza.
- Normalizar IDs de clubes entre OpenLigaDB, OpenFootball y API-Football, con casos de ascensos y alias.
- Preparar staging con PostgreSQL e integración Django/CORE, roles, cuotas, CSRF, rollback.
- Revisar regulación y derechos de datos antes de comercialización.

## Código abierto auditado
- [penaltyblog](https://github.com/martineastwood/penaltyblog), MIT: Poisson, Dixon-Coles y bivariado; candidato a comparar, no incorporado.
- [callumfm/dixon-coles](https://github.com/callumfm/dixon-coles), MIT: implementación rápida de referencia.
- [Reymes/football-match-prediction](https://github.com/Reymes/football-match-prediction), MIT: estudio de calibración y paper betting; no adoptar resultados externos como propios.
- [socceraction](https://github.com/ML-KULeuven/socceraction), MIT: eventos/VAEP, sujetos a licencia separada de datos.
- [openfootball/football.json](https://github.com/openfootball/football.json), CC0: fuente del histórico.
- [API-Football](https://www.api-football.com/documentation-v3): proveedor de datos, no código libre ni licencia automática.

**Propiedad intelectual:** librerías MIT se usan bajo su licencia; estar en GitHub no las convierte en propiedad exclusiva de JF SOLUCIONES.
