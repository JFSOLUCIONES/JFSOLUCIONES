# JF SOLUCIONES | FreeLLMAPI: verificación real y seguridad

Fecha de ejecución: **23/11/2026**. Responsable: laboratorio técnico JF SOLUCIONES.

## Referencias y trazabilidad

- Upstream: https://github.com/tashfeenahmed/freellmapi
- Revisión exacta ejecutada en GitHub Actions: `43b92cdfedd2c85b17f666080bab5b6c8707a0fa` (rama upstream `main` observada el 23/11/2026).
- La revisión probada **no se debe confundir** con la release `v0.16.40`; no se ha ensayado esa imagen ni un digest de GHCR.
- Ejecución dinámica: https://github.com/JFSOLUCIONES/JFSOLUCIONES/actions/runs/45263120524
- Ejecución de auditoría detallada: https://github.com/JFSOLUCIONES/JFSOLUCIONES/actions/runs/45263403031
- Rama de trabajo JF: `lab/freellmapi-contract-20261123`, PR N° 12, mantener en borrador.

## Prueba dinámica con el software auténtico

Ejecutada en **GitHub-hosted runner temporal**, no en VPS1/VPS2:
- Instalación con `npm ci` y compilación real con `npm run build`: **correctas**.
- Servidor Node original arranca en `127.0.0.1:3001` con `NODE_ENV=production`.
- `GET /api/ping`: respuesta correcta.
- `POST /v1/chat/completions` sin token: **HTTP 401**.
- Misma ruta con token deliberadamente inválido: **HTTP 401**.
- No se configuraron claves de proveedores; **no hubo inferencia** ni se probó failover, velocidad, cuotas, calidad o facturación.
- Clave de cifrado aleatoria y base de datos de ensayo se crearon solo en el runner; archivo de log de arranque no fue expuesto y se eliminó al finalizar.
- No se utilizó el VPS ni se modificó ningún workflow n8n.

## Auditoría SCA sobre dependencias de producción

Comando de la CI: `npm audit --omit=dev --json`, analizado sin publicar el JSON completo.

| Severidad reportada por npm | Conteo |
|---|---:|
| Crítica | 0 |
| Alta | **13** |
| Moderada | **9** |
| Baja | 0 |

**Bloqueo:** la CI se marca intencionalmente como **failure** cuando existen hallazgos altos o críticos. La aplicación arranca, pero **NO está aprobada** para producción ni para recibir información de clientes.

### Paquetes de severidad alta reportados

**Dependencias directas:** `compression`, `multer`, `sharp`, `shadcn`, `undici`, `vite`.

**Dependencias transitivas:** `@modelcontextprotocol/sdk`, `body-parser`, `brace-expansion`, `browserslist`, `fast-uri`, `source-map-js`, `zod`.

La salida de npm también marcó vulnerabilidades moderadas en `@hono/node-server`, `@ts-morph/common`, `baseline-browser-mapping`, `hono`, `ip-address`, `minimatch`, `postcss-selector-parser`, `qs` y `ts-morph`.

El campo `fixAvailable` fue afirmativo para todos los paquetes listados, pero **eso no demuestra que los arreglos sean compatibles o seguros**. El conteo de npm es por paquete afectado y no constituye una comprobación de explotación efectiva en JF SOLUCIONES.

## Ruta técnica de remediación

1. Revisar avisos GHSA/CVE de cada dependencia, distinguir rutas realmente alcanzables y los cambios de versión necesarios; priorizar `@modelcontextprotocol/sdk`, `multer`, `undici`, `sharp` y `compression`.
2. En copia aislada del upstream y con commits fijados, generar una propuesta de actualizaciones compatibles sin `npm audit fix --force`. Registrar los cambios del lockfile, licencias y integridad de artefactos.
3. Repetir `npm ci`, `npm run build`, suite de pruebas upstream, auditoría npm y el mismo smoke de arranque/401.
4. Exigir **cero vulnerabilidades altas/críticas** o un dictamen de riesgo documentado y aceptado por seguridad antes de cualquier integración experimental mayor.
5. Verificar aparte imagen Docker por digest, privilegios reales y actualizador Watchtower. No montar `docker.sock`, no usar `:latest` y no publicar puertos.
6. Para entornos comerciales, exigir controles multicliente, auditoría, aislamiento de datos, presupuestos y acuerdos con proveedores; FreeLLMAPI es single-user por diseño.

**Estado final de esta fase:** **funcionalidad básica validada / seguridad no aprobada / despliegue bloqueado**.
