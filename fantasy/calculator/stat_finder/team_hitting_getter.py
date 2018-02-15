import json
import requests
from calculator.settings.api import TEAM_AT_HOME_URI, TEAM_AWAY_URI
from calculator.settings.api import TEAM_VS_LEFTY_URI, TEAM_VS_RIGHTY_URI

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


def get_splits_by_uri(uri):
    CURRENT_URL = BASE_URL + uri
    try:
        RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    CURRENT_DICT = JSON_RESPONSE['team_hitting_season_leader_sit']['queryResults']['row']
    return CURRENT_DICT

def get_at_home_splits():
    return get_splits_by_uri(TEAM_AT_HOME_URI)

def get_away_splits():
    return get_splits_by_uri(TEAM_AWAY_URI)

def get_verse_lefty_splits():
    return get_splits_by_uri(TEAM_VS_LEFTY_URI)

def get_verse_righty_splits():
    return get_splits_by_uri(TEAM_VS_RIGHTY_URI)
