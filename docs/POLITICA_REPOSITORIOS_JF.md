# Política de repositorios de JF SOLUCIONES

Actualizada: 2026-11-20.

## Principios

- Cada producto o sistema operativo debe tener su propio repositorio de GitHub, separado de otros clientes y servicios.
- **Privado por defecto**. Solo publicar proyectos expresamente autorizados para distribución abierta.
- El repositorio público `JFSOLUCIONES/JFSOLUCIONES` contiene el prototipo editorial NO+; no se utiliza para alojar código privado de otros sistemas.
- Nunca versionar secretos, tokens, certificados, claves SSH, archivos `.env`, volcados de bases de datos, respaldos, registros sensibles, material de clientes ni datos personales.
- Todo cambio de producción debe pasar por rama, pull request, pruebas, revisión de secretos y plan de reversión.
- Las pruebas de staging no equivalen a aprobación para producción. Los resultados deben registrar versión, fecha y alcance.
- Respetar las licencias de terceros al incorporar proyectos o componentes externos.
- Conservar el historial técnico y los artefactos de desarrollo en repositorios privados; usar documentación sanitizada para los repositorios públicos.

## Convención recomendada

- Un repositorio privado por sistema: `jf-<sistema>`.
- Ramas protegidas: `main` y `release/*`.
- Desarrollo en `feature/*` y `hardening/*`.
- Activar análisis de dependencias, escaneo de secretos y controles CI donde estén disponibles.

## Condiciones para registrar un sistema

1. Confirmar el titular del código y que no exista previamente un repositorio correcto.
2. Crear o seleccionar repositorio **privado** con permisos mínimos.
3. Publicar solo fuente verificada y documentación que no exponga infraestructura.
4. Añadir README, .gitignore, instrucciones de pruebas, riesgos conocidos y procedimiento de rollback.
5. Registrar el estado real (candidato, staging, producción), sin declarar despliegues no ejecutados.
