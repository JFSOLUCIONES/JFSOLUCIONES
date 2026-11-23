# LAB JF — FreeLLMAPI (contrato sintético, sin despliegue)

**Estado:** laboratorio de GitHub exclusivamente; no instalado en VPS, no integrado en n8n, no conectado a Gestión360 ni a clientes. Este código de prueba es original de JF SOLUCIONES; **no** incorpora código de FreeLLMAPI.

## Hipótesis y fuentes

Proyecto externo: https://github.com/tashfeenahmed/freellmapi

Documentación de la API: https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/api/01-rest-api.md

- FreeLLMAPI expone una API OpenAI-compatible en `POST /v1/chat/completions`.
- El servidor de pruebas se publica localmente en puerto 3001.
- El propietario advierte que el producto es para experimentación personal, no para producción. Cada proveedor impone sus propios términos y límites.
- No ofrece aislamiento multiempresa listo para comercializar. Las cuotas agregadas no equivalen a tokens garantizados.

## Auditoría estática de upstream

Consultar [LAB_FREELLMAPI_AUDITORIA.md](LAB_FREELLMAPI_AUDITORIA.md): revisión de Docker, entrypoint, versiones, superficie de exposición, seguridad y puertas de aprobación. Es una revisión preliminar sin análisis dinámico del servicio.

## Qué sí comprobamos

1. Validación de URL *loopback*, HTTP local y puerto 3001.
2. Construcción de un mensaje **fijo y sintético**, nunca contenidos de clientes.
3. Compatibilidad esperada de HTTP, JSON y cabecera `x-routed-via`, usando respuestas simuladas.
4. Manejo de HTTP 429, errores de transporte y esquema incorrecto sin imprimir secretos.
5. **Petición HTTP real a un servidor simulado local**, con clave deliberadamente falsa, respuesta correcta, error 429 y rechazo de redirecciones. No se ha contactado FreeLLMAPI.

Ejecutar con Node.js 22+:

```sh
npm test
```

El workflow de GitHub Actions existente también ejecuta las pruebas para cambios en `src/` y `test/`.

## Qué NO hemos comprobado

- **No hay consulta real** a FreeLLMAPI ni a APIs de terceros.
- No hay credenciales ni claves en GitHub, ni de prueba ni de producción.
- No se ha instalado Docker, ni se ha configurado un servicio externo.
- No está validada la seguridad del código externo, licencias de proveedores, latencia, precisión, enrutamiento, fallover real, coste ni SLA.
- No se debe utilizar con información sensible o datos de clientes.

## Pasos posteriores (requieren validación manual)

1. Auditar release/tags, `Dockerfile`, `docker-compose.yml`, scripts de instalación, dependencias, mecanismos de actualización y telemetría del proveedor. No ejecutar `curl | bash`.
2. Preparar en una máquina de pruebas separada una instalación con origen fijado por hash, sin puertos públicos y con salida a red restringida.
3. Si existe una clave de pruebas autorizada y las condiciones lo permiten, ejecutar la sonda con datos sintéticos y registrar solo éxito, tiempo, proveedor y estado HTTP sin guardar prompts/respuestas.
4. Medir 429/fallback con controles del proveedor, sin eludir límites, sin cuentas duplicadas y sin cargar información real.
5. Para **uso empresarial**, evaluar un gateway comercial apto para producción con APIs autorizadas, controles de acceso multiempresa, costos, logs redactados, auditoría y SLA. FreeLLMAPI no se desplegará en producción sobre la base de esta prueba.

## Política de aprobación

- PR se mantiene **draft**.
- No merges, despliegues, actualización de n8n, acceso VPS ni consumo real hasta revisión técnica.
- Este laboratorio no implica elegibilidad en promociones de contribución open source.
