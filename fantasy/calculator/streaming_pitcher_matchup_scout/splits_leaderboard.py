import csv
import datetime
import main
from calculator.settings.logger import log
from calculator.mlbdotcom_teamscraper import calculate_all_team_expections
from static.team_map import TEAM_MAP


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

def get_where(team, tuple_list):
    for t in tuple_list:
        if team == t[1]:
            return t[0]

def write_to_csv():
    all_lefty_expected_games = get_left_leaderboard(mlb)
    all_righty_expected_games = get_righty_leaderboard(mlb)
    all_home_expected_games = get_home_leaderboard(mlb)
    all_road_expected_games = get_away_leaderboard(mlb)

    sheet_path = 'calculator/data/splits_leaderboard.csv'    

    column_titles = ['Team', 'righty', 'lefty', 'home', 'road', 'lefty at', 'lefty vs', 'righty at', 'righty vs']
    
    with open(sheet_path, "w") as csvFile:
        # Write an empty CSV with the header we will use in that CSV. 
        writer = csv.DictWriter(csvFile, fieldnames=column_titles)
        writer.writeheader()
        for team in TEAM_MAP:
            lefty = get_where(team, all_lefty_expected_games)
            righty = get_where(team, all_righty_expected_games)
            home = get_where(team, all_home_expected_games)
            road = get_where(team, all_road_expected_games)
            lefty_home = (lefty + home)/2
            lefty_road = (lefty + road)/2
            righty_home = (righty + home)/2
            righty_road = (righty + road)/2
            writer.writerow(
                {
                    'Team': team,
                    'righty': righty,
                    'lefty': lefty,
                    'home': home,
                    'road': road,
                    'lefty at': lefty_home, 
                    'lefty vs': lefty_road, 
                    'righty at': righty_home, 
                    'righty vs': righty_road
                }
            )


def leaderboard_controller():
    leaderboard_resp_1 = str(input(
        'What Leaderboard would you like to see?\n\t1. General Expected Game\n' \
        '\t2. Righty Splits\n\t3. Lefty Splits\n\t4. Home Splits\n' \
        '\t5. Road Splits\n\t6. CSV\n\t8. Main Menu\n\t0. Exit\n'
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
    elif leaderboard_resp_1 == '6' or 'csv' in leaderboard_resp_1 or 'print' in leaderboard_resp_1:
        print('\n\nWrite CSV:\n')
        write_to_csv()
    elif leaderboard_resp_1 == 'exit' or leaderboard_resp_1 == '9':
        exit()
    elif leaderboard_resp_1 == 'main' or leaderboard_resp_1 == '8':
        main.main()
    else:
        print('Unrecognized option.\n')
    leaderboard_controller()
