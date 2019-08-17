from calculator.mlbdotcom_teamscraper import calculate_all_team_expections

def get_arm_side():
    pitcher_arm_side_input = input('Is the pitcher a lefty or righty?\n')
    pitcher_arm_side_input = pitcher_arm_side_input.lower().strip()
    if pitcher_arm_side_input == 'lefty' or pitcher_arm_side_input == 'l' \
        or pitcher_arm_side_input == 'left':
        pitcher_arm_side = 'left'
    elif pitcher_arm_side_input == 'righty' or pitcher_arm_side_input == 'r' \
        or pitcher_arm_side_input == 'right':
        pitcher_arm_side = 'right'
    else:
        print('Unrecognized arm side, try again?')
        get_arm_side()
    return pitcher_arm_side

def check_matchups_recognized(matchups_list, league):
    for team in matchups_list:
        if team not in league:
            print('Unrecognized team in matchups. Start Over.\n')
            ask_for_matchups(league)

def ask_for_matchups(league):
    pitcher_1_matchups_list = []
    pitcher_2_matchups_list = []
    input_response_2 = input('What are the first pitchers matchups?\n').upper()
    pitcher_1_matchups_list = [x.strip() for x in input_response_2.split(',')]
    check_matchups_recognized(pitcher_1_matchups_list, league)
    pitcher_1_arm_side = get_arm_side()
    input_response_3 = input('What are the second pitchers matchups?\n').upper()
    pitcher_2_matchups_list = [x.strip() for x in input_response_3.split(',')]
    check_matchups_recognized(pitcher_2_matchups_list, league)
    pitcher_2_arm_side = get_arm_side()
    return pitcher_1_matchups_list, pitcher_1_arm_side, pitcher_2_matchups_list, pitcher_2_arm_side


def expected_matchup_righty(team_abbr, league):
    return league[team_abbr].expected_game_righty_split

def expected_matchup_lefty(team_abbr, league):
    return league[team_abbr].expected_game_lefty_split


def get_expected_week_outcomes(matchups_list, arm_side, league):
    expected = 0.0
    if arm_side == 'left':
        for matchup in matchups_list:
            add = expected_matchup_lefty(matchup, league)
            # import pdb; pdb.set_trace()
            expected += add
    elif arm_side == 'right':
        for matchup in matchups_list:
            add = expected_matchup_righty(matchup, league)
            expected += add
    else:
        assert 1 == 2, 'How did I get here??\n'
    return expected


def print_expected_matchups():
    mlb = calculate_all_team_expections()
    pitcher_1_matchups_list, pitcher_1_arm_side, pitcher_2_matchups_list, pitcher_2_arm_side = ask_for_matchups(mlb)
    pitcher_1_total = get_expected_week_outcomes(pitcher_1_matchups_list, pitcher_1_arm_side, mlb)
    pitcher_2_total = get_expected_week_outcomes(pitcher_2_matchups_list, pitcher_2_arm_side, mlb)
    print('Pitcher 1s total for his arm side is %f' % pitcher_1_total)
    print('Pitcher 2s total for his arm side is %f' % pitcher_2_total)
