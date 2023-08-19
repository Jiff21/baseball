import json
import requests
from datetime import datetime
from calculator.settings.logger import log
from calculator.settings.api import BASE_URL, UPDATED_BASE_URL
from calculator.settings.api import TEAM_STATS_URI, log

def get_team_stats():
    log.debug("TODO WRITE TESTS, get_team_stats")
    current_url = UPDATED_BASE_URL + TEAM_STATS_URI
    log.debug('DATA SOURCE: %s' % current_url)
    try:
        response = requests.get(current_url)
    except requests.exceptions.RequestException as e:
        print('Error in get_team_stats')
        print(e)
        sys.exit(1)
    print("WOKRING ON MAKING THIS WORK. For Reason TEAM ABV does not match ARI va AZ. Switch to teamAbbrev")
    team_stats_dict = response.json()['stats']
    # team_stats_dict = json_stats['stats']
    return team_stats_dict
