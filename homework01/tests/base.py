import os
import pytest
from homework01.ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
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
        self.fill(os.environ['username'], basic_locators.USERNAME_FIELD_LOCATOR)
        self.fill(os.environ['password'], basic_locators.PASSWORD_FIELD_LOCATOR)
        self.click(basic_locators.CREDENTIALS_SEND_BUTTON_LOCATOR)

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
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise
