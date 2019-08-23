import json
import requests
from calculator.settings.logger import log
from calculator.settings.api import UPDATED_BASE_URL



def get_splits_by_uri(uri):
    print("TODO WRITE TESTS")
    current_url = UPDATED_BASE_URL + uri
    try:
        response = requests.get(current_url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    response_text = response.text
    response_json = json.loads(response_text)
    current_dict = response_json['team_hitting_season_leader_sit']['queryResults']['row']
    return current_dict
