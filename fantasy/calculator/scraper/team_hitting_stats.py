import json
import requests
from datetime import datetime
from calculator.settings.logger import log
from calculator.settings.api import BASE_URL, UPDATED_BASE_URL


TEAM_STATS_URI = 'named.team_hitting_season_leader_master.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&recSP=1&recPP=50'


def get_team_stats():
    print("TODO WRITE TESTS, get_team_stats")
    current_url = BASE_URL + TEAM_STATS_URI
    try:
        response = requests.get(current_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    stats_response = response.text
    json_stats = json.loads(stats_response)
    team_stats_dict = json_stats['team_hitting_season_leader_master']['queryResults']['row']
    return team_stats_dict
