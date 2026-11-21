"""Isolated SQLite reference database: NOT a production PostgreSQL migration."""
import sqlite3
from pathlib import Path

SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS subscriptions(
  tenant_id TEXT PRIMARY KEY, active_from TEXT NOT NULL, expires_at TEXT NOT NULL,
  amount_pen INTEGER NOT NULL DEFAULT 500, duration_days INTEGER NOT NULL DEFAULT 30,
  receipt_reference TEXT NOT NULL, activated_by TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS projects(
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, name TEXT NOT NULL,
  category TEXT NOT NULL, created_by TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_projects_tenant ON projects(tenant_id);
CREATE TABLE IF NOT EXISTS surveys(
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
  tenant_id TEXT NOT NULL, input_epsg INTEGER NOT NULL, projected_epsg INTEGER NOT NULL,
  source_vertices_json TEXT NOT NULL, projected_vertices_json TEXT NOT NULL,
  area_m2 REAL NOT NULL, perimeter_m REAL NOT NULL, created_by TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_surveys_tenant_project ON surveys(tenant_id, project_id);
CREATE TABLE IF NOT EXISTS deliverables(
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
  tenant_id TEXT NOT NULL, discipline TEXT NOT NULL, file_sha256 TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft', author_id TEXT NOT NULL,
  reviewer_id TEXT, review_comment TEXT, reviewed_at TEXT, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_deliverables_tenant_project ON deliverables(tenant_id,project_id);
CREATE TABLE IF NOT EXISTS vouchers(
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, reference TEXT NOT NULL,
  amount_pen REAL NOT NULL, state TEXT NOT NULL DEFAULT 'pending_manual_check',
  created_by TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_logs(
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, actor_id TEXT NOT NULL,
  action TEXT NOT NULL, entity_type TEXT NOT NULL, entity_id TEXT,
  occurred_at TEXT NOT NULL
);
'''

def connect(path: str):
    c = sqlite3.connect(path, check_same_thread=False, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    return c

def initialize(path: str):
    if path != ':memory:':
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as conn:
        conn.executescript(SCHEMA)
