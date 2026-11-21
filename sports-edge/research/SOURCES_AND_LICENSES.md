# JF SPORTS EDGE AI — Registro de investigación (21/11/2026)

Registro de recursos evaluados. **No significa que JF SOLUCIONES sea dueño del código de terceros**; deben respetarse sus licencias, la atribución y las condiciones de datos.

| Recurso | Uso en evaluación | Derechos / condición |
|---|---|---|
| https://github.com/callumfm/dixon-coles | Poisson/Dixon-Coles, regularización, validación temporal | MIT declarada; conservar avisos |
| https://github.com/Reymes/football-match-prediction | Elo, calibración y backtesting | MIT declarada; evaluar dependencias |
| https://github.com/MattCheng23/football-analysis | Referencia de investigación china y puertas de validación | Licencia sin verificar; no copiar código |
| https://github.com/BA-Barry/football-prediction | Agentes/LLM + investigación deportiva en chino | Sin licencia abierta declarada en raíz; no copiar |
| https://www.openligadb.de/en/terms-of-use | Datos de calendario/resultados | Datos ODbL 1.0, Fair Use, caché central y atribución |
| https://www.api-football.com/documentation-v3 | Cuotas/estadísticas/partidos, sujeto a cobertura y plan | Servicio comercial; licencia y precio por confirmar |
| https://football-data.co.uk/data | CSV históricos para backtest | Condiciones de redistribución por verificar |

## Principios de desarrollo

- Código original de JF SOLUCIONES: desarrollar y testear en rama de investigación.
- Nunca añadir secretos, credenciales SSH, tokens, datos privados de clientes ni volcados PostgreSQL a este repositorio **público**.
- Al evaluar código ajeno: registrar URL, commit, autor, licencia, cambios y obligaciones.
- La licencia de datos deportivos no es la misma que la licencia del código fuente.
- No usar porcentajes como probabilidades verificadas hasta realizar calibración fuera de muestra, comparación contra cuotas vigentes y registro prepartido inalterable.
- Combinadas de tres partidos requieren cálculo y pruebas de dependencia; la probabilidad conjunta no se obtiene automáticamente multiplicando valores.
