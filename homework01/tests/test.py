import pytest
from base import BaseCase
from ui.locators import basic_locators


class TestHomework01(BaseCase):
    @pytest.mark.UI
    def test_log_in(self):
        self.log_in()
        assert self.find(basic_locators.DASHBOARD_CREATE_CAMPAIGN_LOCATOR)

    @pytest.mark.UI
    def test_log_out(self):
        self.log_in()
        assert self.log_out()

    @pytest.mark.UI
    def test_change_info(self):
        self.log_in()
        self.change_user_name()

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
        self.menu_navigation(section, check_value)
