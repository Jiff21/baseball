from calculator.settings.logger import log
from calculator.mlbdotcom_teamscraper import calculate_all_team_expections
import main


mlb = calculate_all_team_expections()


def get_left_leaderboard(league):
    list = []
    for team in league:
        list.append((
            league[team].expected_game_lefty_split,
            team
        ))
    list.sort(reverse=True)
    return list


def get_righty_leaderboard(league):
    list = []
    for team in league:
        list.append((
            league[team].expected_game_righty_split,
            team
        ))
    list.sort(reverse=True)
    return list


def get_home_leaderboard(league):
    list = []
    for team in league:
        list.append((
            league[team].expected_game_home_split,
            team
        ))
    list.sort(reverse=True)
    return list


def get_away_leaderboard(league):
    list = []
    for team in league:
        list.append((
            league[team].expected_game_away_split,
            team
        ))
    list.sort(reverse=True)
    return list


def get_generic_leaderboard(league):
    list = []
    for team in league:
        list.append((
            league[team].expected_game_no_split,
            team
        ))
    list.sort(reverse=True)
    return list


def print_leaderboard(leaderboard):
    for score in leaderboard:
        print(score)


def print_generic_leaderboard():
    generic_expected_games = get_generic_leaderboard(mlb)
    print_leaderboard(generic_expected_games)


def print_lefty_leaderboard():
    all_lefty_expected_games = get_left_leaderboard(mlb)
    print_leaderboard(all_lefty_expected_games)


def print_righty_leaderboard():
    all_righty_expected_games = get_righty_leaderboard(mlb)
    print_leaderboard(all_righty_expected_games)


def print_home_leaderboard():
    all_home_expected_games = get_home_leaderboard(mlb)
    print_leaderboard(all_home_expected_games)


def print_road_leaderboard():
    all_road_expected_games = get_away_leaderboard(mlb)
    print_leaderboard(all_road_expected_games)


def leaderboard_controller():
    print('TODO: WRITE TESTS, something off left and right same')
    leaderboard_resp_1 = str(input(
        'What Leaderboard would you like to see?\n\t1. General Expected Game\n' \
        '\t2. Righty Splits\n\t3. Lefty Splits\n\t4. Home Splits\n' \
        '\t5. Road Splits\n\t6. Exit\n\t7. Main Menu\n'
    )).lower()
    if leaderboard_resp_1 == '1' or 'general' in leaderboard_resp_1:
        print('\n\nGeneric expected game:\n')
        print_generic_leaderboard()
    elif leaderboard_resp_1 == '2' or 'right' in leaderboard_resp_1:
        print('\n\nRighty Splits:\n')
        print_righty_leaderboard()
    elif leaderboard_resp_1 == '3' or 'left' in leaderboard_resp_1:
        print('\n\nLefty Splits:\n')
        print_lefty_leaderboard()
    elif leaderboard_resp_1 == '4' or 'home' in leaderboard_resp_1:
        print('\n\nHome Splits:\n')
        print_home_leaderboard()
    elif leaderboard_resp_1 == '5' or 'away' in leaderboard_resp_1 or 'road' in leaderboard_resp_1:
        print('\n\nRoad Splits:\n')
        print_road_leaderboard()
    elif leaderboard_resp_1 == 'exit' or leaderboard_resp_1 == '6':
        exit()
    elif leaderboard_resp_1 == 'main' or leaderboard_resp_1 == '7':
        main.main()
    else:
        print('Unrecognized option.\n')
    leaderboard_controller()
