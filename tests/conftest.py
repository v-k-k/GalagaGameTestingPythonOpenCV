from pytest import fixture
from selenium import webdriver
import constants


@fixture(scope='class', autouse=True)
def init_driver(request):
    options = webdriver.ChromeOptions()
    options.binary_location = constants.BROWSER_PATH
    browser = webdriver.Chrome(executable_path=constants.DRIVER_PATH, options=options)
    browser.maximize_window()
    yield browser
    browser.close()
    browser.quit()
