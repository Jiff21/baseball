import json
import requests

def get_relevant_part_of_standings_dict(feed_me_json):
    TEAM_STANDING_DICT = feed_me_json['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(feed_me_json['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    return TEAM_STANDING_DICT

def get_short_name_from_standing_dict(feed_me_json):
    return feed_me_json['team_short']

def get_righty_from_standing_dict(feed_me_json):
    return feed_me_json['vs_right']

def get_lefty_from_standing_dict(feed_me_json):
    return feed_me_json['vs_left']



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
