# Periódico NO MÁS — NO+ Connect / JF SOLUCIONES

Base técnica **original** para evolucionar un periódico digital multimedia y su sala de redacción asistida por IA.

> Estado: prototipo de código en GitHub. **No está desplegado en producción ni sustituye los workflows de WhatsApp actuales**. No debe publicar denuncias o noticias sin autorización editorial humana.

## Qué está funcionando fuera de este repositorio

- Portal inicial: https://periodiconomas.space (la web de producción se administra en el VPS; este repositorio no contiene todavía una copia verificada de ese sitio).
- Entrada de WhatsApp Cloud API: receptor de n8n `/webhook/meta-whatsapp`.
- Acuse automático editorial de NO+ confirmado en ejecución real.
- Laboratorio aislado de clasificación inicial: workflow n8n `7i0ZAP1XRLpG6qmS`.

## Este repositorio contiene

- `src/editorial/triage.js`: clasificador editorial determinista con barreras para no publicar.
- `test/triage.test.js`: pruebas automatizadas de clasificación y seguridad.
- `docs/ARQUITECTURA.md`: plan de integración n8n, IA, CMS, radio y publicidad.
- `docs/OPEN_SOURCE.md`: proyectos upstream, licencias y estrategia de incorporación.
- `docs/SEGURIDAD_EDITORIAL.md`: revisión, verificación, datos personales y control de publicación.
- `package.json`: comando de pruebas.

## Ejecutar pruebas

Requiere Node.js 20+.

```bash
npm test
```

No requiere instalar dependencias ni utilizar tokens de Meta.

## Prioridades

1. Conectar el clasificador NO+ a una cola aislada mediante API interna segura; preservar el acuse de WhatsApp vigente.
2. Expedientes y aprobaciones editoriales con roles, bitácora y fuentes documentales.
3. Integrar Payload CMS (evaluar despliegue separado).
4. Radar de fuentes verificadas; AI solo sugiere, nunca confirma por sí misma.
5. Radio NO+ con AzuraCast después de dimensionar VPS, ancho de banda y licencias.
6. Publicidad con Revive Adserver tras validación comercial, privacidad y seguridad.

**No incluir jamás tokens, claves de Meta, contraseñas, datos reales de denunciantes ni backups del VPS en este repositorio público.**
