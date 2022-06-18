import json
import requests
from datetime import datetime
from calculator.settings.logger import log
from calculator.settings.api import BASE_URL, UPDATED_BASE_URL
from calculator.settings.api import TEAM_STATS_URI, log

def get_team_stats():
    log.debug("TODO WRITE TESTS, get_team_stats")
    current_url = BASE_URL + TEAM_STATS_URI
    log.debug('DATA SOURCE: %s' % current_url)
    try:
        response = requests.get(current_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    stats_response = response.text
    json_stats = json.loads(stats_response)
    team_stats_dict = json_stats['team_hitting_season_leader_master']['queryResults']['row']
    return team_stats_dict
