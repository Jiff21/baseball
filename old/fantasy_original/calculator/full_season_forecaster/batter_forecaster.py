from calculator.settings.logger import log
from calculator.settings.scoring_settings import ScoringSettings
import main

# ssp = ScoringSettings.Batting

class BatterExtrapolator(object):

    def __self__(self):
        log.debug('Running Batter extrapolator')

    def get_plate_appearances(self):
        return float(
            input('How many Plate Appearances does/did the '
            'batter have?\n\t\t\t\t\t\t')
        )

    def get_current_points(self):
        return float(
            input('How many Points does/did the ' \
            'batter have?\n\t\t\t\t\t\t')
        )

    def get_points_per_pa(self):
        plate_appearances = self.get_plate_appearances()
        points = self.get_current_points()
        return points/plate_appearances

    def get_expected_pas(self):
        bo_number = float(
            input('How many Plate Appears do you expect/did the batter ' \
            'to have next year?\nLinupe spot:1=670,2=650,3=630,5=581,6=541,7=523' \
            '8=460\n\t\t\t\t\t\t')
        )
        if bo_number == 1.0:
            exp_pa = 670
        elif bo_number == 2.0:
            exp_pa = 650
        elif bo_number == 3.0:
            exp_pa = 630
        elif bo_number == 4.0:
            exp_pa = 600
        elif bo_number == 5.0:
            exp_pa = 581
        elif bo_number == 6.0:
            exp_pa = 541
        elif bo_number == 7.0:
            exp_pa = 523
        else:
            exp_pa = bo_number
        return exp_pa

    def ask_for_details(self, previous_total):
        quest = input(
            'Do you want to hedge with previous year?\n\t\t\t\t\t\t'
        ).lower().strip()
        if quest == 'yes' or quest == 'y':
            points_per_pa = self.get_points_per_pa()
            expected_pas = self.get_expected_pas()
            expected_pts = points_per_pa * expected_pas
            averaged = (previous_total + expected_pts) / 2
            print('\nThe batter would score %.2f next year.\n' % averaged)
        e_prompt = input('\nExit?\n\t\t\t\t\t\t')
        if e_prompt == 'y' or e_prompt == 'yes':
            exit()
        else:
            main.main()


    def run(self):
        points_per_pa = self.get_points_per_pa()
        expected_pas = self.get_expected_pas()
        expected_pts = points_per_pa * expected_pas
        print('The batter would score %.2f next year.\n' % expected_pts)
        self.ask_for_details(expected_pts)
