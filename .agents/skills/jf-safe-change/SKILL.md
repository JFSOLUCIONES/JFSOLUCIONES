---
name: jf-safe-change
description: Planifica, implementa y audita cambios de código de JF SOLUCIONES con evidencias CI y permisos mínimos, sin modificar producción ni secretos.
---

# JF Safe Change — procedimiento de ingeniería

Usar cuando se solicite arreglar, ampliar, integrar o acelerar un sistema JF SOLUCIONES. Esta skill **no concede permisos**, ni ejecuta cambios por sí sola; siempre está subordinada a `AGENTS.md`, a la gobernanza n8n y a autorizaciones específicas.

## Datos mínimos

Recopilar nombre y repositorio del proyecto, rama/SHA base, entorno (mock, CI, staging o producción), objetivo y criterios de aceptación. Si el entorno real no es verificable, no afirmar un estado operativo.

## Secuencia

1. **Descubrimiento de solo lectura.** Consultar repositorio, PRs abiertos, últimas acciones CI, inventario y documentación autorizados. Registrar SHA, fecha y fuente de cada afirmación. Preferir recuperar el test fallido antes de editar.
2. **Hipótesis pequeña.** Localizar una causa reproducible; no combinar arreglos con despliegues, actualizaciones mayores ni refactorizaciones masivas. Identificar un rollback.
3. **Pruebas y parche.** Añadir test de regresión sin secretos y modificar solo lo necesario en rama separada. El código de proveedores debe impedir redirecciones de tokens y rechazar fallos de autenticación, paginación o esquema. Evitar redes externas en CI salvo dependencias verificadas.
4. **Seguridad.** Ejecutar SCA de `runtime` y de `dev` por separado; no describir reclasificación `devDependency` como corrección de CVE. Verificar licencias, rutas de ejecución, Docker digest, permisos y logs saneados.
5. **Validación.** Registrar pruebas unitarias, integración, lint, build, mocks y E2E cada una con su alcance. No confundir salud HTTP con autorización multiempresa. Un 302 sin sesión no demuestra que el cliente pueda iniciar sesión.
6. **PR en borrador.** Guardar diff, evidencia CI, hallazgos pendientes y no incluir claves, bases de datos, medios privados ni datos sensibles.
7. **Gate de publicación.** **Bloquear merge/deploy** hasta pruebas, política de riesgo, backups con recuperación, monitoreo y aprobación humana verificable. Si un componente falla, explicar bloqueo y siguiente acción específica.

## Contrato de resultado

Entrega: enlaces exactos a PR/runs, SHA base y del cambio, pruebas y resultados, si se tocó o no producción y lista priorizada de bloqueos. No prometer trabajo en segundo plano ni asegurar exactitud predictiva.
