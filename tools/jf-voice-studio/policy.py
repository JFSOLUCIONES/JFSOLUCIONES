"""JF Voice Studio: barreras de seguridad y licencia sin servicios externos."""
from __future__ import annotations

import json
import re
from pathlib import Path

_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")
LANGUAGES = frozenset({"es", "en", "fr", "pt", "de", "it", "zh", "ja", "ko"})


class PolicyError(ValueError):
    pass


def validate_profile_id(profile_id: str) -> str:
    if not isinstance(profile_id, str) or not _ID.fullmatch(profile_id):
        raise PolicyError("Identificador de perfil invalido")
    return profile_id


def require_approval(*, approved: bool, ai_disclosed: bool) -> None:
    if approved is not True:
        raise PolicyError("Guion pendiente de aprobacion humana")
    if ai_disclosed is not True:
        raise PolicyError("Falta indicar que el audio es generado con IA")


def read_authorized_profile(base: Path, profile_id: str) -> Path:
    profile_id = validate_profile_id(profile_id)
    base = base.resolve()
    audio = (base / f"{profile_id}.wav").resolve()
    metadata = (base / f"{profile_id}.json").resolve()
    if audio.parent != base or metadata.parent != base:
        raise PolicyError("Ruta de perfil no permitida")
    if not audio.is_file() or not metadata.is_file():
        raise PolicyError("Perfil de voz inexistente")
    try:
        rights = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PolicyError("Ficha de derechos invalida") from exc
    if rights.get("rights_verified") is not True:
        raise PolicyError("Derechos sin verificar")
    if rights.get("allowed_use") not in {"institutional_narration", "commercial_voiceover"}:
        raise PolicyError("Uso fuera de licencia")
    if not rights.get("license_evidence") or not rights.get("reference_source"):
        raise PolicyError("Falta evidencia de procedencia")
    return audio
