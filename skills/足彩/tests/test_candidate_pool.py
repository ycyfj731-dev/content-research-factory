import os
import sys
import unittest
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(__file__)
PARENT = os.path.dirname(HERE)
if PARENT not in sys.path:
    sys.path.insert(0, PARENT)

from candidate_pool import MatchSnapshot, TimedValue, filter_candidate_pool, ticket_time


UTC = timezone.utc


class CandidatePoolTests(unittest.TestCase):
    def test_ticket_time_is_earliest_kickoff_minus_30m(self):
        matches = [
            MatchSnapshot("late", datetime(2026, 9, 21, 15, 0, tzinfo=UTC), {"H": .5, "D": .3, "A": .2}),
            MatchSnapshot("early", datetime(2026, 9, 21, 12, 0, tzinfo=UTC), {"H": .5, "D": .3, "A": .2}),
        ]
        self.assertEqual(
            ticket_time(matches),
            datetime(2026, 9, 21, 11, 30, tzinfo=UTC),
        )

    def test_future_feature_is_rejected_for_whole_ticket_cutoff(self):
        cutoff = datetime(2026, 9, 21, 11, 30, tzinfo=UTC)
        legal = MatchSnapshot(
            "legal",
            datetime(2026, 9, 21, 12, 0, tzinfo=UTC),
            {"H": .5, "D": .3, "A": .2},
            features={"odds": TimedValue(2.0, cutoff - timedelta(minutes=1))},
        )
        leaked = MatchSnapshot(
            "leaked",
            datetime(2026, 9, 21, 20, 0, tzinfo=UTC),
            {"H": .5, "D": .3, "A": .2},
            features={"lineup": TimedValue("starting XI", cutoff + timedelta(hours=7))},
        )
        pool = filter_candidate_pool([legal, leaked], cutoff)
        self.assertEqual([m.match_id for m in pool], ["legal"])


if __name__ == "__main__":
    unittest.main()
