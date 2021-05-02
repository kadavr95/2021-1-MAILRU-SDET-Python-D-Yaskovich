import logging
import time

import allure
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.pages_locators import BasePageLocators
from utils.decorators import wait

CLICK_RETRY = 3
DEFAULT_TIMEOUT = 10


logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass


class BasePage(object):
    url = 'https://target.my.com/'
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')
        assert self.is_opened()

    def is_opened(self):
        def _check_url():
            if not self.driver.current_url.startswith(self.url):
                raise PageNotLoadedException(
                    f'{self.url} did not opened in {DEFAULT_TIMEOUT} for {self.__class__.__name__}.\n'
                    f'Current url: {self.driver.current_url}.')
            return True

        return wait(_check_url, error=PageNotLoadedException, check=True, timeout=DEFAULT_TIMEOUT, interval=0.1)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def fill(self, value, locator):
        field = self.find(locator)
        field.clear()
        field.send_keys(value)

    def search(self, query):
        search = self.find(self.locators.QUERY_LOCATOR)
        search.clear()
        search.send_keys(query)
        self.click(self.locators.GO_LOCATOR)

    @allure.step('Clicking {locator}')
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException or ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise