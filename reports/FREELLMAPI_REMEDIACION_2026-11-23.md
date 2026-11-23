# JF SOLUCIONES | Ensayo de remediación de FreeLLMAPI

Fecha: 2026-11-23 (Perú). Documento experimental. **No autoriza despliegues ni uso comercial.**

## Comprobaciones verificadas

- Revisión exacta upstream: `43b92cdfedd2c85b17f666080bab5b6c8707a0fa`.
- PR de trabajo JF: https://github.com/JFSOLUCIONES/JFSOLUCIONES/pull/12 (draft).
- Ejecución con `npm audit fix --package-lock-only --ignore-scripts`, sin `--force`, en un GitHub-hosted runner efímero:
  https://github.com/JFSOLUCIONES/JFSOLUCIONES/actions/runs/45266352630
- Reporte inicial de dependencias de producción (`npm audit --omit=dev`): 0 críticas, **13 altas**, 9 moderadas.
- Reporte tras arreglo compatible de lockfile: 0 críticas, **1 alta**, 4 moderadas.
- Alerta alta aún presente en ese punto: `undici`. Las comprobaciones `npm ci`, compilación, migraciones y lint terminaron correctamente.
- Se probó el servidor original con datos sintéticos, pero no se agregaron proveedores ni se realizó inferencia real.

## Intento de parche concreto para el bloqueo restante

El proveedor de `undici` documenta `6.29.1` como versión corregida de CVE-2026-109869 / GHSA-xjj6-f33q-929c:
https://github.com/nodejs/undici/security/advisories/GHSA-xjj6-f33q-929c

Se preparó una nueva ejecución aislada:
https://github.com/JFSOLUCIONES/JFSOLUCIONES/actions/runs/45266812778

El flujo incorpora:
1. Fix no forzado de las dependencias, con propuesta solo de lockfile.
2. Actualización dirigida de `@freellmapi/server` a `undici@6.29.1`, dentro de la línea 6.x.
3. Reauditoría de producción, compilación, migraciones y lint.
4. **Suite completa upstream** con las dependencias ensayadas.
5. Gate final: solo `success` para el job de remediación si no hay alertas altas/críticas **y** pasan las pruebas.

**Resultado verificado:** en la ejecución 45266812778, el job `remediation-preview` terminó con **success**. La auditoría después de actualizar `undici@6.29.1` reportó **0 críticas, 0 altas, 4 moderadas**. `npm ci`, compilación, migraciones, lint y la suite completa `npm test` terminaron con éxito. El job separado `upstream-smoke` sigue en **failure de forma esperada**, porque audita el lockfile **original** con 13 alertas altas: este fallo mide el riesgo de la versión sin parche. No confundir el parche temporal validado con una release upstream corregida o con autorización de desplegar.

## Seguridad operacional

- Los cambios en `package.json` / `package-lock.json` durante esta prueba son **temporales** dentro del runner; no se copian al repositorio original y tampoco se fusionan en `main` de JF.
- No se usaron secretos de GitHub, datos de clientes, claves de proveedores, VPS1, VPS2, n8n ni Gestión360.
- La herramienta es single-user por diseño; pasar una auditoría npm no la habilita para sistemas multiempresa.
- Falta demostrar compatibilidad real con proveedores autorizados, aislamiento, control de costos, red segura, rollback y auditoría de la imagen Docker por digest.

## Resultado de decisión hasta ahora

La remediación **redujo 13 de 13 alertas altas** dentro del runner temporal y superó la suite completa, con **4 moderadas pendientes**. No publicar ni usar comercialmente hasta conservar el lockfile, revisar las moderadas, verificar imágenes y red, y realizar pruebas por tenant y proveedor con autorización.
