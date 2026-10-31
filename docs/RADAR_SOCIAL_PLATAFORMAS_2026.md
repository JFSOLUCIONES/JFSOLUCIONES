# NO+ Radar Social | Cobertura pública sin atajos inseguros

Investigación: 31 de octubre de 2026.

## Conclusión

No existe un repositorio que otorgue por sí mismo acceso universal, autorizado, permanente y confiable a publicaciones de Facebook, Instagram y TikTok. Muchos scrapers de perfiles fallan, vulneran condiciones de plataformas o exponen credenciales. NO+ combinará APIs oficiales donde obtengamos permisos, fuentes públicas accesibles, RSS-Bridge y observación manual verificada.

## Repositorios externos investigados

| Proyecto | GitHub | Función | Decisión |
|---|---|---|---|
| RSS-Bridge | https://github.com/RSS-Bridge/rss-bridge | RSS de servicios públicos compatibles (incluye puentes de TikTok y Telegram) | Probar en staging con fuentes autorizadas y límites |
| changedetection.io | https://github.com/dgtlmoon/changedetection.io | Avisos cuando cambian páginas accesibles | Considerar para portales oficiales, licitaciones y comunicados |
| Crawlee | https://github.com/apify/crawlee | Framework configurable de crawling | Solo sitios donde los términos y permisos lo permitan |
| Playwright | https://github.com/microsoft/playwright | Navegación automatizada y pruebas | Útil para webs públicas autorizadas, no para acceder a perfiles privados |
| yt-dlp | https://github.com/yt-dlp/yt-dlp | Procesar enlaces de video cuando exista autorización | No usar para descargar material ajeno de forma masiva |
| snscrape | https://github.com/JustAnotherArchivist/snscrape | Referencia histórica de scraping social | No depender de él para producción; ver mantenimiento y políticas |

## Accesos permitidos y limitaciones

- Facebook Graph: publicar/leer contenido de nuestras páginas autorizadas; para páginas públicas de terceros se requieren permisos/features correspondientes, no acceso libre a todo Facebook.
- Instagram Graph: funciones de cuentas profesionales y búsqueda de hashtags según permisos, aprobación y límites; no acceso genérico a perfiles privados o personales.
- TikTok Research API: aprobación restringida por elegibilidad institucional y geográfica; NO+ Perú no debe asumir acceso.
- Telegram público, YouTube, blogs, páginas municipales, portal transparencia, SEACE, medios y publicaciones RSS: mejor camino inicial para alertas documentables.
- La persona periodista puede aportar manualmente un enlace de post público; NO+ registra URL, fecha, extracto y evidencia lícita, luego corrobora con documentos independientes.
- Nunca automatizar inicio de sesión en cuentas ajenas, ignorar bloqueos, resolver CAPTCHA para evadir controles ni extraer datos de grupos privados.

## Plan de puesta en marcha

1. Probar `radar_social/radar.py` y pruebas unitarias en GitHub.
2. Agregar catálogo privado de fuentes públicas de Lambayeque (medios, organismos, páginas propias y enlaces permitidos).
3. Conectar resultados de hallazgo con expediente privado en JF Editorial y workflow n8n, con deduplicación persistente y aprobación manual.
4. Validar APIs oficiales Facebook/Instagram para cuentas gestionadas y permisos aprobados.
5. Integrar RSS-Bridge y changedetection.io solo si RAM, puertos y términos lo permiten.
6. Crear tablero: nuevas señales, fuentes coincidentes, documentos de respaldo, grado de certeza, prioridad y responsables.
7. Mantener fuentes de trabajo internas protegidas; publicar atribuciones cuando legal, ética y periodísticamente corresponda.

## Estado

**Implementado:** código del normalizador RSS/Atom y tests.
**No implementado:** conexión real a APIs Facebook/Instagram/TikTok, feed público de producción, extracción masiva o monitoreo periódico activo.
**No publicados:** hallazgos ni alertas automáticas.
