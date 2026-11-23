# JF SOLUCIONES — AGENTS.md

Este archivo guía a los agentes de desarrollo que lean **este repositorio público**. No concede privilegios, acceso a VPS, ni permisos para actuar en nombre de clientes. Para los controles reales, verificar la gobernanza vigente en **JF CONTROL AI / n8n**. La mera lectura de este documento no demuestra que otros agentes apliquen estas barreras.

## Alcance real de este repositorio

Repositorio `JFSOLUCIONES/JFSOLUCIONES`: núcleo experimental del periódico digital NO+, documentación de continuidad y laboratorios de ingeniería JF. **No es un volcado de producción de todos los proyectos**, y no se asume que una rama experimental esté desplegada.

Para sistemas particulares, conservar repositorios separados y privados. Evitar incluir información operativa sensible de los clientes en ramas públicas.

## Principios innegociables

1. **Primero evidencia, después acciones**: distinguir observado, simulado, verificado en staging y verificado en producción. Registrar fecha, ejecución CI, SHA y fuente.
2. **Sin root sin límites**: utilizar solo comandos y credenciales preautorizados por servicio y entorno. Nada de editar `sshd`, firewall, cuentas, Docker socket o secretos desde un workflow genérico.
3. **No tocar clientes**: sin publicar en redes, mandar WhatsApp, generar facturas, alterar bases de datos, reproducir voces identificables o activar publicidad sin autorización humana, política aplicable y derechos comprobados.
4. **GitHub no es una bóveda**: prohibidos `.env`, llaves privadas, cookies, OAuth tokens, dumps, datos personales, materiales clínicos, archivos de voz de clientes, registros identificables y copias sin anonimizar.
5. **Branch + pull request en borrador** para cambios técnicos; ejecutar tests, escáner de dependencias y revisión. El `merge`, deploy, restauración y rollback requieren aprobación específica.
6. **Licencias upstream**: antes de reutilizar código externo, verificar el archivo LICENSE, la licencia de las dependencias y las funciones comunitarias vs empresariales; no inferir compatibilidad solo por estrellas de GitHub.
7. **No ejecutar remoto a ciegas**: evitar `curl | bash`, imágenes `:latest`, scripts sin inspeccionar y servicios expuestos en `0.0.0.0` en VPS compartidos.
8. **No presentar simulaciones como producción**. Tests con mocks verifican contratos, no funcionamiento real de APIs, pagos, inferencias o entregas.

## Arquitectura de responsabilidad

- **Gestión360**: catálogo maestro de productos, clientes y autorizaciones; validar acceso y roles antes de integrar.
- **JF CONNECT / n8n**: orquestador de flujos y observabilidad, con acciones separadas en lectura, ensayo y cambios de producción.
- **VPS1**: sistemas actualmente alojados; cambios solo con inventario vigente, preflight, backup verificable y rollback. No instalar laboratorios experimentales allí automáticamente.
- **VPS2**: posible entorno de desarrollo únicamente después de comprobar recursos libres, aislamiento, permisos y concurrencia con sistemas existentes. No equivale a un sandbox gratuito por tener disco disponible.
- **Google Drive**: documentos operativos y copias **cifradas** cuando estén verificadas; nunca almacenar identidades privadas ni claves junto a las copias. Verificar restauraciones, no solo archivos.
- **GitHub**: fuente versionada, PR, CI, artefactos revisables, pruebas y documentación. No sustituye backup ni gestión de credenciales.

## Flujo estándar de un agente para cada tarea

1. Inventariar código, versión, dependencias, estado verificado, límites y responsables.
2. Formular cambio y criterios de aceptación (funcionales, seguridad, privacidad, accesibilidad, licencia y costos).
3. Hacer cambio mínimo, reversible, en una rama. Tests sintéticos primero.
4. Ejecutar CI, SCA y pruebas de integración sin secretos ni acceso a clientes; conservar evidencias y SHA.
5. **Fail closed**: si hay hallazgos altos/críticos, CI roto, datos no confirmados, acceso no autorizado o falta rollback, dejar bloqueado el deploy.
6. Para staging, exigir autorización de entorno, instantánea/backup y monitoreo; para producción, aprobación humana explícita y plan de reversión.
7. Registrar resultado con enlaces verificables y actualizar el catálogo maestro si hay un mecanismo de escritura autorizado.

## JF LAB FreeLLMAPI

- Base: `docs/LAB_FREELLMAPI.md`, `docs/LAB_FREELLMAPI_AUDITORIA.md` y `reports/FREELLMAPI_REMEDIACION_2026-11-23.md`.
- CI: `.github/workflows/freellmapi-upstream-isolated.yml`.
- Versión upstream ensayada: SHA `43b92cdfedd2c85b17f666080bab5b6c8707a0fa`; el flujo intenta actualizaciones de dependencias **solo en runner temporal**, y genera parche verificable para revisión.
- Aun con SCA alta/crítica en cero, queda pendiente auditoría de las moderadas, artefactos, tráfico real de proveedores y controles multiempresa.
- **NO** activar FreeLLMAPI como gateway comercial: está orientado a un operador único y no reemplaza la autenticación ni la separación de datos por cliente.

## Cómo construir conocimiento reutilizable (sin autoaprendizaje oculto)

El agente no adquiere privilegios o habilidades permanentes por leer este archivo. El conocimiento se conserva de manera auditable como **código, tests, instrucciones, ADRs, bitácoras y PRs**. Versionar las decisiones, enlazar documentación oficial, descartar hipótesis fallidas y exigir revisión. No copiar credenciales, conversaciones privadas o datos de cliente para entrenar modelos.

## Comandos verificables de este repositorio

```bash
npm test
```

Sin secretos ni necesidad de ejecutar FreeLLMAPI real. Ver los workflows CI para las pruebas del upstream; esos comandos **no** son instrucciones de despliegue.
