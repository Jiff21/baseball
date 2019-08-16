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
