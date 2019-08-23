from calculator.full_season_forecaster.run_pitcher_forecaster import PitchingExtrapolator
from calculator.full_season_forecaster.batter_forecaster import BatterExtrapolator
from calculator.mlbdotcom_teamscraper import calculate_all_team_expections
from calculator.streaming_pitcher_matchup_scout.compare_week_matchup import print_expected_matchups
from calculator.streaming_pitcher_matchup_scout.compare_week_matchup import print_expected_matchups_detailed
from calculator.streaming_pitcher_matchup_scout.splits_leaderboard import leaderboard_controller


def start():
    input_response_1 = input('What would you like to do?\n' \
        '\t1. Leaderboards\n\t2. Calculate all splits\n' \
        '\t3. Compare SP matchups\n\t4. Compare SP detailed\n' \
        '\t5. Pitcher extrapolator\n\t6. Batter extrapolator\n'
    )
    input_response_1 = input_response_1.lower()
    if input_response_1 == '1' or 'Leaderboard' in input_response_1:
        leaderboard_controller()
    elif input_response_1 == '2' or 'calculate all splits' in input_response_1:
        calculate_all_team_expections()
    elif input_response_1 == '3' or \
    'compare 2 sp matchup' in input_response_1 or \
    'compare sp' in input_response_1:
        print_expected_matchups()
    elif input_response_1 == '4' or \
    'compare 2 sp matchup detailed' in input_response_1 or \
    'compare sp detail' in input_response_1:
        print_expected_matchups_detailed()
    elif input_response_1 == '5' or 'pitcher extrapolator' in input_response_1:
        pitching_extrapolator = PitchingExtrapolator()
        pitching_extrapolator.run()
    elif input_response_1 == '6' or 'batter extrapolator' in input_response_1:
        batter_extrapolator = BatterExtrapolator()
        batter_extrapolator.run()
    elif 'exit' in input_response_1 or input_response_1 == 'e':
        exit()
    else:
        print('Unrecognized option. Try again\n')
        start()
