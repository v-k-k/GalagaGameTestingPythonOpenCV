import sys
import constants
import datetime
from _pytest.runner import runtestprotocol
from pytest import fixture
from selenium import webdriver
from controls import GameControl
from game import Game
from tester import Tester
from pages import GalagaPage


def pytest_runtest_protocol(item, nextitem):
    t1 = datetime.datetime.now()
    reports = runtestprotocol(item, nextitem=nextitem)
    t2 = datetime.datetime.now()
    delta = t2 - t1
    sec = int(delta.total_seconds())
    ms = delta.total_seconds() - sec
    ms1 = str(ms)
    border = "   ----------------------------------"
    output = f"  |\n |\n |{border}\n --> | Test execution time: {str(sec)}s {str(ms1[2:5])}ms |\n  {border}\n\n"
    sys.stdout.write(output)
    sys.stdout.flush()
    return True


@fixture(scope='session')
def init_driver(request):
    options = webdriver.ChromeOptions()
    options.binary_location = constants.BROWSER_PATH
    browser = webdriver.Chrome(executable_path=constants.DRIVER_PATH, options=options)
    browser.maximize_window()
    yield browser
    browser.close()
    browser.quit()


@fixture(scope='function', autouse=True)
def tester(init_driver):
    return Tester(
        GameControl(
            Game(
                GalagaPage(init_driver)
            )
        )
    )
