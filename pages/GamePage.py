import base64

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from utils import Base, Image
import numpy as np
import constants
import cv2


class GalagaPageLocators:

    CANVAS = (By.ID, "nes-canvas")


class GalagaPage(Base):
    """Singleton GamePage"""

    _driver = None
    _actions = None
    __instance = None
    __source = constants.GAME_SOURCE

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(GalagaPage, cls).__new__(cls)
        return cls.__instance

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
    def __canvas_image(self):
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

    @property
    def image(self):
        image, gray_image = self.__canvas_image
        binary_image = cv2.Laplacian(gray_image[0:240, 0:205], cv2.CV_8UC1)
        dilated_image = cv2.dilate(binary_image, np.ones((6, 6)))
        _, thresh = cv2.threshold(dilated_image, constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
        components = cv2.connectedComponentsWithStats(thresh, constants.CONNECTIVITY, cv2.CV_32S)
        centers = components[3]
        retval, threshold = cv2.threshold(thresh, 200, 255, cv2.THRESH_BINARY_INV)
        return Image(image, threshold)

