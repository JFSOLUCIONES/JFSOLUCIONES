# NO+ Radar Social — prototipo operativo reproducible

Motor original y portable para monitorear **fuentes públicas autorizadas** y priorizar hallazgos de interés periodístico, sin republicar automáticamente ni afirmar culpabilidad.

## Qué realiza hoy

- Lee un catálogo de fuentes RSS/Atom configuradas por NO+ y enlaces públicos permitidos.
- Descarga feeds RSS/Atom mediante HTTPS, con límite de tamaño y tiempo de respuesta; valida URLs y evita destinos privados (en despliegue, además aplicar controles de red contra SSRF).
- Normaliza títulos, fechas, URL y plataforma; calcula huellas para deduplicación.
- Clasifica coincidencias: política, contrataciones, denuncias, economía, salud, deportes, tecnología y otros.
- Registra en JSON hallazgos **PENDIENTE_VERIFICACION** para revisión en la mesa de redacción.
- Incluye pruebas unitarias con datos sintéticos.

## Instrucciones

Requiere Python 3.11+.

```bash
python3 -m unittest discover -s radar_social/tests -v
python3 radar_social/radar.py --sources radar_social/sources.example.json --output radar_social/hallazgos.json
```

El catálogo de ejemplo no habilita ninguna fuente por defecto para no generar una falsa demostración de cobertura. Configurar fuentes autorizadas, enlaces de medios, blogs o RSS-Bridge en una **copia local**. Los archivos `hallazgos.json` deben permanecer privados si contienen notas editoriales o material de investigación.

## Plataformas

- **Facebook:** Graph API y permisos para páginas/contenido autorizado; no permite minería universal de publicaciones de cualquier perfil o grupo.
- **Instagram:** Graph API para cuentas profesionales/hashtags autorizados y permisos específicos.
- **TikTok:** Research API solo con elegibilidad/aprobación, u otras integraciones permitidas.
- **YouTube, Telegram público, Mastodon, web y blogs:** RSS/Atom, API oficial o RSS-Bridge según los requisitos de cada fuente.
- **changedetection.io:** sirve para cambios en páginas oficiales públicamente accesibles, no para entrar en perfiles privados.

No incluir tokens ni cookies de sesión en `sources.example.json`. No emplear proxies evasivos ni resolver CAPTCHA de forma no autorizada.

### Herramientas upstream (mantener en sus repos)

- https://github.com/RSS-Bridge/rss-bridge
- https://github.com/dgtlmoon/changedetection.io
- https://github.com/apify/crawlee (framework de crawling para sitios accesibles donde las reglas lo permitan)
- https://github.com/microsoft/playwright (navegación y pruebas permitidas, no acceso indiscriminado a redes)
- https://github.com/yt-dlp/yt-dlp (descargas únicamente cuando la autorización y los derechos lo permitan)

Antes de desplegar cualquiera, revisar licencia, mantenibilidad y restricciones de cada plataforma.
