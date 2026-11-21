#!/bin/sh
# SOLO operador autorizado: NO instala, modifica, lee ni transmite secretos.
# El administrador debe autorizar ejecución en un rol sin sudo/root y con rutas fijas.
set -eu
ROOT=/opt/jfgestion360
printf '%s\n' GEOPLAN_SOURCE_MAP_V1
if [ ! -d "$ROOT" ]; then printf '%s\n' ROOT_ABSENT GEOPLAN_SOURCE_MAP_DONE; exit 0; fi
printf '%s\n' ROOT_PRESENT
# Solo presencia de archivos y rutas de código conocidas. No imprime contenido.
for path in manage.py backend/manage.py app/manage.py web/manage.py \
            system_hub/urls.py system_hub/models.py system_hub/views.py \
            system_hub/apps.py requirements.txt pyproject.toml \
            compose.yaml docker-compose.yml; do
    if [ -f "$ROOT/$path" ]; then printf 'FOUND:%s\n' "$path"; else printf 'MISSING:%s\n' "$path"; fi
done
printf '%s\n' GEOPLAN_SOURCE_MAP_DONE
