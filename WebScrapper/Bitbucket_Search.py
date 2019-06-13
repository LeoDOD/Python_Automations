import os

from nerodia.browser import Browser
from selenium.webdriver.chrome.options import Options as chrome_options
from time import sleep
import csv
import re


def file_recursion():
    try:

        browse_repo = browser.table(id='browse-table')
        # print(f'\nNumber of items = {sum(1 for e in browse_repo) - 1}\n')
        for item in browse_repo:
            if 'File' in item.text:
                file_match = file_ending.findall(item[0].text.replace('File', '').strip())
                if file_match:
                    browser.goto(browser.url + '/' + item[0].text.replace('File', '').strip())
                    # browser.link(text='Raw file').click()
                    match = connectionstring.findall(browser.text)
                    if match:
                        print(f'Found {match} in {browser.url}')
                    browser.back()
            elif 'Directory' in item.text:
                # print(f'Checking Folder {item.text}')
                browser.goto(browser.url + '/' + item.text.replace('Directory', '').strip())
                file_recursion()
                browser.back()
    except:
        print('Empty Repo')


# start browser
browser = Browser(browser='chrome')
browser.window().maximize()
browser.goto('https://bitbucket.paya.com/projects')
browser.text_field(id='j_username').send_keys(os.environ['username'])
browser.text_field(id='j_password').send_keys(os.environ['passsword'])
browser.button(id='submit').click()
total_files_bb = 0
file_ending = re.compile(r'(\w+\.config\b|\w+\.cs\b|\w+\.vb\b|\w+\.js\b|\w+\.json\b|\w+\.txt\b|\w+\.yml\b)')
connectionstring = re.compile(
    r'([uU]ser\s[iI][dD]=[\S]+;|[pP]assword=[\S]+;|[dD]atabase=[\w0-9\-]+;|[sS]erver=[\w0-9\-\\]+;)+')

table = browser.table(id='projects-table')
print(f'Number of Projects = {sum(1 for e in table)-1}')
bad_strings = ['Description', 'AutomationCoreCode', '-old', "-OLD", 'APIGEE', 'Boomtown', 'CARD_API',
               'CoreDataServices', 'CoreProcesses', 'Core_project', 'Databases', 'DevOps', 'EnterpriseACH',
               'GatewayProcesses', 'GatewayProject', 'Geti', 'Jmeter Load Testing', 'MVR', 'MyOnlineReports Automation',
               'PayaExchange', 'PayaExchange_Projects', 'SED', '']
for row in table:
    if row[0].text != 'UNO':
        continue
    else:
        print(f'Checking project {row[0].text}')
        row[0].click()
        repos = browser.table(id='repositories-table')
        print(f'Number of Repos = {sum(1 for e in repos) - 1}')
        for repo in repos:
            if 'Repository' not in repo.text:
                continue
            else:
                print(f'Checking Repo {repo.text.replace("Repository", "")}')
                browser.link(text=repo.text.replace('Repository', '')).click()
                file_recursion()
            browser.back()
        browser.back()
