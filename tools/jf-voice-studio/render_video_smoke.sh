#!/usr/bin/env bash
# Producción demostrativa reproducible: audio sintético autorizado -> MP4 H.264/AAC + subtítulos mov_text.
# No conecta con Chatterbox ni utiliza material de clientes. No publica.
set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Uso: bash render_video_smoke.sh voz.wav subtitulos.srt salida.mp4" >&2
    exit 2
fi
audio="$1"
subs="$2"
output="$3"
test -f "$audio" || { echo "Falta audio de laboratorio" >&2; exit 3; }
test -f "$subs" || { echo "Faltan subtitulos de laboratorio" >&2; exit 4; }
command -v ffmpeg >/dev/null || { echo "Falta FFmpeg" >&2; exit 5; }
command -v ffprobe >/dev/null || { echo "Falta FFprobe" >&2; exit 6; }

font=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
test -f "$font" || { echo "Instalar fonts-dejavu-core" >&2; exit 7; }
duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio")
length=$(awk -v t="$duration" 'BEGIN {printf "%.2f", t+2.1}')
ffmpeg -hide_banner -loglevel error -nostdin -y \
  -f lavfi -i "color=c=0x081527:s=720x1280:r=25:d=$length" \
  -i "$audio" -i "$subs" \
  -filter_complex "[0:v]drawbox=x=0:y=0:w=iw:h=14:color=0x26A5FF:t=fill,drawbox=x=50:y=250:w=620:h=4:color=0x26A5FF:t=fill,drawtext=fontfile=$font:text='JF SOLUCIONES':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=110,drawtext=fontfile=$font:text='VOICE + VIDEO STUDIO':fontcolor=0x7FCFFF:fontsize=30:x=(w-text_w)/2:y=300,drawtext=fontfile=$font:text='PRUEBA DE LABORATORIO':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=550,drawtext=fontfile=$font:text='VOZ IA GENERICA - NO CLONADA':fontcolor=0x7FCFFF:fontsize=24:x=(w-text_w)/2:y=850,drawtext=fontfile=$font:text='SIN PUBLICACION':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=1060[v];[1:a]aresample=48000,apad=pad_dur=3[a]" \
  -map '[v]' -map '[a]' -map 2:0 \
  -c:v libx264 -preset veryfast -crf 24 -pix_fmt yuv420p \
  -c:a aac -ar 48000 -b:a 128k \
  -c:s mov_text -metadata:s:s:0 language=spa \
  -t "$length" -movflags +faststart "$output"

ffprobe -v error -show_entries format=duration,size:stream=codec_name,codec_type,width,height -of json "$output"
