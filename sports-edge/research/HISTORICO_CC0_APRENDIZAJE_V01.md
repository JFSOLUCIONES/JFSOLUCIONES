# JF SPORTS EDGE | Laboratorio CC0 y permiso de datos (21/11/2026)

## Conclusión sobre football-data.co.uk

La política publicada el 20/11/2026 en https://football-data.co.uk/contact.php distingue:
- Descargas manuales para personas físicas y estudio personal/académico.
- Descargas automatizadas ligeras para ese uso, máximo dos veces por semana.
- NO destina los archivos gratuitos a proyectos comerciales o de entrenamiento automatizado de IA que impliquen uso intensivo de bots/scrapers.
- Deriva usos distintos del personal/académico al proveedor licenciado TheStatsAPI.

No confundir **uso privado del propietario** con una licencia de entrenamiento del producto JF SPORTS EDGE AI. No automatizar ese proveedor ni usarlo para entrenar el agente comercial mientras no exista autorización expresa para la finalidad concreta.

## Alternativa ejecutable con derechos CC0

Datos: https://github.com/openfootball/football.json bajo CC0-1.0. Bundesliga: carpetas YYYY-YY/de.1.json (resultados, no lesionados ni cuotas); el repositorio admite 2010-11 en adelante para esta ruta. Hay otras temporadas y formatos en https://github.com/openfootball/deutschland que deben normalizarse con controles de calidad.

Script de JF SOLUCIONES: **JF_SPORTS_EDGE_HISTORICO_CC0_V1.zip**, artefacto verificado de la conversación (sin secretos, no conectado a producción). Su hash SHA256 es:

`0cc312b5ed074d80b7d1abc902f82f0f11cfaabad2fd8fcb9946212e719e10f9`

### Procedimiento en VPS1, fuera de Django/Docker producción

1. Crear carpeta aislada `/root/jf-sports-edge-research/cc0`, subir y descomprimir el ZIP.
2. Ejecutar los ocho tests `python3 -m unittest discover -s JF_SPORTS_EDGE_HISTORICO_CC0_V1/tests -v`.
3. `git clone --depth=1 https://github.com/openfootball/football.json.git football-json`.
4. Ejecutar:

```bash
python3 JF_SPORTS_EDGE_HISTORICO_CC0_V1/learn_offline.py \
 --data-dir ./football-json --league de.1 \
 --cal-season 2024-25 --test-season 2025-26 \
 --before 2026-11-21 --output ./reporte_entrenamiento_bundesliga.json
```

El laboratorio pronostica partidos secuencialmente sin usar resultados del mismo día ni futuros, ajusta temperatura solo con 2024/25, evalúa en 2025/26 y contrasta **Brier/log-loss** frente a frecuencias históricas. `status=RESEARCH_ONLY_NOT_PRODUCTION_CALIBRATED` se conserva aunque mejore el baseline. **No hay reportes reales ni resultados de entrenamiento todavía**, solamente pruebas unitarias sintéticas. El estudio no contiene lesiones, alineaciones ni cuotas; necesita validación ampliada y mercado con licencia antes de recomendaciones.

## Seguridad

No guardar credenciales, datos de clientes, ni artefactos grandes/datasets licenciados en el repositorio público. No fusionar cambios en `main` ni desplegar CORE sin pruebas independientes. Fecha de investigación: 2026-11-21.
