# Catálogo de código abierto para Periódico NO MÁS

El código de terceros permanece en sus repositorios originales. No copiar su código fuente masivamente a nuestro proyecto: evaluar versiones, licencias, mantenimiento, avisos y riesgos de seguridad antes de instalar.

| Motor | Repositorio oficial | Propuesta | Etapa |
|---|---|---|---|
| Payload CMS | https://github.com/payloadcms/payload | Redacción, borradores, roles, medios, revisiones, web | Fase C |
| Aleph (OCCRP) | https://github.com/alephdata/aleph | Exploración y búsqueda documental de investigaciones | Fase D |
| OpenSanctions | https://github.com/opensanctions/opensanctions | Resolver entidades y contrastar listas con limitaciones/contexto | Fase D |
| changedetection.io | https://github.com/dgtlmoon/changedetection.io | Detectar cambios en documentos y páginas oficiales | Fase D |
| RSS-Bridge | https://github.com/RSS-Bridge/rss-bridge | Agregar fuentes donde RSS sea insuficiente, respetar accesos | Fase D |
| Meedan Check | https://github.com/meedan/check | Referente técnico para flujos de verificación colaborativa | Evaluación |
| AzuraCast | https://github.com/AzuraCast/AzuraCast | Emisión y programación de Radio NO MÁS | Fase E |
| Revive Adserver | https://github.com/revive-adserver/revive-adserver | Inventario de campañas, banners y métricas comerciales | Fase E |

## Licencias y condiciones conocidas

- Payload CMS: MIT (conservar avisos de copyright y licencia).
- AzuraCast: AGPL-3.0; estudiar obligaciones si se modifica y ofrece por red.
- Revive Adserver: GPL-2.0 o posterior. El proyecto **advierte descargar distribuciones desde su sitio oficial**, no desplegar ZIP del repositorio de desarrollo.
- Para todos los demás proyectos, revisar su licencia en la revisión concreta antes de reutilizar código o datos. Datos de OpenSanctions, bases documentales, fotografías y señales de radio pueden imponer términos separados del código.

## Política de instalación

1. Inventariar versión, última publicación, vulnerabilidades, recursos y licencia.
2. Instalar primero en entorno de ensayo privado, no en VPS de producción compartido.
3. Integrar por API, con credenciales mínimas y circuit breakers.
4. Documentar migración, backup, rollback y pruebas de carga.
5. Nunca extraer en masa ni reproducir íntegramente artículos ajenos sin permiso.

## Prioridad editorial

La necesidad inmediata no es instalar seis servidores; es conectar **captación + expediente + verificación + aprobación** sobre la plataforma que ya funciona.
