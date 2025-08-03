from calculator.settings.logger import log
from calculator.full_season_forecaster.pitcher_calculator import calculate_game


# TODO: Write tests
class SplitExpectedGame(object):

    def __init__(self):
        """get necessary data from standings."""
        pass


    def calculate_generic_expected_game(self, team, league, innings=7):
        log.debug('calculating generic expected games')
        expected_game = calculate_game(
            innings, # AVG innings starter (could improve)
            league[team].runs_per_game,
            league[team].walks_per_game,
            league[team].hits_per_game,
            league[team].homeruns_per_game,
            league[team].strikeouts_per_game,
            0, # Saves
            league[team].win_avg,
            league[team].loss_avg,
            0 # quality_starts
        )
        league[team].expected_game_no_split = expected_game

    def calculate_lefty_expected_game(self, team, league, innings=7):
        log.debug('calculating expected_game_vs_left')
        expected_starter_plate_appearance = (innings/float(9)) * league[team].plate_appearences_per_game
        splits_r_expected = league[team].vs_l_r_per_pa * expected_starter_plate_appearance
        splits_h_expected = league[team].vs_l_h_per_pa * expected_starter_plate_appearance
        splits_hr_expected = league[team].vs_l_hr_per_pa * expected_starter_plate_appearance
        splits_bb_expected = league[team].vs_l_bb_per_pa * expected_starter_plate_appearance
        splits_so_expected = league[team].vs_l_so_per_pa * expected_starter_plate_appearance
        expected_game = calculate_game(
            innings, # AVG innings starter (could improve)
            splits_r_expected,
            splits_bb_expected,
            splits_h_expected,
            splits_hr_expected,
            splits_so_expected,
            0, # Saves
            league[team].wins_avg_left,
            league[team].losses_avg_left,
            0 # quality_starts
        )
        league[team].expected_game_lefty_split = expected_game

    def calculate_righty_expected_game(self, team, league, innings=7):
        log.debug('calculating righty expected game')
        expected_starter_plate_appearance = (innings/float(9)) * league[team].plate_appearences_per_game
        splits_r_expected = league[team].vs_r_r_per_pa * expected_starter_plate_appearance
        splits_h_expected = league[team].vs_r_h_per_pa * expected_starter_plate_appearance
        splits_hr_expected = league[team].vs_r_hr_per_pa * expected_starter_plate_appearance
        splits_bb_expected = league[team].vs_r_bb_per_pa * expected_starter_plate_appearance
        splits_so_expected = league[team].vs_r_so_per_pa * expected_starter_plate_appearance
        expected_game = calculate_game(
            innings, # AVG innings starter (could improve)
            splits_r_expected,
            splits_bb_expected,
            splits_h_expected,
            splits_hr_expected,
            splits_so_expected,
            0, # Saves
            league[team].wins_avg_right,
            league[team].loss_avg_right,
            0 # quality_starts
        )
        league[team].expected_game_righty_split = expected_game

    def calculate_home_expected_game(self, team, league, innings=7):
        log.debug('calculating home expected game')
        expected_game = calculate_game(
            innings, # AVG innings starter (could improve)
            league[team].home_r_pg,
            league[team].home_bb_pg,
            league[team].home_h_pg,
            league[team].home_hr_pg,
            league[team].home_so_pg,
            0, # Saves
            league[team].w_avg_home,
            league[team].l_avg_home,
            0 # quality_starts
        )
        league[team].expected_game_home_split = expected_game


    def calculate_away_expected_game(self, team, league, innings=7):
        log.debug('calculating home expected game')
        expected_game = calculate_game(
            innings, # AVG innings starter (could improve)
            league[team].away_r_pg,
            league[team].away_bb_pg,
            league[team].away_h_pg,
            league[team].away_hr_pg,
            league[team].away_so_pg,
            0, # Saves
            league[team].w_avg_road,
            league[team].l_avg_road,
            0 # quality_starts
        )
        league[team].expected_game_away_split = expected_game
