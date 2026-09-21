import os
import sys
import unittest

HERE = os.path.dirname(__file__)
PARENT = os.path.dirname(HERE)
if PARENT not in sys.path:
    sys.path.insert(0, PARENT)

from optimizer import MatchProb, coverage, optimize_fixed_matches, optimize_joint, top_k_paths


def mp(match_id, h, d, a):
    return MatchProb(match_id, {"H": h, "D": d, "A": a})


class OptimizerTests(unittest.TestCase):
    def test_fixed_top8_are_highest_probability_paths(self):
        matches = [
            mp("m1", .70, .20, .10),
            mp("m2", .65, .25, .10),
            mp("m3", .60, .25, .15),
            mp("m4", .58, .27, .15),
            mp("m5", .56, .29, .15),
            mp("m6", .54, .31, .15),
            mp("m7", .52, .30, .18),
        ]
        selected = optimize_fixed_matches(matches)
        all_paths = top_k_paths(matches, k=3 ** 7)
        self.assertEqual(selected.paths, tuple(all_paths[:8]))

    def test_mutually_exclusive_path_coverage_is_sum(self):
        matches = [mp(f"m{i}", .6, .3, .1) for i in range(1, 8)]
        selected = optimize_fixed_matches(matches)
        self.assertAlmostEqual(
            selected.coverage,
            sum(p.probability for p in selected.paths),
            places=15,
        )

    def test_joint_search_counterexample(self):
        # First six matches are identical. Candidate A has higher max single-result
        # probability than B, but B's second branch is much larger and therefore
        # gives better Top-8 ticket coverage.
        base = [mp(f"m{i}", .70, .20, .10) for i in range(1, 7)]
        a = mp("A", .60, .20, .20)
        b = mp("B", .59, .40, .01)

        cover_a = optimize_fixed_matches(base + [a]).coverage
        cover_b = optimize_fixed_matches(base + [b]).coverage
        self.assertGreater(.60, .59)
        self.assertGreater(cover_b, cover_a)

        best = optimize_joint(base + [a, b])
        self.assertIn("B", [m.match_id for m in best.matches])
        self.assertNotIn("A", [m.match_id for m in best.matches])


if __name__ == "__main__":
    unittest.main()
