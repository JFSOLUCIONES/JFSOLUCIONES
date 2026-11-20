# LEGADO DIGITAL JF SOLUCIONES — Índice maestro público

**Actualizado:** 2026-11-20 · **Responsable de los proyectos:** JF SOLUCIONES ONLINE
**Objetivo:** permitir a futuros administradores y herederos legalmente habilitados localizar, mantener y reconstruir los sistemas de JF SOLUCIONES.

> Este índice es **público y no sensible**. Un enlace en este índice NO significa que el sistema esté respaldado o que su código fuente completo esté depositado en GitHub. Las credenciales y los datos de clientes nunca se publican aquí.

## Empieza aquí
1. **Patrimonio digital y recuperación**: [Pull Request N° 1](https://github.com/JFSOLUCIONES/JFSOLUCIONES/pull/1). Contiene guía sucesoria, matriz de recuperación, catálogo público ampliado de activos, plan de pruebas y hoja de ruta. Está en borrador, pendiente de revisión y fusión.
2. **Agente comercial JF SALES V2**: [Pull Request N° 2](https://github.com/JFSOLUCIONES/JFSOLUCIONES/pull/2). Desarrollo parcial, no asumir despliegue.
3. **JF SPORTS EDGE AI**: [Pull Request N° 3](https://github.com/JFSOLUCIONES/JFSOLUCIONES/pull/3). Prototipo deportivo y plan de despliegue controlado.
4. **JF VOICE & VIDEO STUDIO**: [Pull Request N° 4](https://github.com/JFSOLUCIONES/JFSOLUCIONES/pull/4). Documentación OSS, API experimental, pruebas de licencias y ensamblaje MP4. El motor clonador aún no está desplegado.

## Auditoría de estado puntual del 20/11/2026
- **GitHub:** 1 repositorio visible y público (`JFSOLUCIONES/JFSOLUCIONES`), 4 PR abiertos en borrador.
- **n8n:** 110 workflows listados (43 activos, 67 inactivos); la lista no es una copia de sus definiciones completas.
- **VPS1/VPS2:** auditorías de lectura finalizadas (ejecuciones 1247 y 1248).
- **Kokoro:** generación MP3 comprobada en n8n ejecución 1256.
- **Control de licencias de voz OSS:** bloqueo por defecto comprobado en n8n ejecución 1251.
- **GitHub Actions:** legado 44801323601 y voice/video 44800714607, ambas pruebas de laboratorio completadas.
- **Respaldos n8n:** ejecuciones recientes exitosas; no equivalen a pruebas de restauración integral.

## Criterio HEREDABLE
Un sistema **NO** es heredable hasta que:
- Exista fuente original reproducible en repositorio adecuado bajo custodia empresarial.
- Exista inventario de sus dependencias y procedimientos de inicio/parada.
- Las copias cifradas se hayan verificado y probado restaurando de forma aislada.
- Una persona administradora y su suplente tengan vías legales y técnicas de acceso, con 2FA y claves de recuperación en custodia privada.
- La documentación indique qué hacer ante un fallo y cómo evitar afectar a los clientes.

## Accesos y seguridad
- No subir contraseñas, tokens, datos personales, expedientes, grabaciones de clientes, `.env`, llaves privadas o `N8N_ENCRYPTION_KEY`.
- Las llaves privadas de respaldo `age` deben estar en custodia offline del titular y/o custodio designado; el VPS solo conserva destinatarios públicos.
- Crear repositorios privados de propiedad empresarial y nombrar al menos dos administradores legales.
- El sucesor de GitHub de una cuenta personal puede gestionar repositorios públicos bajo reglas de GitHub, **pero no inicia sesión como el titular y no reemplaza el acceso administrativo a repositorios privados**. Fuente: https://docs.github.com/en/repositories/creating-and-managing-repositories/access-to-repositories

## Próximos hitos prioritarios
1. Repositorio(s) privados / organización empresarial, control dual y 2FA.
2. Exportación segura de los sistemas y workflows a repos privados.
3. Ejercicio de recuperación real de n8n + PostgreSQL + archivos, y comprobación de backups remotos.
4. Prueba de síntesis Chatterbox/OpenVoice en staging de VPS2 con licencia de voz autorizada.
5. Integración del panel JF CONNECT con motor de audio y video, permisos y aprobación humana.

**Aviso:** el repositorio principal contiene código y documentación NO+, por lo que el resto de sistemas no está aún reproducible desde esta rama. Esta página es la entrada para los trabajos de recuperación, no una certificación de copias completas.
