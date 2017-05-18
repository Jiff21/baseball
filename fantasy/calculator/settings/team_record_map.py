import re
from settings.team_object import Team

def return_wins_losses(j,s):
    for stand_team in j:
        if str(stand_team['team_short']) == s:
            wins = int(stand_team['w'])
            losses = int(stand_team['l'])
            games = wins + losses
            print games
            v_left = map(int, re.findall(r'\d+', stand_team['vs_left']))
            w_v_left = float(v_left[0]) / (float(v_left[0]) + float(v_left[1]))
            l_v_left = float(v_left[1]) / (float(v_left[0]) + float(v_left[1]))
            g_v_left = float(v_left[0]) + float(v_left[1])
            v_right = map(int, re.findall(r'\d+', stand_team['vs_right']))
            w_v_right = float(v_right[0]) / (float(v_right[0]) + float(v_right[1]))
            l_v_right = float(v_right[1]) / (float(v_right[0]) + float(v_right[1]))
            g_v_right = float(v_right[0]) + float(v_right[1])
            home_rec = map(int, re.findall(r'\d+', stand_team['home']))
            w_at_home = float(home_rec[0]) / (float(home_rec[0]) + float(home_rec[1]))
            l_at_home = float(home_rec[1]) / (float(home_rec[0]) + float(home_rec[1]))
            g_at_home = float(home_rec[0]) + float(home_rec[1])
            away_rec = map(int, re.findall(r'\d+', stand_team['away']))
            w_on_road = float(away_rec[0]) / (float(away_rec[0]) + float(away_rec[1]))
            l_on_road = float(away_rec[1]) / (float(away_rec[0]) + float(away_rec[1]))
            g_on_road = float(away_rec[0]) + float(away_rec[1])
            win_avg = float(wins)/float(games)
            loss_avg = float(losses)/float(games)
            return win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road

TEAM_RECORD_MAP = {}

def create_teams(all_teams, TEAM_STANDING_DICT):
    for t in all_teams:
        win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road = return_wins_losses(TEAM_STANDING_DICT, t)
        team_object = Team(t, win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road)
        t = t.replace(" ", "_").lower()
        TEAM_RECORD_MAP[t] = team_object
    return TEAM_RECORD_MAP

def get_record_map(ALL_TEAM_SHORT_NAMES, TEAM_STANDING_DICT):
    TEAM_RECORD_MAP = create_teams(ALL_TEAM_SHORT_NAMES, TEAM_STANDING_DICT)
    return TEAM_RECORD_MAP