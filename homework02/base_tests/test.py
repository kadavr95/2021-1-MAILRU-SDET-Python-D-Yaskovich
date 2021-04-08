import os
import time
from contextlib import contextmanager

import allure
import pytest
from selenium.webdriver.common.by import By

from base_tests.base import BaseCase
from utils.decorators import wait


class TestAllureSelenium(BaseCase):

    @allure.epic('Python Mail.ru Homework 2')
    @allure.feature('UI tests')
    @allure.story('Log test')
    @allure.testcase('https://dimini.tk')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.issue('https://dimini.atlassian.net/')
    @allure.description("""
                        Some description
                        """
                        )
    @pytest.mark.UI
    # @pytest.mark.skip("SKIP")
    def test_log_in(self):
        authorized_page = self.unauthorized_page.log_in()
        assert authorized_page.find(authorized_page.locators.DASHBOARD_CAMPAIGN_LOCATOR)

    @pytest.mark.UI
    def test_log_in_wrong_password(self):
        self.unauthorized_page.log_in(login="test20210328@dimini.tk", password="LetMeInLetMeIiiIINNnN")
        assert self.unauthorized_page.find(self.unauthorized_page.locators.WRONG_CREDENTIALS_ERROR_LOCATOR)

    @pytest.mark.UI
    def test_log_in_login_is_not_email(self):
        self.unauthorized_page.log_in(login="test20210328", password="U[ti3T5oEauI")
        assert self.unauthorized_page.find(self.unauthorized_page.locators.LOG_IN_ERROR_MESSAGE_LOCATOR)

