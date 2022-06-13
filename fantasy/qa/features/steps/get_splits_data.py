import time
from behave import given, when, then, step
from calculator.scraper.team_splits_stats import SplitsScraper

@step('we load the test data for single team "{split_type}" Splits')
def step_impl(context, split_type):
    split_type = split_type.lower()
    if split_type == 'home':
        context.execute_steps(
            u'''Given we load the test data "single_team_home_split"'''
        )
    elif split_type == 'road':
        context.execute_steps(
            u'''Given we load the test data "single_team_road_split"'''
        )
    elif split_type == 'lefty':
        context.execute_steps(
            u'''Given we load the test data "single_team_lefty_splits"'''
        )
    elif split_type == 'righty':
        context.execute_steps(
            u'''Given we load the test data "single_team_righty_splits"'''
        )


@step('we create a SplitsScraper object')
def step_impl(context):
    context.split_scraper = SplitsScraper()


@step('we get runs')
def step_impl(context):
    context.current_stat = context.split_scraper.get_runs(context.current_data)


@step('we get rbi')
def step_impl(context):
    context.current_stat = context.split_scraper.get_rbi(context.current_data)


@step('we get games')
def step_impl(context):
    context.current_stat = context.split_scraper.get_games(context.current_data)


@step('we get hits')
def step_impl(context):
    context.current_stat = context.split_scraper.get_hits(context.current_data)


@step('we get homeruns')
def step_impl(context):
    context.current_stat = context.split_scraper.get_home_runs(
        context.current_data
    )


@step('we get walks')
def step_impl(context):
    context.current_stat = context.split_scraper.get_walks(
        context.current_data
    )


@step('we get strikeouts')
def step_impl(context):
    context.current_stat = context.split_scraper.get_strikeouts(
        context.current_data
    )


@step('we get plate appearances')
def step_impl(context):
    context.current_stat = context.split_scraper.get_plate_appearances(
        context.current_data
    )


@step('we set runs to {runs:d} and games to {games:d}')
def step_impl(context, runs, games):
    context.runs = runs
    context.games = games


@step('we get runs per game')
def step_impl(context):
    context.current_stat = context.split_scraper.get_runs_per_game(
        context.runs,
        context.games
    )






#
# @step('the current stat should be a float equal to "{current_float:g}"')
# def step_impl(context, current_float):
#     context.current_float = round(current_float, 16)
#     context.current_stat = round(context.current_stat, 16)
#     assert context.current_stat == current_float, 'Did not get expected float '\
#         'of %.16f instead %.16f' % (current_float, context.current_stat)
#
# @step('the current stat should be an int equal to "{number:d}"')
# def step_impl(context, number):
#     # number = int(number)
#     assert context.current_stat == number, 'Did not get expected int '\
#         'of %d instead %d' % (number, context.current_stat)
#
# @step('we get wins')
# def step_impl(context):
#     context.current_stat = context.standings.get_wins(context.current_data)
#
# @step('we get losses')
# def step_impl(context):
#     context.current_stat = context.standings.get_losses(context.current_data)
#
# @step('we get standings for a righty pitching splits')
# def step_impl(context):
#     context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_vs_right(context.current_data)
#
# @step('we get standings for a lefty pitching splits')
# def step_impl(context):
#     context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_vs_left(context.current_data)
#
# @step('we get standings for home pitching splits')
# def step_impl(context):
#     context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_at_home(context.current_data)
#
# @step('we get standings for road pitching splits')
# def step_impl(context):
#     context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_at_road(context.current_data)
#
# @step('we set the win avg to the current stat')
# def step_impl(context):
#     context.current_stat = context.win_avg_split
#
# @step('we set the loss avg to the current stat')
# def step_impl(context):
#     context.current_stat = context.loss_avg_split
#
# @step('we set the game avg to the current stat')
# def step_impl(context):
#     context.current_stat = context.game_avg_split
#
# @step('we get total games')
# def step_impl(context):
#     context.current_stat = context.standings.get_games_total(context.current_data)
#
# @step('we set the win avg')
# def step_impl(context):
#     context.current_stat = context.standings.set_win_avg(context.current_data)
#
# @step('we set the loss avg')
# def step_impl(context):
#     context.current_stat = context.standings.set_loss_avg(context.current_data)
#
# @step('we get run avg')
# def step_impl(context):
#     context.current_stat = context.standings.get_run_avg(context.current_data)
#
# @step('we get the standings from mlb api')
# def step_impl(context):
#     context.standings_api_data = get_standings()
#
# # Move this to scraper.standings
# from calculator.mlbdotcom_teamscraper import set_league_standings_data
# @step('we map standings to teams')
# def step_impl(context):
#     standings_data = StandingsData()
#     set_league_standings_data(context.standings_api_data)
#     print(context.league['HOU'].wins)
# #     for text in context.standings_data:
# #         print(text)
#     # assert 1 == 2, 'Still to do'
#
# @step('standings should have set "{games}" to "{expected_value}" for "{team_abbrev}"')
# def step_impl(context, games, expected_value, team_abbrev):
#     assert context.league['HOU'].abbr == 'HOU', context.mlb['HOU'].abbr
#     # assert context.league[team_abbrev].wins == expected_value, mlb[team_abbrev].wins
