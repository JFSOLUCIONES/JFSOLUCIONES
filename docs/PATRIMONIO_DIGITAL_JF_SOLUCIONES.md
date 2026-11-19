# Patrimonio digital de JF SOLUCIONES

Actualizado: 2026-11-19. Documento de inventario **público y no sensible**.

## Propósito
GitHub centraliza código original autorizado, especificaciones de servicios, registros de procedencia y documentación. JF CONNECT n8n orquesta trabajos programados. JF CONTROL AI inspecciona VPS1/VPS2 con permisos mínimos. Gestión 360 representa el catálogo y los estados; cada portal de cliente exhibe exclusivamente información autorizada.

## Capas
1. **ChatGPT + Plugins + Skills**: planificación, investigación, revisión, creación de workflows y ejecución a través de conectores específicos.
2. **JF CONNECT n8n**: triggers, colas, webhooks, integraciones, reintentos, registros y supervisión.
3. **JF CONTROL AI**: auditoría restringida de VPS1/VPS2, salud de infraestructura, copias verificadas y operaciones expresamente autorizadas.
4. **Gestión 360**: inventario maestro de sistemas, clientes, roles, accesos, incidencias y auditorías.
5. **Aplicaciones de clientes**: portales aislados con control de acceso por organización y separación de datos.

## Evidencia mínima por activo
- ID, nombre, propietario/licencia, URL oficial (sin tokens), entorno, servicio responsable.
- Estado: `propuesta`, `desarrollo`, `staging`, `produccion_verificada`, `bloqueado` o `retirado`.
- Evidencia de última comprobación: fecha UTC, tipo de chequeo, workflow/ejecución y alcance real.
- Responsable de aprobación; revisión de permisos, datos personales y condiciones de licencia.
- **No confundir existencia de un contenedor con salud funcional de la aplicación.**

## Seguridad y derechos
- Nunca subir archivos `.env`, claves SSH, tokens, contraseñas, información de clientes, expedientes ni exportaciones privadas.
- Descubrir software externo **no** transfiere derechos de autor; enlazar fuente y licencia, revisar obligaciones antes de reutilizar código.
- Proteger despliegues mediante cuentas de propósito único, comandos permitidos, backup y prueba de restauración, registro y rollback.
- El repositorio `JFSOLUCIONES/JFSOLUCIONES` es público: no trasladar allí sistemas privados sin un repositorio adecuado y permisos explícitos.

## JF SPORTS EDGE
- Motor deportivo existente (en pantalla de Gestión 360): v0.3.5, no validado aún como modelo productivo independiente.
- Portal HTML v0.3.6: demostrativo local, sin enlace real a proveedor de cuotas.
- Paquetes CORE v0.4.x: pruebas locales declaradas; despliegue del contenedor independiente aún no comprobado.
- VPS1: `jfgestion360-web-1` y `jfgestion360-db-1` presentes en inventario de solo lectura.
- `jf-sports-edge-core`: **no detectado en VPS1** (comprobación del 2026-11-19).
- Condiciones antes de clientes: datos/odds licenciados, calibración y validación fuera de muestra, incertidumbre, permisos de usuario, privacidad y evaluación legal.

## Operación reproducible
Un flujo de n8n debe tener contrato de entradas/salidas, credenciales segregadas, idempotencia, límites, timeouts, historial, alertas, pruebas y posibilidad de reversión. Los procesos automáticos operan en n8n sin requerir sesión abierta de ChatGPT; ChatGPT no supervisa de forma continua por sí mismo.

## Prioridades
1. Mantener inventario y supervisión en lectura; crear avisos de fallos con canal autorizado.
2. Establecer repositorio **privado** por aplicación para código, dependencias y pipelines.
3. Preparar servicio de staging independiente para Sports Edge; no reemplazar `jfgestion360-web-1`.
4. Crear adaptadores de API oficiales y pruebas cronológicas reproducibles antes de publicar predicciones.
5. Integrar Gestión 360 con estados obtenidos de APIs autenticadas; no registrar secretos en frontend ni logs.
