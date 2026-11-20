# Legado digital JF SOLUCIONES — guía inicial para quienes continúen la empresa

**Edición:** 2026-11-20. **Clasificación:** material público sin credenciales ni datos de clientes.
**Estado:** guía operacional en construcción; NO acredita respaldo completo de todos los proyectos.

## Para la familia y los administradores designados

Esta documentación sirve para que una persona autorizada pueda continuar la empresa y reconstruir sus sistemas sin depender de recuerdos del fundador. No constituye testamento, representación legal ni autorización automática para acceder a datos de terceros.

### Qué es cada cosa
- **GitHub / repositorios:** versiones de código, pruebas, configuración sanitizada, documentación y cambios.
- **JF CONNECT n8n:** flujos que ejecutan procesos, API y tareas programadas; no sustituye una copia versionada de sus workflows.
- **JF CONTROL AI:** herramientas de auditoría y recuperación sobre los servidores con mínimos privilegios.
- **VPS1 / VPS2:** servicios, contenedores, bases de datos y almacenamiento que requieren copias independientes.
- **Gestión 360:** catálogo y seguimiento funcional; la interfaz no equivale a los archivos fuente.
- **Almacenamiento privado cifrado:** copias de datos, llaves de recuperación y materiales cuya exposición pública está prohibida.

### Acceso de sucesión (preparar fuera del repositorio)
1. Designar formalmente un administrador tecnológico y un sustituto con capacidad legal para actuar por la empresa. Registrar cómo localizar al custodio, pero NO publicar sus datos personales aquí.
2. Configurar 2FA y guardar códigos de recuperación, llaves físicas y una copia sellada de las instrucciones de acceso en custodia offline independiente. Nunca colocar contraseñas, seeds, recovery codes ni claves privadas en GitHub, n8n o el chat.
3. Para la continuidad de repositorios privados, asignar acceso administrativo previamente a una segunda persona o, preferentemente, a una organización bajo control empresarial con dos propietarios autorizados. El "account successor" de una cuenta personal GitHub NO inicia sesión en ella ni equivale a acceso a repositorios privados.
4. Documentar fuera de GitHub: contratos, dominio, registrador DNS, facturación de hosting, proveedores, recuperación del correo, SaaS, custodia legal, licencias, ubicación de respaldos cifrados y clave privada de descifrado. Sin esa información, la recuperación puede ser imposible.
5. Formalizar instrucciones sucesorias con asesoría legal peruana y obligaciones de datos personales y contratos de clientes. Los hijos menores no deben custodiar contraseñas directamente.

### Procedimiento de primera respuesta
1. Verificar quién está legalmente autorizado y suspender cambios peligrosos hasta inventariar. **No detener automáticamente sistemas esenciales ni revocar credenciales sin plan de continuidad**.
2. Obtener lista de repositorios en GitHub y clonar cada uno; validar SHA y ramas/tags protegidos.
3. Verificar el estado de los dominios, n8n, JF CONTROL AI, proveedores de correo y VPS mediante canales autorizados.
4. Localizar el manifiesto privado de copias y comprobar su fecha, tamaño, checksum y cobertura de cada servicio.
5. Restaurar un proyecto en un **entorno aislado**, nunca sobre producción; registrar resultados, pasos y tiempos de recuperación.
6. Rotar credenciales en custodia cuando cambie el responsable, migrar dominios/documentación si corresponde, mantener bitácora y aprobación por cliente.
7. Retomar la producción únicamente tras validar pruebas funcionales, integridad de datos, derechos y permisos de publicación.

### Reglas para cualquier repositorio
- Un proyecto necesita README, arquitectura, dependencias/versiones, build/test/deploy, configuración EXAMPLE (sin secretos), catálogo de datos persistentes, backup/restore, test de humo, licencia, origen de assets externos y responsable.
- Una imagen Docker detectada no prueba que el código fuente esté disponible; un pipeline de backup en verde no prueba una restauración.
- Los códigos fuente y configuraciones con secretos o IP/estructura interna sensibles requieren **repositorios privados** y acceso empresarial; el repositorio público solo contiene documentación no sensible.
- Conservar evidencia de restauración, no solo logs de subida. Para n8n, respaldar base de datos y `N8N_ENCRYPTION_KEY` mediante custodia offline separada.

### Regla de conservación
- Código/documentación → Git + espejo privado/offline.
- Bases de datos/medios → respaldo cifrado `age`, hash SHA-256 verificado con descarga remota y prueba periódica de recuperación.
- Claves privadas → custodia offline del titular/administrador habilitado; en VPS solo recipient público de `age`.
- Retener material temporal un máximo de 48 horas **después de publicación** cuando la obligación contractual permita borrarlo; no eliminar archivos sin copia verificada y prueba de restauración.

### Documentos de referencia
- [Patrimonio digital](PATRIMONIO_DIGITAL_JF_SOLUCIONES.md)
- [Catálogo público](CATALOGO_ACTIVOS_PUBLICO.json)
- [Matriz de recuperación](MATRIZ_RECUPERACION_JF.md)
- [Producción de voz y video](PLAN_QA_VOZ_VIDEO_2026.md)
- [GitHub: continuidad](https://docs.github.com/en/repositories/creating-and-managing-repositories/access-to-repositories)
- [GitHub: autenticación y recuperación](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication-recovery-methods)
