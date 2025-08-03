# -*- coding: UTF-8 -*-
import os
import logging
from behave import *
# from qa.functional.features.browser import Browser
# logging.basicConfig()
#
# def before_scenario(context, scenario):
#     if 'browser' in context.tags:
#         context.browser = Browser()
#         context.driver = context.browser.get_browser_driver()
#     if 'skip' in context.tags:
#         jira_number = get_jira_number_from_tags(context)
#         scenario.skip("\n\tSkipping tests until %s is fixed" % jira_number)
#         return
#
# def after_scenario(context, scenario):
#     if 'browser' in context.tags:
#         context.driver.quit()
