import json
import os
import time
from behave import given, when, then, step
from static.team_map import TEAM_MAP
from calculator.scraper.league import get_all_team_names
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

@step('we load the test data "{file_name}"')
def step_impl(context, file_name):
    context.file_path = '../../stubbed_data/%s.json' % file_name
    test_data = os.path.join(
        os.path.dirname(__file__),
        context.file_path
    )
    with open(test_data) as f:
        double_quoted = f.read().replace('\'', "\"")
        context.current_data = json.loads(double_quoted)
        assert isinstance(context.current_data, dict)


@step('we create the MLB league map')
def step_impl(context):
    context.league = get_all_team_names(TEAM_MAP)


@step('the current stat should be an int equal to {number:d}')
def step_impl(context, number):
    assert isinstance(number, int)
    assert context.current_stat == number, 'Did not get expected int '\
        'of %d instead %d' % (number, context.current_stat)


@step('the current stat should be a float equal to {current_float:g}')
def step_impl(context, current_float):
    assert isinstance(current_float, float)
    context.current_float = round(current_float, 16)
    context.current_stat = round(context.current_stat, 16)
    assert context.current_stat == current_float, 'Did not get expected float '\
        'of %.16f instead %.16f' % (current_float, context.current_stat)
