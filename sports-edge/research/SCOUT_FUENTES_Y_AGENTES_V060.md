# JF SPORTS EDGE AI — Scout y conocimiento histórico (v0.6)

**Estado:** diseño de investigación; NO desplegado; no hay API de lesiones/plantillas conectada y el CORE no emite recomendaciones calibradas.

## Hallazgo y decisión de fuentes (21 de noviembre de 2026)

| Objetivo | Proveedor / código | Evaluación |
|---|---|---|
| Datos históricos de largo alcance | https://github.com/openfootball/football.json | CC0-1.0; cobertura según liga, equipos y temporada. No es tiempo real. |
| Fixture y marcador del piloto | https://www.openligadb.de | Ya conectado en v0.5.x; respetar ODbL, atribución y caché. |
| Lesiones, sanciones, titulares, suplentes, jugadores, estadísticas y cuotas | https://www.api-football.com/documentation-v3 | Preferido para primer piloto. Comprobar coverage.injuries/lineups/players/statistics/odds por liga y temporada. |
| Alineaciones probables y oficiales, bajas y xG cuando se incluyan en el plan | https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/lineups-and-formations | Segunda opción. Distinguir expectedLineups y lineups (confirmed). |
| Modelos de goles mejorados | https://github.com/martineastwood/penaltyblog | Examinar licencia/versiones; candidatos Dixon–Coles y Poisson bivariado. |
| Calibración | https://scikit-learn.org/stable/modules/calibration.html | Brier, log-loss, reliability plots, calibradores sigmoid/isotonic/temperature. Validación por tiempo. |
| Datos de eventos para laboratorio | https://github.com/hudl/open-data | Datos de estudio. Revisar convenio y prohibición de comercialización sin permiso. |
| SoccerData (scrapers) | https://github.com/probberechts/soccerdata | Código Apache-2.0 no equivale a permiso de uso comercial de las fuentes; no vulnerar términos. |

**Exclusión esencial:** https://football-data.co.uk/data indica que sus archivos gratuitos son para individuos privados y NO para productos comerciales ni entrenamiento automatizado por bots/scrapers/IA. No usar esos archivos en JF SOLUCIONES sin licencia expresa. 

## Arquitectura de agentes

1. **JF Match Collector:** fixtures con IDs canónicos, fuentes por licencia, caché server-side, fecha UTC.
2. **JF Scout:** lesión, suspensión, convocados, jugadores titulares (probables u oficiales), suplentes, posición, últimos minutos, xG, xA, último estado confirmado, contexto de calendario y descansos.
3. **JF Model Ensemble:** Poisson, Dixon–Coles, clasificación opcional, pesos recientes; nunca entrenar con partidos futuros.
4. **JF Calibrator:** cronología train -> calibrate -> test, congelar probabilidades T-15min, evaluar Brier/log-loss/ECE vs modelo base en datos futuros.
5. **JF Reviewer:** detener pronósticos si hay cobertura incompleta, lesiones/lineups sin confirmar, cuotas no verificadas, drift del modelo o errores de feed.
6. **JF Analyst Narrator:** responder consultas solo desde datos estructurados trazables; citar hora de actualización; no fabricar experiencia o porcentajes.
7. **JF Admin:** auditoría, cuotas, historial, restricciones multi-tenant, revisión de métricas.

## Esquema de disponibilidad previa al partido

Cada equipo contiene team_id, coverage flags por lesión/alineación/estadísticas, lineup {state: confirmed|expected|unavailable, updated_at, starting_player_ids, bench_player_ids}, absences [{player_id, reason, provider, updated_at}] y players [{player_id, minutes, xg, xa}]. 

Las bajas desconocidas no se convierten en '0'. Los probables no se rotulan como confirmados. Un jugador no puede aparecer a la vez como titular y ausente. Los datos registrados después del pronóstico no participan en él.

Las métricas de disponibilidad son **features** para un modelo que tendrá que aprender los efectos deportivos mediante validación fuera de muestra; nunca descontar manualmente 15% por ausencia de una estrella sin evidencia.

## Plan de ejecución

- Verificar cuenta y cobertura comercial en API-Football (el plan gratuito publicado ofrece 100 llamadas diarias, sujeto a cobertura/rate limits; cada liga puede tener flags distintos).
- Ingesta con n8n y caché segura con claves sólo del servidor. Mapear IDs por proveedor y fechas.
- En T-24 h obtener ausencias y probables; T-60 min actualizar oficiales si existen; T-15 min congelar snapshot; postpartido medir calibración.
- Para escenarios combinados de 3 partidos, verificar mercado individual, mismo periodo temporal y dependencias antes de cuantificar probabilidad conjunta.
- Mostrar al cliente histórico, forma, bajas verificadas y probabilidad estimada con calidad registrada; no convertir predicciones no calibradas en garantías comerciales.

**Precisión comercial:** una base de 30+ temporadas de resultados puede aportar conocimiento documental. No atribuir a un agente experiencia profesional humana de 30 años. Tampoco constituye por sí sola calibración ni rentabilidad. 
