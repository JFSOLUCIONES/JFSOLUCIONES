# NO+ — Edición digital de 12 páginas y 36 noticias | Plan editorial v2

**Fecha:** 7 de noviembre de 2026. **Estado:** DISEÑO EN REVISIÓN / NO DESPLEGADO.

Este documento define una ampliación del prototipo editorial existente. No altera el sitio público, la base de datos ni los workflows de WhatsApp. No contiene claves, datos de denunciantes ni expedientes privados.

## Distribución de la edición

| Página | Sección | Noticias previstas |
| --- | --- | ---: |
| 1 | Portada regional | 3 |
| 2 | Lambayeque: política local | 3 |
| 3 | Lambayeque: fiscalización y obras | 3 |
| 4 | Lambayeque: sociedad, educación y seguridad | 3 |
| 5 | Lambayeque: economía y salud | 3 |
| 6 | Perú: política nacional | 3 |
| 7 | Perú: justicia y economía | 3 |
| 8 | Perú: actualidad | 3 |
| 9 | Internacional: geopolítica | 3 |
| 10 | Internacional: sociedad y economía | 3 |
| 11 | Deportes de Lambayeque y nacionales | 3 |
| 12 | Cultura, tecnología y servicios | 3 |
| **TOTAL** | **12 páginas** | **36** |

## Estado de cada pieza

DETECTADA -> INVESTIGACIÓN -> CONTRASTE -> BORRADOR -> AUDITORÍA -> APROBADA -> MAQUETADA -> PROGRAMADA -> PUBLICADA -> RECTIFICADA.

La clasificación automatizada y los modelos de IA solo generan propuestas. Las investigaciones sensibles necesitan un editor responsable y derecho de respuesta cuando corresponda. Una noticia jamás se considera validada exclusivamente por obtener una respuesta de un modelo.

## Datos mínimos

Cada noticia requiere identificador, página, sección, título, entradilla, texto completo, fecha de hecho, fecha de publicación, fuentes, registro de verificación, situación del descargo, fotografía autorizada y crédito, revisor, estado de aprobación y URL de publicación (solo después de publicar). Las fuentes internas sensibles permanecen fuera de GitHub público.

## Maquetación y calidad

- Diseño editorial de 12 páginas con títulos legibles, columnas, sumillas, folios, créditos e imágenes periodísticas reales.
- Flyer promocional individual 4:5 con la identidad oficial de NO+, máximo 30 % de superficie textual, fotografía auténtica, y archivo final con dimensiones reales comprobadas.
- El límite 70/30 de los flyers no se aplica a las páginas interiores del periódico.
- Revisión de 12 páginas renderizadas antes de generar PDF final.
- Etiqueta BORRADOR mientras falten fuentes, derechos, imágenes, aprobación editorial o revisión jurídica.
- Ningún script del proyecto publica automáticamente desde esta rama.

## Migración por fases, sin alterar producción

1. Rescatar y revisar el editor local NO+ y sus respaldos verificables.
2. Auditar recursos del VPS y capacidad para una aplicación editorial aislada.
3. Recuperar el radar y el clasificador existentes en n8n, sin duplicar webhooks.
4. Incorporar 36 fichas con investigación comprobable, contenido y archivos visuales autorizados.
5. Probar HTML/PDF y adaptación móvil, incluidos controles automáticos y aprobación humana.
6. Solo entonces conectar publicación web y redes con permisos e historial de publicación.

**Advertencia:** Esta rama contiene un plan público, sin secretos. Las configuraciones operativas multiempresa y expedientes de NO+ deben permanecer en un repositorio privado y sistemas de almacenamiento controlado.
