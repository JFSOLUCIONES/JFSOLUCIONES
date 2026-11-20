# JF VOICE & VIDEO STUDIO — estudio OSS y arquitectura
Fecha: 2026-11-20. Estado: investigación y prototipo; NO desplegado.

## Infraestructura verificada (n8n)
- JF VOICE ENGINE original s3FbmAefttTQMF79: genera MP3 por Speaches/Kokoro (ejecución N° 1245, éxito).
- JF VOICE ENGINE ROSA T3X9rJehW4pA30zT: flujo independiente, bloqueado por defecto; ejecución N° 1243 verificó rechazo sin aprobación.
- Auditoría VPS1 n8n N° 1247: 7,8 GiB RAM; 49 GB libres. VPS2 N° 1248: 23 GiB RAM; 271 GB libres; jf-ai-speaches activo.
- SSH disponible para auditoría restringida, NO para instalaciones, administración de Docker o reinicios. Estado de GPU NO verificado.
- El repositorio JFSOLUCIONES/JFSOLUCIONES es público: nunca subir voces, videos de clientes, identificaciones, llaves ni secretos.

## Proyectos auditados
| Proyecto oficial | Función | Licencia/condición y estado | Decisión |
|---|---|---|---|
| Resemble-AI Chatterbox Multilingual V3 | TTS zero-shot con audio de referencia, español | MIT; retirada de mantenimiento desde agosto 2026 | Experimento y demostración, no dependencia única |
| MyShell OpenVoice V2 | Clonación del timbre, español y otras lenguas | MIT, uso comercial según proyecto | Alternativa principal |
| QwenAudio / Fun-CosyVoice 3 | TTS multilingüe zero-shot en español | Código Apache-2.0; comprobar pesos concretos | Alternativa avanzada |
| Speaches + Kokoro | TTS actual, sin clonación de este audio | Validar checkpoint desplegado | Respaldo operativo |
| Demucs | Separación de voces/música | MIT upstream; revisar pesos | Limpieza de muestras |
| faster-whisper + WhisperX | Transcripción y subtítulos sincronizados | Verificar checkpoints y licencias individuales | Subtitulado |
| MuseTalk 1.5 | Lip-sync autorizado | MIT código; revisar demás modelos | Fase video con GPU |
| FFmpeg | Corte, mezcla, MP4, WAV y SRT | LGPL/GPL según binario | Exportación |
| F5-TTS pesos oficiales | Voice cloning | Pesos CC-BY-NC; código MIT | NO USAR pesos oficiales comercialmente |

## Plataforma objetivo (modular, no todo implantado)
1. Ingesta de audio/video con hash, titularidad/licencia y aprobación.
2. Aislamiento vocal y normalización con FFmpeg y Demucs.
3. Biblioteca privada de voces por cliente: WAV y JSON con derechos, alcance y trazabilidad.
4. Síntesis por adaptador de motor (Chatterbox, OpenVoice V2, CosyVoice 3, Kokoro), guion editable.
5. Revisión de pronunciación peruana, pausas, texto, naturalidad, marca de IA y control de calidad.
6. Transcripción y subtítulos SRT con faster-whisper/WhisperX.
7. Video vertical 9:16 y horizontal, mezcla de música licenciada, exportador FFmpeg.
8. Lip-sync solo con autorización de imagen; aprobación humana; publicación separada mediante permisos de la cuenta.

## Garantías de ejecución
- La frase «esa voz no pertenece a nadie» NO prueba que el audio generado por terceros sea libre; comprobar términos de su fuente antes de clonación comercial.
- Narradora sintética no se presenta como voz real de una alcaldesa ni se atribuyen declaraciones falsas.
- No despliegue en VPS sin auditoría CPU/GPU, respaldo restaurable, credenciales y permisos de administrador.
- Secretos exclusivamente en credenciales n8n / gestor de secretos; no incrustar en workflows públicos.
- No guardar audio personal o de clientes en este repositorio público.
- Limitar acceso, concurrencia, retención, logs y gastos; aprobar cada exportación/publicación.
- Los checkpoints de un sistema pueden tener licencia distinta del código.

## Referencias oficiales consultadas 20/11/2026
- https://github.com/resemble-ai/chatterbox
- https://github.com/myshell-ai/OpenVoice
- https://github.com/QwenAudio/CosyVoice
- https://github.com/adefossez/demucs
- https://github.com/SYSTRAN/faster-whisper
- https://github.com/m-bain/whisperX
- https://github.com/TMElyralab/MuseTalk
- https://github.com/SWivid/F5-TTS

## Fases y estado
- Fase 0, inventario + derechos + arquitectura: documentada.
- Fase 1, API privada de síntesis y pruebas sin carga de modelos: código experimental en rama.
- Fase 2, deployment aislado en VPS autorizado + benchmarks con CPU/GPU: pendiente.
- Fase 3, encadenar n8n, audio, subtítulos, video, QA y almacenamiento seguro: pendiente.
- Fase 4, demo para Lurín con narración IA declarada y material autorizado: pendiente.
