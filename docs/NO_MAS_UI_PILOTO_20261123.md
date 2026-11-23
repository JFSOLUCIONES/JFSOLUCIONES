# NO+ | Piloto de interfaz de alto impacto (23/11/2026)

**Estado:** PROTOTIPO LOCAL, PENDIENTE DE REVISIÓN. No desplegado. La página de producción está administrada fuera de este repositorio y su código no está aquí verificado.

## Qué se agregó

- **prototipos/no-mas-ui-preview.html**: concepto responsive autónomo, sin dependencias de red; marca NO+ en negro, rojo y blanco; portada, secciones de muestra y navegación para celular.
- **test/no-mas-ui.test.js**: controles estructurales de contenido ficticio identificado, accesibilidad básica, diseño adaptable y ausencia de recursos remotos.
- Documento de alcance y criterios de aceptación.

No hay un CMS conectado, noticias reales ni cambios en base de datos, servidor, n8n o el sitio público.

## Decisiones de diseño

- Jerarquía editorial marcada: titular con tipografía serif, interfaz sans, elementos secundarios de alto contraste.
- Reducción de movimiento, foco visible, enlace para saltar al contenido, botones etiquetados y menú desplegable mediante teclado.
- Composición abstracta y marcadores de posición sin fotografías documentales; se prohíbe confundir la muestra con noticias reales.
- Diseño móvil: composición de una columna en pantallas estrechas.
- Sin librerías ni servicios externos para no crear dependencias del frontend original.

## Herramientas consideradas para siguientes etapas (NO instaladas)

| Proyecto | Uso potencial | Condición |
|---|---|---|
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | Guía y razonamiento visual asistido | Revisar scripts/versión/licencia antes de usar |
| https://github.com/shadcn-ui/ui | Componentes si el frontend elegido es React | No forzar migración de CMS |
| https://github.com/storybookjs/storybook | Biblioteca de componentes compartidos | Valorar costo de CI |
| https://github.com/microsoft/playwright | Pruebas de navegación y capturas responsivas | Ejecutar en staging |
| https://github.com/dequelabs/axe-core | Auditorías de accesibilidad | Mantener revisión manual |

## Revisión obligatoria antes de integrar en NO+ real

1. Obtener código o plantilla real de producción de forma autorizada y mantener respaldo recuperable.
2. Inventariar CMS, rutas, funcionalidades, plugins, fuentes de datos y tema actual.
3. Revisar en PC/tablet/móvil, contraste WCAG, orden de tabulación y controles con lector de pantalla.
4. Medir Lighthouse (LCP, CLS, INP y accesibilidad) y hacer capturas visuales antes/después.
5. Integrar una sola plantilla en *staging*, preservando URL, artículos, medios, SEO, cookies y analítica.
6. Registrar commit, pruebas y procedimiento exacto de rollback; aprobación humana antes de publicar.

## Ejecución de las pruebas locales

Con Node.js 20+:

~~~bash
npm test
~~~

Estas pruebas estáticas **no certifican** accesibilidad, visualización o integración real en un navegador. Falta evaluación con Playwright/axe/Lighthouse y aprobación editorial.

## Fronteras y seguridad

- El repositorio público contiene exclusivamente NO+; no poner aquí datos internos, sistemas de clientes, backups o infraestructura privada.
- El agente de diseño genera propuestas y reportes. No recibe permisos root abiertos ni capacidad de publicar directamente.
- Es responsabilidad del titular decidir y aprobar la publicación; no se habilita despliegue automático.
