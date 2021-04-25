import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import UnauthorizedPageLocators
from ui.pages.authorized_page import AuthorizedPage


class UnauthorizedPage(BasePage):
    locators = UnauthorizedPageLocators()

    def log_in(self, login="test20210328@dimini.tk", password="U[ti3T5oEauI"):
        self.click(self.locators.LOG_IN_BUTTON_LOCATOR)
        self.fill(login, self.locators.USERNAME_FIELD_LOCATOR)
        self.fill(password, self.locators.PASSWORD_FIELD_LOCATOR)
        self.click(self.locators.CREDENTIALS_SEND_BUTTON_LOCATOR)
        return AuthorizedPage(self.driver)