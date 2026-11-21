"""Fail-closed readiness checks. Never authorizes automated cash wagering."""
from __future__ import annotations
from datetime import datetime,timezone,timedelta
from math import isfinite
MIN_HOLDOUT=250
MAX_ECE=0.05

def _dt(value):
    if not isinstance(value,str):raise ValueError("time_required")
    d=datetime.fromisoformat(value.replace("Z","+00:00"))
    if d.tzinfo is None:raise ValueError("timezone_required")
    return d.astimezone(timezone.utc)

def readiness(*,evidence:dict,fixture:dict,quote:dict|None,as_of:str):
    now=_dt(as_of);reasons=[]
    if not isinstance(evidence,dict) or not isinstance(fixture,dict):raise ValueError("data_required")
    market=fixture.get("market")
    if market not in ("local","empate","visitante","ambos_si","ambos_no",
                      "mas_1_5","menos_1_5","mas_2_5","menos_2_5"):
        reasons.append("market_not_supported")
    kickoff=_dt(fixture.get("kickoff_utc"))
    if kickoff<=now+timedelta(minutes=5):reasons.append("kickoff_too_close")
    if fixture.get("fixture_id") in (None,"") or fixture.get("home_id") in (None,"") or fixture.get("away_id") in (None,""):
        reasons.append("missing_fixture_identity")
    if fixture.get("home_id")==fixture.get("away_id"):reasons.append("same_team")
    if not fixture.get("fixture_provider"):reasons.append("fixture_source_missing")
    observed=_dt(fixture.get("fixture_observed_utc"))
    if observed>now:reasons.append("future_fixture_snapshot")
    if now-observed>timedelta(hours=6):reasons.append("fixture_stale")
    if evidence.get("market")!=market:reasons.append("different_market_evidence")
    if type(evidence.get("n")) is not int or evidence["n"]<MIN_HOLDOUT:reasons.append("insufficient_independent_holdout")
    metrics=evidence.get("metrics") or {}
    ece,brier,baseline=(metrics.get(k) for k in ("ece","brier","baseline_brier"))
    if any(type(x) not in (int,float) or not isfinite(x) for x in (ece,brier,baseline)):
        reasons.append("invalid_calibration_metrics")
    elif not (0<=ece<=MAX_ECE and 0<=brier<baseline):
        reasons.append("calibration_not_approved")
    if evidence.get("time_split_verified") is not True:reasons.append("walkforward_unverified")
    if evidence.get("asof_snapshots_verified") is not True:reasons.append("snapshot_integrity_unverified")
    if not evidence.get("model_version"):reasons.append("model_version_missing")
    if quote is None:reasons.append("verified_odds_missing")
    else:
        try:t=_dt(quote.get("observed_utc"))
        except (ValueError,TypeError):reasons.append("invalid_quote_timestamp")
        else:
            if t>now or now-t>timedelta(minutes=30):reasons.append("quote_stale")
        odds=quote.get("decimal_odds")
        if type(odds) not in (int,float) or not isfinite(odds) or odds<=1:reasons.append("invalid_quote")
        if quote.get("fixture_id")!=fixture.get("fixture_id") or quote.get("market")!=market:reasons.append("quote_fixture_market_mismatch")
        if not quote.get("licensed_provider"):reasons.append("quote_provenance_missing")
    return {"status":"PAPER_READY" if not reasons else "BLOCKED",
            "reasons":sorted(set(reasons)), "cash_betting_enabled":False}
