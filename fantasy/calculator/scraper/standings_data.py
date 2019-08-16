import json
import re
import requests
from datetime import datetime
from calculator.settings.api import BASE_URL, TEAM_STANDING_URI

class StandingsData():

    def __init__(self):
        """get necessary data from standings."""
        pass

    def get_wins(self, current_dict):
        return int(current_dict['w'])

    def get_losses(self, current_dict):
        return int(current_dict['l'])

    def break_dash_record_split(self, current_dict, string):
        self.record_split = list(map(int, re.findall(r'\d+', current_dict[string])))
        self.first_number = float(self.record_split[0]) / (float(self.record_split[0]) + float(self.record_split[1]))
        self.second_number = float(self.record_split[1]) / (float(self.record_split[0]) + float(self.record_split[1]))
        self.total = float(self.record_split[0]) + float(self.record_split[1])
        return self.first_number, self.second_number, self.total

    def get_vs_left(self, current_dict):
        w_v_left, l_v_left, g_v_left = self.break_dash_record_split(current_dict, 'vs_left')
        return w_v_left, l_v_left, g_v_left

    def get_vs_right(self, current_dict):
        w_v_left, l_v_left, g_v_left = self.break_dash_record_split(current_dict, 'vs_right')
        return w_v_left, l_v_left, g_v_left

    def get_at_home(self, current_dict):
        w_avg_home, l_avg_home, g_at_home = self.break_dash_record_split(current_dict, 'home')
        return w_avg_home, l_avg_home, g_at_home

    def get_at_road(self, current_dict):
        w_avg_road, l_avg_road, g_at_road = self.break_dash_record_split(current_dict, 'away')
        return w_avg_road, l_avg_road, g_at_road

    def get_games_total(self, current_dict):
        self.wins = self.get_wins(current_dict)
        self.losses = self.get_losses(current_dict)
        return self.wins + self.losses

    def set_win_avg(self, current_dict):
        self.wins = self.get_wins(current_dict)
        self.total = self.get_games_total(current_dict)
        return self.wins / self.total

    def set_loss_avg(self, current_dict):
        self.losses = self.get_losses(current_dict)
        self.total = self.get_games_total(current_dict)
        return self.losses / self.total

    ## TODO think I have 2
    def get_run_avg(self, current_dict):
        games = self.get_games_total(current_dict)
        return int(current_dict['runs']) / games



def get_standings():
    today = datetime.now().strftime('%Y/%m/%d')
    # TEAM_STANDING_URI = '/named.standings_schedule_date.bam?season=2019&schedule_game_date.game_date=%27' + today + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
    CURRENT_URL = BASE_URL + TEAM_STANDING_URI
    # CURRENT_URL = UPDATED_BASE_URL + TEAM_STANDING_URI
    try:
        TEAM_STANDING_RESPONSE = requests.get(CURRENT_URL)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    STANDING_TEXT = TEAM_STANDING_RESPONSE.text
    # Text is cheating a comma in last, first, could load whole data otherwise
    # STANDING_TEXT = re.sub(r'\"[,]"', lambda x: x.group(0).replace(",", "\,"),  STANDING_TEXT)
    JSON_STANDINGS = json.loads(STANDING_TEXT)
    # Standings are in two blocks al and NL. This combines them.
    tsd = JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][0]['queryResults']['row']
    tsd.extend(JSON_STANDINGS['standings_schedule_date']['standings_all_date_rptr']['standings_all_date'][1]['queryResults']['row'])
    return tsd
