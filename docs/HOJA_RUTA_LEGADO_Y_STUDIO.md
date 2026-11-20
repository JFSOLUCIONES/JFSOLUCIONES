# Hoja de ruta activa — Legado digital y JF Voice & Video Studio

Actualizado: 2026-11-20. Documento público sin contraseñas ni datos de clientes.
GitHub Issues está deshabilitado en el repositorio actual (respuesta 410); este documento actúa como tablero de tareas hasta contar con un mecanismo de seguimiento habilitado.

## Prioridad 0 — Continuidad para herederos
- [x] Crear guía pública de legado y recuperación.
- [x] Inventariar por familias 110 workflows n8n (43 activos / 67 inactivos).
- [x] Ampliar catálogo público de 20 activos sin datos secretos.
- [x] Ejecutar CI de integridad del catálogo (N° 44800160841).
- [ ] Crear repositorio(s) **privados**, propiedad empresarial, con dos administradores y 2FA.
- [ ] Designar custodio legal adulto y suplente para continuidad; instrucción jurídica separada y privada.
- [ ] Habilitar recuperación 2FA/GitHub, correo, dominio y proveedor VPS en sobre offline seguro.
- [ ] Incorporar cada proyecto fuente real a un repositorio privado con pruebas de despliegue.
- [ ] Exportar n8n/BD/medios cifrados a backup remoto y espejo offline con recuperación comprobada.
- [ ] Ejecutar al menos una restauración completa aislada por tipo de servicio.

## Prioridad 1 — JF Voice & Video Studio
- [x] TTS Kokoro real probado en n8n (ejecución 1256).
- [x] Bloqueo de guion sin aprobación validado (n8n ejecución 1251).
- [x] Prototipo Chatterbox y controles documentados en PR #4.
- [x] Render y subtítulos MP4 de laboratorio demostrados por GitHub Actions N° 44800714607.
- [ ] Comprobar titularidad/licencia de la voz sintética del video de referencia.
- [ ] Verificar GPU/CPU y autorización de administración para despliegue de staging en VPS2.
- [ ] Instalar y comparar Chatterbox Multilingual V3, OpenVoice V2 y CosyVoice 3 sin afectar producción.
- [ ] Activar biblioteca privada de voces con control de licencias y acceso por cliente.
- [ ] Separación de voz/música Demucs y transcripción automática faster-whisper/WhisperX.
- [ ] Video real: ensamblaje, subtítulos, mezcla, QA, y posible lip-sync solo autorizado.
- [ ] Conectar interfaz autenticada de ai.jfconnect.online a la cola y motor probado.
- [ ] Documentar pruebas de recuperación del worker y repositorio privado de modelos/perfiles.
- [ ] Preparar demostración profesional para Lurín con autorización y rotulación clara de IA.

## Prioridad 2 — Catálogo total
- [ ] JF CONNECT AI, JF STUDIO, Gestión 360, JF CONTROL AI y API.
- [ ] JF SPORTS EDGE, JF CHINA, JF SALES/COMERCIAL, JF META y JF Academy.
- [ ] JF DIGITAL, JF Elecciones, JF Créditos360, Postiz, JF STREAM, E4F/E4G.
- [ ] CERTSE FAP, AM-MEDIC, NO+ y demás clientes, bajo permisos y contratos por cliente.
- [ ] Registrar fecha, responsable, repositorio, commit, backup y RESTORE_OK en Gestión 360.

## Definición de terminado para un activo
No se marca HEREDABLE ni RESTAURABLE hasta comprobar:
1. Código fuente íntegro disponible en repositorio seguro y construible desde cero.
2. Dependencias, infraestructura y variables documentadas sin revelar valores secretos.
3. Copia consistente de los datos y medios, cifrada y con hashes comprobados.
4. Claves de recuperación bajo control de custodio autorizado fuera del repositorio.
5. Ensayo aislado de recuperación, verificación funcional, acceso seguro y tiempo anotado.

No fusionar código experimental ni reiniciar servicios sin revisión y plan de retorno.
