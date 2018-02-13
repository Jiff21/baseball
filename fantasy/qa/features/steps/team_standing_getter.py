import json
import os
import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from calculator.stat_finder.team_standing_getter import get_relevant_part_of_standings_dict

start_dir = os.path.dirname(__file__)

@given('we have stubbed standing data')
def step_impl(context):
    team_stats = '../../stubbed_data/standings.json'
    full_path = os.path.join(start_dir, team_stats)
    with open(full_path) as data_file:
        context.TEAM_STANDING_JSON = json.load(data_file)

@step('we get the relevant part of the standings json')
def step_impl(context):
    context.TEAM_HITTING_STATS = get_relevant_part_of_standings_dict(context.TEAM_STANDING_JSON)

@step('TEAM_STANDING_DICT short code should be mia')
def step_impl(context):
    assert context.TEAM_STANDING_DICT[1]['file_code'] == 'mia', \
        'didn\'t get expected code instead got %s' % (
            context.TEAM_STANDING_DICT[1]['file_code']
        )



# @step('fail intentionally')
# def step_impl(context):
#     # print(context.TEAM_STANDING_JSON)
#     assert 1 == 2
