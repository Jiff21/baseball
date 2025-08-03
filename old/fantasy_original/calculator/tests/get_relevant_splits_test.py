import ast
import json
import os
import unittest
from calculator.mlbdotcom_teamscraper import get_relevant_splits_per_dict

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
        run_avg, hit_avg, hr_avg, walk_avg= get_relevant_splits_per_dict(test_team_home_split)
        assert run_avg == 6.464285714285714, 'incorrect run_avg %f' % run_avg
        assert hit_avg == 10.875000, 'incorrect hit_avg %f' % hit_avg
        assert hr_avg == 1.500000, 'incorrect hr_avg %f' % hr_avg
        assert walk_avg == 3.285714, 'incorrect walk_avg %f' % walk_avg


if __name__ == '__main__':
    unittest.main()
