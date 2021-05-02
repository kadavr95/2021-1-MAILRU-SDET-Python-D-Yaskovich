import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import SegmentsPageLocators


class SegmentsPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = SegmentsPageLocators()