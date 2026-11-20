# JF SPORTS EDGE — v0.4.3 staging controlado

**Fecha 2026-11-19. Estado: artefacto de staging preparado, NO desplegado.**

### Evidencia

- Se abrió y verificó paquete previo `JF_SPORTS_EDGE_API_V042_PILOTO.zip` SHA256 `6192662526ba91cfe2bc550b7fe43209a2ef0f5645d6b69d0b07d656a63f8e59`.
- Se ejecutó `python -m unittest discover -s tests -q`: **25 pruebas OK**.
- Se ejecutó preflight remoto n8n VPS1 `d5K2mynDD2rCD9IJ`, ejecución **948**: inventario lectura, sin despliegue ni modificación de Gestión360.
- Nueva entrega: `JF_SPORTS_EDGE_API_V043_STAGING_CONTROLADO.zip` SHA256 `44e59224839d42e788bf033d212b0fe30277e1ae6e9243a9a74831f7d3b831ea`.

### Nuevos archivos dentro del ZIP

- `Dockerfile.api.staging`: imagen mínima Python con usuario sin privilegios y `/data` dedicado.
- `compose.api.staging.yaml`: `network_mode: host` en VPS Linux, API escuchando **solo 127.0.0.1:8088**, memoria limitada, solo lectura, capacidades retiradas, volumen persistente propio.
- `ops/deploy_api_staging_authorized.sh`: provisión de secreto local aleatorio y despliegue de proyecto Docker separado, con preflight y comprobación `GET /health`.
- `ops/stop_api_staging_authorized.sh`: rollback sin eliminar volumen.
- `GESTION360_GATEWAY_INTEGRACION.md`: contrato servidor-a-servidor, controles de sesión/tenant, requisito de revisar el framework antes de modificar su backend.

**No se desplegó**: falta credencial de despliegue autorizada o intervención de administrador VPS; SSH n8n permanece de inventario restringido. Docker no disponible en el entorno de construcción, por lo que la imagen/Compose se validaron estáticamente pero el contenedor no fue probado en VPS.

### Política de seguridad

No almacenar secretos ni datos personales en este repositorio público. No exponer API interna, ni añadir el botón al cliente hasta probar el gateway autenticado. El CORE responde con `abstained` y no inventa cuotas ni recomendaciones.
