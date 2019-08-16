import re

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
        w_avg_home, w_avg_home, g_at_home = self.break_dash_record_split(current_dict, 'home')
        return w_avg_home, w_avg_home, g_at_home

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
