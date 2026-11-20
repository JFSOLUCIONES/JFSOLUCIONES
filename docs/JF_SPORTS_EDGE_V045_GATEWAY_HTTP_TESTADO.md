# JF SPORTS EDGE v0.4.5 — Gateway privado probado localmente

**Estado: NO DESPLEGADO**. El gateway técnico se entrega en el ZIP `JF_SPORTS_EDGE_API_V045_GATEWAY_PROBADO.zip` SHA-256 `2103f0ce2a2060dc2ac43e1e28e1b5cc32118484bf860691780cc3cfd0945f8e`.

## Evidencia
- Se abrió e inspeccionó el ZIP v0.4.4 previo, SHA-256 `abbd326b136622a77f70b03efef39380fbbae2726777fc004f61149e92463309`.
- Se ejecutó `python -m unittest discover -s tests -q`: **28 pruebas OK**.
- Nuevo módulo `gestion360_gateway_client.py`: cliente HTTP interno sin credenciales frontend; autoriza únicamente URL loopback o HTTPS configurado por operador; tenant, usuario e idempotency key se envían desde backend confiable.
- Nuevo test `tests/test_gateway_client.py` con servidor real local: POST 202, GET 200, `abstained`, idempotencia, 401 y denegación cross-tenant 404.
- Nuevo documento `GESTION360_GATEWAY_PYTHON_V045.md` detalla procedimiento de integración backend y responsabilidades de autenticación.

## Bloqueo
- El contenedor `jfgestion360-web-1` y el VPS de Contabo aún no han sido modificados.
- Conector SSH n8n existente solo ofrece comandos de auditoría, no permisos de despliegue.
- Requiere operador de Contabo autorizado para staging y acceso al código/framework real de Gestión360. No es legítimo inferir el framework ni falsificar un gateway instalado.
- Configuración Docker host loopback por sí sola NO permite que otro contenedor acceda por su `127.0.0.1`. Red privada o reverse proxy autenticado obligatorio.

## Restricción de producto
- CORE solo devuelve abstención porque no hay modelo calibrado ni cuotas oficiales verificadas; no inventar picks.
- No publicar UI de solicitud hasta prueba real de API↔backend Gestión360 y seguridad de sesiones.
