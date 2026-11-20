# JF VOICE STUDIO OSS - prototipo de worker de voz

Estado: NO desplegado en VPS. El adaptador es solo de audio MP3 y utiliza Chatterbox Multilingual V3. El repositorio upstream Chatterbox dejó de recibir mantenimiento desde agosto de 2026: usar solo en evaluación controlada. El despliegue y compatibilidad con los checkpoints no se han probado.

## Requisitos del piloto
- Python 3.11, ffmpeg, memoria suficiente; GPU NVIDIA preferida, no verificada en nuestros VPS.
- Registro de un perfil de voz privado: un WAV sin música y un JSON con derechos validados.
- Clave fuerte en variable JF_VOICE_SERVICE_KEY, almacenada en gestor de secretos.
- Docker o VM aislada, 1 worker, acceso por red privada y sin exposición pública.

## Inicio manual en una VM de pruebas
1. Crear entorno virtual Python 3.11.
2. Instalar los paquetes de requirements.txt; revisar licencias, pesos y dependencias antes de la descarga.
3. Exportar JF_VOICE_SERVICE_KEY y JF_VOICE_PROFILES_DIR de forma segura.
4. Ejecutar: uvicorn app:app --host 127.0.0.1 --port 8088 --workers 1
5. Confirmar GET /health. Este resultado NO significa que el modelo se haya cargado.
6. Ejecutar una única prueba POST /v1/speech y medir latencia, RAM, pronunciación y calidad.

## Ficha de perfil privada, no subir a GitHub
Archivo: /srv/jf-voice/profiles/demo_01.json
Contenido de ejemplo:
    {
      "rights_verified": true,
      "reference_source": "licensed_synthetic",
      "allowed_use": "institutional_narration",
      "license_evidence": "registro-privado-de-derechos-001"
    }
Audio de referencia asociado: /srv/jf-voice/profiles/demo_01.wav
Los campos de ejemplo son ilustrativos: NO marcarlos como verificados sin la evidencia real.

## Petición de prueba (si el sistema está instalado)
POST http://127.0.0.1:8088/v1/speech
Header: X-JF-Service-Key: <token privado>
JSON:
    {
      "text": "Presentamos una demostración audiovisual con voz sintética.",
      "voice_profile_id": "demo_01",
      "language_id": "es",
      "approved": true,
      "ai_disclosed": true
    }

La respuesta es audio/mpeg para guardar como MP3. El servicio no almacena los guiones enviados y no publica nada.

## Pruebas de autorización sin descargar modelos
Desde tools/jf-voice-studio:
    python -m unittest discover -s tests -v

## Integración futura n8n
- Input guion, cliente, voz, aprobacion, licencias -> control humano -> HTTP Request a worker.
- En la solicitud n8n seleccionar autenticación Header Auth con X-JF-Service-Key y credencial configurada manualmente.
- Guardar audio binario únicamente en el almacén privado de medios con retención definida.
- Subtitular con faster-whisper/WhisperX y montar MP4 con FFmpeg solo después de aprobación.
- El flujo Kokoro s3FbmAefttTQMF79 sigue siendo respaldo y se conserva sin cambios.
- El flujo Rosa T3X9rJehW4pA30zT continúa separado y sin publicación automática.

## Lo no resuelto
No hay acceso SSH de administración, modelo instalado ni datos de rendimiento. No introducir audio, datos personales, claves o tokens en este repositorio público. La licencia del audio sintético original debe confirmarse con su proveedor antes de utilizarla comercialmente.
