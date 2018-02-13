import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from calculator.full_season_forecaster.pitcher_calaculator import calculate_game

@given('Scoring Settings are set to default')
def step_impl(context):
    class ScoringSettings(object):
    	class Batting(object):
    		S = 1
    		D = 2
    		T = 3
    		HR = 4
    		BB = 1
    		IBB = 1
    		HBP = 1
    		R = 1
    		RBI = 1
    		SB = 2
    		CS = -1
    		SO = -1
    	class Pitching(object):
    		BB = -1.0
    		BBI = -1.0
    		ER = -1.0
    		HA = -1.0
    		HB = -1.0
    		HRA = -3.0
    		INN = 3.0
    		K = 1.0
    		W = 5.0
    		L = -3.0
    		S = 5.0
    		QS = 0.0

    ssp = ScoringSettings.Pitching
    # Defaults
    context.saves = 0.0
    context.wins = 0.0
    context.losses = 0.0
    context.quality_starts = 0.0

@step('the pitcher goes "{number}" innings')
def step_impl(context, number):
    context.innings = number

@step('the pitcher allows "{number}" earned runs')
def step_impl(context, number):
    context.earned_runs = number

@step('the pitcher walks "{number}" batter')
def step_impl(context, number):
    context.walks = number

@step('the pitcher allows "{number}" hits')
def step_impl(context, number):
    context.hits = number

@step('the pitcher gives up "{number}" homeruns')
def step_impl(context, number):
    context.home_runs = number

@step('the pitcher stikes out "{number}" batters')
def step_impl(context, number):
    context.strikeouts = number

@step('the pitcher gets a save')
def step_impl(context):
    context.saves = 1

@step('the pitcher gets a win')
def step_impl(context):
    context.wins = 1

@step('the pitcher takes a loss')
def step_impl(context):
    context.losses = 1

@step('the pitcher gets a quality start')
def step_impl(context):
    context.quality_starts = 1

@step('we calculate game')
def step_impl(context):
    context.game_total = calculate_game(context.innings, context.earned_runs, \
        context.walks, context.hits, context.home_runs, context.strikeouts, \
        context.saves, context.wins, context.losses, context.quality_starts)
    print(context.game_total)

@step('we expect his score to be "{number}"')
def step_impl(context, number):
    print(context.game_total)
    print(round(float(number),1))
    assert round(float(number),1) == float(context.game_total), \
        'Didn\'t get expected score, got %f' % context.game_total
