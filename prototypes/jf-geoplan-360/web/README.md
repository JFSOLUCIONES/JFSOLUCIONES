# JF GeoPlan 360 — laboratorio visual v0.2 (21-11-2026)

Abre `index.html` en un navegador moderno. La interfaz está desarrollada sin librerías externas y funciona localmente con `app.mjs`, `logic.mjs` y `styles.css`.

## Lo que funciona
- Navegación por módulos (proyectos, planos, suelos, presupuestos, proveedores, clientes, enlaces MASTER/cliente, legado).
- Implantación geométrica de dos canchas de fútbol 6 o 7 en un lote rectangular simulado, con validación de encaje y esquema SVG.
- Entrada de coordenadas planas métricas CSV, cálculo de perímetro/área y exportación básica a DXF R12.
- Escenarios de ingresos/costos y recuperación simple.
- Directorio de proveedores con páginas externas (precios publicados, no cotizaciones).
- Lista de comprobación de suelo, permisos, roles y recuperación; plantillas de RFQ.
- Enlaces conocidos que cumplen un validador de URL; los accesos sin verificar siguen deshabilitados.

## Lo que NO hace
No es el sistema de producción, no es CAD completo, no ingresa con usuarios reales, no registra datos en servidor, no firma planos, no cobra suscripciones, no realiza georreferenciación, no envía RFQ y no reemplaza al ingeniero colegiado.

## Pruebas
`node --test tests.mjs` (9 pruebas).

## Próximo desarrollo privado
- Realizar ingeniería inversa **autorizada** de la estructura actual de JF Gestión360 `/opt/jfgestion360` y abrir un entorno staging con respaldo y rollback.
- Backend transaccional, Postgres + PostGIS; modelos tenant/org/user/project/parcel/survey/quote/documents/subscription/audit.
- Roles y acceso validados en servidor, row-level security y almacenamiento con ACL.
- Importadores CSV, GPX, GeoJSON, DXF y formatos GNSS con metadatos CRS/EPSG, transformaciones y trazabilidad.
- Integración de QGIS, ezdxf, FreeCAD y estándares IFC bajo licencias verificadas, según caso.
- Validar requisitos de facturación electrónica SUNAT y firma digital peruana antes de ofrecerlos.
- Suscripción piloto S/ 500 por 30 días, cobro adelantado, aviso día 28, vencimiento sin eliminar documentos, pero con bloqueo de operaciones nuevas; nunca bloquear exportación legítima.
- Ensayo real de recuperación y administración sucesoria legal sin contraseñas compartidas.

## Código y privacidad
El código de laboratorio no contiene secretos, datos de clientes ni coordenadas reales. No utilizar este prototipo para adoptar decisiones de inversión sin topografía, estudio de suelos, cotizaciones y normas vigentes.
