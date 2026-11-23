# JF SOLUCIONES | Radar verificable de agentes de programación

**Corte:** 23 de noviembre de 2026. **Estado:** investigación, sin instalación en VPS ni credenciales de proveedores. Las versiones observadas corresponden a un momento; volver a fijar el SHA antes de adoptar.

## Dos candidatos activos para prueba controlada

| Candidato | GitHub y commit verificado | Licencia raíz revisada | Capacidades y oportunidad | Riesgo / decisión |
|---|---|---|---|---|
| **Qwen Code (QwenLM)** | [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code), `main` `56c15cf50286ff55f886d4375a46a362bef806d3` | Apache-2.0 | Agente de programación; documentación oficial indica skills, subagentes, Auto-Memory y MCP, además de uso de APIs OpenAI/Anthropic/Gemini/Qwen y modelos locales. Encaja con JF CONNECT y habilidades de código, sujeto a compatibilidad real | **Candidato A**: piloto offline y de solo lectura; memoria limitada a documentos auditados, no conversaciones/credenciales de clientes |
| **OpenCode** | [anomalyco/opencode](https://github.com/anomalyco/opencode), `dev` `9a8a656e96cc0bb646d423cec12c2c86cb0b3e46` | MIT | Agente de terminal y escritorio. El README describe perfiles `plan` (sin edición por defecto, solicita permiso bash) y `build` (acceso más amplio). Útil para exploración y cambios con aprobación | **Candidato B**: exclusivamente perfil `plan` sin comandos de escritura durante auditoría. No ejecutar su comando de instalación `curl | bash` ni conceder build sobre VPS compartidos |

## Alternativas para referencia, no piloto principal

- [Continue](https://github.com/continuedev/continue), Apache-2.0, `main` `5522c6f44ca0ac3528b37244818fbfa39b5af470`. El README publicado expresa que el repositorio **ya no recibe mantenimiento activo y queda en modo lectura**. No priorizarlo para nuevo despliegue.
- [Aider](https://github.com/Aider-AI/aider), metadata GitHub Apache-2.0, `main` `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` (commit de mayo de 2026). Utilizable como referencia de pair-programming, pero requiere verificar release, dependencias, licencia de partes integradas y mantenimiento antes de adoptarlo.

## Política JF del agente que aprende

Los agentes pueden usar memoria propia o cargar instrucciones, pero **ningún agente adquiere permisos ni control de infraestructura automáticamente**. El conocimiento útil se conserva y verifica mediante:
- `AGENTS.md` por repositorio y las habilidades `.agents/skills/jf-safe-change/` y `.agents/skills/jf-oss-screen/` (archivos de este PR).
- Pruebas unitarias, reportes SCA, decisiones ADR, versiones y commits de los cambios.
- JF CONNECT (n8n): autorizaciones verificables para lectura, ensayo y operación; credenciales segregadas por proyecto.
- Gestión360: catálogo y roles empresariales, no una fuente de credenciales para agentes.
- Drive: decisiones y bitácoras operativas; no almacenar API keys o dumps sin cifrar.

**Nunca** entrenar automáticamente un modelo ni importar datos privados de clientes o chats a repositorios de habilidades. `AGENTS.md` y SKILL.md solo funcionan si el agente instalado y autorizado los lee efectivamente.

## Experimento permitido de adopción

1. Verificar release exacta, lockfile, hash, permisos y política de redes.
2. Ejecutar solo `--help`/versión o revisión local de código sintético en GitHub runner aislado, sin claves, sin shell persistente, sin permisos de GitHub para escribir, sin conexión a VPS.
3. Crear tarea reproducible: localizar un bug sintético en un archivo de muestra; comparar parches y pruebas. No usar clientes, prompts reales ni muestras de claves.
4. Medir cantidad de cambios defectuosos, tests correctos, costo por ejecución, tiempo de revisión humana, latencia y consumo.
5. Rechazar automáticamente cualquier solicitud de `docker.sock`, root, secretos, redes internas o escrituras remotas.
6. Para instalación en VPS2 se requiere autorización de operador, aislamiento de red/CPU/RAM, backup restaurable y mecanismo de reversión. **Capacidad libre no equivale a autorización.**

## Estado de implantación

**No se instalaron Qwen Code ni OpenCode en VPS1/VPS2**, ni se conectaron a n8n, Gestión360, GitHub con permisos de escritura o a proveedores reales durante esta investigación. El trabajo terminado es selección de código fuente, condiciones de licencia, plantillas de habilidades y pruebas de integridad en GitHub.
