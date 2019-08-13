import requests
import json
import re

from calculator.settings.logger import log

from calculator.full_season_forecaster.pitcher_calculator import calculate_game
from datetime import datetime

import operator

TEAM_AVG_GAME = {}
LEFTY_AVG_GAME = {}
RIGHTY_AVG_GAME = {}
HOME_AVG_GAME = {}
AWAY_AVG_GAME = {}

from calculator.settings.api import BASE_URL, UPDATED_BASE_URL, TEAM_AWAY_URI, TEAM_AT_HOME_URI
from calculator.settings.api import TEAM_VS_LEFTY_URI, TEAM_VS_RIGHTY_URI
from calculator.settings.api import TEAM_STANDING_URI

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
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    TEAM_STATS_DICT = JSON_RESPONSE['team_hitting_season_leader_master']['queryResults']['row']
    return TEAM_STATS_DICT

TEAM_STATS_DICT = get_team_stats()

ALL_TEAM_SHORT_NAMES = []

class Team(object):
    def __init__(self):
        """Return a team and there win loss splits."""
        self.standings = None

        def set_wins(wins):
            self.wins = wins

        def set_losses(losses):
            self.losses = losses

        def set_games(games_played):
            self.games_played = games_played

        def set_win_avg(win_avg):
            self.win_avg = get_avg(self.wins, self.losses)

        def set_loss_avg(loss_avg):
            self.loss_avg = loss_avg

        def get_avg(avg_to_get, other_half):
            avg = avg_to_get / avg_to_get + other_half
            return get_avg

def get_all_team_names(d):
    mlb = {}
    for t in d:
        team = Team()
        team.short_name = t['team_short']
        team.abbr = t['team_abbrev']
        mlb[team.abbr] = team
    return mlb

mlb = get_all_team_names(TEAM_STATS_DICT)

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

    return runs_per_game, hits_per_game, hr_per_game, waks_per_game

def get_pitcher_splits_per_dict(splits_dict):
    log.debug('running get_pitcher_splits_per_dict')
    r = int(splits_dict['r'])
    # import pdb; pdb.set_trace()
    plate_appearances = int(splits_dict['tpa'])
    runs_per_pa = get_avg(r, plate_appearances)

    h = int(splits_dict['h'])
    hits_per_pa = get_avg(h, plate_appearances)

    hr = int(splits_dict['hr'])
    hr_per_pa = get_avg(hr, plate_appearances)

    bb = int(splits_dict['bb'])
    walks_per_pa = get_avg(bb, plate_appearances)
    # import pdb; pdb.set_trace()

    return runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa

for stats in TEAM_AT_HOME_DICT:
    log.debug('getting home splits')
    runs_per_game, hits_per_game, hr_per_game, waks_per_game = get_relevant_splits_per_dict(stats)
    mlb[stats['name_abbrev']].home_r_pg = runs_per_game
    mlb[stats['name_abbrev']].home_h_pg = hits_per_game
    mlb[stats['name_abbrev']].home_hr_pg = hr_per_game
    mlb[stats['name_abbrev']].home_bb_pg = waks_per_game

TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)

for stats in TEAM_AWAY_DICT:
    log.debug('getting away splits')
    runs_per_game, hits_per_game, hr_per_game, waks_per_game = get_relevant_splits_per_dict(stats)
    mlb[stats['name_abbrev']].away_r_pg = runs_per_game
    mlb[stats['name_abbrev']].away_h_pg = hits_per_game
    mlb[stats['name_abbrev']].away_hr_pg = hr_per_game
    mlb[stats['name_abbrev']].away_bb_pg = waks_per_game

TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY_URI)

for stats in TEAM_VS_LEFTY_DICT:
    log.debug('getting lefty splits')
    runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa = get_pitcher_splits_per_dict(stats)
    mlb[stats['name_abbrev']].vs_l_r_per_pa = runs_per_game
    mlb[stats['name_abbrev']].vs_l_h_per_pa = hits_per_game
    mlb[stats['name_abbrev']].vs_l_hr_per_pa = hr_per_game
    mlb[stats['name_abbrev']].vs_l_bb_per_pa = waks_per_game

TEAM_VS_RIGHTY_DICT = get_splits_by_uri(TEAM_VS_RIGHTY_URI)

for stats in TEAM_VS_RIGHTY_DICT:
    log.debug('getting righty splits')
    runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa = get_pitcher_splits_per_dict(stats)
    mlb[stats['name_abbrev']].vs_r_r_per_pa = runs_per_game
    mlb[stats['name_abbrev']].vs_r_h_per_pa = hits_per_game
    mlb[stats['name_abbrev']].vs_r_hr_per_pa = hr_per_game
    mlb[stats['name_abbrev']].vs_r_bb_per_pa = waks_per_game

def get_standings():
    today = datetime.now().strftime('%Y/%m/%d')
    # TEAM_STANDING_URI = '/named.standings_schedule_date.bam?season=2019&schedule_game_date.game_date=%27' + today + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
    CURRENT_URL = BASE_URL + TEAM_STANDING_URI
    # CURRENT_URL = UPDATED_BASE_URL + TEAM_STANDING_URI
    try:
        TEAM_STANDING_RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    STANDING_TEXT = TEAM_STANDING_RESPONSE.text
    JSON_STANDINGS = json.loads(STANDING_TEXT)
    # Standings are in two blocks al and NL. This combines them.
    tsd = JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    tsd.extend(JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    return tsd


TEAM_STANDING_DICT = get_standings()

class StandingsData(object):

    def __init__(self):
        """get necessary data from standings."""
        pass

    def get_wins(self, current_dict):
        return int(current_dict['w'])

    def get_losses(self, current_dict):
        return int(current_dict['l'])

    def break_dash_record_split(self, current_dict, string):
        record_split = list(map(int, re.findall(r'\d+', current_dict[string])))
        first_number = float(record_split[0]) / (float(record_split[0]) + float(record_split[1]))
        second_number = float(record_split[1]) / (float(record_split[0]) + float(record_split[1]))
        total = float(record_split[0]) + float(record_split[1])
        return first_number, second_number, total

    def get_vs_left(self, current_dict):
        w_v_left, l_v_left, g_v_left = self.break_dash_record_split(current_dict, 'vs_left')
        return w_v_left, l_v_left, g_v_left

    def get_vs_right(self, current_dict):
        w_v_left, l_v_left, g_v_left = self.break_dash_record_split(current_dict, 'vs_right')
        return w_v_left, l_v_left, g_v_left

    def get_at_home(self, current_dict):
        w_avg_home, w_avg_home, g_at_home = self.break_dash_record_split(current_dict, 'home')
        return w_avg_home, w_avg_home, g_at_home

    def get_at_road(self, current_dict):
        w_avg_road, l_avg_road, g_at_road = self.break_dash_record_split(current_dict, 'away')
        return w_avg_road, l_avg_road, g_at_road

    def get_games_total(self, current_dict):
        wins = self.get_wins(current_dict)
        losses = self.get_losses(current_dict)
        return wins + losses

    def set_win_avg(self, current_dict):
        wins = self.get_wins(current_dict)
        total = self.get_games_total(current_dict)
        return wins / total

    def set_loss_avg(self, current_dict):
        losses = self.get_losses(current_dict)
        total = self.get_games_total(current_dict)
        return wins / total

    def get_run_avg(self, current_dict):
        games = self.get_games_total(current_dict)
        return int(current_dict['runs']) / games

standings_data = StandingsData()

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


class SelfCalculated(object):

    def __init__(self):
        """get necessary data from standings."""
        pass

    def get_total_innings(self, team):
        innings = team.games * 9
        return innings


## Finish these just in case
self_calc = SelfCalculated()
innings = self_calc.get_total_innings(mlb['HOU'])
assert innings == 1062, innings

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

team_stats = TeamStatsNoSplit()

print(TEAM_STATS_DICT[0])

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

# TODO: Write tests

# TODO: Better loop
for team in TEAM_STATS_DICT:
    log.debug('expected_game_no_spit')
    expected_game = calculate_game(
        7, # AVG innings starter (could improve)
        mlb[team['team_abbrev']].runs_per_game,
        mlb[team['team_abbrev']].walks_per_game,
        mlb[team['team_abbrev']].hits_per_game,
        mlb[team['team_abbrev']].homeruns_per_game,
        mlb[team['team_abbrev']].strikeouts_per_game,
        0, # Saves
        mlb[team['team_abbrev']].win_avg,
        mlb[team['team_abbrev']].loss_avg,
        0 # quality_starts
    )
    mlb[team['team_abbrev']].expected_game_no_spit = expected_game

# TODO: Write tests
print(mlb['MIA'].expected_game_no_spit)
#
#
# def get_expected_game_by_dict(SPLITS_DICT, ADD_TO_DICT, type):
#     for team in SPLITS_DICT:
#         team_name = team['team_full']
#         short_name = team['team_short'].lower().replace(' ', '_')
#         records = TEAM_RECORD_MAP[short_name]
#         if type == 'home':
#             w = records.w_at_home
#             l = records.l_at_home
#             games = records.g_at_home
#         elif type == 'away':
#             w = records.w_on_road
#             l = records.l_on_road
#             games = records.g_on_road
#         elif type == 'lefty':
#             w = records.w_v_left
#             l = records.l_v_left
#             games = records.g_v_left
#         elif type == 'righty':
#             w = records.w_v_right
#             l = records.l_v_right
#             games = records.g_v_right
#         else:
#             assert 1 == 2, 'got to else in get_expected_game_by_dict'
#         print('In get expected. Losses ' + str(l))
#         inning = games * 8.75
#         runs_per_game = float(team['r']) / games
#         walks_per_game = float(team['bb']) / games
#         hits_per_game = float(team['h']) / games
#         homeruns_per_game = float(team['hr']) / games
#         strikeouts_per_game = float(team['so']) / games
#         ts = short_name.lower().replace(' ', '_')
#         # print 'Games %.2f:\n' % (games)
#         expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
#             homeruns_per_game, strikeouts_per_game, 0, w, l, 0)
#         ADD_TO_DICT[team_name] = expected_game
#
#
# get_expected_game_by_dict(TEAM_AT_HOME_DICT, HOME_AVG_GAME, 'home')
# get_expected_game_by_dict(TEAM_AWAY_DICT, AWAY_AVG_GAME, 'away')
# get_expected_game_by_dict(TEAM_VS_LEFTY_DICT, LEFTY_AVG_GAME, 'lefty')
# get_expected_game_by_dict(TEAM_VS_RIGHTY_DICT, RIGHTY_AVG_GAME, 'righty')
#
#
#
# sorted_x = sorted(TEAM_AVG_GAME.items(), key=operator.itemgetter(1))
# for key, value in sorted_x:
#     print('Pitchers average %.2ipts against %s' % (value, key))
#     print('Home: %.2f, Away %.2f, Lefty: %.2f, righty %f\n' % \
#         (
#             LEFTY_AVG_GAME[key],
#             RIGHTY_AVG_GAME[key],
#             HOME_AVG_GAME[key],
#             AWAY_AVG_GAME[key]
#         )
    # )
