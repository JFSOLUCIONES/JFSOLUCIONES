# JF SOLUCIONES — matriz de recuperación de sistemas

Fecha: 2026-11-20. Documento público NO contiene bases, rutas secretas, credenciales ni identidad de clientes individuales.

## Inventario observado y alcance (no equivale a restauración)
| Familia | Presencia detectada | Código privado en GitHub | Backup cifrado remoto restaurado | Estado real |
|---|---|---|---|---|
| JF CONNECT n8n + BD + panel | VPS1 / n8n 110 workflows, 43 activos | No acreditado | No acreditado aquí | Operativo parcialmente verificado |
| JF CONTROL AI | Auditorías n8n VPS1 y VPS2 | No acreditado | No acreditado aquí | Auditorías limitadas verificadas |
| JF VOICE ENGINE Kokoro | Motor Speaches VPS2 | Prototipo y documentación en PR #4; sistema local no exportado | No acreditado | Síntesis MP3 validada (ej. 1256) |
| JF VOICE STUDIO Chatterbox | n8n workflow piloto + código experimental | PR #4 borrador | Sin checkpoint instalado | Motor de clonación pendiente de prueba |
| JF STUDIO / JF CONNECT AI panel | VPS1 | No acreditado | No acreditado aquí | Contenedores vistos |
| Gestión 360 | VPS1 | No acreditado | No acreditado aquí | Contenedores vistos |
| JF SPORTS EDGE | VPS1 / workflows | PR #3 parcial, no copia total | No acreditado | Staging/API detectada; no certificar funcionalidad |
| JF CHINA | VPS1/n8n | No acreditado | No acreditado aquí | Workflows activos detectados |
| JF SALES / JF Comercial | n8n | PR #2 parcial | No acreditado | Desarrollo y QA |
| JF Academy / Digital / Elecciones | VPS1/n8n | No acreditado | No acreditado aquí | Contenedores y workflows detectados |
| JF Créditos360, Postiz | VPS2/n8n | No acreditado | Hay flujos de backup; pruebas específicas por activo pendientes en este inventario | Contenedores detectados |
| AM-Medic / CERTSE / NO+ | n8n y sitios/servicios respectivos | Una porción de NO+ en repo público; exportación global no acreditada | No acreditado aquí | Integración por cliente, permisos y datos independientes |
| JF STREAM / Cuyvalle / E4F/E4G | VPS1 | No acreditado | No acreditado aquí | Contenedores detectados |

## Procedimiento para pasar de detectado a recuperable
1. **Inventario**: identificar repo, fuente real, dependencias, BD, archivos persistentes, credenciales de servicio, responsable y servicios externos.
2. **Código**: exportar revisión verificada y sanitizada a **repo privado** de cada aplicación, con README, licencias y tests.
3. **Copia cifrada**: respaldo consistente PostgreSQL/Redis/objetos, cifrado con destinatario público `age`, comprobación remota SHA-256; nunca archivos en claro en Git público.
4. **Restauración**: usar copia aislada; comprobar conteos, inicio, endpoint/cola y workflows de muestra; registrar `RESTORE_OK` solo con pruebas.
5. **Continuidad**: programar periodicidad de respaldo y ensayos de restauración, alertas y procedimiento de transferencia a un administrador designado.

## Evidencia disponible
- Auditorías de VPS N° 1247 (VPS1) y 1248 (VPS2) el 2026-11-20: exit 0, `auditVerified=true`.
- En 2026-11-20, VPS1: 7,8 GiB RAM total / 49 GB libres aprox; VPS2: 23 GiB RAM / 271 GB libres aprox.
- n8n consultado el 2026-11-20: 110 workflows visibles, 43 activos y 67 inactivos.
- Kokoro original `s3FbmAefttTQMF79` ejecución N° 1256: MP3 65,8 KB y estado final `success`.
- GitHub conectado: 1 repo visible `JFSOLUCIONES/JFSOLUCIONES` (público). PR #1 patrimonio, #2 ventas, #3 deportes, #4 voz/video; no asumir que están fusionados.
- **Alerta:** una lista de workflows por n8n, un contenedor sano o un backup reciente NO garantizan recuperación.

## Bloqueantes para recuperación completa
- Repositorios privados de la empresa no visibles/creados desde esta integración.
- Acceso a VPS actualmente limitado al comando de auditoría; no implica permisos de exportación o restauración.
- Se requiere custodio legal y duplicado offline de recuperación de correo, GitHub, DNS, VPS, n8n encryption key y llave de descifrado.
- Verificar que respaldos remotos actuales realmente contienen base + configuración y pasan restauración aislada.
- No migrar datos o material de clientes sin derechos, contratos y segregación de permisos.
