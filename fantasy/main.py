from calculator.full_season_forecaster.pitcher_inning_extrapelator import inning_extrapolator
from calculator.mlbdotcom_teamscraper import calculate_all_team_expections

input = raw_input('What would you like to do?\n' \
    '(options: pitcher extrapolator, calculate all splits, ' \
    'compare 2 matchup week)\n'
)

if 'pitcher extrapolator' in input:
    inning_extrapolator()
elif 'calculate all splits' in input:
    calculate_all_team_expections()
else:
    assert 1 == 2, 'working on it'


# if __name__ == main():
    # TODO
