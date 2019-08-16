import json
import operator
import re
import requests
from datetime import datetime
from calculator.settings.logger import log
from calculator.settings.team_object import Team
from calculator.settings.api import BASE_URL, UPDATED_BASE_URL, TEAM_AWAY_URI, TEAM_AT_HOME_URI
from calculator.settings.api import TEAM_VS_LEFTY_URI, TEAM_VS_RIGHTY_URI
from calculator.settings.api import TEAM_STANDING_URI
from calculator.full_season_forecaster.pitcher_calculator import calculate_game
from calculator.scraper.standings_data import get_standings, StandingsData

from static.team_map import TEAM_MAP


def get_all_team_names(d):
    mlb = {}
    for t in d:
        print(t)
        team = Team()
        team.abbr = t
        team.id = d[t]
        mlb[team.abbr] = team
    return mlb

mlb = get_all_team_names(TEAM_MAP)

import pdb; pdb.set_trace()

# TODO : FIX URL Here
# from calculator.settings.api import TEAM_STATS_URI
TEAM_STATS_URI = 'named.team_hitting_season_leader_master.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&recSP=1&recPP=50'

def get_team_stats():
    CURRENT_URL = BASE_URL + TEAM_STATS_URI
    try:
        RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    # print(RESPONSE.text)
    # TEXT = RESPONSE.text.replace('\'', "\"")
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    TEAM_STATS_DICT = JSON_RESPONSE['team_hitting_season_leader_master']['queryResults']['row']
    return TEAM_STATS_DICT

TEAM_STATS_DICT = get_team_stats()

ALL_TEAM_SHORT_NAMES = []


# def get_all_team_names(d):
#     mlb = {}
#     for t in d:
#         team = Team()
#         team.short_name = t['team_short']
#         team.abbr = t['team_abbrev']
#         mlb[team.abbr] = team
#     return mlb
#
# mlb = get_all_team_names(TEAM_STATS_DICT)

def get_splits_by_uri(uri):
    CURRENT_URL = UPDATED_BASE_URL + uri
    try:
        RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    CURRENT_DICT = JSON_RESPONSE['team_hitting_season_leader_sit']['queryResults']['row']
    return CURRENT_DICT

TEAM_AT_HOME_DICT = get_splits_by_uri(TEAM_AT_HOME_URI)

def get_avg(number, total):
    return number / total

def get_relevant_splits_per_dict(splits_dict):
    log.debug('running get_relevant_splits_per_dict')
    r = int(splits_dict['r'])
    g = int(splits_dict['g'])
    runs_per_game = get_avg(r, g)

    h = int(splits_dict['h'])
    hits_per_game = get_avg(h, g)

    hr = int(splits_dict['hr'])
    hr_per_game = get_avg(hr, g)

    bb = int(splits_dict['bb'])
    waks_per_game = get_avg(bb, g)

    so = int(splits_dict['so'])
    so_per_game = get_avg(so, g)

    return runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game

def get_pitcher_splits_per_dict(splits_dict):
    log.debug('running get_pitcher_splits_per_dict')
    r = int(splits_dict['r'])

    plate_appearances = int(splits_dict['tpa'])
    runs_per_pa = get_avg(r, plate_appearances)

    h = int(splits_dict['h'])
    hits_per_pa = get_avg(h, plate_appearances)

    hr = int(splits_dict['hr'])
    hr_per_pa = get_avg(hr, plate_appearances)

    bb = int(splits_dict['bb'])
    walks_per_pa = get_avg(bb, plate_appearances)

    so = int(splits_dict['so'])
    so_per_pa = get_avg(so, plate_appearances)

    return runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa

for stats in TEAM_AT_HOME_DICT:
    log.debug('getting home splits')
    runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game = get_relevant_splits_per_dict(stats)
    mlb[stats['name_abbrev']].home_r_pg = runs_per_game
    mlb[stats['name_abbrev']].home_h_pg = hits_per_game
    mlb[stats['name_abbrev']].home_hr_pg = hr_per_game
    mlb[stats['name_abbrev']].home_bb_pg = waks_per_game
    mlb[stats['name_abbrev']].home_so_pg = so_per_game

TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)

for stats in TEAM_AWAY_DICT:
    log.debug('getting away splits')
    runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game = get_relevant_splits_per_dict(stats)
    mlb[stats['name_abbrev']].away_r_pg = runs_per_game
    mlb[stats['name_abbrev']].away_h_pg = hits_per_game
    mlb[stats['name_abbrev']].away_hr_pg = hr_per_game
    mlb[stats['name_abbrev']].away_bb_pg = waks_per_game
    mlb[stats['name_abbrev']].away_so_pg = so_per_game

TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY_URI)

for stats in TEAM_VS_LEFTY_DICT:
    log.debug('getting lefty splits')
    runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa = get_pitcher_splits_per_dict(stats)
    mlb[stats['name_abbrev']].vs_l_r_per_pa = runs_per_pa
    mlb[stats['name_abbrev']].vs_l_h_per_pa = hits_per_pa
    mlb[stats['name_abbrev']].vs_l_hr_per_pa = hr_per_pa
    mlb[stats['name_abbrev']].vs_l_bb_per_pa = walks_per_pa
    mlb[stats['name_abbrev']].vs_l_so_per_pa = so_per_pa

TEAM_VS_RIGHTY_DICT = get_splits_by_uri(TEAM_VS_RIGHTY_URI)

for stats in TEAM_VS_RIGHTY_DICT:
    log.debug('getting righty splits')
    runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa = get_pitcher_splits_per_dict(stats)
    mlb[stats['name_abbrev']].vs_r_r_per_pa = runs_per_pa
    mlb[stats['name_abbrev']].vs_r_h_per_pa = hits_per_pa
    mlb[stats['name_abbrev']].vs_r_hr_per_pa = hr_per_pa
    mlb[stats['name_abbrev']].vs_r_bb_per_pa = walks_per_pa
    mlb[stats['name_abbrev']].vs_r_so_per_pa = so_per_pa

# Get standings and win loss for splits
TEAM_STANDING_DICT = get_standings()
standings_data = StandingsData()

def set_league_standings_data():
    for current_standings in TEAM_STANDING_DICT:
        log.debug('getting standings data')
        assert isinstance(current_standings, dict), type(current_standings)

        wins = standings_data.get_wins(current_standings)
        mlb[current_standings['team_abbrev']].wins = wins

        losses = standings_data.get_losses(current_standings)
        mlb[current_standings['team_abbrev']].losses = standings_data.get_losses(current_standings)

        mlb[current_standings['team_abbrev']].games = standings_data.get_games_total(current_standings)

        mlb[current_standings['team_abbrev']].win_avg = standings_data.set_win_avg(current_standings)

        mlb[current_standings['team_abbrev']].loss_avg = standings_data.set_loss_avg(current_standings)

        wins_avg_left, loss_avg_left, g_v_left = standings_data.get_vs_left(current_standings)
        mlb[current_standings['team_abbrev']].wins_avg_left = wins_avg_left
        mlb[current_standings['team_abbrev']].losses_avg_left = loss_avg_left
        mlb[current_standings['team_abbrev']].g_v_left = g_v_left

        wins_avg_right, loss_avg_right, g_v_right = standings_data.get_vs_right(current_standings)
        mlb[current_standings['team_abbrev']].wins_avg_right = wins_avg_right
        mlb[current_standings['team_abbrev']].loss_avg_right = loss_avg_right
        mlb[current_standings['team_abbrev']].g_v_right = g_v_right

        w_avg_home, l_avg_home, g_at_home = standings_data.get_at_home(current_standings)
        mlb[current_standings['team_abbrev']].w_avg_home = wins_avg_right
        mlb[current_standings['team_abbrev']].l_avg_home = l_avg_home
        mlb[current_standings['team_abbrev']].g_at_home = g_at_home

        w_avg_road, l_avg_road, g_at_road = standings_data.get_at_road(current_standings)
        mlb[current_standings['team_abbrev']].w_avg_road = w_avg_road
        mlb[current_standings['team_abbrev']].l_avg_road = l_avg_road
        mlb[current_standings['team_abbrev']].g_at_road = g_at_road

        mlb[current_standings['team_abbrev']].run_avg = standings_data.get_run_avg(current_standings)

set_league_standings_data()

class SelfCalculated(object):

    def __init__(self):
        """get necessary data from standings."""
        pass

    def get_total_innings(self, team):
        innings = team.games * 9
        return innings

    def plate_appearances_per_game(self, team):
        innings = team.games * 9

        return innings


## Finish these just in case
self_calc = SelfCalculated()
innings = self_calc.get_total_innings(mlb['HOU'])
assert innings == 1089, 'TODO: Write test for innings %d' % innings


class TeamStatsNoSplit(object):

    def __init__(self):
        """get necessary data from standings."""
        pass

    def get_walks_per_game(self, current_dict):
        return int(current_dict['bb']) / int(current_dict['g'])

    def get_hits_per_game(self, current_dict):
        return int(current_dict['h']) / int(current_dict['g'])

    def get_runs_per_game(self, current_dict):
        return int(current_dict['r']) / int(current_dict['g'])

    def get_homeruns_per_game(self, current_dict):
        return int(current_dict['hr']) / int(current_dict['g'])

    def get_strikeouts_per_game(self, current_dict):
        return int(current_dict['so']) / int(current_dict['g'])

    def get_total_plate_appearance(self, current_dict):
        return int(current_dict['tpa'])

    def get_plate_appearences_per_game(self, current_dict):
        return int(current_dict['tpa']) / int(current_dict['g'])


team_stats = TeamStatsNoSplit()

# print(TEAM_STATS_DICT[0])

for t_stat in TEAM_STATS_DICT:
    log.debug('getting team stats (no split)')
    assert isinstance(t_stat, dict), type(t_stat)

    walks_per_game = team_stats.get_walks_per_game(t_stat)
    mlb[t_stat['team_abbrev']].walks_per_game = walks_per_game

    hits_per_game = team_stats.get_hits_per_game(t_stat)
    mlb[t_stat['team_abbrev']].hits_per_game = hits_per_game

    runs_per_game = team_stats.get_runs_per_game(t_stat)
    mlb[t_stat['team_abbrev']].runs_per_game = runs_per_game

    homeruns_per_game = team_stats.get_homeruns_per_game(t_stat)
    mlb[t_stat['team_abbrev']].homeruns_per_game = homeruns_per_game

    strikeouts_per_game = team_stats.get_strikeouts_per_game(t_stat)
    mlb[t_stat['team_abbrev']].strikeouts_per_game = strikeouts_per_game

    total_plate_appearances = team_stats.get_total_plate_appearance(t_stat)
    mlb[t_stat['team_abbrev']].total_plate_appearances = total_plate_appearances

    plate_appearences_per_game = team_stats.get_plate_appearences_per_game(t_stat)
    mlb[t_stat['team_abbrev']].plate_appearences_per_game = plate_appearences_per_game


# TODO: Write tests all of above
print('TODO: Write test for total_plate_appearances %f' % mlb['HOU'].total_plate_appearances)
# print(mlb['HOU'].plate_appearences_per_game)

for team in mlb:
    log.debug('calculating expected_game_no_spit')
    expected_game = calculate_game(
        7, # AVG innings starter (could improve)
        mlb[team].runs_per_game,
        mlb[team].walks_per_game,
        mlb[team].hits_per_game,
        mlb[team].homeruns_per_game,
        mlb[team].strikeouts_per_game,
        0, # Saves
        mlb[team].win_avg,
        mlb[team].loss_avg,
        0 # quality_starts
    )
    mlb[team].expected_game_no_spit = expected_game

# TODO Random stats to get for future/ general _expected
# mlb[stats['name_abbrev']].home_r_pg = runs_per_game
# mlb[stats['name_abbrev']].home_h_pg = hits_per_game
# mlb[stats['name_abbrev']].home_hr_pg = hr_per_game
# mlb[stats['name_abbrev']].home_bb_pg = waks_per_game

# TODO: Write tests
print('TODO: Write test for expected game all %f' % mlb['HOU'].expected_game_no_spit)

class SplitExpectedGame(object):

    def __init__(self):
        """get necessary data from standings."""
        pass

    def calculate_lefty_expected_game(self, team):
        log.debug('calculating expected_game_vs_left')
        started_expected_innings = 9
        expected_starter_plate_appearance = (started_expected_innings/float(9)) * mlb[team].plate_appearences_per_game
        splits_r_expected = mlb[team].vs_l_r_per_pa * expected_starter_plate_appearance
        splits_h_expected = mlb[team].vs_l_h_per_pa * expected_starter_plate_appearance
        splits_hr_expected = mlb[team].vs_l_hr_per_pa * expected_starter_plate_appearance
        splits_bb_expected = mlb[team].vs_l_bb_per_pa * expected_starter_plate_appearance
        splits_so_expected = mlb[team].vs_l_so_per_pa * expected_starter_plate_appearance
        expected_game = calculate_game(
            started_expected_innings, # AVG innings starter (could improve)
            splits_r_expected,
            splits_bb_expected,
            splits_h_expected,
            splits_hr_expected,
            splits_so_expected,
            0, # Saves
            mlb[team].wins_avg_left,
            mlb[team].losses_avg_left,
            0 # quality_starts
        )
        mlb[team].expected_game_lefty_spit = expected_game

    def calculate_righty_expected_game(self, team):
        log.debug('calculating righty expected game')
        started_expected_innings = 9
        expected_starter_plate_appearance = (started_expected_innings/float(9)) * mlb[team].plate_appearences_per_game
        splits_r_expected = mlb[team].vs_r_r_per_pa * expected_starter_plate_appearance
        splits_h_expected = mlb[team].vs_r_h_per_pa * expected_starter_plate_appearance
        splits_hr_expected = mlb[team].vs_r_hr_per_pa * expected_starter_plate_appearance
        splits_bb_expected = mlb[team].vs_r_bb_per_pa * expected_starter_plate_appearance
        splits_so_expected = mlb[team].vs_r_so_per_pa * expected_starter_plate_appearance
        expected_game = calculate_game(
            started_expected_innings, # AVG innings starter (could improve)
            splits_r_expected,
            splits_bb_expected,
            splits_h_expected,
            splits_hr_expected,
            splits_so_expected,
            0, # Saves
            mlb[team].wins_avg_right,
            mlb[team].loss_avg_right,
            0 # quality_starts
        )
        mlb[team].expected_game_righty_spit = expected_game

    def calculate_home_expected_game(self, team):
        log.debug('calculating home expected game')
        started_expected_innings = 9
        expected_game = calculate_game(
            started_expected_innings, # AVG innings starter (could improve)
            mlb[stats['name_abbrev']].home_r_pg,
            mlb[stats['name_abbrev']].home_bb_pg,
            mlb[stats['name_abbrev']].home_h_pg,
            mlb[stats['name_abbrev']].home_hr_pg,
            mlb[stats['name_abbrev']].home_so_pg,
            0, # Saves
            mlb[team].w_avg_home,
            mlb[team].l_avg_home,
            0 # quality_starts
        )
        mlb[team].expected_game_home_spit = expected_game


    def calculate_away_expected_game(self, team):
        log.debug('calculating home expected game')
        started_expected_innings = 9
        expected_game = calculate_game(
            started_expected_innings, # AVG innings starter (could improve)
            mlb[stats['name_abbrev']].away_r_pg,
            mlb[stats['name_abbrev']].away_bb_pg,
            mlb[stats['name_abbrev']].away_h_pg,
            mlb[stats['name_abbrev']].away_hr_pg,
            mlb[stats['name_abbrev']].away_so_pg,
            0, # Saves
            mlb[team].w_avg_road,
            mlb[team].l_avg_road,
            0 # quality_starts
        )
        mlb[team].expected_game_away_spit = expected_game

split_expected_game_calculator = SplitExpectedGame()

def calculate_all_team_expections():
    for team in mlb:
        split_expected_game_calculator.calculate_lefty_expected_game(team)
        split_expected_game_calculator.calculate_righty_expected_game(team)
        split_expected_game_calculator.calculate_home_expected_game(team)
        split_expected_game_calculator.calculate_away_expected_game(team)
        print('TODO: Write test for expected splits lefty. %s %f' % (
            team,
            mlb[team].expected_game_lefty_spit
            )
        )
        print('TODO: Write test for expected splits righty. %s %f' % (
            team,
            mlb[team].expected_game_righty_spit
            )
        )
        print('TODO: Write test for expected splits home. %s %f' % (
            team,
            mlb[team].expected_game_home_spit
            )
        )

        print('TODO: Write test for expected splits away. %s %f' % (
            team,
            mlb[team].expected_game_away_spit
            )
        )

calculate_all_team_expections()
## Something is off, home road splits produce higher projects then left right splits. should even out
