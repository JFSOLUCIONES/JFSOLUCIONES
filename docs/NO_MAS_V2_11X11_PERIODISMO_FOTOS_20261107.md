# NO+ V2 | Política editorial, imágenes y dimensiones — 07/11/2026

## Auditoría local de los seis PDF aportados
- El piloto NO+ 08/11/2026 tiene 12 páginas **A4 210×297 mm** y **cero fotografías incrustadas en páginas 2–12**; son notas breves de estilo tarjeta con fuentes impresas.
- El compositor principal Windows, según el código de revisión `components/EditorialWorkspace.tsx`, usa `@page{size:11in 11in;margin:0}`, es decir **279,4×279,4 mm**.
- La pantalla de portada `app/editorial/portada-ia/page.tsx` usa aún **A4**: corregir para coincidir 11×11.
- El criterio `score()` de portada se basa en palabras clave: no es investigación IA ni selección editorial validada.
- La portada consulta la API PostgreSQL; borradores solo existentes en el navegador pueden quedar fuera.
- El validador exige 180 palabras, evidencia, fuentes internas, fotografía, permiso de uso y crédito.
- Referencias de estilo estudiadas: *El Dato*, *Región 3*, *Diario Lo Último*, *Diario La Verdad* y *Panorama* de noviembre 2026. Adaptar variedad visual, fotos y reportajes; evitar copiar estilos o contenidos exactamente.

## Regla de producción vigente
- **36 piezas únicas en 11 páginas interiores**, 3 páginas con 4 piezas y 8 páginas con 3 piezas. La portada destaca, pero no duplica las historias como si fueran nuevas.
- Dar trato periodístico a cada historia: hechos, contexto, cifras, actores, contraargumentos/descargos, documentos, hipótesis abiertas, explicación útil y perspectivas verificables.
- El periodista IA simula el criterio de un investigador profesional veterano; no declara experiencia personal ficticia.
- Redactar de forma original, crítica, incisiva; usar humor o ironía únicamente sin alterar o inventar hechos.
- Publicar fotografías de hechos auténticos con derechos comprobados; fotos en PDF de competidores NO se presumen reutilizables. Marcar claramente cualquier ilustración que no documente el hecho.
- **Mantener URLs y fichas de fuentes en el expediente interno**, eliminando listas de fuentes, recuadros `ABRIR DOCUMENTO` y enlaces a medios competidores del PDF, flyers y copys. Conservar atribuciones sustantivas dentro del texto y los créditos fotográficos exigidos por permisos o licencias.
- El principio «70% visual, 30% texto» se reserva a flyers sociales; las páginas interiores periodísticas necesitan texto desarrollado y fotografías.
- La portada la decide un director editorial según trascendencia pública, actualidad, impacto, rigor, originalidad y fuerza visual verificable, sobre reportajes concluidos; requiere aprobación.
- Nueve publicaciones diarias: **3 Lambayeque, 3 Perú y 3 Mundo**, reportajes originales con adaptación para Facebook/Instagram y flyer 4:5, previa aprobación.
- PDF de 12 páginas y nueve publicaciones deben versionarse por edición y aprobarse separadamente; nunca publicar solo porque un artículo pasó validación.
- Para pruebas WhatsApp: exclusivamente destinatarios autorizados, respetando ventana de servicio o plantillas aprobadas según Meta.

## Integración del PDF al editor Windows
Existe un ZIP de actualización **local** (se entrega fuera de GitHub público) para instalar biblioteca PDF privada con ruta `/editorial/ediciones`. Requiere sesión `isAdmin`, no publica el PDF, no toca PostgreSQL, ajusta dos reglas de formato A4 de la portada e incorpora el enlace en el panel. Se exige probarlo en la PC Windows antes de declararlo instalado. El piloto viejo permanece A4 y no está aprobado.

## Siguiente implementación
El agente investigador + verificadores deben alimentar expedientes estructurados, la curaduría fotográfica necesita licencia y validación, la maquetación debe usar 11×11 con previsualización, y la publicación se bloquea hasta aprobación y revisión. No simular que todo eso ya opera.
