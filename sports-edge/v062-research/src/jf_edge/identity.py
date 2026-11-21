"""JF SPORTS EDGE — explicit provider identity registry and fixture reconciliation.

Research adapter. External provider IDs MUST be mapped explicitly. Never match
teams by a fuzzy name, a crest or a similar-looking fixture by default.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from unicodedata import normalize

PROVIDERS = frozenset(('openfootball', 'openligadb', 'api-football'))

class IdentityError(ValueError):
    pass

def _text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 160:
        raise IdentityError(f'{label}_invalid')
    return normalize('NFKC', value).strip()

def _instant(value, label):
    try:
        d = datetime.fromisoformat(_text(value, label).replace('Z', '+00:00'))
    except (TypeError, ValueError) as exc:
        raise IdentityError(f'{label}_invalid') from exc
    if d.tzinfo is None:
        raise IdentityError(f'{label}_timezone_required')
    return d.astimezone(timezone.utc)

class TeamRegistry:
    """Rows: {canonical, competition, season, identifiers:{provider:exact id}}."""

    def __init__(self, rows):
        if not isinstance(rows, list) or not rows:
            raise IdentityError('registry_empty')
        self.by_provider = {}
        self.canonical = set()
        for row in rows:
            if not isinstance(row, dict):
                raise IdentityError('registry_record_invalid')
            name = _text(row.get('canonical'), 'canonical')
            league = _text(row.get('competition'), 'competition')
            season = _text(row.get('season'), 'season')
            entry = (league, season, name)
            if entry in self.canonical:
                raise IdentityError('duplicate_canonical_team')
            self.canonical.add(entry)
            refs = row.get('identifiers')
            if not isinstance(refs, dict) or not refs:
                raise IdentityError('identifiers_missing')
            for provider, raw in refs.items():
                if provider not in PROVIDERS:
                    raise IdentityError('provider_not_allowed')
                value = _text(str(raw) if type(raw) is int else raw, 'provider_team_id')
                key = (league, season, provider, value.casefold())
                if key in self.by_provider:
                    raise IdentityError('provider_identity_collision')
                self.by_provider[key] = name

    def resolve(self, *, competition, season, provider, team_id):
        if provider not in PROVIDERS:
            raise IdentityError('provider_not_allowed')
        value = _text(str(team_id) if type(team_id) is int else team_id, 'team_id')
        key = (_text(competition, 'competition'), _text(season, 'season'),
               provider, value.casefold())
        if key not in self.by_provider:
            raise IdentityError('team_unmapped')
        return self.by_provider[key]

def reconcile_fixture(primary, secondary, registry, *, as_of, max_delta_minutes=120):
    """Verify same competition, season, ordered teams and compatible time.

    This only verifies identity, not lineups, injuries or odds.
    """
    if not isinstance(primary, dict) or not isinstance(secondary, dict):
        raise IdentityError('fixture_record_invalid')
    if not isinstance(registry, TeamRegistry):
        raise IdentityError('registry_invalid')
    now = _instant(as_of, 'as_of')
    league, season = primary.get('competition'), primary.get('season')
    if league != secondary.get('competition') or season != secondary.get('season'):
        raise IdentityError('league_or_season_mismatch')
    if primary.get('provider') == secondary.get('provider'):
        raise IdentityError('independent_provider_required')
    if not isinstance(max_delta_minutes, int) or not 0 <= max_delta_minutes <= 180:
        raise IdentityError('kickoff_tolerance_invalid')
    identities = []
    for event in (primary, secondary):
        src = event.get('provider')
        home = registry.resolve(competition=league, season=season,
                                provider=src, team_id=event.get('home_id'))
        away = registry.resolve(competition=league, season=season,
                                provider=src, team_id=event.get('away_id'))
        if home == away:
            raise IdentityError('same_team')
        _text(event.get('fixture_id'), 'fixture_id')
        observed = _instant(event.get('observed_utc'), 'observed')
        if observed > now or now-observed > timedelta(hours=6):
            raise IdentityError('stale_or_future_fixture')
        kickoff = _instant(event.get('kickoff_utc'), 'kickoff')
        if kickoff <= now + timedelta(minutes=5):
            raise IdentityError('fixture_started_or_too_close')
        if event.get('status') not in ('NS', 'Programado', 'scheduled'):
            raise IdentityError('not_scheduled')
        identities.append((home, away, kickoff))
    if identities[0][:2] != identities[1][:2]:
        raise IdentityError('teams_or_home_side_mismatch')
    delta = abs((identities[0][2]-identities[1][2]).total_seconds())
    if delta > max_delta_minutes*60:
        raise IdentityError('kickoff_mismatch')
    return {
        'canonical_home': identities[0][0],
        'canonical_away': identities[0][1],
        'competition': league, 'season': season,
        'primary_fixture_id': primary['fixture_id'],
        'secondary_fixture_id': secondary['fixture_id'],
        'kickoff_utc': identities[0][2].isoformat(),
        'provider_identity_verified': True,
        'injuries_verified': False, 'odds_verified': False,
        'prediction_ready': False,
    }
