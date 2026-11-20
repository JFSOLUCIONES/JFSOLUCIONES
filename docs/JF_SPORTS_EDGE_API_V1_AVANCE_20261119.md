# JF SPORTS EDGE AI — Inicio de API interna (19 nov 2026)

## Verificado
- Se implementó en un paquete local separado del VPS el módulo Python `api_v1.py`, basado en CORE v0.4.1.
- Se probaron **25 tests** (21 heredados + 4 suites de integración API) con la biblioteca estándar de Python.
- Ciclo HTTP: POST `/internal/v1/analyses` (202), GET `/internal/v1/analyses/{uuid}` (200).
- Cabeceras internas: Authorization Bearer del servicio, X-JF-Tenant-Id, X-JF-User-Id, Idempotency-Key.
- Respuesta segura: `abstained`, propuestas vacías, motivo `MODEL_NOT_CALIBRATED`.
- Persistencia SQLite transaccional e idempotencia por tenant/usuario.
- El paquete completo descargable fue entregado en ChatGPT como `JF_SPORTS_EDGE_API_V042_PILOTO.zip` (SHA-256 `6192662526ba91cfe2bc550b7fe43209a2ef0f5645d6b69d0b07d656a63f8e59`).

## NO realizado
- El código de API aún no está incorporado a este repositorio; aquí se conserva el acta técnica para revisión.
- No hay acceso de escritura autorizado al backend Gestión360 ni al VPS de producción.
- No se ha cambiado la página del cliente ni desplegado CORE v0.4.2.
- Sin proveedor de cuotas verificadas ni modelo calibrado. No se generan propuestas reales.
- n8n sigue recopilando información; no está conectado al ciclo HTTP del nuevo servicio.

## Integración requerida (gateway Gestión360)
1. Revisar framework, router, autenticación/RBAC y contratos del backend de Gestión360; no suponer tecnología.
2. Crear rutas autenticadas del navegador `POST /api/v1/sports-edge/analyses` y `GET /api/v1/sports-edge/analyses/{id}`.
3. Derivar los IDs de usuario/tenant **desde la sesión del servidor**, jamás desde el navegador, y llamar por red interna a la API.
4. Aprovisionar secreto mediante gestor seguro, contenedor y volumen separados; no usar PostgreSQL ni volúmenes existentes.
5. Ejecutar en staging las pruebas 401, 403/404 tenant, 409 idempotencia, 422 validación, estado abstained, timeout, rollback.
6. Crear una UI con estados en espera / abstención / propuestas solamente cuando un modelo y cuotas reales hayan superado QA.
7. Conectar n8n y fuente de cuotas autorizada, versionar modelo y registrar snapshots. No hacer apuestas automáticas.

## Controles y seguridad
El token de servicio debe permanecer en el backend. API liga a loopback, nunca se expone al navegador. Validación fuera de muestra es requisito antes de presentar valor esperado como recomendación. Ningún dato de cliente o secreto se incluye aquí.
