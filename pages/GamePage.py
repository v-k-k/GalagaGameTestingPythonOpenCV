import base64
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import Base
from utils.timeouts import Timeouts
import numpy as np
import constants
import cv2


class GalagaPageLocators:

    CANVAS = (By.ID, "nes-canvas")


class GalagaPage(Base):
    _driver = None
    _actions = None
    __instance = None
    __source = constants.GAME_SOURCE

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance:
    #         cls.__instance = super(GalagaPage, cls).__new__(cls)
    #     return cls.__instance

    def __init__(self, driver):
        if not self._driver:
            self._driver = driver
        self._driver.get(self.__source)

    @property
    def canvas(self):
        return self._driver.find_element(*GalagaPageLocators.CANVAS)

    @property
    def actions(self):
        if not self._actions:
            self._actions = ActionChains(self._driver)
        return self._actions

    @property
    def canvas_image(self):
        canvas_base64 = self._driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", self.canvas
        )
        image = cv2.imdecode(
            np.frombuffer(
                base64.b64decode(canvas_base64),
                np.uint8
            ), 1
        )
        return image, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def perform_double_enter_click(self):
        self.logger.info("Performing double ENTER")
        self.actions.pause(Timeouts.MID.value) \
                    .send_keys(Keys.RETURN + Keys.RETURN) \
                    .perform()
        return self

    def perform_canvas_click_with_enter(self):
        self.logger.info("Performing canvas click with ENTER")
        self.actions.move_to_element_with_offset(self.canvas, 50, 50) \
                    .click(self.canvas) \
                    .send_keys(Keys.RETURN) \
                    .perform()
        return self

    def perform_single_enter_click(self):
        self.logger.info("Performing single ENTER")
        self.actions.pause(Timeouts.MID.value) \
            .send_keys(Keys.RETURN) \
            .perform()
        return self

    def press_left_x(self):
        self.logger.info("Pressing down LEFT + X")
        self.actions.key_down(Keys.LEFT) \
                    .key_down('x') \
                    .perform()
        return self

    def release_left_x(self):
        self.logger.info("Releasing LEFT + X")
        self.actions.key_up(Keys.LEFT) \
                    .key_up('x') \
                    .perform()
        return self

    def press_right_x(self):
        self.logger.info("Pressing down RIGHT + X")
        self.actions.key_down(Keys.RIGHT) \
                    .key_down('x') \
                    .perform()
        return self

    def release_right_x(self):
        self.logger.info("Releasing RIGHT + X")
        self.actions.key_up(Keys.RIGHT) \
                    .key_up('x') \
                    .perform()
        return self
