# NO+ JF Editorial — MVP 0.2 (31-10-2026)

## Estado probado
Se inspeccionó la muestra CKEditor 5 del usuario (v48.5.1). Incluía clave de licencia; **no se subió ni se reutilizó esa clave**.

Se generó un paquete descargable independiente `NO_MAS_JF_EDITORIAL_MVP_02.zip` que añade al starter Next.js/React:
- panel de expedientes y secciones (política, región, Perú, mundo, deportes, salud, economía y consejos);
- CKEditor React con configuración de licencia de entorno, sin funciones premium obligatorias;
- estados de borrador, verificación, revisión y aprobado;
- barrera mínima: titular, extensión, evidencia y derechos/crédito de imagen antes de aprobación;
- persistencia local solo en navegador y exportación JSON;
- maqueta HTML de 12 páginas cuadradas para imprimir a PDF, **solo con artículos aprobados**.

## Riesgos y límites
**Es un laboratorio, NO una aplicación lista para el público.** No hay autenticación, base de datos central, gestión de documentos sensibles, API segura, integración con WhatsApp o salida comercial apta para imprenta. La paginación de navegador y los textos pueden desbordarse; confirmar visualmente cada página. No usar con datos personales. No se usan fotografías ajenas sin autorización.

**La compilación no está verificada**: el entorno de ejecución no tenía dependencias CKEditor en caché y la instalación offline devolvió ENOTCACHED.

## Próximo trabajo
1. Probar `npm install && npm run build` en PC/VPS de laboratorio.
2. Añadir PostgreSQL, autenticación y privilegios de editor, aprobación verificable.
3. Completar banco fotográfico propio y maquetador paginado (12 páginas 11 × 11 pulgadas).
4. Probar exportación PDF y preflight de impresión antes de activar distribución.
5. Recién entonces integrar bot NO+ y suscriptores verificados.

No almacenar la licencia ni tokens de producción en GitHub. Los archivos de código se entregaron como ZIP en la conversación; este documento no constituye un despliegue ni una confirmación de subida del ZIP al repositorio.
