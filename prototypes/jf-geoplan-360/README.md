# JF GeoPlan 360 · prototipo no productivo

Módulo concebido para JF Gestión 360. Este repositorio público contiene **solamente un prototipo aislado y documentación genérica**, NO el código de producción, información de predios, planos reales, contratos, credenciales o datos de clientes.

## Piloto: complejo deportivo en Ferreñafe, Perú
Evaluación inicial de dos canchas con dos configuraciones hipotéticas:
- Variante fútbol 6: 2 campos de 40 × 25 m, lote de simulación 80 × 60 m (4.800 m²).
- Variante fútbol 7: 2 campos de 50 × 30 m, lote de simulación 80 × 80 m (6.400 m²).
- Bandas de seguridad preliminares: 2 m; pendientes de revisión normativa/profesional.
- El modelo **no representa linderos, pendiente, coordenadas, permisos, accesos verificados ni un expediente apto para construir**.

Se requiere levantamiento topográfico, estudio geotécnico, evaluación de drenaje, acceso vial, zonificación municipal, inspección de riesgo, verificación SUNARP y planos firmados por responsables habilitados. La evaluación financiera es una simulación de sensibilidad y no garantiza ventas ni rentabilidad.

## Contenido
- `theme.css`: esquema visual de ejemplo con blanco predominante, azul marino y celeste, aislado bajo `.jf-geoplan`.
- `layout.mjs`: generador determinista de ubicaciones *hipotéticas* de dos campos en un rectángulo sin georreferenciación.
- `layout.test.mjs`: pruebas de límites, dimensiones y rechazo de lotes insuficientes.
- `AGENTE.md`: contrato de responsabilidades del asistente y controles para multiempresa.

## Verificación del prototipo
```sh
node --test prototypes/jf-geoplan-360/layout.test.mjs
```

**No modifica ni despliega** la aplicación que está en `gestion360.jfconnect.online`. Para integrar el tema y la geometría se requiere identificar el repositorio real de Gestión360, entorno staging, respaldos y plan de reversión. Las acciones sobre bases de datos, facturación, firma profesional, tenant y producción necesitan autorización específica.
