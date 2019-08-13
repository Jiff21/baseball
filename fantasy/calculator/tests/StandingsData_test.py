import ast
import json
import os
import unittest
from calculator.mlbdotcom_teamscraper import StandingsData

class FunctionalTest(unittest.TestCase):

    def test_standing_object(self):
        test_data = os.path.join(
             os.path.dirname(__file__),
            './stubbed_data/single_team_standings.json'
        )
        with open(test_data) as f:
            double_quoted = f.read().replace('\'', "\"")
            standings_data = json.loads(double_quoted)
            assert isinstance(standings_data, dict)
        standings = StandingsData()
        wins = standings.get_wins(standings_data)
        assert wins == 77, 'did not get wins %d' % wins
        losses = standings.get_losses(standings_data)
        assert losses == 41, 'did not get expected losses %d' % losses

        wins_avg_right, loss_avg_right, g_v_right = standings.get_vs_right(standings_data)
        assert wins_avg_right == 0.6046511627906976, 'did not get expected wins_avg_right %d' % wins_avg_right
        assert loss_avg_right == 0.3953488372093023, 'did not get expected loss_avg_right %d' % loss_avg_right
        assert g_v_right == 86, 'did not get expected g_v_right %d' % g_v_right

        w_avg_road, l_avg_road, g_at_road = standings.get_at_road(standings_data)
        assert w_avg_road == 0.5666666666666667, 'did not get expected w_avg_road %d' % w_avg_road
        assert l_avg_road == 0.43333333333333335, 'did not get expected l_avg_road %d' % l_avg_road
        assert g_at_road == 60, 'did not get expected g_at_road %d' % g_at_road

if __name__ == '__main__':
    unittest.main()
