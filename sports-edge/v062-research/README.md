# JF SPORTS EDGE AI v0.6.2 — Scout e identidad de encuentros

**Estado:** investigación local, **no** desplegado en Django/CORE. No habilita recomendaciones de apuestas ni consume créditos de clientes.

## Entregable

Se añadieron `identity.py`, `scout_evidence.py` y `test_identity_scout.py` a esta rama de GitHub.

- Resuelve IDs de clubes por proveedor y temporada, sin coincidencias difusas.
- Bloquea partidos con equipos/localía cambiada, liga incorrecta, horario discordante o snapshots obsoletos/futuros.
- Distingue alineaciones oficiales, probables y desconocidas.
- Exige 11 jugadores en una alineación confirmada y detecta bajas conflictivas.
- Mantiene `known_absences = None` cuando la fuente no certifica **completitud**, aunque la lista de ausencias venga vacía.
- Valida la fecha y procedencia de estadísticas por jugador.
- El resultado dice explícitamente `probabilities_calibrated=False`, no inventa porcentajes de impacto deportivo.

**Tests:** paquete completo v0.6.2 pasó **46/46 pruebas locales**: 27 anteriores + 19 nuevas. Se crearon IDs y clubes **ficticios** para pruebas; no son un mapeo real de API-Football/OpenLigaDB.

**ZIP en la conversación:** `JF_SPORTS_EDGE_V062_SCOUT_RESEARCH.zip`, SHA256 `49e7367940071b292f4716f22dcc23ccdca4050c5309f30f9cc1025354984587`. Incluye también la base v0.6.1. No está instalado en VPS1; no se debe repetir bootstrap anterior.

## Fuentes y licencias verificadas

| Recurso | Función | Recomendación |
|---|---|---|
| [API-Football](https://www.api-football.com/documentation-v3) | Alineaciones, lesiones, estadísticas y cuotas según cobertura | Alta prioridad; requiere credencial y revisar uso/plan |
| [OpenFootball](https://github.com/openfootball/football.json) | Histórico CC0 | Ya se usa |
| [penaltyblog](https://github.com/martineastwood/penaltyblog) | Poisson, Dixon–Coles, Poisson bivariado; MIT | Benchmark en investigación |
| [Pandera](https://github.com/unionai-oss/pandera) | Contratos de calidad de datos; MIT | Incorporar si escala la ingesta |
| [Evidently](https://github.com/evidentlyai/evidently) | Drift, calidad, monitoreo de ML; Apache-2.0 | Tras generar meses de snapshots |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agentes con estado; MIT | Opcional, sin duplicar n8n |

Los permisos de librerías no autorizan automáticamente el uso de datos de terceros. `fixtures/players` puede contener resultados posteriores al partido; la predicción prepartido requiere snapshots observados antes del kickoff.

## Bloqueos que permanecen

1. Activar un proveedor con llave propia en almacenamiento seguro y confirmar cobertura por competencia y temporada. No compartir claves en GitHub ni en el chat.
2. Construir el mapeo **real** y firmado de IDs de equipos. El código de tests usa solo nombres/IDs ficticios.
3. Registrar snapshots de cuotas, lesionados y convocatorias antes del inicio.
4. Validar temporada por temporada 1X2, ambos marcan y goles; no recomendar BTTS ni +1.5 basándose en el holdout disponible, donde el baseline era mejor.
5. Integración end-to-end en staging CORE/Django, permisos multi-tenant, historial, cuotas, controles de concurrencia.
6. Release de producción mediante flujo con aprobación, checksum, backups y rollback. Los workflows n8n existentes **solo hacen QA/validate/status**.

**Evidencia anterior:** n8n 1523 evaluó 306 partidos, y n8n 1526/1527 mantuvo servicios saludables. Estas validaciones pertenecen a v0.6.1; v0.6.2 todavía está local.
