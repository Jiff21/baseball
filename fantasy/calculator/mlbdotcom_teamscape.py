import requests
import json
import re
from pitcher_outing import calculate_game
import operator
from datetime import datetime

TEAM_AVG_GAME = {}
Lefty_AVG_GAME = {}
RIGHTY_AVG_GAME = {}
HOME_AVG_GAME = {}
AWAY_AVG_GAME = {}


BASE_URL = 'http://mlb.mlb.com/lookup/json/'
TEAM_STATS_URI = 'named.team_hitting_season_leader_master.bam?season=2017&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&recSP=1&recPP=50'
TEAM_AT_HOME_URI = 'named.team_hitting_season_leader_sit.bam?season=2017&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27h%27&recSP=1&recPP=50'
TEAM_AWAY_URI = '/named.team_hitting_season_leader_sit.bam?season=2017&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27a%27&recSP=1&recPP=50'
TEAM_VS_LEFTY = '/named.team_hitting_season_leader_sit.bam?season=2017&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27vl%27&recSP=1&recPP=50'
TEAM_VS_RIGHTY = '/named.team_hitting_season_leader_sit.bam?season=2017&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27vr%27&recSP=1&recPP=50'


def get_team_stats():
    CURRENT_URL = BASE_URL + TEAM_STATS_URI
    RESPONSE = requests.get(CURRENT_URL)
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    TEAM_STATS_DICT = JSON_RESPONSE['team_hitting_season_leader_master']['queryResults']['row']
    return TEAM_STATS_DICT

TEAM_STATS_DICT = get_team_stats()


def get_splits_by_uri(uri):
    CURRENT_URL = BASE_URL + uri
    RESPONSE = requests.get(CURRENT_URL)
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    CURRENT_DICT = JSON_RESPONSE['team_hitting_season_leader_sit']['queryResults']['row']
    return CURRENT_DICT

TEAM_AT_HOME_DICT = get_splits_by_uri(TEAM_AT_HOME_URI)
TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)
TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY)
TEAM_VS_RIGHTY_DICT = get_splits_by_uri(TEAM_VS_RIGHTY)


def get_standings():
    today = datetime.now().strftime('%Y/%m/%d')
    TEAM_STANDING_URI = '/named.standings_schedule_date.bam?season=2017&schedule_game_date.game_date=%27' + today + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
    CURRENT_URL = BASE_URL + TEAM_STANDING_URI
    TEAM_STANDING_RESPONSE = requests.get(CURRENT_URL)
    STANDING_TEXT = TEAM_STANDING_RESPONSE.text
    JSON_STANDINGS = json.loads(STANDING_TEXT)
    # Standings are in two blocks al and NL. This combines them.
    TEAM_STANDING_DICT = JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])

TEAM_STANDING_DICT = get_standings()


def return_wins_losses(j,s,g):
    print '\n %s' % s
    for stand_team in j:
        if str(stand_team['team_short']) == s:
            wins = int(stand_team['w'])
            losses = int(stand_team['l'])
            v_left = map(int, re.findall(r'\d+', stand_team['vs_left']))
            w_v_left =float(v_left[0]) / (float(v_left[0]) + float(v_left[1]))
            l_v_left =float(v_left[1]) / (float(v_left[0]) + float(v_left[1]))
            v_right = map(int, re.findall(r'\d+', stand_team['vs_right']))
            w_v_right = float(v_right[0]) / (float(v_right[0]) + float(v_right[1]))
            l_v_right = float(v_right[1]) / (float(v_right[0]) + float(v_right[1]))
            home_rec = map(int, re.findall(r'\d+', stand_team['home']))
            w_at_home = float(home_rec[0]) / (float(home_rec[0]) + float(home_rec[1]))
            l_at_home = float(home_rec[1]) / (float(home_rec[0]) + float(home_rec[1]))
            away_rec = map(int, re.findall(r'\d+', stand_team['away']))
            w_on_road = float(away_rec[0]) / (float(away_rec[0]) + float(away_rec[1]))
            l_on_road = float(away_rec[1]) / (float(away_rec[0]) + float(away_rec[1]))
            win_avg = float(wins)/float(g)
            loss_avg = float(losses)/float(g)
            return win_avg, loss_avg, w_v_left, l_v_left, w_v_right, l_v_right, \
                w_at_home, l_at_home, w_on_road, l_on_road


win, loss, left_win, left_loss, right_win, right_loss, home_win, home_loss, away_win, \
        away_loss = return_wins_losses(TEAM_STANDING_DICT, short_name, games)


for team in TEAM_STATS_DICT:
    team_name = team['team_full']
    short_name = team['team_short']
    inning = float(team['g']) * 9.0
    games = float(team['g'])
    runs_per_game = float(team['r']) / games
    walks_per_game = float(team['bb']) / games
    hits_per_game = float(team['h']) / games
    homeruns_per_game = float(team['hr']) / games
    strikeouts_per_game = float(team['so']) / games
    win, loss, left_win, left_loss, right_win, right_loss, home_win, home_loss, away_win, \
        away_loss = return_wins_losses(TEAM_STANDING_DICT, short_name, games)
    expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
        homeruns_per_game, strikeouts_per_game, 0, win, loss, 0)
    expected_lefty_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
        homeruns_per_game, strikeouts_per_game, 0, left_win, left_loss, 0)
    expected_righty_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
        homeruns_per_game, strikeouts_per_game, 0, right_win, right_loss, 0)
    expected_home_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
        homeruns_per_game, strikeouts_per_game, 0, home_win, home_loss, 0)
    expected_away_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
        homeruns_per_game, strikeouts_per_game, 0, away_win, away_loss, 0)
    TEAM_AVG_GAME[team_name] = expected_game
    Lefty_AVG_GAME[team_name] = expected_lefty_game
    RIGHTY_AVG_GAME[team_name] = expected_righty_game
    HOME_AVG_GAME[team_name] = expected_home_game
    AWAY_AVG_GAME[team_name] = expected_away_game


def get_expected_game_by_dict(SPLITS_DICT, ADD_TO_DICT, w, l):
    for team in SPLITS_DICT:
        team_name = team['team_full']
        short_name = team['team_short']
        inning = float(team['g']) * 8.75
        games = float(team['g'])
        runs_per_game = float(team['r']) / games
        walks_per_game = float(team['bb']) / games
        hits_per_game = float(team['h']) / games
        homeruns_per_game = float(team['hr']) / games
        strikeouts_per_game = float(team['so']) / games  
        expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
            homeruns_per_game, strikeouts_per_game, 0, w, l, 0)
        ADD_TO_DICT[team_name] = expected_game

get_expected_game_by_dict(TEAM_AT_HOME_DICT, HOME_AVG_GAME, home_win, home_loss)
print HOME_AVG_GAME



# sorted_x = sorted(TEAM_AVG_GAME.items(), key=operator.itemgetter(1))
# for key, value in sorted_x:
#     print 'Pitchers average %.2ipts against %s' % (value, key)
#     print 'Home: %.2f, Away %.2f, Lefty: %.2f, righty %f\n' % \
#         (Lefty_AVG_GAME[key], RIGHTY_AVG_GAME[key], HOME_AVG_GAME[key], AWAY_AVG_GAME[key])
