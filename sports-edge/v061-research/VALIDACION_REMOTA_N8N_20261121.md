# JF SPORTS EDGE — Primera validación remota v0.6.1

**Fecha:** 2026-11-21 (America/Lima)  
**Procedencia:** ejecución real JF CONNECT n8n `1523` del workflow `ka6RNMPXWolXvgQ5` (manual, credencial SSH DEV restringida).  
**Operaciones:** `sudo -n /usr/local/sbin/jf-edge-research-v061 qa`; luego `sudo -n /usr/local/sbin/jf-edge-research-v061 validate`.  
**Resultado n8n:** `status=success`, `QA_OK`, `HOLDOUT_306_QUALITY_GATE_OK`, `VALIDATE_OK`. El flujo declara `productionDeployed=false`; no despliega CORE ni Django.

## Resultado de evaluación 2025/26 (306 encuentros) — motor unificado

Versión `JF_CC0_SINGLE_ENGINE_MARKETS_0.6.1`. Estado `RESEARCH_ONLY_NOT_COMMERCIAL`.

| Mercado | Brier JF | Brier referencia | Log-loss JF | Log-loss referencia | ECE JF | ECE referencia |
|---|---:|---:|---:|---:|---:|---:|
| 1X2 | 0.593443 | 0.647967 | 0.997569 | 1.070834 | 0.075927 top-class | 0.009441 top-class |
| Ambos anotan Sí | 0.244896 | 0.238361 | 0.682874 | 0.669746 | 0.064674 | 0.047310 |
| Más de 1.5 goles | 0.139762 | 0.137286 | 0.453641 | 0.447254 | 0.043620 | 0.023921 |
| Más de 2.5 goles | 0.231607 | 0.234294 | 0.654848 | 0.661514 | 0.072388 | 0.055623 |

**Observaciones:**
- 1X2: accuracy 0.535948 frente a 0.437908; mejora Brier y log-loss, **pero calibración ECE peor**.
- Ambos anotan Sí y más de 1.5: referencia supera a JF en Brier/log-loss; NO habilitar recomendaciones.
- Más de 2.5: leve mejora JF Brier/log-loss; ECE peor.
- ECE 1X2 de la clase más probable no es directamente comparable con ECE binario por mercado.
- En binarios, proporciones observadas vs media de probabilidades:
  - BTTS Sí: 0.617647 vs JF 0.554565 (subestima).
  - Más de 1.5: 0.836601 vs JF 0.794417 (subestima).
  - Más de 2.5: 0.637255 vs JF 0.583664 (subestima).
- Las cuotas teóricas y predicciones estadísticas no equivalen a ganancias ni a mercados con cuotas reales.

## Decisiones
1. No activar apuestas recomendadas ni consumo comercial por estos mercados.
2. Mejorar modelos y recalibración por mercado mediante validación temporal repetida, no optimizando directamente sobre este holdout.
3. Integrar proveedores autorizados de alineaciones, bajas y cuotas bajo claves de servidor.
4. Preparar staging Django/CORE, reportes auditables y gate por market/fixture sin elevar SSH a root general.
5. Mantener el último portal productivo estable hasta QA y aprobación.

**Importante:** Documento es auditoría de la ejecución aportada por n8n; no representa despliegue nuevo.
