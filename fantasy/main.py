from calculator.full_season_forecaster.pitcher_inning_extrapelator import inning_extrapolator
from calculator.mlbdotcom_teamscraper import calculate_all_team_expections
from calculator.streaming_pitcher_matchup_scout.compare_week_matchup import print_expected_matchups
from calculator.streaming_pitcher_matchup_scout.compare_week_matchup import print_expected_matchups_detailed

def main():
    input_response_1 = input('What would you like to do?\n' \
        '(options: pitcher extrapolator, calculate all splits, ' \
        'compare 2 SP matchup)\n'
    )
    input_response_1 = input_response_1.lower()

    if 'pitcher extrapolator' in input_response_1:
        inning_extrapolator()
    elif 'calculate all splits' in input_response_1:
        calculate_all_team_expections()
    elif 'compare 2 sp matchup detailed' in input_response_1 or 'compare sp detail' in input_response_1:
        print_expected_matchups_detailed()
    elif 'compare 2 sp matchup' in input_response_1 or 'compare sp' in input_response_1:
        print_expected_matchups()
    elif 'exit' in input_response_1 or input_response_1 == 'e':
        pass
    else:
        print('Unrecognized option. Try again\n')
        main()


if __name__ == "__main__":
    # execute only if run as a script
    main()
