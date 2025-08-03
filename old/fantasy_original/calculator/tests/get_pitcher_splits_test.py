import ast
import json
import os
import unittest
from calculator.mlbdotcom_teamscraper import get_pitcher_splits_per_dict

class FunctionalTest(unittest.TestCase):

    def test_steaming(self):
        test_data = os.path.join(
             os.path.dirname(__file__),
            './stubbed_data/get_relevant_splits.json'
        )
        with open(test_data) as f:
            double_quoted = f.read().replace('\'', "\"")
            test_team_home_split = json.loads(double_quoted)
            assert isinstance(test_team_home_split, dict)
        assert(int(test_team_home_split['tpa'])) == 2214, 'Unexpected tpa' % int(test_team_home_split['tpa'])
        assert(int(test_team_home_split['r'])) == 362, 'Unexpected r %d' % int(test_team_home_split['r'])
        runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa = get_pitcher_splits_per_dict(test_team_home_split)
        assert runs_per_pa == 0.16350496838301717, 'incorrect runs_per_pa %f' % runs_per_pa
        assert hits_per_pa == 0.2750677506775068, 'incorrect hits_per_pa %f' % hits_per_pa
        assert hr_per_pa == 0.037940379403794036, 'incorrect hr_per_pa %f' % hr_per_pa
        assert walks_per_pa == 0.08310749774164408, 'incorrect walks_per_pa %f' % walks_per_pa


if __name__ == '__main__':
    unittest.main()
