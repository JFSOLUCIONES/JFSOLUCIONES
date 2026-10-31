# NO+ | Estructura editorial definitiva — sábado 31 de octubre de 2026

## Regla diaria

**9 noticias principales:** 3 de Lambayeque, 3 del Perú, 3 internacionales. Cada una requiere reportaje desarrollado para la edición premium y un resumen propio, independiente, para redes. Publicar el resumen solo tras verificar el reportaje y aprobarlo. Redes generan tráfico a `https://periodiconomas.space` y ofrecen suscripción de **S/ 10 / 30 días**, claramente marcada como prelanzamiento hasta activar el cobro.

## Secciones permanentes de cada edición

- **Lambayeque y actualidad política**: decisiones de gobierno regional, municipalidades, Consejo Regional, obras, Contraloría, MEF/SEACE y políticas públicas.
- **Fiscalización y corrupción**: contratos, gasto público, sentencias y diligencias; riesgos documentados ≠ culpabilidad.
- **Política nacional**: Congreso, Ejecutivo, justicia y elecciones sin campañas encubiertas.
- **Salud**: prevención, servicios y ciencia con fuentes sanitarias.
- **Tecnología**: IA, ciberseguridad, conectividad y transformación digital.
- **Economía**: empleo, comercio, precios, producción y emprendimiento.
- **Deportes**: Lambayeque y Perú primero; calendario y resultados confirmados, nunca inventados.
- **Humor / caricatura editorial**: sátira sobre políticas y situaciones verificadas, claramente identificada como opinión o humor; sin falsos testimonios ni imputaciones.
- **Cultura y comunidad**: vida local, música, patrimonio y entrevistas.

## Mapa de 8 páginas (edición diaria)

1. Portada principal: titular de coyuntura Lambayeque, índice 3/3/3, llamado a web y premium.
2. Lambayeque 1: investigación principal (fiscalización, salud, política, educación, según importancia).
3. Lambayeque 2 y 3: dos reportajes completos + recuadro de coyuntura política.
4. Perú 1 y 2: dos reportajes completos, contexto político/económico.
5. Perú 3 + deportes: reportaje nacional desarrollado + actualidad deportiva comprobada.
6. Mundo 1 y 2: dos reportajes internacionales, salud y política.
7. Mundo 3 + tecnología/economía: tercer reportaje internacional y análisis tecnológico/económico.
8. Editorial/opinión + humor + agenda cultural + correcciones + contactos + suscripción y publicidad.

Los apartados de deportes, humor y otros segmentos **no reemplazan** las nueve noticias: son contenidos adicionales. Si no hay información comprobada suficiente, mostrar 'En seguimiento' en lugar de inventar un titular.

## Sistema visual

- Identidad NO+ y logo original cuando se aporte el recurso autorizado; mientras tanto mostrar marca tipográfica provisional, sin declararla logotipo oficial.
- Flyers verticales 4:5, **máximo 30 % de superficie de texto**; la regla NO se aplica a las páginas completas del periódico, donde la legibilidad de reportajes exige texto.
- Firma y fecha de edición en todas las páginas; versión digital accesible en móvil.
- Llamado a la acción en redes: «Lee el informe completo en periodiconomas.space. NO+ Premium: S/ 10 por 30 días, próximamente».
- Contacto obligatorio: **+51 906 605 712**; sitio **periodiconomas.space**.

## Cadena de trabajo

1. Radar de temas / búsqueda documental.
2. Verificación de al menos una fuente primaria cuando exista, contraste independiente y fechas.
3. Expediente privado con trazabilidad; atribución pública cuando sea necesaria.
4. Reportaje completo con hallazgos, contexto, límites de certeza y preguntas de fiscalización.
5. Maquetación de PDF 8 páginas.
6. 9 resúmenes para redes + flyer/imagen autorizada.
7. Revisión humana; publicación manual hasta completar automatización, sin cobrar membresías prematuramente.

## Modelo de registro

Cada noticia contiene `alcance:local|nacional|internacional`, `secciones:string[]`, `titulo`, `fecha_hecho`, `fuentes_internas`, `datos_confirmados`, `pendientes`, `reportaje`, `resumen_social`, `aprobacion_editorial`, `autopublicacion:false`.

## Tareas pendientes

- Integrar CMS/web de suscripciones y URL de cada edición; dominio apuntando al VPS no implica portal en producción.
- Acceso premium, registro, pago validado, entrega WhatsApp con opt-in y plantillas aprobadas.
- Logo original y autorizaciones de fotografías.
- Generación PDF definitiva y pruebas móviles, impresión y correcciones.
