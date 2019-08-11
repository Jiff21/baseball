import requests
import json
import re

from calculator.full_season_forecaster.pitcher_calculator import calculate_game
from datetime import datetime

import operator

TEAM_AVG_GAME = {}
LEFTY_AVG_GAME = {}
RIGHTY_AVG_GAME = {}
HOME_AVG_GAME = {}
AWAY_AVG_GAME = {}


BASE_URL = 'http://mlb.mlb.com/lookup/json/'
TEAM_STATS_URI = 'named.team_hitting_season_leader_master.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&recSP=1&recPP=50'
TEAM_AT_HOME_URI = 'named.team_hitting_season_leader_sit.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27h%27&recSP=1&recPP=50'
TEAM_AWAY_URI = '/named.team_hitting_season_leader_sit.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27a%27&recSP=1&recPP=50'
TEAM_VS_LEFTY_URI = '/named.team_hitting_season_leader_sit.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27vl%27&recSP=1&recPP=50'
TEAM_VS_RIGHTY_URI = '/named.team_hitting_season_leader_sit.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27vr%27&recSP=1&recPP=50'


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

def get_all_team_names(d):
    for t in d:
        current_name = t['team_short']
        ALL_TEAM_SHORT_NAMES.append(current_name)


get_all_team_names(TEAM_STATS_DICT)




class Team(object):
    def __init__(self):
        """Return a team and there win loss splits."""
        self.name = None
        # self.win_avg = win_avg
        # self.games = games
        # self.loss_avg = loss_avg
        # self.w_v_left = w_v_left
        # self.l_v_left = l_v_left
        # self.w_v_right = w_v_right
        # self.l_v_right = l_v_right
        # self.w_at_home = w_at_home
        # self.l_at_home = l_at_home
        # self.w_on_road = w_on_road
        # self.l_on_road = l_on_road
        # self.g_v_left = g_v_left
        # self.g_v_right = g_v_left
        # self.g_at_home = g_v_left
        # self.g_on_road = g_v_left

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

def get_splits_by_uri(uri):
    CURRENT_URL = BASE_URL + uri
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
TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)
TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY_URI)
TEAM_VS_RIGHTY_DICT = get_splits_by_uri(TEAM_VS_RIGHTY_URI)


def get_standings():
    today = datetime.now().strftime('%Y/%m/%d')
    TEAM_STANDING_URI = '/named.standings_schedule_date.bam?season=2019&schedule_game_date.game_date=%27' + today + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
    CURRENT_URL = BASE_URL + TEAM_STANDING_URI
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
    return tsd[0]


TEAM_STANDING_DICT = get_standings()

def return_wins_losses(j,s):
    print('You are here. J was a string, changed to json now. ')
    # j = json. s is team name we're looking for.
    for stand_team in j:
        # why is this vs_left
        print(stand_team)
        stand_team = json.loads(stand_team)

        print(str(stand_team['team_short']))
        if str(stand_team['team_short']) == s:
            wins = int(stand_team['w'])
            losses = int(stand_team['l'])
            games = wins + losses
            v_left = list(map(int, re.findall(r'\d+', stand_team['vs_left'])))
            w_v_left = float(v_left[0]) / (float(v_left[0]) + float(v_left[1]))
            l_v_left = float(v_left[1]) / (float(v_left[0]) + float(v_left[1]))
            g_v_left = float(v_left[0]) + float(v_left[1])
            v_right = list(map(int, re.findall(r'\d+', stand_team['vs_right'])))
            w_v_right = float(v_right[0]) / (float(v_right[0]) + float(v_right[1]))
            l_v_right = float(v_right[1]) / (float(v_right[0]) + float(v_right[1]))
            g_v_right = float(v_right[0]) + float(v_right[1])
            home_rec = list(map(int, re.findall(r'\d+', stand_team['home'])))
            w_at_home = float(home_rec[0]) / (float(home_rec[0]) + float(home_rec[1]))
            l_at_home = float(home_rec[1]) / (float(home_rec[0]) + float(home_rec[1]))
            g_at_home = float(home_rec[0]) + float(home_rec[1])
            away_rec = list(map(int, re.findall(r'\d+', stand_team['away'])))
            w_on_road = float(away_rec[0]) / (float(away_rec[0]) + float(away_rec[1]))
            l_on_road = float(away_rec[1]) / (float(away_rec[0]) + float(away_rec[1]))
            g_on_road = float(away_rec[0]) + float(away_rec[1])
            win_avg = float(wins)/float(games)
            loss_avg = float(losses)/float(games)
            return win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road

TEAM_RECORD_MAP = {}

def create_teams(all_teams):
    for t in all_teams:
        print('creating ' + t)
        win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road = return_wins_losses(TEAM_STANDING_DICT, t)
        team_object = Team(t, win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road)
        t = t.replace(" ", "_").lower()
        TEAM_RECORD_MAP[t] = team_object
    return TEAM_RECORD_MAP

TEAM_RECORD_MAP = create_teams(ALL_TEAM_SHORT_NAMES)

# TODO Why is this here?
create_teams(ALL_TEAM_SHORT_NAMES)

for team in TEAM_STATS_DICT:
    team = Team()
    team.name = s
    team_name = team['team_full']
    short_name = team['team_short']
    inning = float(team['g']) * 9.0
    games = float(team['g'])
    runs_per_game = float(team['r']) / games
    walks_per_game = float(team['bb']) / games
    hits_per_game = float(team['h']) / games
    homeruns_per_game = float(team['hr']) / games
    strikeouts_per_game = float(team['so']) / games
    records = TEAM_RECORD_MAP[short_name.lower().replace(' ', '_')]
    win = records.win_avg
    loss = records.loss_avg
    games = records.games
    print ('Games: %.2f \n runs_per_game: %.2f' % (games, runs_per_game))
    expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
        homeruns_per_game, strikeouts_per_game, 0, win, loss, 0)
    TEAM_AVG_GAME[team_name] = expected_game



def get_expected_game_by_dict(SPLITS_DICT, ADD_TO_DICT, type):
    for team in SPLITS_DICT:
        team_name = team['team_full']
        short_name = team['team_short'].lower().replace(' ', '_')
        records = TEAM_RECORD_MAP[short_name]
        if type == 'home':
            w = records.w_at_home
            l = records.l_at_home
            games = records.g_at_home
        elif type == 'away':
            w = records.w_on_road
            l = records.l_on_road
            games = records.g_on_road
        elif type == 'lefty':
            w = records.w_v_left
            l = records.l_v_left
            games = records.g_v_left
        elif type == 'righty':
            w = records.w_v_right
            l = records.l_v_right
            games = records.g_v_right
        else:
            assert 1 == 2, 'got to else in get_expected_game_by_dict'
        print('In get expected. Losses ' + str(l))
        inning = games * 8.75
        runs_per_game = float(team['r']) / games
        walks_per_game = float(team['bb']) / games
        hits_per_game = float(team['h']) / games
        homeruns_per_game = float(team['hr']) / games
        strikeouts_per_game = float(team['so']) / games
        ts = short_name.lower().replace(' ', '_')
        # print 'Games %.2f:\n' % (games)
        expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
            homeruns_per_game, strikeouts_per_game, 0, w, l, 0)
        ADD_TO_DICT[team_name] = expected_game


get_expected_game_by_dict(TEAM_AT_HOME_DICT, HOME_AVG_GAME, 'home')
get_expected_game_by_dict(TEAM_AWAY_DICT, AWAY_AVG_GAME, 'away')
get_expected_game_by_dict(TEAM_VS_LEFTY_DICT, LEFTY_AVG_GAME, 'lefty')
get_expected_game_by_dict(TEAM_VS_RIGHTY_DICT, RIGHTY_AVG_GAME, 'righty')



sorted_x = sorted(TEAM_AVG_GAME.items(), key=operator.itemgetter(1))
for key, value in sorted_x:
    print('Pitchers average %.2ipts against %s' % (value, key))
    print('Home: %.2f, Away %.2f, Lefty: %.2f, righty %f\n' % \
        (
            LEFTY_AVG_GAME[key],
            RIGHTY_AVG_GAME[key],
            HOME_AVG_GAME[key],
            AWAY_AVG_GAME[key]
        )
    )
