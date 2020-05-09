from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import traceback
import time


# Parent class where basic common methods are defined

class BasePage(object):

    def __init__(self, browser, base_url='http://www.ravenpack.com/signin/', env="NA"):
        print("basePage__init__")
        self.base_url = base_url
        self.browser = browser
        self.timeout = 30
        self.environment = env

    def check_if_elements_exist_generic(self, locator_duplet):
        print("check_if_elements_exist_generic", locator_duplet[1])
        try:
            element = self.browser.find_element(locator_duplet[0], locator_duplet[1])
            return element
        except (NoSuchElementException, TimeoutException, WebDriverException):
            print(locator_duplet, "check_if_elements_exist_generic - exception")
            return False

    def explicit_wait_for_element(self, element, waiting_seconds=15):
        print("explicit_wait_for_element", element[1])
        try:
            WebDriverWait(self.browser, waiting_seconds).until(
                EC.presence_of_element_located(element)
            )
            return True
        except (NoSuchElementException, TimeoutException):
            print('element not found')
            return False

    def explicit_wait_for_visibility_of_element(self, element, waiting_seconds=15):
        print("explicit_wait_for_visibility_of_element", element[1])
        try:
            WebDriverWait(self.browser, waiting_seconds).until(
                EC.visibility_of_element_located(element)
            )
            return True
        except (NoSuchElementException, TimeoutException):
            print('element not found')
            return False

    def explicit_wait_for_elements_to_visible(self, locator, waiting_seconds=15):
        print("explicit_wait_for_elements_to_visible", locator[1])
        try:
            WebDriverWait(self.browser, waiting_seconds).until(
                EC.visibility_of_all_elements_located(locator)
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def find_element(self, *loc):
        return self.browser.find_element(*loc)

    def find_element_duplet(self, duplet):
        return self.browser.find_element(duplet[0], duplet[1])

    def __getattr__(self, what):
        try:
            if what in self.locator_dictionary.keys():
                try:
                    element = WebDriverWait(self.browser, self.timeout).until(
                        EC.presence_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()

                try:
                    element = WebDriverWait(self.browser, self.timeout).until(
                        EC.visibility_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()
                # I could have returned element, however because of lazy loading, I am seeking the element before return
                return self.find_element(*self.locator_dictionary[what])
        except AttributeError:
            super(BasePage, self).__getattribute__("method_missing")(what)
