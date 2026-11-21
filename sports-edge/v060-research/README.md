# JF SPORTS EDGE AI — CORE v0.6, cierre técnico controlado

**Fecha:** 21 de noviembre de 2026. **Estado:** candidato de investigación probado localmente, NO desplegado en producción. **No habilita apuestas automáticas ni recomendaciones comerciales**.

## Estado verificable
- Gestión360: portal v0.5.2 desplegado; control de acceso por cliente.
- n8n workflow `fAGr63LuklTmnJOr`: ejecución 1501 confirmó CORE HTTP 200, Django HTTP 302.
- CORE v0.4.5: crea solicitudes con auditoría, devuelve abstención `MODEL_NOT_CALIBRATED`.
- Historia CC0 OpenFootball Bundesliga: 4.929 resultados, corrección de 12 empates 0-0 codificados `[0,0]`; holdout 2025/26 de 306 partidos, exactitud 0,53595; Brier multiclase sumado 0,59344; log-loss 0,99757; ECE top-class 0,07593. No se certifica rentabilidad.
- n8n: credencial restringida de desarrollo SSH, sin API deportiva de cuotas/lesiones/alineaciones registrada. SSH NO implica acceso root ni despliegue productivo.
- QA local candidato: 13 pruebas de release y 8 de evaluación histórica aprobadas.

## Entregable original
`JF_SPORTS_EDGE_V060_CANDIDATO.zip`: paquete original en conversación, SHA256 `898c329dffbf9d519299616ce89a89cb628a37090467d3686aa1f94ac24fefd9`. Contiene lector CC0 corregido, cálculo transparente de mercados, gate de calidad por mercado y origen de cuotas, ledger de snapshots inmutables, tests y plantilla de GitHub Actions. **No confundir** esta entrada de trazabilidad con el ZIP completo en GitHub.

## Criterios de aceptación para cerrar producción
- [x] Tenant/client auth y control de cuotas en piloto.
- [x] Asistente Bundesliga y selección de tres partidos en investigación.
- [x] Histórico CC0 0-0 reparado, holdout 306, cifras registradas.
- [x] Auditoría y monitor n8n de VPS1.
- [x] Modelos matemáticos y ledger investigación con tests aislados.
- [ ] Integración de una única versión de modelo con CORE y portal, sin mezclar calibraciones.
- [ ] Datos con licencia de cuotas, lesiones, alineaciones y estadísticas por jugador; llaves en servidor.
- [ ] Validación cronológica de cada mercado 1X2/BTTS/over y escenarios combinados, benchmarks y snapshots congelados.
- [ ] Informes productivos persistentes por cliente, pruebas de roles/CSRF/frescura/proveedores, créditos solo si informe válido.
- [ ] Despliegue n8n con comandos sudo allowlist en servidor, prueba de rollback y autorización del propietario.
- [ ] Revisión normativa aplicable en Perú y revisión contractual de datos antes de ofrecer apuestas.

### Siguiente entrega
Preparar CORE v0.6 para *staging* y conectar un proveedor de datos autorizado, sin modificar aún las imágenes de producción. Mantener separación entre estadísticas/escenarios de investigación y recomendaciones económicas hasta aprobación técnica y legal.

**Regla editorial:** no anunciar 80% de éxito, rentabilidad ni 30 años de experiencia profesional de agentes. Los agentes pueden consultar décadas de datos históricos, pero no adquirir experiencia humana.
