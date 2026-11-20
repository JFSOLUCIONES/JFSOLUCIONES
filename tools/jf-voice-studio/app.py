"""API interna experimental para sintesis MP3 por Chatterbox Multilingual V3.

No publicar la API hacia Internet, no registrar guiones ni audios. En ambientes
sin GPU las pruebas de rendimiento pueden resultar lentas. No desplegado.
"""
from __future__ import annotations

import hmac
import io
import os
import subprocess
import threading
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from policy import LANGUAGES, PolicyError, read_authorized_profile, require_approval

app = FastAPI(title="JF VOICE STUDIO - OSS privado", version="0.1.0")
_LOCK = threading.Lock()
PROFILES_DIR = Path(os.getenv("JF_VOICE_PROFILES_DIR", "/srv/jf-voice/profiles"))
SERVICE_KEY = os.getenv("JF_VOICE_SERVICE_KEY", "")


class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=600)
    voice_profile_id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]{2,63}$")
    language_id: str = "es"
    approved: bool = False
    ai_disclosed: bool = False


@lru_cache(maxsize=1)
def load_model():
    import torch
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return ChatterboxMultilingualTTS.from_pretrained(device=device, t3_model="v3")


@app.get("/health")
def health():
    # Salud de la API != disponibilidad ni calidad real del modelo.
    return {
        "status": "api_up",
        "engine": "chatterbox-multilingual-v3",
        "model_cached": load_model.cache_info().currsize > 0,
    }


@app.post("/v1/speech")
def synthesize(
    request: SpeechRequest,
    x_jf_service_key: str | None = Header(default=None, alias="X-JF-Service-Key"),
):
    if not SERVICE_KEY:
        raise HTTPException(status_code=503, detail="Credencial no configurada")
    if not x_jf_service_key or not hmac.compare_digest(x_jf_service_key, SERVICE_KEY):
        raise HTTPException(status_code=401, detail="No autorizado")
    try:
        require_approval(approved=request.approved, ai_disclosed=request.ai_disclosed)
        if request.language_id not in LANGUAGES:
            raise PolicyError("Idioma no habilitado")
        reference = read_authorized_profile(PROFILES_DIR, request.voice_profile_id)
    except PolicyError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    # Evitar que varias solicitudes consuman toda la RAM/VRAM del VPS.
    with _LOCK:
        try:
            model = load_model()
            waveform = model.generate(
                request.text, audio_prompt_path=str(reference), language_id=request.language_id
            )
            samples = np.asarray(waveform.squeeze().detach().cpu(), dtype=np.float32)
            if samples.ndim != 1 or samples.size == 0:
                raise RuntimeError("Audio invalido")
            pcm = (np.clip(samples, -1, 1) * 32767).astype(np.int16)
            memory = io.BytesIO()
            with wave.open(memory, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(int(model.sr))
                wav.writeframes(pcm.tobytes())
            result = subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error",
                    "-f", "wav", "-i", "pipe:0",
                    "-codec:a", "libmp3lame", "-b:a", "160k", "-f", "mp3", "pipe:1",
                ],
                input=memory.getvalue(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                timeout=90,
            )
        except Exception as exc:
            # No filtrar rutas privadas, voz fuente ni texto del usuario.
            raise HTTPException(status_code=503, detail="Motor TTS no disponible") from exc

    return Response(
        content=result.stdout,
        media_type="audio/mpeg",
        headers={"X-JF-Synthetic-Audio": "true", "Cache-Control": "no-store"},
    )
