import json
import operator
import re
import requests
from datetime import datetime
from calculator.full_season_forecaster.pitcher_calculator import calculate_game
from calculator.scraper.league import get_all_team_names
from calculator.scraper.standings_data import get_standings, StandingsData
from calculator.settings.api import BASE_URL, UPDATED_BASE_URL, TEAM_AWAY_URI, TEAM_AT_HOME_URI
from calculator.settings.api import TEAM_VS_LEFTY_URI, TEAM_VS_RIGHTY_URI
from calculator.settings.api import TEAM_STANDING_URL
from calculator.settings.logger import log
from static.team_map import TEAM_MAP

# Todo Test that find by ID gets correct team from api
mlb = get_all_team_names(TEAM_MAP)

# import pdb; pdb.set_trace()
from calculator.scraper.team_hitting_stats import get_team_stats
TEAM_STATS_DICT = get_team_stats()

from calculator.scraper.team_splits_stats import SplitsScraper

split_scraper = SplitsScraper()
TEAM_AT_HOME_DICT = split_scraper.get_splits_by_uri(TEAM_AT_HOME_URI)


#
# def get_relevant_splits_per_dict(splits_dict):
#     log.debug('running get_relevant_splits_per_dict')
#     r = int(splits_dict['r'])
#     g = int(splits_dict['g'])
#     runs_per_game = get_avg(r, g)
#
#     h = int(splits_dict['h'])
#     hits_per_game = get_avg(h, g)
#
#     hr = int(splits_dict['hr'])
#     hr_per_game = get_avg(hr, g)
#
#     bb = int(splits_dict['bb'])
#     waks_per_game = get_avg(bb, g)
#
#     so = int(splits_dict['so'])
#     so_per_game = get_avg(so, g)
#
#     return runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game


for stats in TEAM_AT_HOME_DICT:
    log.debug('getting home splits')
    runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game = split_scraper.get_relevant_splits_per_dict(stats)
    mlb[stats['teamAbbrev']].home_r_pg = runs_per_game
    mlb[stats['teamAbbrev']].home_h_pg = hits_per_game
    mlb[stats['teamAbbrev']].home_hr_pg = hr_per_game
    mlb[stats['teamAbbrev']].home_bb_pg = waks_per_game
    mlb[stats['teamAbbrev']].home_so_pg = so_per_game

TEAM_AWAY_DICT = split_scraper.get_splits_by_uri(TEAM_AWAY_URI)

for stats in TEAM_AWAY_DICT:
    log.debug('getting away splits')
    runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game = split_scraper.get_relevant_splits_per_dict(stats)
    mlb[stats['teamAbbrev']].away_r_pg = runs_per_game
    mlb[stats['teamAbbrev']].away_h_pg = hits_per_game
    mlb[stats['teamAbbrev']].away_hr_pg = hr_per_game
    mlb[stats['teamAbbrev']].away_bb_pg = waks_per_game
    mlb[stats['teamAbbrev']].away_so_pg = so_per_game

TEAM_VS_LEFTY_DICT = split_scraper.get_splits_by_uri(TEAM_VS_LEFTY_URI)


for stats in TEAM_VS_LEFTY_DICT:
    log.debug('getting lefty splits')
    runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa = split_scraper.get_pitcher_rl_splits_per_dict(stats)
    mlb[stats['teamAbbrev']].vs_l_r_per_pa = runs_per_pa
    mlb[stats['teamAbbrev']].vs_l_h_per_pa = hits_per_pa
    mlb[stats['teamAbbrev']].vs_l_hr_per_pa = hr_per_pa
    mlb[stats['teamAbbrev']].vs_l_bb_per_pa = walks_per_pa
    mlb[stats['teamAbbrev']].vs_l_so_per_pa = so_per_pa

TEAM_VS_RIGHTY_DICT = split_scraper.get_splits_by_uri(TEAM_VS_RIGHTY_URI)

for stats in TEAM_VS_RIGHTY_DICT:
    log.debug('getting righty splits')
    rbi_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa = split_scraper.get_pitcher_rl_splits_per_dict(stats)
    mlb[stats['teamAbbrev']].vs_r_r_per_pa = rbi_per_pa
    mlb[stats['teamAbbrev']].vs_r_h_per_pa = hits_per_pa
    mlb[stats['teamAbbrev']].vs_r_hr_per_pa = hr_per_pa
    mlb[stats['teamAbbrev']].vs_r_bb_per_pa = walks_per_pa
    mlb[stats['teamAbbrev']].vs_r_so_per_pa = so_per_pa

# Get standings and win loss for splits
TEAM_STANDING_DICT = get_standings()
standings_data = StandingsData()

def set_league_standings_data(current_standings_dict):
    assert isinstance(current_standings_dict, list), type(current_standings_dict)
    for current_standings in current_standings_dict:
        log.debug('\n\n getting set_league_standings_data data')
        print(current_standings['team']['abbreviation'])
        log.debug('\n\n')
        assert isinstance(current_standings, dict), type(current_standings)

        wins = standings_data.get_wins(current_standings)
        log.debug(wins)

        mlb[current_standings['team']['abbreviation']].wins = wins

        losses = standings_data.get_losses(current_standings)
        mlb[current_standings['team']['abbreviation']].losses = standings_data.get_losses(current_standings)

        mlb[current_standings['team']['abbreviation']].games = standings_data.get_games_total(current_standings)

        mlb[current_standings['team']['abbreviation']].win_avg = standings_data.set_win_avg(current_standings)

        mlb[current_standings['team']['abbreviation']].loss_avg = standings_data.set_loss_avg(current_standings)

        wins_avg_left, loss_avg_left, g_v_left = standings_data.get_vs_left(current_standings)
        mlb[current_standings['team']['abbreviation']].wins_avg_left = wins_avg_left
        mlb[current_standings['team']['abbreviation']].losses_avg_left = loss_avg_left
        mlb[current_standings['team']['abbreviation']].g_v_left = g_v_left

        wins_avg_right, loss_avg_right, g_v_right = standings_data.get_vs_right(current_standings)
        mlb[current_standings['team']['abbreviation']].wins_avg_right = wins_avg_right
        mlb[current_standings['team']['abbreviation']].loss_avg_right = loss_avg_right
        mlb[current_standings['team']['abbreviation']].g_v_right = g_v_right

        w_avg_home, l_avg_home, g_at_home = standings_data.get_at_home(current_standings)
        mlb[current_standings['team']['abbreviation']].w_avg_home = wins_avg_right
        mlb[current_standings['team']['abbreviation']].l_avg_home = l_avg_home
        mlb[current_standings['team']['abbreviation']].g_at_home = g_at_home

        w_avg_road, l_avg_road, g_at_road = standings_data.get_at_road(current_standings)
        mlb[current_standings['team']['abbreviation']].w_avg_road = w_avg_road
        mlb[current_standings['team']['abbreviation']].l_avg_road = l_avg_road
        mlb[current_standings['team']['abbreviation']].g_at_road = g_at_road

        mlb[current_standings['team']['abbreviation']].run_avg = standings_data.get_run_avg(current_standings)

set_league_standings_data(TEAM_STANDING_DICT)

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
# assert innings == 1089, 'TODO: Write test for innings %d' % innings


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

for t_stat in TEAM_STATS_DICT:
    log.debug('getting team stats (no split)')
    assert isinstance(t_stat, dict), type(t_stat)

    walks_per_game = team_stats.get_walks_per_game(t_stat)
    log.debug('REMOVE LATER - this used to just pass t_stat was there a reason why?')
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

# TODO Random stats to get for future/ general _expected
# mlb[stats['teamAbbrev']].home_r_pg = runs_per_game
# mlb[stats['teamAbbrev']].home_h_pg = hits_per_game
# mlb[stats['teamAbbrev']].home_hr_pg = hr_per_game
# mlb[stats['teamAbbrev']].home_bb_pg = waks_per_game

from calculator.expected_game.split_expected import SplitExpectedGame
split_expected_game_calculator = SplitExpectedGame()



#
# for team in mlb:
#     log.debug('calculating expected_game_no_split')
#     expected_game = calculate_game(
#         7, # AVG innings starter (could improve)
#         mlb[team].runs_per_game,
#         mlb[team].walks_per_game,
#         mlb[team].hits_per_game,
#         mlb[team].homeruns_per_game,
#         mlb[team].strikeouts_per_game,
#         0, # Saves
#         mlb[team].win_avg,
#         mlb[team].loss_avg,
#         0 # quality_starts
#     )
#     mlb[team].expected_game_no_split = expected_game



def calculate_all_team_expections():
    for team in mlb:
        split_expected_game_calculator.calculate_generic_expected_game(team, mlb, 9)
        split_expected_game_calculator.calculate_lefty_expected_game(team, mlb, 9)
        split_expected_game_calculator.calculate_righty_expected_game(team, mlb, 9)
        split_expected_game_calculator.calculate_home_expected_game(team, mlb, 9)
        split_expected_game_calculator.calculate_away_expected_game(team, mlb, 9)
        print('TODO: Write test for expected game all %f' % mlb[team].expected_game_no_split)
        print('TODO: Write test for expected splits lefty. %s %f' % (
            team,
            mlb[team].expected_game_lefty_split
            )
        )
        print('TODO: Write test for expected splits righty. %s %f' % (
            team,
            mlb[team].expected_game_righty_split
            )
        )
        print('TODO: Write test for expected splits home. %s %f' % (
            team,
            mlb[team].expected_game_home_split
            )
        )

        print('TODO: Write test for expected splits away. %s %f' % (
            team,
            mlb[team].expected_game_away_split
            )
        )
    return mlb

# calculate_all_team_expections()
## Something is off, home road splits produce higher projects then left right splits. should even out
