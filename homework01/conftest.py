import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com/')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    browser = webdriver.Chrome("/home/kadavr95/Documents/2021-1-MAILRU-SDET-Python-D-Yaskovich/homework01/chromedriver")
    browser.get(url)
    browser.set_window_size(1920, 1080)
    yield browser
    browser.close()
