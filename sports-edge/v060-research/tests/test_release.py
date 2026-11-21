"""Reproducible unit regression tests, no network, no credentials."""
import sys, unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import date
import json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jf_edge.market_math import market_probabilities, fair_odds, expected_value
from jf_edge.quality_gate import readiness
from jf_edge.learn_offline import load_matches, poisson_probs, temp_scale

NOW="2026-11-21T09:00:00Z"
KICK="2026-11-21T13:00:00Z"
FIX={"fixture_id":"400","home_id":"10","away_id":"20","kickoff_utc":KICK,
     "fixture_observed_utc":"2026-11-21T08:55:00Z","fixture_provider":"provider","market":"local"}
EVID={"market":"local","n":306,
      "metrics":{"ece":0.07593,"brier":0.59344,"baseline_brier":0.64797},
      "time_split_verified":True,"asof_snapshots_verified":False,
      "model_version":"JF_POISSON_CC0_WALKFORWARD_0.1"}
QUOTE={"fixture_id":"400","market":"local","decimal_odds":2.2,
       "observed_utc":"2026-11-21T08:59:00Z","licensed_provider":"licensed-data"}

class QA(unittest.TestCase):
    def test_market_masses(self):
        m=market_probabilities(1.55,1.2)
        for keys in (("local","empate","visitante"),("ambos_si","ambos_no"),
                     ("mas_1_5","menos_1_5"),("mas_2_5","menos_2_5")):
            self.assertAlmostEqual(sum(m[k] for k in keys),1.0,places=7)
        self.assertAlmostEqual(m["doble_1x"],m["local"]+m["empate"],places=7)
    def test_fair_odds_and_ev(self):
        self.assertEqual(fair_odds(0.5),2)
        self.assertAlmostEqual(expected_value(0.5,2.2),0.1)
    def test_invalid_rates(self):
        with self.assertRaises(ValueError):market_probabilities(-1,2)
    def test_invalid_odds(self):
        with self.assertRaises(ValueError):expected_value(0.6,1)
    def test_pilot_model_blocked(self):
        g=readiness(evidence=EVID,fixture=FIX,quote=QUOTE,as_of=NOW)
        self.assertEqual(g["status"],"BLOCKED")
        self.assertIn("calibration_not_approved",g["reasons"])
        self.assertFalse(g["cash_betting_enabled"])
    def test_missing_odds(self):
        g=readiness(evidence=EVID,fixture=FIX,quote=None,as_of=NOW)
        self.assertIn("verified_odds_missing",g["reasons"])
    def test_stale_fixture(self):
        g=readiness(evidence=EVID,fixture={**FIX,"fixture_observed_utc":"2026-11-20T08:00:00Z"},quote=QUOTE,as_of=NOW)
        self.assertIn("fixture_stale",g["reasons"])
    def test_future_quote(self):
        g=readiness(evidence=EVID,fixture=FIX,quote={**QUOTE,"observed_utc":"2026-11-21T10:00:00Z"},as_of=NOW)
        self.assertIn("quote_stale",g["reasons"])
    def test_different_market_not_interchangeable(self):
        g=readiness(evidence=EVID,fixture={**FIX,"market":"ambos_si"},quote=QUOTE,as_of=NOW)
        self.assertIn("different_market_evidence",g["reasons"])
    def test_paper_only_even_with_better_evidence(self):
        evidence={**EVID,"asof_snapshots_verified":True,
                  "metrics":{"ece":0.03,"brier":0.54,"baseline_brier":0.64}}
        g=readiness(evidence=evidence,fixture=FIX,quote=QUOTE,as_of=NOW)
        self.assertEqual(g["status"],"PAPER_READY")
        self.assertFalse(g["cash_betting_enabled"])
    def test_flat_score_00_historical(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"2025-26";p.mkdir()
            (p/"de.1.json").write_text(json.dumps({"matches":[
                {"date":"2025-09-01","team1":"A","team2":"B","score":[0,0]},
                {"date":"2025-09-02","team1":"C","team2":"D","score":{"ft":[2,1]}}]}))
            self.assertEqual(len(load_matches(Path(d),"de.1",date(2026,11,21))),2)
    def test_flat_score_current_season_is_not_result(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"2026-27";p.mkdir()
            (p/"de.1.json").write_text(json.dumps({"matches":[
                {"date":"2026-11-20","team1":"A","team2":"B","score":[0,0]}]}))
            with self.assertRaises(ValueError):load_matches(Path(d),"de.1",date(2026,11,21))
    def test_historical_poisson_mass(self):
        self.assertAlmostEqual(sum(poisson_probs(1.55,1.2)),1.0)
        self.assertAlmostEqual(sum(temp_scale([0.3,0.3,0.4],1.2)),1.0)

if __name__=="__main__":unittest.main()
