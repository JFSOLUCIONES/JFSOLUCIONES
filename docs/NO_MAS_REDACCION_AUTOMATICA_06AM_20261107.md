# NO+ | Redacción automática y distribución 06:00 (Perú)

**Estado:** arquitectura de producción y primera etapa de radar desplegada. Las etapas 2–6 no están desplegadas. Corte: 2026-11-07.

## Objetivo editorial
Preparar diariamente una edición de 12 páginas, hasta 36 noticias verificadas, portada de alto impacto, artículos de redacción propia y distribución del enlace/portada a lectores suscritos por WhatsApp **a las 06:00 America/Lima**, siempre que exista una edición autorizada.

## Lo que YA está instalado y probado
- n8n: `NO+ | Radar 02:30 Lima | 36 espacios en borrador`, workflow **wjz1hDGVR8KjcICF**.
- Flujo activado: Schedule Trigger 02:30 `America/Lima`; 5 RSS (región, país, mundo, deportes, cultura); parseo, deduplicación simple, cola de 12×3. No contiene ningún nodo de publicación ni WhatsApp.
- Prueba manual con 336 entradas RSS, 333 candidatos deduplicados con heurística básica y 36 casillas con candidatos. Estos valores NO prueban corroboración, redacción ni clasificaciones temáticas precisas.
- Tabla privada n8n `NO_MAS_RADAR_CANDIDATOS_DIARIOS` id `PWXQ9SBXaBdEEMA9` con 36 filas guardadas en prueba; estado `DETECTADA` y banderas `source_verified=false`, `approved=false`. UPSERT por `edition_date` y `slot_id`.
- Suite local de edición Next.js/CKEditor: `C:\JF_SOLUCIONES\NO_MAS_EDITORIAL`; PostgreSQL Docker local 127.0.0.1:55432, contenedor `no-editorial-pg`, 3 expedientes en PostgreSQL y 15 mostrados en navegador. Falta resguardar/exportar los 15 de la UI. No conectar n8n con `localhost` del VPS: es otro equipo.
- `periodiconomas.space` devuelve HTTP 200, pero no hay prueba de despliegue del editor Next.js local.

## Flujo objetivo
1. **02:30 Radar**: RSS, fuentes públicas, enlaces originales, fechas del hecho/publicación, 72h con rotulado; no considerar Google News una corroboración primaria.
2. **03:00 Verificador**: mínimo dos fuentes independientes o documento primario, identificación de contradicciones, fechas, hechos, afirmaciones, descargos y riesgos legales.
3. **03:45 Redactor IA**: reportaje ORIGINAL escrito con voz NO+: lenguaje directo, ganchos atractivos, contexto local y humor inteligente; jamás inventar datos ni copiar el texto fuente. Estatus BORRADOR.
4. **04:30 Arte**: foto original o licenciada, créditos, logo NO+ original, portada premium, láminas 4:5, edición PDF 12 páginas y versión web. No recrear un acontecimiento sin señalizar la simulación.
5. **05:30 Auditor**: revisión factual y de derechos, fotos, menores, correcciones, derecho de réplica y aprobación editorial **independiente** de quien redactó. Investigación sensible necesita revisión humana de forma obligatoria.
6. **06:00 Distribuidor**: exigir edición íntegra y aprobada, fuentes trazadas, links públicos correctos, lectores opt-in para recibir ediciones, bajas operativas, plantilla Meta aprobada, idempotencia por `edition_id+subscriber_id`, límites de velocidad, registro de respuestas API y manejo de fallas.

**Regla:** si falta autorización o consentimientos: NO ENVIAR; permitir boletín reducido previamente aprobado o registrar bloqueo, nunca publicar noticias ficticias para alcanzar 36.

## Gates de producción
- `PROHIBIDO`: titular sin fuente verificable, fecha engañosa, denuncia como hecho probado, fotos sin derechos, atribución incompleta, destinatario sin opt-in de periódico.
- El estado `aprobado` del editor local actualmente no representa por sí mismo autorización final independiente.
- La tabla `NO_MAS_WHATSAPP_CONTACTOS` contiene hash/consentimiento genérico; ello no demuestra opt-in específico a boletín NO+ ni identifica necesariamente números entregables.
- Meta requiere opt-in y respeta bajas; fuera de la ventana de 24 h, usar plantillas autorizadas; los medios principalmente noticiosos deben registrarse como News Page en Facebook. Revisar: https://whatsappbusiness.com/policy/

## Pendientes técnicos
1. Copia local del JSON con los 15 expedientes (Ctrl+J después de pulsar Exportar expediente, verificar contadores antes de toda sincronización).
2. Migrar el editor a un servicio alcanzable por el VPS, usando conexión privada y respaldo/restauración probada, con migraciones de datos y protección de secretos.
3. Roles y 2 personas para aprobar; idempotencia y versionado; bloqueo de sincronizaciones masivas; sistema de fuentes y dictámenes.
4. Servicio de investigación/redacción IA con navegación real y trazas; control de coste y lotes.
5. Servicio de diagramación profesional y activos visuales con licencia.
6. Registro de consentimiento por categoría NOTICIAS_DIARIAS, plantilla Meta, número autorizado y validación del estado de Meta; pruebas con números propios antes de cualquier envío.
7. Endpoints API publicados, configuración de dominio, reconciliación de entregas y alertas de falla.

## Reglas de estilo NO+
Informativo, investigador, ágil, incisivo y a veces pícaro. La «pimienta y ají» se aplica al titular y narración **sin cambiar hechos, añadir insinuaciones infundadas o crear difamación**. Distinguir noticia, crónica, opinión, humor editorial y publicidad.

El radar no publica: produce candidatos. Hasta que las capas de verificación y salida estén instaladas, ningún lector debe recibir mensajes automáticos por este sistema.
