"""JF SPORTS EDGE — pre-kickoff squad evidence adapter (original code).
No predictions, no human expert claims, no fabricated player availability.
"""
from __future__ import annotations
from datetime import datetime, timezone
from math import isfinite

ABSENT = {"injured", "suspended", "unavailable"}
LINEUP = {"confirmed", "expected", "unavailable"}


def utc(value):
    if not isinstance(value, str):
        raise ValueError("timestamp_required")
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as ex:
        raise ValueError("invalid_time") from ex
    if d.tzinfo is None:
        raise ValueError("timezone_required")
    return d.astimezone(timezone.utc)


def features(team, *, as_of, kickoff):
    """Use facts known BEFORE kickoff; record missing coverage as unknown.

    Input: {team_id, coverage:{injuries,lineup,player_statistics},
      lineup:{state,updated_at,starting_player_ids,bench_player_ids},
      absences:[{player_id,reason,provider,updated_at}],
      players:[{player_id,minutes,xg,xa}]}.
    xG+xA proxy is descriptive, NOT an effect on winning probabilities.
    """
    when = utc(as_of)
    if when >= utc(kickoff):
        raise ValueError("prediction_after_kickoff")
    if not isinstance(team, dict) or not team.get("team_id"):
        raise ValueError("team_id_required")
    flags = team.get("coverage")
    if not isinstance(flags, dict) or any(type(flags.get(k)) is not bool
        for k in ("injuries", "lineup", "player_statistics")):
        raise ValueError("coverage_required")
    lp = team.get("lineup")
    if not isinstance(lp, dict) or lp.get("state") not in LINEUP:
        raise ValueError("lineup_state_invalid")
    if utc(lp.get("updated_at")) > when:
        raise ValueError("future_lineup_leakage")
    starters = lp.get("starting_player_ids", [])
    bench = lp.get("bench_player_ids", [])
    if not isinstance(starters, list) or not isinstance(bench, list):
        raise ValueError("lineup_ids_invalid")
    if any(type(x) is not str or not x for x in starters + bench) or len(set(starters + bench)) != len(starters + bench):
        raise ValueError("duplicate_or_invalid_player")
    if lp["state"] == "confirmed" and (len(starters) != 11 or not flags["lineup"]):
        raise ValueError("confirmed_lineup_needs_11")
    if lp["state"] == "expected" and not flags["lineup"]:
        raise ValueError("no_expected_lineup_coverage")
    if lp["state"] == "unavailable" and (starters or bench):
        raise ValueError("unexpected_players_without_lineup")
    absents = team.get("absences", [])
    if not isinstance(absents, list) or (absents and not flags["injuries"]):
        raise ValueError("absence_coverage_invalid")
    missing_ids = set()
    for row in absents:
        if not isinstance(row, dict) or row.get("reason") not in ABSENT or not row.get("provider"):
            raise ValueError("absence_data_invalid")
        pid = row.get("player_id")
        if type(pid) is not str or not pid or pid in missing_ids:
            raise ValueError("duplicate_absence")
        if utc(row.get("updated_at")) > when:
            raise ValueError("future_absence_leakage")
        missing_ids.add(pid)
    if any(pid in starters for pid in missing_ids):
        raise ValueError("absent_marked_starter")
    players = team.get("players", [])
    if not isinstance(players, list) or (players and not flags["player_statistics"]):
        raise ValueError("player_stats_coverage_invalid")
    production = {}
    for row in players:
        if not isinstance(row, dict):
            raise ValueError("player_stats_invalid")
        pid = row.get("player_id")
        if type(pid) is not str or not pid or pid in production:
            raise ValueError("duplicate_stats")
        measures = [row.get(k) for k in ("minutes", "xg", "xa")]
        if any(type(v) not in (int,float) or not isfinite(v) or v < 0 for v in measures):
            raise ValueError("invalid_numeric_stat")
        production[pid] = float(row["xg"] + row["xa"])
    total = sum(production.values())
    return {
        "team_id": str(team["team_id"]), "as_of_utc": when.isoformat(),
        "lineup_state": lp["state"], "known_starters": len(starters),
        "absences_reported": len(missing_ids) if flags["injuries"] else None,
        "missing_information": [k for k in ("injuries","lineup","player_statistics") if not flags[k]],
        "absent_xg_xa_share_observed": round(sum(production.get(x,0) for x in missing_ids)/total,4)
            if total > 0 and flags["injuries"] and flags["player_statistics"] else None,
        "ready_for_feature_extraction": lp["state"] == "confirmed" and len(starters) == 11
            and flags["injuries"] and flags["player_statistics"],
        "prediction_calibrated": False
    }
