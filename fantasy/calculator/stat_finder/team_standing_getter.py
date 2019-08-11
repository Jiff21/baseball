import os
import re
import json
import requests
from calculator.settings.api import BASE_URL, TEAM_STANDING_URI
from calculator.settings.api import STATS_API, STANDINGS_URI

def get_relevant_part_of_standings_dict(feed_me_json):
    TEAM_STANDING_DICT = feed_me_json['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(feed_me_json['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    # print(type(TEAM_STANDING_DICT))
    # assert 1 == 2
    return TEAM_STANDING_DICT

def get_short_name_from_standing_dict(feed_me_json):
    return feed_me_json['team_short']

def get_wins_from_standing_dict(feed_me_json):
    # print(feed_me_json[0])
    # print(feed_me_json[0]['w'])
    return int(feed_me_json['w'])

def get_losses_from_standing_dict(feed_me_json):
    return int(feed_me_json['l'])

def get_games_from_standing_dict(feed_me_json):
    return int(feed_me_json['l']) + int(feed_me_json['w'])

def get_righty_from_standing_dict(feed_me_json):
    ''' w_v_right & l_v_right return floats for win/loss percentage'''
    v_right = list(map(int, re.findall(r'\d+', feed_me_json['vs_right'])))
    w_v_right = float(v_right[0]) / (float(v_right[0]) + float(v_right[1]))
    l_v_right = float(v_right[1]) / (float(v_right[0]) + float(v_right[1]))
    g_v_right = float(v_right[0]) + float(v_right[1])
    return w_v_right, l_v_right, g_v_right

def get_lefty_from_standing_dict(feed_me_json):
    v_left = list(map(int, re.findall(r'\d+', feed_me_json['vs_left'])))
    w_v_left = float(v_left[0]) / (float(v_left[0]) + float(v_left[1]))
    l_v_left = float(v_left[1]) / (float(v_left[0]) + float(v_left[1]))
    g_v_left = float(v_left[0]) + float(v_left[1])
    return w_v_left, l_v_left, g_v_left

def get_home_from_standing_dict(feed_me_json):
    home_rec = list(map(int, re.findall(r'\d+', feed_me_json['home'])))
    w_at_home = float(home_rec[0]) / (float(home_rec[0]) + float(home_rec[1]))
    l_at_home = float(home_rec[1]) / (float(home_rec[0]) + float(home_rec[1]))
    g_at_home = float(home_rec[0]) + float(home_rec[1])
    return w_at_home, l_at_home, g_at_home

def get_away_from_standing_dict(feed_me_json):
    away_rec = list(map(int, re.findall(r'\d+', feed_me_json['away'])))
    w_on_road = float(away_rec[0]) / (float(away_rec[0]) + float(away_rec[1]))
    l_on_road = float(away_rec[1]) / (float(away_rec[0]) + float(away_rec[1]))
    g_on_road = float(away_rec[0]) + float(away_rec[1])
    return w_on_road, l_on_road, g_on_road

def return_wins_losses(feed_me_json):
    print('maybe return_wins_losses this should be json. You mapped some stuff you shouldn\'t have.\n' + str(type(feed_me_json)))
    print('return_wins_losses' + feed_me_json)
    wins = get_wins_from_standing_dict(feed_me_json)
    losses = get_losses_from_standing_dict(feed_me_json)
    games = get_games_from_standing_dict(feed_me_json)
    w_v_right, l_v_right, g_v_right = get_righty_from_standing_dict(feed_me_json)
    w_v_left, l_v_left, g_v_left = get_lefty_from_standing_dict(feed_me_json)
    w_at_home, l_at_home, g_at_home = get_home_from_standing_dict(feed_me_json)
    w_on_road, l_on_road, g_on_road = get_away_from_standing_dict(feed_me_json)
    win_avg = float(wins)/float(games)
    loss_avg = float(losses)/float(games)
    return win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, \
        l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road


def get_standings():
    CURRENT_URL = BASE_URL + TEAM_STANDING_URI
    try:
        TEAM_STANDING_RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    STANDING_TEXT = TEAM_STANDING_RESPONSE.text
    JSON_STANDINGS = json.loads(STANDING_TEXT)
    # Standings are in two blocks al and NL. This combines them.
    TEAM_STANDING_DICT = JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    return TEAM_STANDING_DICT
