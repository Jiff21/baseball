import unittest
import json
import os
from pprint import pprint
from calculator.settings.standings import get_all_team_names

start_dir = os.path.dirname(__file__)
file_path = 'stubbed_data/team_hitting_season_leader_master.json'
full_path = os.path.join(start_dir, file_path)

with open(full_path) as data_file:
    TEAM_HITTING_STATS = json.load(data_file)

class StandingsTest(unittest.TestCase):

    def test_get_all_team_names(self):
        self.TEAM_STATS_DICT = TEAM_HITTING_STATS['team_hitting_season_leader_master']['queryResults']['row']
        self.teams = get_all_team_names(self.TEAM_STATS_DICT)
        assert len(self.teams) == 30, 'Did\'t get 30 teams. Instead' % len(self.teams)
        assert self.teams[0] == 'Houston', 'Houston was not the first team'
        assert self.teams[29] == 'San Diego', 'San Diego was not the last team'
        assert self.teams[25] == 'San Francisco', 'San Francisco was not the first team'

if __name__ == '__main__':
    unittest.main()
