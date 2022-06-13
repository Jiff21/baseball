import json
import re
import requests
from datetime import datetime
from calculator.settings.team_object import Team
from calculator.settings.team_record_map import get_record_map
from calculator.settings.api import BASE_URL,TEAM_STATS_URI, TEAM_AT_HOME_URI, TEAM_AWAY_URI, TEAM_VS_LEFTY_URI, TEAM_VS_RIGHTY_URI
from calculator.stat_finder.team_standing_getter import get_standings
from calculator.mlbdotcom_teamscape import get_splits_by_uri


def get_team_stats():
    CURRENT_URL = BASE_URL + TEAM_STATS_URI
    try:
        RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    TEXT = RESPONSE.text
    JSON_RESPONSE = json.loads(TEXT)
    TEAM_STATS_DICT = JSON_RESPONSE['team_hitting_season_leader_master']['queryResults']['row']
    return TEAM_STATS_DICT

def get_all_team_names(passed_json):
    the_names = []
    log.debug('all team abbreviation, but from team_short')
    for t in passed_json:
        log.debug(t['team_short'])
        current_name = t['team_short']
        the_names.append(current_name)
    return the_names



class Standings(object):
    TEAM_STATS_DICT = get_team_stats()
    ALL_TEAM_SHORT_NAMES = get_all_team_names(TEAM_STATS_DICT)
    TEAM_STANDING_DICT = get_standings()
    TEAM_AT_HOME_DICT = get_splits_by_uri(TEAM_AT_HOME_URI)
    TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)
    TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY_URI)
    TEAM_VS_RIGHTY_DICT = get_splits_by_uri(TEAM_VS_RIGHTY_URI)
    # From settings
