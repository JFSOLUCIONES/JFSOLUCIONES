# Investigación de referencias — JF GeoPlan 360 | 21-11-2026

## Soluciones revisadas con evidencia

| Referente | Valor comercial | Qué NO asumir |
|---|---|---|
| Dalux BIM Viewer | Visor gratuito BIM/IFC, planos y móviles; integración de modelos externos. Fuente: https://www.dalux.com/es-pe/productos/bim-viewer/ | No es generador automático de planos para licencias y no tenemos confirmación de correo de registro. |
| Coohom | Plano 2D a 3D, modelado/render/recorridos; correo de bienvenida y login Google confirmado 21/11/2026. Sitio: https://www.coohom.com/pricing | Registro ≠ licencia empresarial para reventa / API / extracción; condiciones y costes por render pendientes. |
| Housia | Anteproyectos con IA y ficha de requerimientos fácil; imagen referencial para cliente. Fuente: https://housia.ai/es/planos-de-casas | El proveedor indica que es diseño orientativo, no planos listos para licencia. Registro de correo no confirmado. |
| Loyola Constructores | Publicidad con cálculo S/10 por m² de lote y mínimo S/1,000, paquetes 1 a 3, captación WhatsApp y muestras de planos (capturas del usuario). Web: https://planos.loyalaconstructores.org/ | Es precio publicado ajeno y condiciones particulares, NO precio oficial ni coste de JF. |

## Código abierto y licencias para una oferta SaaS
- QGIS (GPL): https://github.com/qgis/QGIS — análisis SIG; ejecución en entorno propio y cumplimiento de licencia al distribuir software.
- PostGIS (GPL-2 o posterior según componentes): https://postgis.net — índices geoespaciales y geometrias en PostgreSQL.
- FreeCAD (LGPL): https://github.com/FreeCAD/FreeCAD — modelado paramétrico y exportaciones.
- ezdxf (MIT): https://github.com/mozman/ezdxf — generación y lectura DXF (incluido en prototipo).
- IfcOpenShell (LGPL y licencias específicas de componentes): https://github.com/IfcOpenShell/IfcOpenShell — IFC/BIM.
- That Open web-ifc (MPL 2.0): https://github.com/ThatOpen/engine_web-ifc — parser IFC web.
- xeokit (AGPL/comercial para SDK): https://github.com/xeokit/xeokit-sdk — visor BIM; requiere revisión legal antes de incrustarlo en SaaS propietario.
- MapLibre (BSD): https://github.com/maplibre/maplibre-gl-js — mapas web (atribución cartográfica obligatoria).
- Qwen Code (licencia a comprobar según versión exacta): https://github.com/QwenLM/qwen-code — asistente de programación, en entorno de laboratorio con permisos delimitados.

**Decisión:** comercializar primero el flujo de servicio profesional y generación DXF + visor simple, y añadir BIM/3D después de validar licencias, coste de GPU/render, calidad y soporte. No copiar UI, marca o código de competidores sin licencia.

## Ética y responsabilidad profesional
JF SOLUCIONES puede captar, contratar, administrar y preparar borradores. El ingeniero civil asume responsabilidad real de las partes dentro de su competencia profesional; arquitectura, electricidad y sanitaria se asignan a responsables habilitados específicos. Para firma digital válida debe existir evidencia de identidad, certificado y procedimiento de firma verificado; ningún flujo debe adjuntar automáticamente la firma del tío.

RNE / normativas vigentes deben validarse ante fuentes oficiales según localización, tipología y municipio. Referencia de RNE (consultar edición vigente): https://www.gob.pe/vivienda
