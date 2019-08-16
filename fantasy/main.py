from calculator.full_season_forecaster.pitcher_inning_extrapelator import inning_extrapolator
from calculator.mlbdotcom_teamscraper import calculate_all_team_expections

def main():
    input_response_1 = input('What would you like to do?\n' \
        '(options: pitcher extrapolator, calculate all splits, ' \
        'compare 2 matchup week)\n'
    )

    if 'pitcher extrapolator' in input_response_1:
        inning_extrapolator()
    elif 'calculate all splits' in input_response_1:
        calculate_all_team_expections()
    elif 'calculate all splits' in input_response_1:
        calculate_all_team_expections()
    else:
        assert 1 == 2, 'working on it'


if __name__ == "__main__":
    # execute only if run as a script
    main()
