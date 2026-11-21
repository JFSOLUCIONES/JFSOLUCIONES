# JF SPORTS EDGE — laboratorio OSS seguro

**Estado:** solo investigación, datos sintéticos, cero despliegues y cero apuestas.

- Ruff 0.17.6: revisión E4/E7/E9/F y formato de este laboratorio.
- penaltyblog 1.13.1 (MIT): smoke test API de Poisson vs Dixon-Coles con 72 partidos artificiales; 60 para ajuste y 12 para prueba.
- Qwen Code: https://github.com/QwenLM/qwen-code (Apache-2.0). **No instalado ni autorizado en VPS**.
- OpenHands: https://github.com/OpenHands/OpenHands (MIT). **No instalado ni autorizado en VPS**. Su documentación advierte que un agente sin sandbox accede a archivos del host.
- Los resultados numéricos con partidos ficticios **no son métricas deportivas** y NO se comparan con el holdout real Bundesliga 2025/26. La selección del modelo requiere backtest cronológico real reproducible y fuentes con licencia.
- No copiar datos privados, secretos, historial de clientes, cuotas ni código comercial a este repositorio público.
- Orquestación objetivo: JF Director 360 AI (decisiones + QA) -> GitHub PR/CI -> n8n gates -> laboratorio VPS2 con acceso restringido (pendiente autorización técnica) -> staging VPS1 -> revisión humana.
- Drive conserva documentación de ingeniería y respaldos **cifrados**. Un artefacto de trabajo de GitHub no reemplaza backups restorables.

## Puertas de instalación en VPS2

1. Verificar CPU/RAM libres, disco libre y modelos de recursos de todos los clientes del VPS2; ningún inventario Docker prueba por sí mismo espacio libre.
2. Usar usuario no privilegiado, sandbox separado sin directorios ni Docker socket del host; sin montar credenciales ni bases de datos reales.
3. Repositorio privado y token de solo lectura para el agente; sin permiso de despliegue o merge automático.
4. Instalar versión y checksum verificables, conservar licencias; verificar red de salida y cuota de API del modelo, y medir costes.
5. Test de humo read-only, control de procesos, log redactado y apagado/rollback.
6. Ejecutar cualquier modificación de producción únicamente tras aprobación humana y respaldos probados.

## Qué falta después de este laboratorio
- GitHub privado para el CORE completo; conector actual no crea repositorios.
- Confirmar si existe agente host-side fuera de Docker con auditoría explícita.
- Acceso SSH allowlisted de instalación en VPS2; el flujo inventario es de solo lectura.
- Datos de lesiones, alineaciones, cuotas licenciados; PostgreSQL staging y end-to-end Django.
