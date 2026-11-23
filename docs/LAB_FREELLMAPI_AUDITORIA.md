# Auditoría preliminar de FreeLLMAPI para JF SOLUCIONES
**Fecha:** 2026-11-23 (America/Lima)  
**Estado:** revisión estática de código y documentación publicados; **no** pentest, SCA completa, instalación ni tráfico real con proveedores.

## Evidencia examinada (upstream, solo lectura)

- Repositorio: https://github.com/tashfeenahmed/freellmapi
- Commit de referencia en `main`: [43b92cdfedd2c85b17f666080bab5b6c8707a0fa](https://github.com/tashfeenahmed/freellmapi/commit/43b92cdfedd2c85b17f666080bab5b6c8707a0fa)
- Última release observada: `v0.16.40`, publicada el 2026-11-23.
- Archivos consultados: `README.md`, `docs/en/api/01-rest-api.md`, `docs/en/install/01-install.md`, `SECURITY.md`, `package.json`, `Dockerfile`, `docker-entrypoint.sh`, `docker-compose.yml`, `.github/workflows/ci.yml`.
- La copia disponible puede cambiar en futuras revisiones. **No** afirmar que una imagen Docker comparte este hash: revisar su propio digest.

## Matriz de evidencias y riesgos

| Componente | Confirmado en código/documentación | Riesgo y decisión de laboratorio |
|---|---|---|
| API | `/v1/chat/completions`, `model: "auto"`, Bearer, `X-Routed-Via` | Contrato apto para una sonda sintética; no acredita capacidad de inferencia ni fallback |
| Red | Compose publica `${HOST_BIND:-127.0.0.1}:${PORT:-3001}:3001` | Mantener loopback; prohibido `HOST_BIND=0.0.0.0` en VPS compartidos |
| Imagen | `ghcr.io/tashfeenahmed/freellmapi:latest` | Etiqueta mutable: **no desplegar** sin seleccionar release/imagen y verificar digest y procedencia |
| Contenedor | El Dockerfile inicia entrypoint como root para adecuar volumen, después ejecuta `setpriv` como usuario node | Verificar imagen real, UID final y permisos; no confundir drop de privilegios con sandbox completa |
| Actualizador | Servicio Watchtower optativo con perfil `autoupdate`; monta `/var/run/docker.sock` | No habilitar: socket Docker es equivalente a control elevado del host |
| Datos | SQLite; proveedor declara AES-256-GCM y `ENCRYPTION_KEY` | Ni claves ni base de datos de clientes en piloto. Custodiar `.env` fuera de Git |
| Catálogo | Fuente remota firmada, sincronizable; versión gratuita puede usar catálogo retrasado | Evaluar confianza de la firma/canal y efectos de actualizaciones dinámicas |
| Aislamiento | `SECURITY.md`: herramienta single-user, sin multi-tenant; soporte best-effort | **No apta directamente para Gestión360 multiempresa** ni servicio de clientes |
| Seguridad y versiones | `SECURITY.md` aún dice 0.13.x como versión actual; release observada v0.16.40 | Documentación de seguridad desactualizada; solicitar/validar política real antes de desplegar |
| Proveedores | Tiers gratuitos y restricciones individuales | No asumir tokens garantizados; cumplir TOS, límites, privacidad y licencias |

## Comprobación automática disponible

- `src/labs/freellmapi-contract.js`: solo `http://127.0.0.1:3001`, `http://localhost:3001` o IPv6 loopback; redirecciones prohibidas; 10 segundos de timeout.
- `test/freellmapi.test.js`: pruebas unitarias con transporte simulado (sin red).
- `test/freellmapi-http.test.js`: servidor **simulado por nosotros** en `127.0.0.1:3001`; prueba tráfico HTTP local verdadero con token **falso**, JSON sintético, 429 y rechazo de redirect.
- Ejecutar con Node.js 22+: `npm test`. El workflow CI ya existente lo ejecuta en PR.
- **Importante:** el servidor en el test NO es FreeLLMAPI; no verifica el router externo ni el cifrado anunciado.

## Puertas de avance

- **Gate A (este PR):** pruebas unitarias y HTTP simuladas pasan; docs con riesgos; sin secretos.
- **Gate B:** revisión de dependencias (SCA), licencias, Docker, trazabilidad de imagen, instalación offline/aislada sobre equipo de laboratorio propio; aprobar capacidad de revocación y rollback.
- **Gate C:** clave de un proveedor autorizada SOLO para prueba; medir p50/p95, TTL, 429, no filtración de claves, comportamiento de fallback y costes, siempre con datos sintéticos.
- **Gate D:** evaluación por separado de un proxy empresarial con autenticación multiempresa y facturación/aislamiento; FreeLLMAPI no recibe aprobación comercial por herencia.

## Reglas de operación

1. No `curl | bash` ni `:latest` en VPS de JF.
2. No instalar Watchtower ni montar `docker.sock`.
3. No usar claves de Meta, WhatsApp, Gmail, OpenAI, VPS ni clientes.
4. No exponer puertos públicos ni ejecutar código upstream como root en VPS compartidos.
5. No realizar merges ni despliegues de forma automática desde esta rama; mantener PR como **draft**.
6. La implementación/uso de código MIT exige preservar avisos de licencia si se copia o redistribuye; este laboratorio contiene código original de JF y enlaces al upstream.
