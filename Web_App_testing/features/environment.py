# -*- coding: UTF-8 -*-
"""
before_step(context, step), after_step(context, step)
    These run before and after every step.
    The step passed in is an instance of Step.
before_scenario(context, scenario), after_scenario(context, scenario)
    These run before and after each scenario is run.
    The scenario passed in is an instance of Scenario.
before_feature(context, feature), after_feature(context, feature)
    These run before and after each feature file is exercised.
    The feature passed in is an instance of Feature.
before_tag(context, tag), after_tag(context, tag)
"""

import platform
import os
import re
import requests
import uuid
import json
from nerodia.browser import Browser
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from behave import use_step_matcher
from selenium import webdriver
from Web_App_testing.features.support import Config
from faker import Factory
from faker.providers import company, internet
from guerrillamail import GuerrillaMailSession

# -- SETUP: Use cfparse as default matcher
use_step_matcher('cfparse')
with_JIRA = False


def before_all(context):
    global with_JIRA
    # We Generate a Fake set of data and add different sets of data.
    context.fake = Factory.create()
    context.fake.add_provider(company)
    context.fake.add_provider(internet)
    # Set Config File to Data variable and check if we are running locally or in Jenkins
    try:
        # We set the data for the Automation using the ENV variable passed Thru jenkins.
        context.data = Config.Config(str(os.environ['ENV'])).save_to_var()
        # We turn the API on.
        with_JIRA = True
        # If this fails we set it to a hardcoded Value, that can be changed according to your needs.
    except KeyError:
        context.data = Config.Config('QAS').save_to_var()
    if with_JIRA:
        # This will make it so that when Jenkins starts a job thru a timer it will Set the username to itself,
        # instead of using '$BUILD_USER_ID' as the Default.
        if os.environ['USER'] == '$BUILD_USER_ID':
            os.environ['USER'] = 'Jenkins'
        # Capture the Version of MSD depending on the env we are testing
        pattern = re.compile('version: "([^"]*)"')
        r = requests.get(context.data['MSD Version'])
        version = pattern.findall(str(r.content))[0]
        # Generate Cycle name
        context.data['Cycle'] = f"{os.environ['BUILD']}-{os.environ['USER']}-{platform.system()}-" \
                                f"{platform.release()}-{uuid.uuid4().hex[:8]}"
        print(context.data['Cycle'])
        # Create Test Cycles
        print(f"{context.data['JIRA']}/createtestcycle/{os.environ['TP']}"
              f"/{context.data['Cycle']}/{os.environ['ENV']}")
        requests.get(f"{context.data['JIRA']}/createtestcycle/{os.environ['TP']}"
                     f"/{context.data['Cycle']}/{os.environ['ENV']}-{version}-Chrome")
        # Update test cycle to in Progress
        print(f"{context.data['JIRA']}/updatetestcyclestatus/{os.environ['TP']}"
              f"/{context.data['Cycle']}/Start")
        requests.get(f"{context.data['JIRA']}/updatetestcyclestatus/{os.environ['TP']}"
                     f"/{context.data['Cycle']}/Start")


def before_scenario(context, scenario):
    # We set our Guerrilla email. this is the temporary email service.
    context.email_session = GuerrillaMailSession()
    context.temp_email = context.email_session.get_session_state()['email_address']
    # Start browser
    options = chrome_options()
    # options = firefox_options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--private")
    # options.add_argument("--headless")
    # context.browser = webdriver.Edge()
    context.browser = Browser(browser='chrome', options=options)
    context.browser.window().maximize()
    # We create a dict to store the data of the fake user
    context.fake_user = dict()
    # Print which scenario we are about to test
    print(f'Starting test for {scenario.tags[0]}: {context.scenario.name}\n')
    # We use this to determine whether or not we should clean Keycloak,
    # This will only happen is we create an account using a temp email.


def after_scenario(context, scenario):
    # Bring Global Variable for JIRA API
    global with_JIRA
    context.browser.close()
    print(f'Finished test for {scenario.tags[0]}: {context.scenario.name}\n')
    if with_JIRA:
        pattern = re.compile('\w+-\d+')
        tags = list(context.tags)
        for i in tags:
            # We Check all tags in the scenario and capture the ones that match the JIRA KEYs regex.
            tck = pattern.match(i)
            if tck:
                if "Status.passed" != str(scenario.status):
                    # Set test case to Failed
                    print("Scenario Failed\n")
                    r = requests.get(f"{context.data['JIRA']}/updatetestcyclerun/{os.environ['TP']}"
                                     f"/{context.data['Cycle']}/{i}/Failed/Failed")
                else:
                    # Set Test case to Passed
                    print("Scenario Passed\n")
                    r = requests.get(f"{context.data['JIRA']}/updatetestcyclerun/{os.environ['TP']}"
                                     f"/{context.data['Cycle']}/{i}/Passed/Passed")


def after_all(context):
    global with_JIRA
    if with_JIRA:
        requests.get(f"{context.data['JIRA']}/updatetestcyclestatus/{os.environ['TP']}"
                         f"/{context.data['Cycle']}/Complete")