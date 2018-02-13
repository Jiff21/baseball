import json
import requests

def get_relevant_part_of_hitting_dict(feed_me_json):
    TEAM_STATS_DICT = feed_me_json['team_hitting_season_leader_master']['queryResults']['row']
    return TEAM_STATS_DICT

def get_short_name_from_json(feed_me_json):
    return feed_me_json['team_short']

def get_atbats_from_json(feed_me_json):
    return int(feed_me_json['ab'])

def get_rbis_from_json(feed_me_json):
    return int(feed_me_json['rbi'])

def get_walks_from_json(feed_me_json):
    return int(feed_me_json['bb'])

def get_runs_from_json(feed_me_json):
    return int(feed_me_json['r'])

def get_strikeouts_from_json(feed_me_json):
    return int(feed_me_json['so'])

def get_games_from_json(feed_me_json):
    return int(feed_me_json['g'])

def get_hits_from_json(feed_me_json):
    return int(feed_me_json['h'])
