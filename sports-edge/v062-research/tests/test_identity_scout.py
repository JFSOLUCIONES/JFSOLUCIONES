import unittest
from jf_edge.identity import TeamRegistry, reconcile_fixture, IdentityError
from jf_edge.scout_evidence import normalize_team_report, ScoutError

AT='2026-11-21T09:00:00Z'
KICK='2026-11-21T13:00:00Z'

def rows():
    return [
        {'canonical':'team_a','competition':'Bundesliga','season':'2026-27',
         'identifiers':{'openfootball':'Club Azul (SINTETICO)','openligadb':'101','api-football':'301'}},
        {'canonical':'team_b','competition':'Bundesliga','season':'2026-27',
         'identifiers':{'openfootball':'Club Rojo (SINTETICO)','openligadb':'202','api-football':'302'}},
    ]

def fixtures():
    return (
        {'provider':'openligadb','competition':'Bundesliga','season':'2026-27',
         'fixture_id':'m1','home_id':'101','away_id':'202',
         'kickoff_utc':KICK,'observed_utc':'2026-11-21T08:58:00Z','status':'Programado'},
        {'provider':'api-football','competition':'Bundesliga','season':'2026-27',
         'fixture_id':'f1','home_id':'301','away_id':'302',
         'kickoff_utc':'2026-11-21T13:30:00Z',
         'observed_utc':'2026-11-21T08:58:00Z','status':'NS'}
    )

def scout():
    return {'team_id':'301','source':'API-FOOTBALL','observed_utc':AT,'absence_status':'verified_complete',
            'coverage':{'injuries':True,'lineups':True,'player_statistics':True},
            'lineup':{'state':'confirmed','starters':[str(i) for i in range(11)],
                      'bench':['11','12'],'confirmed_at':AT},
            'absences':[{'player_id':'13','reason':'injured','source':'API-FOOTBALL',
                         'observed_utc':AT}],
            'players':[{'player_id':'13','minutes':800,'xg':2.0,'xa':1.0,
                        'observed_utc':AT}]}

class CrossProviderFixtureTests(unittest.TestCase):
    def test_reconcile(self):
        p,s=fixtures(); r=reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
        self.assertEqual((r['canonical_home'],r['canonical_away']),('team_a','team_b'))
        self.assertTrue(r['provider_identity_verified'])
        self.assertFalse(r['prediction_ready'])
    def test_invalid_collision(self):
        v=rows();v[1]['identifiers']['openligadb']='101'
        with self.assertRaisesRegex(IdentityError,'collision'):TeamRegistry(v)
    def test_unmapped_team(self):
        p,s=fixtures();s['away_id']='999'
        with self.assertRaisesRegex(IdentityError,'unmapped'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_home_away_swapped(self):
        p,s=fixtures();s['away_id'],s['home_id']=s['home_id'],s['away_id']
        with self.assertRaisesRegex(IdentityError,'home_side'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_other_league(self):
        p,s=fixtures();s['competition']='Premier League'
        with self.assertRaisesRegex(IdentityError,'season_mismatch'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_stale_fixture(self):
        p,s=fixtures();s['observed_utc']='2026-11-20T00:00:00Z'
        with self.assertRaisesRegex(IdentityError,'stale'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_kickoff_mismatch(self):
        p,s=fixtures();s['kickoff_utc']='2026-11-21T18:30:00Z'
        with self.assertRaisesRegex(IdentityError,'kickoff_mismatch'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_started_match(self):
        p,s=fixtures();p['status']='LIVE'
        with self.assertRaisesRegex(IdentityError,'not_scheduled'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_future_snapshot(self):
        p,s=fixtures();p['observed_utc']='2026-11-21T10:00:00Z'
        with self.assertRaisesRegex(IdentityError,'future'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)
    def test_same_provider_is_not_confirmation(self):
        p,s=fixtures();s['provider']='openligadb';s['home_id']='101';s['away_id']='202'
        with self.assertRaisesRegex(IdentityError,'independent_provider'):reconcile_fixture(p,s,TeamRegistry(rows()),as_of=AT)

class LineupEvidenceTests(unittest.TestCase):
    def test_verified_evidence(self):
        report=normalize_team_report(scout(),as_of=AT,kickoff_utc=KICK)
        self.assertTrue(report['ready_for_contextual_analysis'])
        self.assertFalse(report['probabilities_calibrated'])
    def test_missing_injury_is_unknown(self):
        s=scout();s['coverage']['injuries']=False;s['absences']=[];s['absence_status']='unavailable'
        report=normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
        self.assertIsNone(report['known_absences'])
        self.assertIn('injuries',report['unknown_coverage'])
    def test_partial_injuries_are_not_declared_injury_free(self):
        s=scout();s['absences']=[];s['absence_status']='partial'
        report=normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
        self.assertIsNone(report['known_absences'])
        self.assertFalse(report['ready_for_contextual_analysis'])
    def test_unknown_lineup_not_confirmed(self):
        s=scout();s['lineup']={'state':'unavailable','starters':[],'bench':[]}
        report=normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
        self.assertFalse(report['ready_for_contextual_analysis'])
    def test_wrong_eleven(self):
        s=scout();s['lineup']['starters']=['1']
        with self.assertRaisesRegex(ScoutError,'11_players'):normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
    def test_absent_player_is_starter(self):
        s=scout();s['absences'][0]['player_id']='3'
        with self.assertRaisesRegex(ScoutError,'listed_absent'):normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
    def test_future_absence_not_allowed(self):
        s=scout();s['absences'][0]['observed_utc']='2026-11-22T09:00:00Z'
        with self.assertRaisesRegex(ScoutError,'future_absence'):normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
    def test_expected_lineup_not_ready(self):
        s=scout();s['lineup']['state']='expected'
        report=normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
        self.assertFalse(report['ready_for_contextual_analysis'])
    def test_injury_does_not_set_percent_penalty(self):
        report=normalize_team_report(scout(),as_of=AT,kickoff_utc=KICK)
        self.assertNotIn('win_probability_adjustment',report)

    def test_stale_confirmed_lineup_rejected(self):
        s=scout();s['lineup']['confirmed_at']='2026-11-19T09:00:00Z'
        with self.assertRaisesRegex(ScoutError,'lineup_confirmation_stale'):
            normalize_team_report(s,as_of=AT,kickoff_utc=KICK)
    def test_stale_absence_record_rejected(self):
        s=scout();s['absences'][0]['observed_utc']='2026-11-19T09:00:00Z'
        with self.assertRaisesRegex(ScoutError,'absence_stale'):
            normalize_team_report(s,as_of=AT,kickoff_utc=KICK)

if __name__=='__main__':unittest.main()
