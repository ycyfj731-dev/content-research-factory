import os
import sys
import unittest

HERE = os.path.dirname(__file__)
PARENT = os.path.dirname(HERE)
if PARENT not in sys.path:
    sys.path.insert(0, PARENT)

from constraints import MatchMarket, optimize_min_path_gross
from optimizer import MatchProb, optimize_fixed_matches
from risk import exposure_map


def mp(match_id, h, d, a):
    return MatchProb(match_id, {"H": h, "D": d, "A": a})


class RiskTests(unittest.TestCase):
    def test_each_match_W_sums_to_ticket_coverage(self):
        matches = [mp(f"m{i}", .6, .3, .1) for i in range(1, 8)]
        sel = optimize_fixed_matches(matches)
        ex = exposure_map(sel)
        for m in matches:
            total = sum(ex[(m.match_id, o)].W_ir for o in ("H", "D", "A"))
            self.assertAlmostEqual(total, sel.coverage, places=15)

    def test_coverage_share_sums_to_one_per_match(self):
        matches = [mp(f"m{i}", .6, .3, .1) for i in range(1, 8)]
        sel = optimize_fixed_matches(matches)
        ex = exposure_map(sel)
        for m in matches:
            total = sum(ex[(m.match_id, o)].coverage_share for o in ("H", "D", "A"))
            self.assertAlmostEqual(total, 1.0, places=15)


class ConstraintTests(unittest.TestCase):
    def test_min_path_gross_filters_before_top8(self):
        matches = [mp(f"m{i}", .6, .3, .1) for i in range(1, 8)]
        # H is short-priced; D/A are longer. A sufficiently high gross-return
        # threshold forces the constrained ticket away from the pure COVER Top8.
        markets = [
            MatchMarket(m, {"H": 1.20, "D": 5.0, "A": 9.0})
            for m in matches
        ]
        cover = optimize_fixed_matches(matches)
        constrained = optimize_min_path_gross(markets, min_gross_return=20.0)
        self.assertLessEqual(constrained.coverage, cover.coverage)
        self.assertNotEqual(constrained.paths, cover.paths)


if __name__ == "__main__":
    unittest.main()
