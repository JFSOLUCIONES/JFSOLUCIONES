"""Research-only immutable prediction snapshots and append-only settlement.
This SQLite ledger is NOT a horizontal-scale production ledger.
"""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json,sqlite3,uuid
from contextlib import contextmanager
from pathlib import Path

def _canonical(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def _utc(value):
    if not isinstance(value,str):raise ValueError("invalid_timestamp")
    d=datetime.fromisoformat(value.replace("Z","+00:00"))
    if not d.tzinfo:raise ValueError("timezone_required")
    return d.astimezone(timezone.utc)

class ResearchLedger:
    def __init__(self,path):
        self.path=str(path)
        Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.executescript("""PRAGMA journal_mode=WAL;
              CREATE TABLE IF NOT EXISTS predictions (
                id TEXT PRIMARY KEY,tenant TEXT NOT NULL,fixture_id TEXT NOT NULL,
                request_key TEXT NOT NULL,captured_at TEXT NOT NULL,
                payload TEXT NOT NULL,sha256 TEXT NOT NULL,
                UNIQUE(tenant,request_key));
              CREATE TABLE IF NOT EXISTS settlements (
                prediction_id TEXT PRIMARY KEY,settled_at TEXT NOT NULL,
                result_payload TEXT NOT NULL,result_sha256 TEXT NOT NULL,
                FOREIGN KEY(prediction_id) REFERENCES predictions(id));""")

    @contextmanager
    def db(self):
        db=sqlite3.connect(self.path,timeout=10,isolation_level="IMMEDIATE")
        db.row_factory=sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            with db:yield db
        finally:db.close()

    def record(self,tenant,request_key,payload):
        if not isinstance(tenant,str) or not tenant.startswith("org_") or len(tenant)>100:
            raise ValueError("tenant_invalid")
        if not isinstance(request_key,str) or not 8<=len(request_key)<=128:
            raise ValueError("request_key_invalid")
        if not isinstance(payload,dict):raise ValueError("payload_invalid")
        captured=_utc(payload.get("captured_at"))
        kickoff=_utc(payload.get("kickoff_utc"))
        if captured>=kickoff:raise ValueError("cannot_snapshot_after_kickoff")
        if not payload.get("fixture_id") or not payload.get("model_version") or not payload.get("market"):
            raise ValueError("incomplete_snapshot")
        if not payload.get("source_evidence"):raise ValueError("missing_source")
        p=payload.get("probability")
        if type(p) not in (int,float) or not 0<p<1:raise ValueError("probability_invalid")
        raw=_canonical(payload);sha=hashlib.sha256(raw.encode()).hexdigest()
        with self.db() as db:
            old=db.execute("SELECT * FROM predictions WHERE tenant=? AND request_key=?",(tenant,request_key)).fetchone()
            if old:
                if old["sha256"]!=sha:raise ValueError("idempotency_conflict")
                return old["id"]
            ident=str(uuid.uuid4())
            db.execute("INSERT INTO predictions VALUES (?,?,?,?,?,?,?)",
                       (ident,tenant,str(payload["fixture_id"]),request_key,captured.isoformat(),raw,sha))
            return ident

    def get(self,tenant,ident):
        with self.db() as db:
            row=db.execute("SELECT * FROM predictions WHERE tenant=? AND id=?",(tenant,ident)).fetchone()
            if row is None:return None
            value=dict(row);value["payload"]=json.loads(row["payload"])
            return value

    def settle(self,tenant,ident,settled_at,result):
        when=_utc(settled_at)
        if not isinstance(result,dict) or result.get("status")!="finished":
            raise ValueError("no_official_result")
        score=result.get("score")
        if not isinstance(score,list) or len(score)!=2 or any(type(v) is not int or v<0 for v in score):
            raise ValueError("invalid_score")
        with self.db() as db:
            row=db.execute("SELECT * FROM predictions WHERE tenant=? AND id=?",(tenant,ident)).fetchone()
            if not row:raise ValueError("no_prediction")
            original=json.loads(row["payload"])
            if when<=_utc(original["kickoff_utc"]):raise ValueError("settlement_before_kickoff")
            raw=_canonical(result);sha=hashlib.sha256(raw.encode()).hexdigest()
            old=db.execute("SELECT * FROM settlements WHERE prediction_id=?",(ident,)).fetchone()
            if old:
                if old["result_sha256"]!=sha:raise ValueError("immutable_settlement_conflict")
                return False
            db.execute("INSERT INTO settlements VALUES (?,?,?,?)",(ident,when.isoformat(),raw,sha))
            return True
