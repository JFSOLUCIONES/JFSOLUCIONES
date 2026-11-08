# NO+ | Operación diaria manual y automática · 8 de noviembre de 2026

**No se creó una nueva aplicación.** Se mejoraron los flujos existentes de NO+ en JF CONNECT n8n y el esquema del repositorio de desarrollo. Sin envío externo ni publicación.

## Funciones realmente operativas
- Radar: flujo `wjz1hDGVR8KjcICF` (https://n8n.jfconnect.online/workflow/wjz1hDGVR8KjcICF).
  - Botón `INICIAR EDICION MANUAL DE MANANA`: al pulsarlo, busca candidatos para la edición del día siguiente en America/Lima.
  - Automático `00:10`: inicia/actualiza la edición del día en Lima, no requiere intervención.
  - Automático `02:30`: vuelve a consultar y refrescar posibles novedades, conservando registros previamente verificados o aprobados.
  - Las fuentes se filtran por fecha de publicación desde medianoche del día anterior al ejemplar hasta el instante de captura. La fecha **del hecho** sigue requiriendo investigación independiente. Detección RSS no equivale a verificación.
  - Portada independiente; 36 casillas de noticias en 11 páginas interiores: cuatro casillas en páginas 2, 3, 4; tres en cada página 5–12.
  - Estado de salida: bloqueado para publicación, edición preliminar y sin envío WhatsApp.
  - Prueba manual del 8/11: ejecución n8n **217**, `MANUAL_ANTICIPADO`, fecha editorial `2026-11-09`, 36 casillas guardadas. Si faltan temas de calidad permanecen vacíos.
  - Almacén: tabla `NO_MAS_RADAR_CANDIDATOS_DIARIOS`, datos pendientes de revisar.

- Redes: flujo `N05yU1jn4GUTtVqc` (https://n8n.jfconnect.online/workflow/N05yU1jn4GUTtVqc).
  - Botón `INICIAR PRESELECCION MANUAL DE MANANA`; automático `04:00` Lima.
  - Filtro de noticias meteorológicas rutinarias, títulos triviales y duplicación semántica aproximada. Priorización orientativa por interés público, no sustituye contrastación.
  - Propuesta objetivo 3 Lambayeque, 3 Perú, 3 internacional. Si no hay nueve temas diferenciados, reportar menos. **No son aún nueve redacciones propias ni publicaciones**.
  - Conserva propuestas con estado aprobado/publicado; no crea mensajes Meta ni publicaciones.
  - Prueba manual del 8/11: ejecución **219**, seis candidatos distintos seleccionados para `2026-11-09`. Se omitieron duplicados de un nombramiento diplomático y de un hecho en Cracovia.
  - Almacén: tabla `NO_MAS_REDES_9_PROPUESTAS`.

## Cómo funciona la orden manual
La dirección abre el radar, pulsa **Execute workflow** (Manual Trigger) y el motor prepara la edición del día siguiente; luego puede ejecutar anticipadamente el flujo de nueve propuestas. Las actualizaciones posteriores de madrugada pueden aportar novedades a casillas todavía no revisadas.

**No está habilitado un mensaje libre en WhatsApp como orden de arranque.** Hacerlo requerirá webhook autenticado y autorización por rol; tampoco hay garantía de que un clic de ejecución manual pueda elegir una fecha diferente de mañana, salvo modificación posterior del nodo de entrada.

## Etapas de producción todavía NO instaladas de extremo a extremo
1. **Investigador con Firecrawl**: captura del artículo original, documentos primarios, dos fuentes o documento primario, fechas hecho/publicación; almacén de fuentes privado. La cuenta Firecrawl está conectada a ChatGPT; **NO está configurada todavía como credencial API en n8n**.
2. **Agentes periodísticos**: reutilizar patrones Searcher → Writer → Editor de Awesome LLM Apps, intercalando verificador factual, revisor legal y derecho a réplica. No ejecutar el ejemplo Streamlit como CMS paralelo.
3. **Redactor NO+**: borrador original, datos y citas trazados a evidencia; no copiar la prosa de los medios; titular incisivo solo cuando el fondo esté probado.
4. **Biblioteca de fotos**: original propio u oficial con permiso o licencia documentada; detectar repetición, verificar ubicación/fecha/identidad, créditos obligatorios.
5. **JF STUDIO / diagramador**: PDF 12×11 pulgadas, portada elegida tras investigar, imágenes por nota y tipografía legible; nueve flyers 4:5.
6. **NO+ JF EDITORIAL → periodiconomas.space**: sincronización protegida de los expedientes del editor Windows al backend con control de versiones, roles y publicación.
7. **Salida 06:00**: permitir solo ejemplar autorizado, fotos con derechos, consentimientos WhatsApp específicos, plantilla Meta aprobada cuando corresponda y comprobación de entrega. Por ahora **no está desplegada**.

## Resultado de QA del PDF V5 del 08/11/2026 (prueba local)
- 12 páginas de 792×792 pt (11×11 pulgadas).
- 44 imágenes incrustadas únicas por hash exacto, sin duplicaciones exactas detectadas. Esto no descarta similitud temática.
- No se detectaron errores estructurales de tamaño o notación N.°.
- Se detectó texto mínimo de 7–7,3 pt y la marca `MAQUETA EN REVISIÓN | NO AUTORIZADA PARA DISTRIBUCIÓN`. **No es una copia pública**.
- La evaluación humana debe revisar justificación real, legibilidad en pantalla, contenido, fotografías y riesgos antes de liberar.

## Objetivo de aceptación
Conservar la automatización aunque el director no envíe orden. Una orden manual debe producir la edición de mañana y no provocar borrado de lo investigado. La entrega automática final solo existe cuando **el expediente con fuentes, las fotos, el PDF, el portal y la salida Meta** hayan pasado pruebas reales en ese orden.
