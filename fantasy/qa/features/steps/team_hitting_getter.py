import json
import os
import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from calculator.stat_finder.team_hitting_getter import *


start_dir = os.path.dirname(__file__)

@given('we have stubbed hitting data')
def step_impl(context):
    team_stats = '../../stubbed_data/team_hitting_season_leader_master.json'
    full_path = os.path.join(start_dir, team_stats)
    with open(full_path) as data_file:
        context.TEAM_HITTING_JSON = json.load(data_file)

@step('we get the relevant part of the hitting json')
def step_impl(context):
    context.TEAM_HITTING_STATS = get_relevant_part_of_hitting_dict(context.TEAM_HITTING_JSON)

@step('we expect miami to be the third team in TEAM_HITTING_STATS')
def step_impl(context):
    assert context.TEAM_HITTING_STATS[3]['team_short'] == 'Miami', \
        'didn\'t get expected code instead got %s' % (
            context.TEAM_HITTING_STATS[3]['team_short']
        )

@step('we get the short name for team 3')
def step_impl(context):
    context.short_name = get_short_name_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect short name to be "{name}"')
def step_impl(context, name):
    assert context.short_name == 'Miami', \
        'didn\'t get expected name instead got %s' % (
            context.short_name
        )

@step('we get at bats for team 3')
def step_impl(context):
    context.at_bats = get_atbats_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect at bats to be "{number:d}"')
def step_impl(context, number):
    assert context.at_bats == 3785, \
        'didn\'t get expected ab instead got %s' % (
            context.at_bats
        )

@step('we get RBIs for team 3')
def step_impl(context):
    context.rbis = get_rbis_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect RBIs to be "{number:d}"')
def step_impl(context, number):
    assert context.rbis == number, \
        'didn\'t get expected rbis instead got %s' % (
            context.rbis
        )

@step('we get walks for team 3')
def step_impl(context):
    context.walks = get_walks_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect walks to be "{number:d}"')
def step_impl(context, number):
    assert context.walks == number, \
        'didn\'t get expected walks instead got %s' % (
            context.walks
        )

@step('we get runs for team 3')
def step_impl(context):
    context.runs = get_runs_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect runs to be "{number:d}"')
def step_impl(context, number):
    assert context.runs == number, \
        'didn\'t get expected runs instead got %s' % (
            context.runs
        )

@step('we get strikeouts for team 3')
def step_impl(context):
    context.strikeouts = get_strikeouts_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect strikeouts to be "{number:d}"')
def step_impl(context, number):
    assert context.strikeouts == number, \
        'didn\'t get expected runs instead got %s' % (
            context.strikeouts
        )

@step('we get total games for team 3')
def step_impl(context):
    context.games = get_games_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect total games to be "{number:d}"')
def step_impl(context, number):
    assert context.games == number, \
        'didn\'t get expected huns instead got %s' % (
            context.games
        )

@step('we get hits for team 3')
def step_impl(context):
    context.hits = get_hits_from_json(context.TEAM_HITTING_STATS[3])

@step('we expect hits to be "{number:d}"')
def step_impl(context, number):
    assert context.hits == number, \
        'didn\'t get expected huns instead got %s' % (
            context.hits
        )
