import re
from calculator.settings.team_object import Team
from calculator.stat_finder.team_standing_getter import return_wins_losses


## need a way to map back ab per games
def ab_per_game(passed_json, passed_short_name):
    print('DOES THIS EVER RUNS???')
    for t in passed_json:
        current_name = t['team_short']
        if current_name == passed_short_name:
            games = t['g']
            at_bats = t['ab']
            ab_per_game = float(at_bats)/float(games)
            print('At bats per game is %i for %s' % (ab_per_game, t['team_short']))
            return ab_per_game

TEAM_RECORD_MAP = {}

def create_teams(all_teams, TEAM_STANDING_DICT):
    print('DOES THIS EVER RUNS??? 2')
    for t in all_teams:
        win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, \
        w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, \
        g_at_home, g_on_road = return_wins_losses(TEAM_STANDING_DICT)
        print("create_teams " + t)
        print(g_at_home)
        team_object = Team(t, win_avg, loss_avg, games, w_v_left, l_v_left,
            g_v_left, w_v_right, l_v_right,g_v_right, w_at_home, l_at_home, \
            g_at_home, w_on_road, l_on_road, g_on_road)
        # print("create_teams " + t)
        # print(team_object.name)
        # print (team_object.g_at_home)
        t = t.replace(" ", "_").lower()
        TEAM_RECORD_MAP[t] = team_object
    return TEAM_RECORD_MAP

def get_record_map(ALL_TEAM_SHORT_NAMES, TEAM_STANDING_DICT):
    TEAM_RECORD_MAP = create_teams(ALL_TEAM_SHORT_NAMES, TEAM_STANDING_DICT)
    return TEAM_RECORD_MAP
