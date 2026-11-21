# JF GeoPlan 360 · API de referencia v0.3.0

**Estado:** prototipo aislado, preparado para pruebas, no integrado ni desplegado en JF Gestión360 productivo. **No reemplaza la firma ni la responsabilidad profesional**. No incorpora sistemas de cobro ni firma electrónica.

## Qué hace realmente
- Autenticación de servicio por JWT HS256 validado con issuer/audience, exp y tenant. **La emisión de tokens corresponde al servicio de identidad de Gestión360**, nunca al navegador. Las claves no se guardan en GitHub.
- Proyecto/tenant aislados por consultas parametrizadas, lectura de otros clientes bloqueada (excepto MASTER, que queda auditado). Los administradores deben proveer tokens JWT firmados por un emisor confiable.
- Suscripción piloto **S/500 por 30 días adelantado**. Se admite referencia de voucher; **solo un rol MASTER** puede confirmar manualmente un pago después de verificarlo fuera de la aplicación. Sin pasarela real. Aviso dos días antes del vencimiento y bloqueo de operaciones nuevas al caducar; consulta y acceso a documentos existentes se mantiene.
- Vértices con sistema de coordenadas explícito (EPSG:4326 se transforma a UTM WGS84 automáticamente; CRS proyectados métricos se aceptan). Rechaza autointersecciones y coordenadas inválidas. Calcula área/perímetro y exporta **DXF conceptual**.
- Entregables en borrador con SHA256 documental y envío a revisión profesional por especialidad. **No permite revisión positiva del autor de ese borrador, exige profesional verificado y checklist**. Estado final `approved_for_signature` (NO `signed`). La comprobación real de habilitación CIP/CAP debe integrarse con una fuente autorizada o validación administrativa humana.
- Bitácora transaccional de eventos sin contenido sensible.

## Ejecutar en laboratorio local
Requiere Python 3.11+, dependencias en `requirements.txt` y no debe utilizar ninguna base productiva.

```bash
python -m pip install -r requirements.txt
export GEOPLAN_JWT_SECRET='COLOCAR_CLAVE_ALEATORIA_DE_AL_MENOS_32_CARACTERES'
export GEOPLAN_DB_PATH='./data/lab.sqlite3'
python -m uvicorn geoplan_api.asgi:app --host 127.0.0.1 --port 8791
python -m pytest -q tests/
```

El secreto de ejemplo **no debe utilizarse**. El mecanismo de JWT de laboratorio se debe reemplazar por integración con el emisor central de JF Gestión360, preferentemente tokens asimétricos con JWKS y expiraciones cortas.

## Lo que falta para convertirse en un producto comercial terminado
1. Permiso de lectura **estrictamente acotado** para `jf_geoplan_dev` sobre el repositorio de Gestión360 en `/opt/jfgestion360`; la credencial actual `JF CONTROL AI - VPS1` restringe cualquier comando excepto `jf-audit`/`jf-inventory` (rechazo 126, ejecución n8n N° 1773). **No ampliar permisos genéricos, no root**.
2. Crear repositorio **privado** de Gestión360 / GeoPlan bajo titularidad de la empresa, versionar fuente legítima sin `.env` ni secretos. El repositorio público solo guarda prototipos seguros.
3. Preparar staging aislado, replicar el control de organizaciones/usuarios existente, realizar migraciones PostgreSQL/PostGIS, activar políticas de aislamiento y pruebas de integración real.
4. Conectar proyectos y expedientes a almacenamiento privado con permisos server-side, no permitir nombres de archivo como rutas directas. OCR/render/IA deben usar cola con límites por tenant.
5. Validar licencias y condiciones del RNE peruano con profesionales habilitados; firma digital a través de proveedor o firmante calificado y verificación de certificado. No basta con estampar firma.
6. Implementar firma de contratos, integración tributaria SUNAT, cobro seguro, recordatorio real programado, acceso de clientes, y prueba de recuperación.
7. Certificación de geo-topografía: validación de CRS fuente, datum, precisión instrumental, control de cierre, georreferenciación, observaciones del terreno y profesional responsable.

## Seguridad
Se deben añadir rate limit, validación real de membresías con Gestión360, KMS para claves de firma, backups cifrados ensayados, control de materiales subidos, observabilidad, escaneo de dependencias y pruebas de carga. Este servicio no expone puertos en Internet durante laboratorio.

## Licencias OSS y alternativas evaluadas
- ezdxf (MIT), pyproj (MIT), Shapely (BSD), QGIS (GPL), FreeCAD (LGPL), IfcOpenShell (LGPL), That Open web-ifc (MPL 2.0) y xeokit SDK (AGPL/comercial según componente): verificar licencia y obligaciones para SaaS antes de incorporar código.
- Dalux BIM Viewer, Coohom y Housia son servicios de terceros: registrarse o visualizar no autoriza clonación de software ni integración comercial sin revisar términos/APIs.
- No usar aquí modelos IFC de clientes o expedientes privados de otros proveedores sin permiso.
