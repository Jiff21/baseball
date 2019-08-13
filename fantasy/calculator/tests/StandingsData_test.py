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


if __name__ == '__main__':
    unittest.main()
