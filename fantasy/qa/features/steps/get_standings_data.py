import time
from behave import given, when, then, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from calculator.scraper.standings_data import StandingsData


@step('we load the test data for single team standings')
def step_impl(context):
    context.execute_steps(u'''Given we load the test data "single_team_standings"''')

@step('we create a standings object')
def step_impl(context):
    context.standings = StandingsData()

@step('the current stat should be a float equal to "{current_float:g}"')
def step_impl(context, current_float):
    context.current_float = float(current_float)
    context.current_stat = float(context.current_stat)
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


        #
        # wins_avg_right, loss_avg_right, g_v_right = standings.get_vs_right(standings_data)
        # assert wins_avg_right == 0.6046511627906976, 'did not get expected wins_avg_right %d' % wins_avg_right
        # assert loss_avg_right == 0.3953488372093023, 'did not get expected loss_avg_right %d' % loss_avg_right
        # assert g_v_right == 86, 'did not get expected g_v_right %d' % g_v_right
        #
        # w_avg_road, l_avg_road, g_at_road = standings.get_at_road(standings_data)
        # assert w_avg_road == 0.5666666666666667, 'did not get expected w_avg_road %d' % w_avg_road
        # assert l_avg_road == 0.43333333333333335, 'did not get expected l_avg_road %d' % l_avg_road
        # assert g_at_road == 60, 'did not get expected g_at_road %d' % g_at_road
        #
        # games = standings.get_games_total(standings_data)
        # assert games == 118, 'Didn\'t get expected total games'
        #
        # win_avg = standings.set_win_avg(standings_data)
        # assert win_avg == 0.652542372881356, 'Didn\'t get expected win_avg'
        #
        # loss_avg = standings.set_loss_avg(standings_data)
        # assert loss_avg == 0.4067796610169492, 'Didn\'t get expected loss_avg'
        #
        # run_avg = standings.get_run_avg(standings_data)
        # assert run_avg == 5.533898305084746, 'Didn\'t get expected run_avg'
