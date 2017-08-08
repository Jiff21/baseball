import unittest
import json
import os
from pprint import pprint
from calculator.settings.standings import get_all_team_names, get_splits_by_uri

start_dir = os.path.dirname(__file__)
team_stats = 'stubbed_data/team_hitting_season_leader_master.json'
full_path = os.path.join(start_dir, team_stats)

with open(full_path) as data_file:
    TEAM_HITTING_STATS = json.load(data_file)

hitting_away = 'stubbed_data/hitting_away.json'
away_path = os.path.join(start_dir, hitting_away)
with open(away_path) as data_file:
    HITTING_AWAY_SPLITS = json.load(data_file)


raw_standing_data = 'stubbed_data/team_standings_2018_08_07.json'
raw_standings_path = os.path.join(start_dir, raw_standing_data)
with open(raw_standings_path) as data_file:
    RAW_STANDINGS = json.load(data_file)
    TEAM_STANDING_DICT = JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])


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
