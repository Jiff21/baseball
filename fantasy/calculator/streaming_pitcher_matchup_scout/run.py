import requests
from calculator.full_season_forecaster.pitcher_calaculator import calculate_game
from calculator.settings.team_record_map import get_record_map
from calculator.settings.standings import Standings
from datetime import datetime
import operator


TEAM_AVG_GAME = {}
LEFTY_AVG_GAME = {}
RIGHTY_AVG_GAME = {}
HOME_AVG_GAME = {}
AWAY_AVG_GAME = {}

Standings = Standings()
TEAM_RECORD_MAP = get_record_map(Standings.ALL_TEAM_SHORT_NAMES, Standings.TEAM_STANDING_DICT)

# for team in Standings.TEAM_STATS_DICT:
#     team_name = team['team_full']
#     short_name = team['team_short']
#     print 'Short Name in all run loop is %s' % short_name
#     inning = float(team['g']) * 9.0
#     games = float(team['g'])
#     runs_per_game = float(team['r']) / games
#     walks_per_game = float(team['bb']) / games
#     hits_per_game = float(team['h']) / games
#     homeruns_per_game = float(team['hr']) / games
#     strikeouts_per_game = float(team['so']) / games
#     records = TEAM_RECORD_MAP[short_name.lower().replace(' ', '_')]
#     win = records.win_avg
#     loss = records.loss_avg
#     games = records.games
#     print 'Games: %.2f \n runs_per_game: %.2f' % (games, runs_per_game)
#     expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
#         homeruns_per_game, strikeouts_per_game, 0, win, loss, 0)
#     TEAM_AVG_GAME[team_name] = expected_game



def get_expected_game_by_dict(SPLITS_DICT, ADD_TO_DICT, type):
    for team in SPLITS_DICT:
        team_name = team['team_full']
        short_name = team['team_short'].replace(" ", "_").lower()
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
            print 'error'
        # inning = games * 8.75
        runs_per_game = float(team['r']) / games
        print ' Runs are ' + str(float(team['r']) ) + ' and games are ' + str(games)  + \
            ' for ' +  team_name
        walks_per_game = float(team['bb']) / games
        hits_per_game = float(team['h']) / games
        homeruns_per_game = float(team['hr']) / games
        strikeouts_per_game = float(team['so']) / games
        ts = short_name.lower().replace(' ', '_')
        print 'In get expected. ' + str(team_name) + \
            ' \nruns_per_game: ' + str(runs_per_game) + \
            ' \nLoss avg ' + str(walks_per_game) + \
            ' \nhits_per_game ' + str(walks_per_game) + \
            ' \nhomeruns_per_game ' + str(homeruns_per_game) + \
            ' \nstrikeouts_per_game ' + str(strikeouts_per_game) + \
            ' \nts ' + str(ts) + \
            '\nand were at '  + type
        # print 'Games %.2f:\n' % (games)
        expected_game = calculate_game(7, runs_per_game, walks_per_game, hits_per_game, \
            homeruns_per_game, strikeouts_per_game, 0, w, l, 0)
        ADD_TO_DICT[team_name] = expected_game



# get_expected_game_by_dict(Standings.TEAM_AT_HOME_DICT, HOME_AVG_GAME, 'home')
# get_expected_game_by_dict(Standings.TEAM_AWAY_DICT, AWAY_AVG_GAME, 'away')
# get_expected_game_by_dict(Standings.TEAM_VS_LEFTY_DICT, LEFTY_AVG_GAME, 'lefty')
get_expected_game_by_dict(Standings.TEAM_VS_RIGHTY_DICT, RIGHTY_AVG_GAME, 'righty')


# sorted_x = sorted(TEAM_AVG_GAME.items(), key=operator.itemgetter(1))
# for key, value in sorted_x:
#     print 'Pitchers average %.2ipts against %s' % (value, key)
#     print 'Home: %.2f, Away %.2f, Lefty: %.2f, righty %f\n' % \
#         (LEFTY_AVG_GAME[key], RIGHTY_AVG_GAME[key], HOME_AVG_GAME[key], AWAY_AVG_GAME[key])
