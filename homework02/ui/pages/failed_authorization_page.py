import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import FailedAuthorizationPageLocators


class FailedAuthorizationPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = FailedAuthorizationPageLocators()
