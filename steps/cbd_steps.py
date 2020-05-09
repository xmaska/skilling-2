import allure
from behave import *

from page_objects.cbd_page import CbdPage


@step('I open the Computer Database Tool')
def step_impl(context):
    page = CbdPage(context)
    page.open_site(context)


@step('I make a screenshot of "{page}"')
def step_impl(context, page):
    allure.attach(context.browser.get_screenshot_as_png(), name='screenshot' + page,
                  attachment_type=allure.attachment_type.PNG)


@step('The Computer Database is open')
def step_impl(context):
    page = CbdPage(context)
    page.check_site_open()


@step('I click on Add new Computer')
def step_impl(context):
    page = CbdPage(context)
    page.click_new_model()


@step('I fill Name as "{comp_name}", Introduced as "{date_start}", Discontinued as "{date_end}" '
      'and company as "{company}"')
def step_impl(context, comp_name, date_start, date_end, company):
    page = CbdPage(context)
    page.fill_model_form(comp_name, date_start, date_end, company)


@step('I click on create this computer which is valid: "{valid}"')
def step_impl(context, valid):
    page = CbdPage(context)
    page.click_create(valid)


@step('I filter for "{computer}"')
def step_impl(context, computer):
    page = CbdPage(context)
    page.filter_computer(computer)


@step('I delete the selected computer')
def step_impl(context):
    page = CbdPage(context)
    page.delete_computer()
