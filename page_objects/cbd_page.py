import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from page_objects.base_page_object import BasePage


class CbdPage(BasePage):
    locator_dictionary = {
        "site_header": (By.CSS_SELECTOR, 'a.fill'),
        "add_model": (By.ID, 'add'),
        "model_form_name": (By.ID, "name"),
        "model_form_introduced": (By.ID, "introduced"),
        "model_form_discontinued": (By.ID, "discontinued"),
        "model_form_company": (By.ID, "company"),
        "model_button_create": (By.CLASS_NAME, "primary"),
        "alert_message": (By.CLASS_NAME, "alert-message"),
        "filter_searchbox": (By.ID, "searchbox"),
        "filter_submit": (By.ID, "searchsubmit"),
        "delete_button": (By.CLASS_NAME, "danger")
    }

    def __init__(self, context):
        print("init_cbd_page")
        BasePage.__init__(self,
                          context.browser,
                          base_url=context.web_url_target)
        self.product = context.product

    def open_site(self, context):
        try:
            context.browser.get(context.web_url_target)
        except TimeoutException as e:
            print("Timeout exception while opening: ", context.web_url_target, e)
        except Exception as e:
            print("Unknown exception while opening main page:", e)

    def check_site_open(self):
        assert self.explicit_wait_for_visibility_of_element(self.locator_dictionary['site_header'], 5), \
            "The Page did not open in 5 seconds!"
        header_text = self.find_element_duplet(self.locator_dictionary['site_header']).text
        assert header_text == "Computer database", "Page title is not the expected one!"

    def click_new_model(self):
        assert self.explicit_wait_for_visibility_of_element(self.locator_dictionary['add_model'], 1), \
            "Add model button not found!"
        self.add_model.click()

    def fill_model_form(self, comp_name, date_start, date_end, company):
        assert self.explicit_wait_for_visibility_of_element(self.locator_dictionary['model_form_name'], 3), \
            "The Add computer form did not open in 3 seconds!"
        # just to ensure the form is rendered...
        time.sleep(1)
        self.model_form_name.send_keys(comp_name)
        self.model_form_introduced.send_keys(date_start)
        self.model_form_discontinued.send_keys(date_end)
        company_select = self.find_element_duplet(self.locator_dictionary['model_form_company'])
        for option in company_select.find_elements_by_tag_name('option'):
            if option.text == company:
                option.click()
                break
        else:
            assert False, f"{company} is not an available option!"

    def click_create(self, valid):
        self.model_button_create.click()
        if valid.lower == "true":
            assert self.explicit_wait_for_visibility_of_element(self.locator_dictionary['alert_message'], 3), \
                'The computer was not created in 3 seconds!'
            alert_text = self.find_element_duplet(self.locator_dictionary['alert_message']).text
            assert "Done !" in alert_text, f"Alert message is not the expected one, it is {alert_text}"
        else:
            assert self.check_if_elements_exist_generic(self.locator_dictionary['model_button_create']), \
                "The user did not remain on the computer create form!"

    def filter_computer(self, computer_name):
        self.filter_searchbox.click()
        assert self.explicit_wait_for_visibility_of_element(self.locator_dictionary['filter_submit'], 3), \
            'The filter page did not open in 3 seconds!'
        self.filter_searchbox.send_keys(computer_name)
        self.filter_submit.click()
        # TODO handle multiple matches...
        computer_locator = (By.XPATH, f'//a[text()="{computer_name}"]')
        self.find_element_duplet(computer_locator).click()

    def delete_computer(self):
        assert self.explicit_wait_for_visibility_of_element(self.locator_dictionary['delete_button'], 3), \
            "Delete button is not visible!"
        self.delete_button.click()
        alert_text = self.find_element_duplet(self.locator_dictionary['alert_message']).text
        assert "Done !" in alert_text, f"Alert message is not the expected one, it is {alert_text}"
