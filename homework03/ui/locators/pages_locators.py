from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_BUTTON = (By.CLASS_NAME, 'enter-item')

    USERNAME_FIELD = (By.ID, 'id_login_email')
    PASSWORD_FIELD = (By.ID, 'id_login_password')

    SUBMIT_BUTTON = (By.XPATH, '//form[@id="popup-login-form"]//button[@type="submit"]')

    INVALID_EMAIL_LOCATOR = (By.ID, 'id_login_email-error')
    LOGIN_ERROR_LOCATOR = (By.XPATH, '//form[@id="popup-login-form"]//div[@class="login-error-message error-message"]')


class MainPageLocators:
    FEED = (By.ID, 'react-feed-stream')
