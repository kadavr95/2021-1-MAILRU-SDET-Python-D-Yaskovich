from selenium.webdriver.common.by import By

LOG_IN_BUTTON_LOCATOR = (By.CSS_SELECTOR, "div[class^='responseHead-module-button']")
USERNAME_FIELD_LOCATOR = (By.NAME, "email")
PASSWORD_FIELD_LOCATOR = (By.NAME, "password")
CREDENTIALS_SEND_BUTTON_LOCATOR = (By.CSS_SELECTOR, "div[class^='authForm-module-button']")
DASHBOARD_CREATE_CAMPAIGN_LOCATOR = (By.CSS_SELECTOR, "a[href='/campaign/new']")

LOG_OUT_EXPAND_LOCATOR = (By.CSS_SELECTOR, "div[class^='right-module-rightButton']")
LOG_OUT_LOCATOR = (By.CSS_SELECTOR, "a[href='/logout']")

PROFILE_LINK_LOCATOR = (By.CSS_SELECTOR, "a[href='/profile']")
FULL_NAME_INPUT_LOCATOR = (By.CSS_SELECTOR, "div[data-name='fio'] input")
SAVE_PROFILE_INPUT_LOCATOR = (By.CSS_SELECTOR, "button[data-class-name='Submit']")
NAME_WRAPPER_LOCATOR = (By.CSS_SELECTOR, "div[class^='right-module-userNameWrap']")

STATISTICS_LINK_LOCATOR = (By.CSS_SELECTOR, "a[href='/statistics']")
STATISTICS_INNER_LINK_LOCATOR = (By.CSS_SELECTOR, "a[href='/statistics/reports']")
SEGMENTS_LINK_LOCATOR = (By.CSS_SELECTOR, "a[href='/segments']")
SEGMENTS_INNER_LINK_LOCATOR = (By.CSS_SELECTOR, "a[href='/segments/share']")
