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


## Auditoría de cobertura del holdout (21/11/2026)

Inspección de `football-json/2025-26/de.1.json` realizada en VPS1 y reportada por la ejecución del usuario:

- `PARTIDOS_ARCHIVO=306`
- `MARCADORES_COMPLETOS=294`
- `SIN_MARCADOR_FINAL=12`
- `PARTIDOS_EVALUADOS_MODELO=294`

**Resultado:** El holdout de 294 coincide exactamente con los 294 registros que incluyen `score.ft` como lista de dos enteros. Cobertura de marcadores completos: **96,08 %**. No hay evidencia de doce registros adicionales omitidos por el evaluador, pero tampoco se ha comprobado todavía cuáles son los doce encuentros sin marcador ni su resultado real.

**Precaución:** La muestra puede estar sesgada por ausencia de resultados. No reemplazar las doce observaciones con marcadores inventados o derivados de la salida del modelo. Auditoría pendiente: enumerar ID/fecha/equipos/jornada de los faltantes, identificar el motivo y verificar con otra fuente con derechos adecuados; después volver a evaluar con el mismo protocolo y sin usar datos futuros.

Esta observación se basa en el resultado de terminal aportado por el operador; no se ha descargado el archivo completo al repositorio de GitHub.


## CORRECCIÓN CRÍTICA: los 12 partidos eran empates 0–0 (21/11/2026)

**El diagnóstico anterior de «marcadores ausentes» queda RECTIFICADO.** Consultamos directamente el archivo original `openfootball/football.json/2025-26/de.1.json` en GitHub (blob SHA `320994ff4b376c0aa7abe7929f9b9740cfc0eff5`) y verificamos que los 12 partidos listados como «sin marcador» tienen el campo **`"score": [0,0]`**. Otros partidos están codificados mediante `"score": {"ft": [local, visitante]}`.

El lector original `learn_offline.py` solo leía `match["score"]["ft"]`, por lo que descartó sistemáticamente 12 empates 0–0 en el holdout. Este sesgo de selección puede afectar a exactitud, Brier, log-loss y calibración. **Retirar de cualquier presentación comercial la exactitud 55,78 %, el ECE 8,13 % y la conclusión de mejora hasta recalcular.** No asumir que los datos faltan en el proveedor ni completar con valores imaginarios.

Reparación propuesta: aceptar las listas `[0,0]` para temporadas históricas ya finalizadas, mantener exclusión de encuentros futuros o no verificados en la temporada corriente, recalcular train/calibrate/test sin fugas y documentar cambios. Los números corregidos están **pendientes de ejecución** en VPS1.
