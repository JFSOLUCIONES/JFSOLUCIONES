# JF SOLUCIONES | Radar de código abierto para acelerar la ingeniería

**Fecha:** 23/11/2026. **Ámbito:** análisis de repositorios y licencias, sin instalar ni desplegar software. Las características y condiciones pueden cambiar: verificar un release y commit específicos antes de adoptar.

## Prioridad comercial y de ingeniería

JF no debe esperar a desarrollar desde cero todas las funciones transversales. Reutilizar **componentes y patrones verificados**: conectividad a LLM, cuotas, claves virtuales, telemetría, UI de panel, trazabilidad, pruebas CI, despliegue reversible. Mantener autoría y aislamiento del código específico de los clientes.

## Proyectos contrastados en GitHub

| Proyecto | Evidencia desde código/README | Licencia revisada | Encaje JF y límites |
|---|---|---|---|
| [FreeLLMAPI](https://github.com/tashfeenahmed/freellmapi) | Router OpenAI-compatible, fallback de proveedores; proyecto single-user | MIT | Laboratorio de interoperabilidad y benchmarking, **no** como gateway comercial multiempresa |
| [LiteLLM](https://github.com/BerriAI/litellm) | Proxy/SDK compatible con proveedores, virtual keys, gasto, load balancing, logging; mantenido activamente | MIT para código general; directorio `litellm/enterprise/` con licencia separada | **Primera opción a evaluar** para proxy empresarial JF, tras verificar qué funciones están en edición abierta y requisitos de seguridad y costo |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | Gateway compatible con modelos, retries, configuración, guardrails, opciones de despliegue; README distingue versión empresarial | MIT para este repositorio; funciones empresariales pueden requerir producto/licencia separada | Segundo candidato para pruebas de rendimiento y reglas de enrutamiento |
| [Langfuse](https://github.com/langfuse/langfuse) | Observabilidad de agentes, trazas, evaluación, prompts y gateway | MIT para código fuera de directorios EE; módulos `ee/` y análogos con licencia separada | Complemento de evaluación y observabilidad, no sustituye tenant isolation de JF CONNECT |
| [Dify](https://github.com/langgenius/dify) | Plataforma de flujos IA y RAG | Licencia Apache 2.0 modificada; **exige licencia comercial** para servicio multi-tenant definido por workspaces y restringe quitar logo del frontend | **No adoptar para SaaS multicliente JF** sin permiso/licencia adecuados; estudiar patrones sin copiar código que infrinja condiciones |

**Licencias verificadas leyendo archivos `LICENSE` de cada repositorio**. No hay justificación para llamar MIT a las partes EE o para suponer que un repositorio sea íntegramente libre de obligaciones comerciales.

## Diseño candidato de arquitectura (propuesta, NO despliegue)

```
                       JF GESTIÓN360
                  autorización y catálogo
                           |
             -----------------------------
             |                           |
       JF CONNECT n8n               Servicios por cliente
     tareas permitidas / MCP         con autorización/tenant
             |                           |
             +---------- JF API Gateway +
                           |
          autenticación + tenant + presupuesto +
           auditoría + rate limits + redacción
                           |
             LiteLLM o Portkey evaluado
                           |
             APIs de proveedores autorizadas
                           |
              Trazas agregadas y sin PII
                   (Langfuse opcional)
```

La pieza **JF API Gateway** debe validar sus propios tokens y roles, límites por cliente y proyecto, secreto separado por tenant, mínimos permisos, presupuesto en soles y reversión de cambios. No basta con instalar un router y colocar un proxy HTTP delante.

## Orden de pruebas para reducir tiempo y deuda técnica

1. **FreeLLMAPI laboratorio:** conservar el parche reproducible del workflow, verificar SHA y prueba del software real; completar moderadas, licencias de dependencias y riesgo de red (no despliegue comercial).
2. **LiteLLM/Portkey laboratorio:** proyecto aislado, sin clientes; autenticación y un máximo de 2 proveedores de prueba. Comparar streaming, tools, retries, rate limits, presupuesto y logs redactados con tests iguales.
3. **Tenant isolation:** tests cruzados: un cliente nunca obtiene tokens, conversaciones ni facturación de otro; aplicar pruebas de cabeceras y errores HTTP.
4. **Observabilidad:** guardar solo hashes/estadísticas, no prompts completos, para piloto; evaluar Langfuse únicamente después de revisar su licencia, recursos y retención de datos.
5. **VPS2:** reservar recursos solo tras un inventario verificado con capacidad real, puertos y backups; no exponer a Internet ni permitir acceso por `docker.sock`.
6. **GitHub:** versionar `AGENTS.md`, decisiones ADR, test matrices, plantillas, runbooks, scans y evidencia CI sin datos privados. Revisión humana antes de merges.
7. **Drive:** conservar documentación empresarial y respaldos cifrados con verificación de restauración. Drive no reemplaza GitHub y GitHub no reemplaza la copia off-site.

## Indicadores de aceptación exigidos antes de prestar servicio

- 0 alertas de seguridad críticas/altas sin excepción evaluada; moderadas con plan documentado.
- 100% pruebas de aislamiento por cliente, autenticación y revocación; pruebas ante 401/403/429/5xx.
- Prueba de recuperación y rollback repetible con evidencia; claves y secretos fuera de logs.
- Comparativa con costo real por millón de tokens y límites de proveedores; **no** prometer cuota gratuita garantizada.
- Criterio humano de publicación y de despliegue aprobado; contratos/licencias de cada componente.

## Estado actual verificable

- FreeLLMAPI remediación en GitHub Actions, commit upstream `43b92cdfedd2c85b17f666080bab5b6c8707a0fa`: 0 críticas, 0 altas, 4 moderadas tras `npm audit fix` no forzado y `undici@6.29.1`; compilación, migraciones, lint, tests completos y gate de remediación **aprobaron** en run 45266812778.
- GitHub fuente: https://github.com/JFSOLUCIONES/JFSOLUCIONES/pull/12.
- n8n JF CONTROL AI verificado en ejecuciones manuales 2504 (gobernanza), 2505 (VPS1) y 2506 (catálogo). Inventario VPS1: Gestión360/n8n/Postgres presentes, contenedor `jf-sports-edge-core` ausente. Catálogo: 25 activos, 17 con pendientes. Ningún cambio ejecutado en esos servicios.

**Ningún proyecto de esta lista ha sido desplegado en la infraestructura JF durante esta auditoría.**
