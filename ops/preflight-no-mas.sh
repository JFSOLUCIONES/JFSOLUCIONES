#!/usr/bin/env bash
# Auditoria NO+ de SOLO LECTURA. No modifica servicios, puertos ni archivos.
set -u
echo '=== NO+ | PREVUELO PARA CMS, PUBLICIDAD Y RADIO ==='
date -Is
echo '-- Sistema --'; uname -a
if [ -r /etc/os-release ]; then grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release; fi
echo '-- Recursos --'; nproc; free -h; df -h / /var 2>/dev/null || df -h /
echo '-- Memoria swap --'; swapon --show || true
echo '-- Servicios --'; systemctl is-active caddy docker 2>/dev/null || true
echo '-- Docker --'; docker --version 2>/dev/null || true
echo '-- Containers (nombres y estado, SIN variables ni credenciales) --'
docker ps --format '{{.Names}} | {{.Status}}' 2>/dev/null || true
echo '-- Puertos TCP escuchando (sin IPs ni procesos) --'
ss -lntH 2>/dev/null | awk '{print $4}' | sed -E 's/.*:([0-9]+)$/puerto \1/' | sort -u || true
echo '-- Dominio NO+ (solo estado HTTP) --'
for u in https://periodiconomas.space/ https://periodiconomas.space/privacidad/ https://periodiconomas.space/condiciones/; do
  code=$(curl -L -sS -o /dev/null -w '%{http_code}' --max-time 12 "$u" || true)
  echo "$u | HTTP $code"
done
echo '-- Estado del Caddyfile (SIN contenido) --'
caddy validate --config /etc/caddy/Caddyfile 2>&1 | grep -E 'Valid configuration|Error:' || true
echo '=== FIN DEL PREVUELO - SIN CAMBIOS ==='
