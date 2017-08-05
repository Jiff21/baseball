import json
import re
import requests
from datetime import datetime
from settings.team_object import Team
from settings.team_record_map import get_record_map
from settings.api import BASE_URL,TEAM_STATS_URI, TEAM_AT_HOME_URI, TEAM_AWAY_URI, TEAM_VS_LEFTY_URI, TEAM_VS_RIGHTY_URI



def get_team_stats():
    CURRENT_URL = BASE_URL + TEAM_STATS_URI
    try:
        RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    TEAM_STATS_DICT = JSON_RESPONSE['team_hitting_season_leader_master']['queryResults']['row']
    return TEAM_STATS_DICT

def get_all_team_names(d):
    for t in d:
        current_name = t['team_short']
        the_names = []
        the_names.append(current_name)
        return the_names

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

def get_standings():
    today = datetime.now().strftime('%Y/%m/%d')
    TEAM_STANDING_URI = '/named.standings_schedule_date.bam?season=2017&schedule_game_date.game_date=%27' + today + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
    CURRENT_URL = BASE_URL + TEAM_STANDING_URI
    try:
        TEAM_STANDING_RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    STANDING_TEXT = TEAM_STANDING_RESPONSE.text
    JSON_STANDINGS = json.loads(STANDING_TEXT)
    # Standings are in two blocks al and NL. This combines them.
    TEAM_STANDING_DICT = JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    TEAM_STANDING_DICT.extend(JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    return TEAM_STANDING_DICT


class Standings(object):
    TEAM_STATS_DICT = get_team_stats()
    ALL_TEAM_SHORT_NAMES = get_all_team_names(TEAM_STATS_DICT)
    for t in ALL_TEAM_SHORT_NAMES:
        print t
    TEAM_STANDING_DICT = get_standings()
    TEAM_AT_HOME_DICT = get_splits_by_uri(TEAM_AT_HOME_URI)
    TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)
    TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY_URI)
    TEAM_VS_RIGHTY_DICT = get_splits_by_uri(TEAM_VS_RIGHTY_URI)
    # From settings


 