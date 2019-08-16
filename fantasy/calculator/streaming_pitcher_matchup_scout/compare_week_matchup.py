
def get_arm_side():
    pitcher_arm_side_input = input('Is the picther a lefty or righty')
    pitcher_arm_side_input = pitcher_arm_side_input.lower
    if pitcher_arm_side_input == 'lefty' or pitcher_arm_side_input == 'l' \
        or pitcher_arm_side_input == left:
        pitcher_arm_side_input = 'left'
    elif pitcher_arm_side_input == 'righty' or pitcher_arm_side_input == 'r' \
        or pitcher_arm_side_input == 'right':
        pitcher_arm_side_input = 'right'
    else:
        print('Unrecognized arm side, try again.')
        get_arm_side()


def ask_for_matchups():
    input_response_2 = input('What are pitcher 1s matchups?')
    pitcher_1_matchups_list = [x.strip() for x in input_response_2.split(',')]
    pitcher_1_arm_side = get_arm_side()
    input_response_3 = input('What are pitcher 2s matchups?')
    pitcher_2_matchups_list = [x.strip() for x in input_response_3.split(',')]
    pitcher_2_arm_side = get_arm_side()
    return pitcher_1_matchups_list, pitcher_1_arm_side, pitcher_2_matchups_list, pitcher_2_arm_side

from calculator.mlbdotcom_teamscraper import calculate_all_team_expections
def get_league_data():
    mlb = calculate_all_team_expections()

def get_expected_week_outcomes(matchups_list, arm_side, league):
    if arm_side == 'left':
        pass
    elif arm_side == 'right':
        pass
    else:
        assert 1 == 2, 'How did I get here?'
