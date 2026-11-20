# JF SOLUCIONES — plan de pruebas para producción de voz y video
Fecha: 2026-11-20 · Documento público y no sensible.

## Alcance verificado
n8n verificó la generación de voz Kokoro en workflow s3FbmAefttTQMF79, ejecución 1256, y el bloqueo editorial en workflow e9LjSHJ6fnb48bQl, ejecución 1251. No se ejecutó clonación de voz.

Un video de laboratorio con FFmpeg y un narrador genérico sería una prueba técnica de ensamblaje, NO una demostración de voz clonada ni un spot final para un cliente.

## Matriz de aceptación
| Etapa | Evidencia exigida | Estado al 20/11/2026 |
|---|---|---|
| Locución Kokoro | MP3 y ejecución real n8n | PASS 1256 |
| Control editorial | No llamar motor sin licencia y aprobación | PASS 1251 |
| Código / permisos | Prueba unitaria GitHub Actions PR 4 | PASS |
| Preparar muestra | FFmpeg WAV 24 kHz mono | PASS laboratorio |
| Chatterbox real | Modelo cargado y voice profile autorizado | BLOQUEADO: sin despliegue |
| OpenVoice V2 | Evaluación de calidad en español | PENDIENTE |
| CosyVoice 3 | Evaluación de prosodia en español | PENDIENTE |
| Música/voces | Separación con Demucs | PENDIENTE |
| Subtítulos | STT y SRT con timestamps | PENDIENTE |
| Montaje MP4 | H.264/AAC y ffprobe | PRUEBA LOCAL |
| Panel JF CONNECT AI | Upload, voz, colas, preview, exportación, permisos | NO VERIFICADO |
| Backup/restore | Restauración cifrada aislada | PENDIENTE |
| Publicación | Aprobación humana y log | NO ACTIVADA |

## Criterios para muestra técnica
- Exportar 9:16 H.264/AAC, comprobar 25/30 fps y decodificación.
- Una nueva narración no debe confundirse con la voz real de una autoridad.
- Guion y fotos/medios deben ser auténticos o estar identificados como recursos sintéticos.
- Revisar pronunciación peruana, claridad, mezcla, volumen y subtítulos.
- El programa de pruebas usará texto neutro, sin datos de clientes ni difusión pública.

## Despliegue y continuidad
No desplegar un motor TTS pesado en VPS1; acceso SSH actual solo permite auditoría. En VPS2 verificar CPU/GPU, ensayar en contenedor aislado y establecer cuotas de memoria, respaldos, contraseña de servicio en gestor de secretos y rollback. Cada cliente requiere permisos propios.
