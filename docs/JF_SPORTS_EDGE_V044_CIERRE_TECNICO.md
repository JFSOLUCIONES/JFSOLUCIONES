# JF SPORTS EDGE v0.4.4 — cierre técnico de staging, no desplegado

Fecha de preparación: 19 de noviembre de 2026 (Perú). **Estado: código verificado localmente, pendiente de instalación autorizada en Contabo.**

## Evidencia de ejecución
- Artefacto: `JF_SPORTS_EDGE_API_V044_STAGING_VERIFICADO.zip`
- SHA-256: `abbd326b136622a77f70b03efef39380fbbae2726777fc004f61149e92463309`.
- 25 pruebas unitarias pasan.
- Prueba HTTP de extremo a extremo contra servidor local vinculado a loopback: health 200, sin autorización 401, POST 202, GET 200 con abstención, reintento idempotente, acceso de otro tenant 404, petición conflictiva 409.
- Docker Compose contiene healthcheck para endpoint `/health`, seguridad por usuario 10001 y volumen dedicado.
- Scripts y verificación sintáctica de Bash y Python revisados.
- Auditoría remota VPS1 existente: n8n SSH solo lectura; no hay permiso de instalación, sin CORE activo.
- Limitación técnica identificada: loopback del VPS no es el loopback del contenedor web de Gestión360; no habilitar frontend hasta conectar una red privada o proxy interno correctamente autorizado.

## Ruta final de operación
1. Operador con privilegios de despliegue aprobados instala en staging aislado con `ops/deploy_api_staging_authorized.sh`. No pasar secretos al chat.
2. Ejecutar `ops/smoke_api_staging.py` contra API interna con token desde gestor privado. Exige URL loopback para el test local.
3. Evaluar framework/rutas del backend Gestión360 y agregar gateway autenticado server-to-server; obtener user/tenant solo desde sesión.
4. Conectar mediante red privada sin publicar el puerto 8088; validar firewall, TLS interno o política equivalente, y permisos.
5. Repetir pruebas cruzadas desde backend autenticado; validar rollback `ops/stop_api_staging_authorized.sh`.
6. En producción, solo habilitar solicitudes con abstención hasta tener cuotas verificadas y modelos calibrados.

## No realizado
- Ni Docker ni el gateway de Gestión360 han sido ejecutados en VPS1.
- No hay apuestas ni recomendaciones de valor generadas automáticamente.
- No se exponen llaves, contraseñas ni datos personales.
