import time
from behave import given, when, then, step
from calculator.scraper.standings_data import StandingsData, get_standings

@step('we load the test data for single team standings')
def step_impl(context):
    context.execute_steps(u'''Given we load the test data "single_team_standings"''')
#
# @step('we load the August 2018 standings test data')
# def step_impl(context):
#     context.execute_steps(u'''Given we load the test data "team_standings_2018_08_07"''')

@step('we create a standings object')
def step_impl(context):
    context.standings = StandingsData()

@step('the current stat should be a float equal to "{current_float:g}"')
def step_impl(context, current_float):
    context.current_float = round(current_float, 16)
    context.current_stat = round(context.current_stat, 16)
    assert context.current_stat == current_float, 'Did not get expected float '\
        'of %.16f instead %.16f' % (current_float, context.current_stat)

@step('the current stat should be an int equal to "{number:d}"')
def step_impl(context, number):
    # number = int(number)
    assert context.current_stat == number, 'Did not get expected int '\
        'of %d instead %d' % (number, context.current_stat)

@step('we get wins')
def step_impl(context):
    context.current_stat = context.standings.get_wins(context.current_data)

@step('we get losses')
def step_impl(context):
    context.current_stat = context.standings.get_losses(context.current_data)

@step('we get standings for a righty pitching splits')
def step_impl(context):
    context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_vs_right(context.current_data)

@step('we get standings for a lefty pitching splits')
def step_impl(context):
    context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_vs_left(context.current_data)

@step('we get standings for home pitching splits')
def step_impl(context):
    context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_at_home(context.current_data)

@step('we get standings for road pitching splits')
def step_impl(context):
    context.win_avg_split, context.loss_avg_split, context.game_avg_split  = context.standings.get_at_road(context.current_data)

@step('we set the win avg to the current stat')
def step_impl(context):
    context.current_stat = context.win_avg_split

@step('we set the loss avg to the current stat')
def step_impl(context):
    context.current_stat = context.loss_avg_split

@step('we set the game avg to the current stat')
def step_impl(context):
    context.current_stat = context.game_avg_split

@step('we get total games')
def step_impl(context):
    context.current_stat = context.standings.get_games_total(context.current_data)

@step('we set the win avg')
def step_impl(context):
    context.current_stat = context.standings.set_win_avg(context.current_data)

@step('we set the loss avg')
def step_impl(context):
    context.current_stat = context.standings.set_loss_avg(context.current_data)

@step('we get run avg')
def step_impl(context):
    context.current_stat = context.standings.get_run_avg(context.current_data)

@step('we get the standings from mlb api')
def step_impl(context):
    context.standings_api_data = get_standings()

# Move this to scraper.standings
from calculator.mlbdotcom_teamscraper import set_league_standings_data
@step('we map standings to teams')
def step_impl(context):
    standings_data = StandingsData()
    set_league_standings_data(context.standings_api_data)
    print(context.league['HOU'].wins)
#     for text in context.standings_data:
#         print(text)
    # assert 1 == 2, 'Still to do'

@step('standings should have set "{games}" to "{expected_value}" for "{team_abbrev}"')
def step_impl(context, games, expected_value, team_abbrev):
    assert context.league['HOU'].abbr == 'HOU', context.mlb['HOU'].abbr
    # assert context.league[team_abbrev].wins == expected_value, mlb[team_abbrev].wins
