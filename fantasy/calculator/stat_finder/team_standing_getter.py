import re
import json
import requests

def get_relevant_part_of_standings_dict(feed_me_json):
    TEAM_STANDING_DICT = feed_me_json['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(feed_me_json['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    return TEAM_STANDING_DICT

def get_short_name_from_standing_dict(feed_me_json):
    return feed_me_json['team_short']

def get_wins_from_standing_dict(feed_me_json):
    print(feed_me_json['w'])
    return int(feed_me_json['w'])

def get_losses_from_standing_dict(feed_me_json):
    return int(feed_me_json['l'])

def get_games_from_standing_dict(feed_me_json):
    return int(feed_me_json['l']) + int(feed_me_json['w'])

def get_righty_from_standing_dict(feed_me_json):
    ''' w_v_right & l_v_right return floats for win/loss percentage'''
    v_right = map(int, re.findall(r'\d+', feed_me_json['vs_right']))
    w_v_right = float(v_right[0]) / (float(v_right[0]) + float(v_right[1]))
    l_v_right = float(v_right[1]) / (float(v_right[0]) + float(v_right[1]))
    g_v_right = float(v_right[0]) + float(v_right[1])
    return w_v_right, l_v_right, g_v_right

def get_lefty_from_standing_dict(feed_me_json):
    v_left = map(int, re.findall(r'\d+', feed_me_json['vs_left']))
    w_v_left = float(v_left[0]) / (float(v_left[0]) + float(v_left[1]))
    l_v_left = float(v_left[1]) / (float(v_left[0]) + float(v_left[1]))
    g_v_left = float(v_left[0]) + float(v_left[1])
    return w_v_left, l_v_left, g_v_left



#
# def return_wins_losses(j,s):
#     for stand_team in j:
#         if str(stand_team['team_short']) == s:
#             # wins = int(stand_team['w'])
#             # losses = int(stand_team['l'])
#             # games = wins + losses
#             # v_left = map(int, re.findall(r'\d+', stand_team['vs_left']))
#             # w_v_left = float(v_left[0]) / (float(v_left[0]) + float(v_left[1]))
#             # l_v_left = float(v_left[1]) / (float(v_left[0]) + float(v_left[1]))
#             # g_v_left = float(v_left[0]) + float(v_left[1])
#             # v_right = map(int, re.findall(r'\d+', stand_team['vs_right']))
#             # w_v_right = float(v_right[0]) / (float(v_right[0]) + float(v_right[1]))
#             # l_v_right = float(v_right[1]) / (float(v_right[0]) + float(v_right[1]))
#             # g_v_right = float(v_right[0]) + float(v_right[1])
#             home_rec = map(int, re.findall(r'\d+', stand_team['home']))
#             w_at_home = float(home_rec[0]) / (float(home_rec[0]) + float(home_rec[1]))
#             l_at_home = float(home_rec[1]) / (float(home_rec[0]) + float(home_rec[1]))
#             g_at_home = float(home_rec[0]) + float(home_rec[1])
#             away_rec = map(int, re.findall(r'\d+', stand_team['away']))
#             w_on_road = float(away_rec[0]) / (float(away_rec[0]) + float(away_rec[1]))
#             l_on_road = float(away_rec[1]) / (float(away_rec[0]) + float(away_rec[1]))
#             g_on_road = float(away_rec[0]) + float(away_rec[1])
#             win_avg = float(wins)/float(games)
#             loss_avg = float(losses)/float(games)
#             print "return_wins_losses" + str(stand_team)
#             print g_at_home
#             return win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, \
#                 l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road

# for team in Standings.TEAM_STATS_DICT:
#     team_name = team['team_full']
#     short_name = team['team_short']
#     print('Short Name in all run loop is %s' % short_name)
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
