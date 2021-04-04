import string
import random
import pytest
from ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException, \
    ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLICK_RETRY = 3
DEFAULT_TIMEOUT = 10


class BaseCase:
    driver = None
    config = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config

    def log_in(self):
        self.click(basic_locators.LOG_IN_BUTTON_LOCATOR)
        self.fill("test20210328@dimini.tk", basic_locators.USERNAME_FIELD_LOCATOR)
        self.fill("U[ti3T5oEauI", basic_locators.PASSWORD_FIELD_LOCATOR)
        self.click(basic_locators.CREDENTIALS_SEND_BUTTON_LOCATOR)

    def log_out(self):
        self.click(basic_locators.LOG_OUT_EXPAND_LOCATOR)
        self.click(basic_locators.LOG_OUT_LOCATOR)
        try:
            self.find(basic_locators.LOG_IN_BUTTON_LOCATOR)
            return True
        except TimeoutException:
            return False

    def change_user_name(self):
        self.click(basic_locators.PROFILE_LINK_LOCATOR)
        random_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.fill(random_text, basic_locators.FULL_NAME_INPUT_LOCATOR)
        self.click(basic_locators.SAVE_PROFILE_INPUT_LOCATOR)
        self.driver.refresh()
        assert random_text == self.find(basic_locators.NAME_WRAPPER_LOCATOR).get_attribute("title")

    def menu_navigation(self, section, check_value):
        self.log_in()
        self.click(section)
        self.find(check_value)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def fill(self, value, locator):
        field = self.find(locator)
        field.clear()
        field.send_keys(value)

    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException or ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise
