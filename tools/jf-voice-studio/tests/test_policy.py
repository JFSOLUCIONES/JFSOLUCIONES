import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from policy import PolicyError, read_authorized_profile, require_approval, validate_profile_id


class PolicyTests(unittest.TestCase):
    def test_bad_profile_id(self):
        for value in ("../secret", "..", "/tmp/x", "x", "Ñ", "file.wav"):
            with self.assertRaises(PolicyError):
                validate_profile_id(value)

    def test_approval(self):
        for approved, disclosed in ((False, False), (True, False), (False, True)):
            with self.assertRaises(PolicyError):
                require_approval(approved=approved, ai_disclosed=disclosed)
        require_approval(approved=True, ai_disclosed=True)

    def test_profile_rights(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "demo_01.wav").write_bytes(b"RIFF")
            meta = base / "demo_01.json"
            def save(verified):
                meta.write_text(json.dumps({
                    "rights_verified": verified,
                    "allowed_use": "institutional_narration",
                    "reference_source": "licensed_synthetic",
                    "license_evidence": "registro-interno-001"
                }))
            save(False)
            with self.assertRaises(PolicyError):
                read_authorized_profile(base, "demo_01")
            save(True)
            self.assertEqual(read_authorized_profile(base, "demo_01"), base / "demo_01.wav")


if __name__ == "__main__":
    unittest.main()
