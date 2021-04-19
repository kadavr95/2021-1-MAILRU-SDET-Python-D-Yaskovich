from ui.locators.pages_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class LoginPage(BasePage):
    url = 'https://auth-ac.my.com'

    locators = LoginPageLocators()

    def login(self, user, password):
        self.click(self.locators.LOGIN_BUTTON)
        self.find(self.locators.USERNAME_FIELD).send_keys(user)
        self.find(self.locators.PASSWORD_FIELD).send_keys(password)
        self.click(self.locators.SUBMIT_BUTTON)

        return MainPage(self.driver)
