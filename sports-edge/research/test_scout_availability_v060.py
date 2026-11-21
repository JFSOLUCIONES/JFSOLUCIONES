"""Smoke tests for the public research adapter. No live keys or provider calls."""
import unittest
from datetime import timezone
from scout_availability_v060 import features

ASOF = "2026-11-21T10:00:00Z"
KICKOFF = "2026-11-21T15:00:00Z"


def sample():
    return {
        "team_id": "t1",
        "coverage": {"injuries": True, "lineup": True, "player_statistics": True},
        "lineup": {"state": "confirmed", "updated_at": ASOF,
            "starting_player_ids": [str(i) for i in range(11)],
            "bench_player_ids": ["11"]},
        "absences": [{"player_id": "12", "reason": "injured",
            "provider": "licensed_source", "updated_at": ASOF}],
        "players": [{"player_id": str(i), "minutes": 900,
            "xg": 1.0, "xa": 1.0} for i in range(13)],
    }


class AvailabilityTests(unittest.TestCase):
    def runit(self, data):
        return features(data, as_of=ASOF, kickoff=KICKOFF)

    def test_valid_confirmed_lineup(self):
        result = self.runit(sample())
        self.assertTrue(result["ready_for_feature_extraction"])
        self.assertEqual(result["absences_reported"], 1)
        self.assertEqual(result["prediction_calibrated"], False)

    def test_unknown_injuries_are_not_zero(self):
        data = sample()
        data["coverage"]["injuries"] = False
        data["absences"] = []
        self.assertIsNone(self.runit(data)["absences_reported"])

    def test_future_injury_rejected(self):
        data = sample()
        data["absences"][0]["updated_at"] = "2026-11-22T10:00:00Z"
        with self.assertRaises(ValueError):
            self.runit(data)

    def test_expected_not_confirmed(self):
        data = sample()
        data["lineup"]["state"] = "expected"
        self.assertFalse(self.runit(data)["ready_for_feature_extraction"])

    def test_absent_cannot_start(self):
        data = sample()
        data["absences"][0]["player_id"] = "0"
        with self.assertRaises(ValueError):
            self.runit(data)


if __name__ == "__main__":
    unittest.main()
