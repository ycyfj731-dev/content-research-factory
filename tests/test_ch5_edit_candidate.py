"""Offline review gate for the unapproved Chapter 5 candidate edit plan."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "projects/youtube/001-therapy-speak/visual-batch-v1"


class TestChapter5EditCandidate(unittest.TestCase):
    def test_boundaries_and_no_premature_speech(self):
        plan = json.loads((ROOT / "ch5-edit-candidate-v1.json").read_text(encoding="utf-8"))
        evidence = json.loads((ROOT / "ch5-pilot-evidence-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["state"], "REVIEW_ONLY_NOT_APPROVED")
        self.assertEqual(plan["media_status"], "NO_RENDER_OR_GENERATION")
        shots = plan["edit_intervals"]
        self.assertEqual([s["unit_id"] for s in shots], ["VC-27","VC-28","VC-29","VC-30"])
        for i, (shot, source) in enumerate(zip(shots, evidence["units"])):
            self.assertEqual(shot["unit_id"], source["unit_id"])
            self.assertEqual(shot["verified_speech_start"], source["spoken_first_word_seconds"])
            self.assertEqual(shot["verified_speech_end"], source["spoken_last_word_seconds"])
            self.assertLessEqual(shot["proposed_cut_in"], shot["verified_speech_start"])
            self.assertGreaterEqual(shot["proposed_cut_out"], shot["verified_speech_end"])
            self.assertEqual(shot["cut_status"], "EDITORIAL_PROPOSAL")
            self.assertEqual(shot["asset_status"], "PENDING_EDITORIAL_AND_RIGHTS_REVIEW")
            if i:
                self.assertAlmostEqual(shots[i-1]["proposed_cut_out"], shot["proposed_cut_in"], places=3)
                self.assertLess(source["spoken_first_word_seconds"], source["spoken_last_word_seconds"])
        self.assertNotIn("APPROVED", {s["cut_status"] for s in shots})

    def test_who_not_fake_archive(self):
        plan = json.loads((ROOT / "ch5-edit-candidate-v1.json").read_text(encoding="utf-8"))
        who = plan["edit_intervals"][2]
        self.assertEqual(who["asset"], "source-verified-typeset")
        self.assertIn("NOT a simulated WHO webpage", who["primary"])
        self.assertIn("rights", " ".join(plan["requirements"]).lower())


if __name__ == "__main__":
    unittest.main()
