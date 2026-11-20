#!/usr/bin/env bash
# Normaliza una muestra ya autorizada y produce WAV mono 24 kHz PCM16.
# No aisla voces de música; para ello usar Demucs/UVR por separado.
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "Uso: bash prepare_reference.sh entrada.mp4|wav salida.wav" >&2
  exit 2
fi
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg" >&2; exit 3; }
input="$1"
output="$2"
test -f "$input" || { echo "Archivo de entrada no encontrado" >&2; exit 4; }
ffmpeg -hide_banner -loglevel error -nostdin -y \
  -i "$input" -vn \
  -af "highpass=f=80,lowpass=f=8500,afftdn=nf=-30:nr=10,loudnorm=I=-19:TP=-1.5:LRA=8" \
  -ac 1 -ar 24000 -c:a pcm_s16le "$output"
echo "WAV preparado. Verificar presencia de música, distorsión y derechos antes de registrar voz."
