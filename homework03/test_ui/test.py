import time

import pytest

from test_ui.base import BaseCase


class TestLogin(BaseCase):
    authorize = False

    def test_login(self, credentials):
        main_page = self.login_page.login(*credentials)
        assert main_page.is_opened()

    def test_invalid_login(self):
        with pytest.raises(TimeoutError):
            self.login_page.login('123', '456')

        email_error_text = self.login_page.find(self.login_page.locators.INVALID_EMAIL_LOCATOR).text
        assert email_error_text == 'Введите правильный формат E-mail'

        login_error_text = self.login_page.find(self.login_page.locators.LOGIN_ERROR_LOCATOR).text
        assert login_error_text == 'Что-то не так! Вероятно, неправильно указаны данные'


class TestLK(BaseCase):

    def test_lk1(self):
        assert self.main_page.is_opened()
        time.sleep(5)

    def test_lk2(self):
        assert self.main_page.is_opened()
        time.sleep(5)
