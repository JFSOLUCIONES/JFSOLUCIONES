#!/usr/bin/env python3
"""Verifica estructura de patrimonio digital sin acceder a servidores ni secretos."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "docs" / "CATALOGO_ACTIVOS_PUBLICO.json"
DOCUMENTS = [
    ROOT / "docs" / "PATRIMONIO_DIGITAL_JF_SOLUCIONES.md",
    ROOT / "docs" / "LEGADO_DIGITAL_GUIA_DE_RECUPERACION.md",
    ROOT / "docs" / "MATRIZ_RECUPERACION_JF.md",
    ROOT / "docs" / "PLAN_QA_VOZ_VIDEO_2026.md",
]
def main() -> int:
    if not CATALOG.is_file() or any(not p.is_file() for p in DOCUMENTS):
        print("ERROR: falta algún archivo del patrimonio")
        return 1
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("github_repo_visibility", data.get("audit_summary", {}).get("github_repo_visibility")) != "public":
        print("ERROR: declaración de privacidad incoherente")
        return 1
    assets = data["assets"]
    ids = [a["id"] for a in assets]
    if len(ids) != len(set(ids)):
        print("ERROR: IDs duplicados")
        return 1
    for a in assets:
        if not {"id", "name", "category", "status"}.issubset(a):
            print("ERROR: ficha incompleta", a.get("id"))
            return 1
    summary = data["audit_summary"]
    groups = data["n8n_aggregates"]
    if sum(g["total"] for g in groups) != summary["n8n_visible_workflows"]:
        print("ERROR: suma de familias n8n incoherente")
        return 1
    if sum(g["activos"] for g in groups) != summary["n8n_active"]:
        print("ERROR: suma de activos n8n incoherente")
        return 1
    if summary["n8n_active"] + summary["n8n_inactive"] != summary["n8n_visible_workflows"]:
        print("ERROR: conteo activos/inactivos incoherente")
        return 1
    print(f"OK: {len(assets)} activos catalogados, {len(groups)} familias, {summary['n8n_visible_workflows']} workflows n8n (foto puntual)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
