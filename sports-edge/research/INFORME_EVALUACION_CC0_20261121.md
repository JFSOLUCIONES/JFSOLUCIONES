# JF SPORTS EDGE AI — Informe de evaluación histórica CC0 N° 001

**Fecha de la ejecución comunicada:** 2026-11-21 (VPS1, ejecución aislada de producción)  
**Modelo:** `JF_POISSON_CC0_WALKFORWARD_0.1`  
**Estado declarado por el evaluador:** `RESEARCH_ONLY_NOT_PRODUCTION_CALIBRATED`

## Datos y particiones

- Fuente: `openfootball/football.json` — CC0-1.0.
- Liga: Bundesliga.
- Temporadas presentes: 2010/11 a 2026/27 (17 temporadas listadas; no significa 17 temporadas completas).
- Partidos completados procesados: 4.917.
- Ajuste/calibración: temporada 2024/25, 306 partidos.
- Evaluación independiente (holdout): temporada 2025/26, 294 partidos (verificar por qué son 294 y no 306 antes de concluir cobertura total).
- Parámetro `temperature_fitted_on_calibration_only`: 1.2.
- Validación reportada: 8 tests de unitarios aprobados.
- Ruta del reporte en el servidor de investigación: `/root/jf-sports-edge-research/cc0/reporte_entrenamiento_bundesliga.json`. La ruta NO implica que el archivo esté respaldado en este repositorio.

## Resultados del holdout

| Métrica | Modelo JF | Referencia | Evaluación |
|---|---:|---:|---|
| Partidos | 294 | 294 | Mismo conjunto |
| Exactitud 1X2 | 0.55782 | 0.45578 | JF +0.10204 (10.204 pp) |
| Log-loss | 0.9816 | 1.05689 | JF menor (mejor) |
| Brier score | 0.58282 | 0.63899 | JF menor (mejor) |
| ECE top class | 0.08128 | 0.00777 | JF **mayor** (peor) |

No afirmar que el 55,78 % sea probabilidad de ganar una apuesta ni ROI. Exactitud 1X2 no valida ambos marcan, goles, combinadas, cuotas, ni rentabilidad. ECE top-class es una medición parcial y sensible a la discretización. Comparar además contra baselines de mercado u otros modelos razonables, no únicamente contra frecuencias históricas.

## Validaciones pendientes

1. Confirmar integridad y cobertura de los 294 encuentros en la temporada de evaluación; explicar faltantes.
2. Comprobar que todo estado y feature utilizado estaba disponible antes de cada partido; auditar ausencia de fugas de datos y el versionado de la fuente.
3. Calcular intervalos de confianza mediante bootstrap agrupado por fecha/jornada y repetir walk-forward en varias temporadas fuera de muestra.
4. Evaluar calibración 1/X/2 por clase y curvas de fiabilidad; comparar sigmoid, isotonic y temperature scaling sin utilizar el holdout para seleccionar parámetros. La documentación de scikit-learn: https://scikit-learn.org/stable/modules/calibration.html.
5. Validar cada mercado de goles/ambos marcan por separado y medir error sobre resultados futuros.
6. Para recomendaciones económicas, adquirir cuotas y fuentes de alineaciones/lesiones con derechos y conservar snapshots timestamped antes del kickoff. Evaluar yield/CLV con registro de operaciones y gastos; no deducir ganancias por exactitud.
7. No activar recomendaciones en producción ni descontar créditos por informes predictivos hasta aprobar estos controles.

**Publicación:** solo informe estadístico agregado y documentación reproducible; sin datos de clientes, tokens ni datasets externos.
