# NO+ | Auditoría de edición y sistema de diagramación

Fecha: 31/10/2026. Documento auditado: `NO_MAS_EDICION_12_PAGINAS_REVISION_EDITORIAL_31_10_2026(1).pdf`.

## Resultado objetivo

- 12 páginas A4: **sí**.
- PDF: 149306 bytes (~146 KB).
- Aproximadamente 2630 palabras extraídas.
- Solo 1 imagen incrustada de 512×512 píxeles: **no son fotografías periodísticas**.
- Interiores casi exclusivamente con bloques de texto breve y mucho espacio vacío.
- Piezas construidas principalmente como ensayo/reseña, no como edición diaria competitiva.

**Dictamen: NO APTO PARA DISTRIBUCIÓN PREMIUM NI IMPRENTA.**

## Herramientas candidatas

1. **The Triplicate / template_newspaper**: https://github.com/docxology/template_newspaper — modelo MIT de 12 páginas tabloid; contenido YAML, columnas fluidas, jerarquía de portada, imágenes y anuncios. Evaluar compatibilidad, seguridad y licencias antes de reutilizar.
2. **Paged.js**: https://github.com/pagedjs/pagedjs y https://github.com/pagedjs/pagedjs-cli — paginación basada en CSS Paged Media, exportación PDF automatizable.
3. **Scribus**: https://www.scribus.net/ — composición editorial y revisión final de imprenta; evitar repositorios espejo como fuente principal de descargas.
4. **WeasyPrint**: https://github.com/Kozea/WeasyPrint — HTML/CSS → PDF, alternativa para plantillas propias y pruebas.

No copiar reportajes, fotografías ni identidades de la competencia. Mantener dependencias oficiales en repositorios de origen, fijando versiones.

## Diseño aprobado como objetivo (aún no implementado)

- 12 páginas con una portada real, 2-4 columnas por página, 2-5 piezas por página según relevancia.
- Al menos siete páginas con material gráfico documental o gráfico propio no engañoso; no falsificar fotografías.
- Tipografía jerarquizada: nombre del medio, titular, bajada, entradilla, cuerpo, citas, datos, pie fotográfico y folio.
- Reportajes locales profundos sobre Lambayeque; nacional/internacional; salud, deportes, servicios y humor editorial con identificación.
- Documentación privada: fuente, fecha, licencia de imagen, periodista, revisión, derecho de respuesta y corrección.
- Edición impresa con sangrado, márgenes, fuentes incrustadas, resolución y perfil de color conforme a imprenta; validar separadamente.
- Diseño responsive para PDF móvil adicional; impresión A4/tabloide tras elegir formato definitivo.

## Gate obligatorio antes de mostrar «listo»

1. Calidad automática: `python tools/pdf_quality_gate.py EDICION.pdf`.
2. Revisión de 12 capturas a tamaño real, sin recortes, páginas vacías o titulares desbordados.
3. Revisión de autenticidad, procedencia y derechos de **cada fotografía**; sin imágenes de IA presentadas como evidencia.
4. Verificación de actualidad de todas las afirmaciones y créditos/atribuciones necesarios.
5. Aprobación humana editorial y legal cuando aplique.
6. Solo después: marca «EDICIÓN APROBADA», envío a lectores y, cuando proceda, cobro.

El programa de calidad es una **barrera mínima técnica**, no un certificador periodístico. La versión anterior debe permanecer etiquetada como borrador.
