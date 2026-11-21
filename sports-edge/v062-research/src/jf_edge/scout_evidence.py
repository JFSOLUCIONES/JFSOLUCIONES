"""JF SPORTS EDGE — point-in-time scouting data-quality gates.

Does not scrape or generate player data. It validates the evidence furnished by a
licensed source. No injury report is NOT proof of an injury-free team.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from math import isfinite

class ScoutError(ValueError):
    pass

def _time(v):
    if not isinstance(v,str):raise ScoutError('timestamp_required')
    try:x=datetime.fromisoformat(v.replace('Z','+00:00'))
    except ValueError as exc:raise ScoutError('timestamp_invalid') from exc
    if x.tzinfo is None:raise ScoutError('timezone_required')
    return x.astimezone(timezone.utc)

def _ids(values, name):
    if not isinstance(values,list) or any(type(x) not in (str,int) or not str(x) for x in values):
        raise ScoutError(f'{name}_invalid')
    out=[str(v) for v in values]
    if len(set(out))!=len(out):raise ScoutError(f'{name}_duplicate')
    return out

def normalize_team_report(raw, *, as_of, kickoff_utc):
    if not isinstance(raw,dict) or not raw.get('team_id') or not raw.get('source'):
        raise ScoutError('team_or_source_missing')
    now=_time(as_of); kick=_time(kickoff_utc)
    if kick<=now:raise ScoutError('match_already_started')
    fields=('injuries','lineups','player_statistics')
    coverage=raw.get('coverage') or {}
    if not isinstance(coverage,dict) or any(type(coverage.get(k)) is not bool for k in fields):
        raise ScoutError('coverage_flags_required')
    updated=_time(raw.get('observed_utc'))
    if updated>now:raise ScoutError('future_team_information')
    if now-updated>timedelta(hours=24):raise ScoutError('team_report_stale')
    lineup=raw.get('lineup') or {}
    if not isinstance(lineup,dict):raise ScoutError('invalid_lineup')
    state=lineup.get('state','unavailable')
    if state not in ('confirmed','expected','unavailable'):
        raise ScoutError('lineup_state_invalid')
    starters=_ids(lineup.get('starters',[]),'starters')
    bench=_ids(lineup.get('bench',[]),'bench')
    if set(starters)&set(bench):raise ScoutError('starter_on_bench')
    if state!='unavailable' and not coverage['lineups']:
        raise ScoutError('lineup_without_coverage')
    if state=='confirmed' and len(starters)!=11:
        raise ScoutError('confirmed_lineup_needs_11_players')
    if state=='unavailable' and (starters or bench):
        raise ScoutError('unknown_lineup_has_players')
    if state=='confirmed':
        confirmation=_time(lineup.get('confirmed_at'))
        if confirmation>now:raise ScoutError('future_lineup_confirmation')
        if now-confirmation>timedelta(hours=24):raise ScoutError('lineup_confirmation_stale')
    absence_status=raw.get('absence_status','partial')
    if absence_status not in ('verified_complete','partial','unavailable'):
        raise ScoutError('absence_status_invalid')
    if absence_status=='verified_complete' and not coverage['injuries']:
        raise ScoutError('complete_absences_without_coverage')
    absences=raw.get('absences',[])
    if not isinstance(absences,list):raise ScoutError('absences_invalid')
    if absences and not coverage['injuries']:
        raise ScoutError('absence_without_coverage')
    absence_ids=[]
    for record in absences:
        if not isinstance(record,dict) or not record.get('source') or record.get('reason') not in ('injured','suspended','unavailable'):
            raise ScoutError('absence_record_invalid')
        player=record.get('player_id')
        if type(player) not in (str,int) or not str(player):raise ScoutError('absence_player_invalid')
        at=_time(record.get('observed_utc'))
        if at>now:raise ScoutError('future_absence')
        if now-at>timedelta(hours=24):raise ScoutError('absence_stale')
        absence_ids.append(str(player))
    if len(set(absence_ids))!=len(absence_ids):raise ScoutError('duplicate_absence')
    if set(absence_ids)&set(starters):raise ScoutError('starter_listed_absent')
    stats=raw.get('players',[])
    if not isinstance(stats,list) or (stats and not coverage['player_statistics']):
        raise ScoutError('player_stats_without_coverage')
    seen=set()
    for record in stats:
        if not isinstance(record,dict):raise ScoutError('player_stat_invalid')
        raw_id=record.get('player_id')
        if type(raw_id) not in (str,int) or not str(raw_id):raise ScoutError('player_id_invalid')
        pid=str(raw_id)
        if pid in seen:raise ScoutError('duplicate_player_stat')
        seen.add(pid)
        for key in ('minutes','xg','xa'):
            value=record.get(key)
            if type(value) not in (int,float) or not isfinite(value) or value<0:
                raise ScoutError('player_stat_value_invalid')
        if _time(record.get('observed_utc'))>now:raise ScoutError('future_player_stat')
    unknown=[k for k in fields if not coverage[k]]
    return {
        'team_id':str(raw['team_id']), 'source':raw['source'],
        'as_of_utc':now.isoformat(), 'lineup_state':state,
        'starting_eleven_count':len(starters) if coverage['lineups'] else None,
        'reported_absence_count':len(absence_ids),
        'known_absences':len(absence_ids) if absence_status=='verified_complete' else None,
        'absence_status':absence_status,
        'unknown_coverage':unknown,
        'ready_for_contextual_analysis':state=='confirmed' and absence_status=='verified_complete' and coverage['player_statistics'],
        'probabilities_calibrated':False,
    }
