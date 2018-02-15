import json
import os
import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from calculator.stat_finder.team_standing_getter import *

start_dir = os.path.dirname(__file__)

@given('we have stubbed team standings data')
def step_impl(context):
    team_stats = '../../stubbed_data/team_standings_2018_08_07.json'
    full_path = os.path.join(start_dir, team_stats)
    with open(full_path) as data_file:
        context.TEAM_STANDING_JSON = json.load(data_file)

@step('we get the relevant part of the standings json')
def step_impl(context):
    context.TEAM_STANDING_DICT = get_relevant_part_of_standings_dict(context.TEAM_STANDING_JSON)

@step('TEAM_STANDING_DICT short code should be mia')
def step_impl(context):
    assert context.TEAM_STANDING_DICT[1]['file_code'] == 'mia', \
        'didn\'t get expected code instead got %s' % (
            context.TEAM_STANDING_DICT[1]['file_code']
        )

@step('we get wins for team 1 from standings')
def step_impl(context):
    context.wins = get_wins_from_standing_dict(context.TEAM_STANDING_DICT[1])

@step('wins should be "{number:d}"')
def step_impl(context, number):
    assert context.wins ==  number, \
        'didn\'t get expected wins instead got %i' % (
            context.wins
        )

@step('we get losses for team 1 from standings')
def step_impl(context):
    context.losses = get_losses_from_standing_dict(context.TEAM_STANDING_DICT[1])

@step('losses should be "{number:d}"')
def step_impl(context, number):
    assert context.losses ==  number, \
        'didn\'t get expected losses instead got %i' % (
            context.losses
        )

@step('we get games for team 1 from standings')
def step_impl(context):
    context.games = get_games_from_standing_dict(context.TEAM_STANDING_DICT[1])

@step('games should be "{number:d}"')
def step_impl(context, number):
    assert context.games ==  number, \
        'didn\'t get expected games instead got %i' % (
            context.games
        )

@step('get verse righty team standings')
def step_impl(context):
    context.w_v_right, context.l_v_right, context.g_v_right = \
        get_righty_from_standing_dict(context.TEAM_STANDING_DICT[1])

@step('win percentage verse righties should be "{number:f}"')
def step_impl(context, number):
    assert round(context.w_v_right,6) ==  round(number,6), \
        'didn\'t get expected wins instead got %f' % (
            round(context.w_v_right,6)
        )

@step('loss percentage verse righties should be "{number:f}"')
def step_impl(context, number):
    assert round(context.l_v_right,6) ==  round(number,6), \
        'didn\'t get expected losses instead got %f' % (
            round(context.l_v_right,6)
        )

@step('team game verse righties should be "{number:d}"')
def step_impl(context, number):
    assert context.g_v_right ==  number, \
        'didn\'t get expected games instead got %i' % (
            context.g_v_right
        )

@step('get verse lefties team standings')
def step_impl(context):
    context.w_v_left, context.l_v_left, context.g_v_left = \
        get_lefty_from_standing_dict(context.TEAM_STANDING_DICT[1])

@step('win percentage verse lefties should be "{number:f}"')
def step_impl(context, number):
    assert round(context.w_v_left,6) ==  round(number,6), \
        'didn\'t get expected wins instead got %f' % (
            round(context.w_v_left,6)
        )

@step('loss percentage verse lefties should be "{number:f}"')
def step_impl(context, number):
    assert round(context.l_v_left,6) ==  round(number,6), \
        'didn\'t get expected losses instead got %f' % (
            round(context.l_v_left,6)
        )

@step('team game verse lefties should be "{number:d}"')
def step_impl(context, number):
    assert context.g_v_left ==  number, \
        'didn\'t get expected games instead got %i' % (
            context.g_v_left
        )

@step('get all win/loss data from standings')
def step_impl(context):
    context.win_avg, context.loss_avg, context.games, context.w_v_left, \
    context.l_v_left, context.w_v_right, context.l_v_right, context.w_at_home, \
    context.l_at_home, context.w_on_road, context.l_on_road, context.g_v_left, \
    context.g_v_right, context.g_at_home, context.g_on_road = \
    return_wins_losses(context.TEAM_STANDING_DICT[1])

@step('general win average should be "{number:f}"')
def step_impl(context, number):
    assert round(context.win_avg,4) ==  round(number,4), \
        'didn\'t get expected wins instead got %f' % (
            round(context.win_avg,4)
        )

@step('general loss average should be "{number:f}"')
def step_impl(context, number):
    assert round(context.loss_avg,4) ==  round(number,4), \
        'didn\'t get expected losses instead got %f' % (
            round(context.loss_avg,4)
        )

@step('team games at home should be "{number:d}"')
def step_impl(context, number):
    assert context.g_at_home ==  number, \
        'didn\'t get expected games instead got %i' % (
            context.g_at_home
        )

@step('road win average should be "{number:f}"')
def step_impl(context, number):
    assert round(context.w_on_road,4) ==  round(number,4), \
        'didn\'t get expected win average instead got %f' % (
            round(context.w_on_road,4)
        )

@step('road loss average should be "{number:f}"')
def step_impl(context, number):
    assert round(context.l_on_road,4) ==  round(number,4), \
        'didn\'t get expected loss average instead got %f' % (
            round(context.l_on_road,4)
        )


@step('When I create a team')
def step_impl(context):
    team_object = Team('Miami', win_avg, loss_avg, games, w_v_left, l_v_left,
        g_v_left, w_v_right, l_v_right,g_v_right, w_at_home, l_at_home, \
        g_at_home, w_on_road, l_on_road, g_on_road)
