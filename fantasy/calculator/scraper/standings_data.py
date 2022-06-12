import json
import re
import requests
from datetime import datetime
from calculator.settings.api import BASE_URL, TEAM_STANDING_URL
from calculator.settings.logger import log
# from calculator.settings.api import STATS_API, STANDINGS_URI

class StandingsData():

    def __init__(self):
        """get necessary data from standings."""
        pass

    def get_wins(self, current_dict):
        log.debug('get wins')
        return int(current_dict['wins'])

    def get_losses(self, current_dict):
        return int(current_dict['losses'])
    #
    # def break_dash_record_split(self, current_dict, string):
    #     log.debug('break_dash_record_split no longer necessary')
    #     print('DELETE break_dash_record_split yet?')
    #     # print(current_dict['records']['splitRecords']['wins'])
    #     self.record_split = list(map(int, re.findall(r'\d+', current_dict[string])))
    #     self.first_number = float(self.record_split[0]) / (float(self.record_split[0]) + float(self.record_split[1]))
    #     self.second_number = float(self.record_split[1]) / (float(self.record_split[0]) + float(self.record_split[1]))
    #     self.total = float(self.record_split[0]) + float(self.record_split[1])
    #     return self.first_number, self.second_number, self.total

    def get_vs_left(self, current_dict):
        leftysplit = current_dict['records']['splitRecords'][2]
        log.debug('in get_vs_left leftysplit is \n%s\n' % leftysplit)
        assert(leftysplit['type'] == 'left')
        w_v_left = leftysplit['wins']
        l_v_left = leftysplit['losses']
        log.debug('TODO ? They have Win % should I just be doing that?')
        g_v_left = leftysplit['wins'] + leftysplit['losses']
        return w_v_left, l_v_left, g_v_left

    def get_vs_right(self, current_dict):
        rightysplit = current_dict['records']['splitRecords'][7]
        log.debug('in get_vs_right rightysplit is \n%s\n' % rightysplit)
        assert(rightysplit['type'] == 'right')
        w_v_right = rightysplit['wins']
        l_v_right = rightysplit['losses']
        g_v_right = rightysplit['wins'] + rightysplit['losses']
        return w_v_right, l_v_right, g_v_right

    def get_at_home(self, current_dict):
        homesplits = current_dict['records']['splitRecords'][0]
        log.debug('in get_at_home homesplits is \n%s\n' % homesplits)
        assert(homesplits['type'] == 'home')
        w_avg_home = homesplits['wins']
        l_avg_home = homesplits['losses']
        g_at_home = homesplits['wins'] + homesplits['losses']
        return w_avg_home, l_avg_home, g_at_home

    def get_at_road(self, current_dict):
        roadsplits = current_dict['records']['splitRecords'][1]
        log.debug('in get_at_road roadsplits is \n%s\n' % roadsplits)
        assert(roadsplits['type'] == 'away')
        w_avg_road = roadsplits['wins']
        l_avg_road = roadsplits['losses']
        g_at_road = roadsplits['wins'] + roadsplits['losses']
        return w_avg_road, l_avg_road, g_at_road

    def get_games_total(self, current_dict):
        # self.wins = self.get_wins(current_dict)
        # self.losses = self.get_losses(current_dict)
        # return self.wins + self.losses
        return current_dict['gamesPlayed']

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
        log.debug('in get_run_avg and %s has scored %s\n' % (
            current_dict['team']['abbreviation'],
            current_dict['runsScored']
        ))
        games = self.get_games_total(current_dict)
        return int(current_dict['runsScored']) / games



def get_standings():
    today = datetime.now().strftime('%Y/%m/%d')
    log.debug('TEAM_STANDING_URL is %s' % TEAM_STANDING_URL)
    try:
        TEAM_STANDING_RESPONSE = requests.get(TEAM_STANDING_URL)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    STANDING_TEXT = TEAM_STANDING_RESPONSE.text
    JSON_STANDINGS = json.loads(STANDING_TEXT)
    # Standings are in two blocks al and NL. This combines them.
    log.debug('use https://jsonpathfinder.com/ if they switch this again')
    tsd = JSON_STANDINGS['records'][0]['teamRecords']
    tsd.extend(JSON_STANDINGS['records'][1]['teamRecords'])
    tsd.extend(JSON_STANDINGS['records'][2]['teamRecords'])
    tsd.extend(JSON_STANDINGS['records'][3]['teamRecords'])
    tsd.extend(JSON_STANDINGS['records'][4]['teamRecords'])
    tsd.extend(JSON_STANDINGS['records'][5]['teamRecords'])
    return tsd
