import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import FailedAuthorizationPageLocators


class FailedAuthorizationPage(BasePage):
    url = 'https://account.my.com/login'
    locators = FailedAuthorizationPageLocators()
