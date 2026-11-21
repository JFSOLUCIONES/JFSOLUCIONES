# JF SPORTS EDGE AI — Diseño v0.5.1 (estudio de mercados)

Evolución del portal JF Gestión360 tras v0.5.0: elegir tres partidos reales de OpenLigaDB y ejecutar un **preview experimental sin consumo de créditos**.

## Qué calcula el prototipo
- Local / empate / visitante.
- Ambos equipos anotan: sí / no.
- Más / menos de 1.5 goles.
- Tres escenarios descriptivos de tres encuentros, sin porcentaje conjunto.
- Muestra histórica de 40+ encuentros ligueros, 5+ partidos por equipo y simple contracción Poisson a la media de liga.

## Restricciones obligatorias
- Rechazar IDs que no estén presentes en caché del calendario del usuario.
- Rechazar partidos iniciados, falsificados, duplicados, que empiecen en cinco minutos y fuentes caducadas o con errores.
- Mantener autenticación Django, membresía tenant, CSRF, y no descontar cuota CORE por un preview no calibrado.
- No copiar código de terceros sin licencia compatible.
- El módulo productivo actual sigue **sin recomendaciones verificadas**. Un informe de apuestas pagado requerirá CORE v0.6 con IDs seleccionados, persistencia de snapshot, cuotas reales y gate de calibración.

## Publicación
No publicar el código operativo ni secretos en el repo público de perfil. Mantener el paquete de despliegue validado en un repositorio privado apropiado cuando exista. Este branch contiene documentación y registro de licencias.
