import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from browserstack.local import Local
import os
import json
import re

REMOTE_RUN = False
CONFIG_FILE = 'config/chrome.json'
TASK_ID = 0

BS_LOCAL = None


def prepare_environment(context):
    global REMOTE_RUN, CONFIG_FILE, TASK_ID, BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
    print('remote_run1', REMOTE_RUN)
    REMOTE_RUN = context.config.userdata['REMOTE'].lower() in ("true", "yes")
    print('remote_context', context.config.userdata['REMOTE'].lower())
    print('remote_run2', REMOTE_RUN)
    CONFIG_FILE = context.config.userdata[
        'CONFIG_FILE'] if 'CONFIG_FILE' in context.config.userdata else 'config/chrome.json'
    TASK_ID = int(context.config.userdata['TASK_ID']) if 'TASK_ID' in context.config.userdata else 0
    print('Setting up environment... Targeting remote machine: %s , Config File: %s , TASK ID: %d' % (
        REMOTE_RUN, CONFIG_FILE, TASK_ID))
    try:
        with open(CONFIG_FILE) as data_file:
            config_from_file = json.load(data_file)
            print('Config file exists and loaded!')
    except FileNotFoundError:
        with open('config/chrome.json') as data_file:
            config_from_file = json.load(data_file)
            print('Config file does not exists! Loaded default chrome.json!')

    BROWSERSTACK_USERNAME = os.environ['BROWSERSTACK_USERNAME'] if 'BROWSERSTACK_USERNAME' in os.environ else \
        config_from_file['user']
    BROWSERSTACK_ACCESS_KEY = os.environ['BROWSERSTACK_ACCESS_KEY'] if 'BROWSERSTACK_ACCESS_KEY' \
                                                                       in os.environ else config_from_file['key']
    return config_from_file


def start_local():
    try:
        # creates an instance of Local
        BS_LOCAL = Local()
        # replace <browserstack-accesskey> with your key. You can also set an environment variable - "BROWSERSTACK_ACCESS_KEY".
        bs_local_args = {"key": BROWSERSTACK_ACCESS_KEY}
        # starts the Local instance with the required arguments
        BS_LOCAL.start(**bs_local_args)
        # check if BrowserStack local instance is running
        print("bs_local running:", BS_LOCAL.isRunning())
    except Exception as e:
        print('Exception occured while instantiating web driver locally' + str(e))


def stop_local():
    """Code to stop browserstack local after end of test."""
    print("stop local")
    if BS_LOCAL is not None:
        BS_LOCAL.stop()


def before_scenario(context, scenario):
    print('before_scenario')


def after_scenario(context, scenario):
    print('after_scenario')
    print("scenario status:" + str(scenario.status))
    if scenario.status == "failed":
        allure.attach(context.browser.get_screenshot_as_png(), name='scenario_failure',
                      attachment_type=allure.attachment_type.PNG)


def before_feature(context, feature):
    feature_name = re.search('\"(.*)\"', str(feature)).group(1)
    print("Before feature:", feature_name)
    # Configuring the target url
    print("User data:", context.config.userdata)
    if context.config.userdata['ENV'] == "TEST" and context.config.userdata['PRODUCT'] == "CDB":
        context.web_url_target = context.config.userdata['urlCDB']
    else:
        print('Referred invalid environment', context.config.userdata['ENV'])

    # Configuring the target product
    if context.config.userdata['PRODUCT'] == 'CDB':
        context.product = 'cdb'
    else:
        print('Referred invalid product', context.config.userdata['PRODUCT'])

    target_environment_name = "-locally"
    local_config = prepare_environment(context)
    print('local_config_after_prepare', local_config)
    desired_capabilities = local_config['environments'][TASK_ID]

    for key in local_config["capabilities"]:
        if key not in desired_capabilities:
            desired_capabilities[key] = local_config["capabilities"][key]

    if 'BUILD' in context.config.userdata:
        desired_capabilities['build'] = context.config.userdata['BUILD']
    if 'NAME' in context.config.userdata:
        desired_capabilities['name'] = feature_name
    # https://www.browserstack.com/local-testing/automate
    if 'BS_LOCAL' in context.config.userdata and context.config.userdata['BS_LOCAL'].lower() in ("true", "yes"):
        start_local()
        desired_capabilities["browserstack.local"] = "true"
    if REMOTE_RUN:
        print('Instantiating browser remotely!')
        target_environment_name = "-BStack"
        opt = webdriver.ChromeOptions()
        # opt.add_experimental_option('w3c', False)
        context.browser = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://%s:%s@hub.browserstack.com/wd/hub" % (
                BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY),
            keep_alive=True,
            options=opt
        )
    else:
        local_browser = local_config['environments'][TASK_ID]['browser']
        print('Instantiating browser locally! Selected browser: ' + local_browser)
        if local_browser.lower() == "chrome":
            chrome_options = Options()
            if 'HEADLESS' in context.config.userdata and context.config.userdata['HEADLESS'].lower() in ("true", "yes"):
                chrome_options.add_argument("--headless")
            context.browser = webdriver.Chrome(chrome_options=chrome_options, keep_alive=True)
            context.browser.set_window_size(1920, 1080)
        elif local_browser.lower() == 'firefox':
            context.browser = webdriver.Firefox()
        elif local_browser.lower() == 'edge':
            context.browser = webdriver.Edge()
        elif local_browser.lower() == 'ie':
            context.browser = webdriver.Ie()
    context.browser.set_page_load_timeout(60)

    print("target capabilities", context.browser.capabilities)
    if 'browserName' in context.browser.capabilities:
        feature.name += ' on ' + context.browser.capabilities['browserName'] + target_environment_name
    elif 'browserName' in context.browser.capabilities['capabilities']:
        print("capaWTF", context.browser.capabilities['capabilities'])
        feature.name += ' on ' + context.browser.capabilities['capabilities']['browserName'] + target_environment_name
    else:
        feature.name += ' on unknown browser ' + target_environment_name
    print("Url of the environment:", context.web_url_target)

    context.browser.maximize_window()


def after_feature(context, feature):
    print('after_feature')
    context.browser.quit()
    if BS_LOCAL:
        stop_local()
