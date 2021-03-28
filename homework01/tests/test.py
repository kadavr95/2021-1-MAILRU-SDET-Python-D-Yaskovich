import string
import random

import pytest
from base import BaseCase
from homework01.ui.locators import basic_locators


class TestHomework01(BaseCase):
    @pytest.mark.UI
    def test_log_in(self):
        self.log_in()
        assert "dashboard" in self.driver.current_url

    @pytest.mark.UI
    def test_log_out(self):
        self.log_in()
        self.click(basic_locators.LOG_OUT_EXPAND_LOCATOR)
        self.click(basic_locators.LOG_OUT_LOCATOR)
        assert self.find(basic_locators.LOG_IN_BUTTON_LOCATOR)

    @pytest.mark.UI
    def test_change_info(self):
        self.log_in()
        self.click(basic_locators.PROFILE_LINK_LOCATOR)
        random_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.fill(random_text, basic_locators.FULL_NAME_INPUT_LOCATOR)
        self.click(basic_locators.SAVE_PROFILE_INPUT_LOCATOR)
        self.driver.refresh()
        self.find(basic_locators.FULL_NAME_INPUT_LOCATOR)
        assert random_text in self.driver.page_source

    @pytest.mark.parametrize(
        "section, check_value",
        [
            pytest.param(
                basic_locators.STATISTICS_LINK_LOCATOR, basic_locators.STATISTICS_INNER_LINK_LOCATOR
            ),
            pytest.param(
                basic_locators.SEGMENTS_LINK_LOCATOR, basic_locators.SEGMENTS_INNER_LINK_LOCATOR
            )
        ]
    )
    @pytest.mark.UI
    def test_navigation(self, section, check_value):
        self.log_in()
        self.click(section)
        assert self.find(check_value)
