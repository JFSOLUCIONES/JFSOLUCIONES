---
name: jf-oss-screen
description: Evalúa herramientas open source de programación, agentes IA, MCP y gateways antes de integrarlas al ecosistema de JF SOLUCIONES.
---

# JF OSS Screen — evaluación de software externo

Esta skill sirve para **investigar**, no para instalar automáticamente. No permite root, acceso al socket Docker, llamadas a proveedores ni ejecución de scripts externos.

## Verificaciones

1. Verificar URL del repositorio, organización, rama y commit SHA; evitar nombres ambiguos y referencias `:latest`.
2. Leer el `LICENSE` auténtico y excepciones de funciones empresariales. Separar código MIT/Apache de directorios `enterprise` o `ee` y restricciones de SaaS.
3. Consultar README y SECURITY.md para requisitos de versiones, permisos, secretos, almacenamiento, red, fallos conocidos y soporte. Un archivo de seguridad desactualizado es señal de revisión adicional.
4. Evaluar actividad de mantenimiento, releases, historial de dependencias, advisories, posibles cambios de propietario y cadena de suministro. No decidir por estrellas o publicidad.
5. Preparar una prueba **sin claves** en GitHub Actions con versión fijada, recursos acotados, `permissions: {}`, sin permisos de escritura y artefactos de hashes. No ejecutar `curl | bash` ni adjuntar `docker.sock`.
6. Informar el valor concreto para JF (ej. generación de tests, agente de código con MCP, auditoría de modelos), coste de APIs/CPU/RAM, dependencia de herramientas existentes y riesgos por cliente.
7. Proponer adopción solo tras revisión humana de licencia, calidad de pruebas, seguridad y reversión. La integración con VPS2 o n8n es una fase separada.

## Salida mínima

Tabla con `repo`, `SHA/fecha`, `licencia + excepciones`, `aplicación JF`, `riesgos`, `decisión` y evidencia. Las credenciales nunca van a GitHub ni Drive; el análisis no instala nada.
