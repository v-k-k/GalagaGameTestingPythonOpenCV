import cv2
import pytesseract
import numpy as np
from time import sleep
from selenium.webdriver.common.keys import Keys

import constants
from detectors import DetectorFactory, DetectorsEnum
from utils import Base, Colors


pytesseract.pytesseract.tesseract_cmd = constants.TESSERACT_EXE


class Game(Base):
    _keypoints_player = None
    _keypoints_enemy = None
    _keypoints_missile = None
    _target_page = None

    def __init__(self, target):
        self._target_page = target
        sleep(5)
        self.logger.warning("Page opened")
        while any(("1981" in pytesseract.image_to_string(self._target_page.image.original),
                   "1985" in pytesseract.image_to_string(self._target_page.image.original))):
            self.logger.warning("Initial screen visible")
            self._target_page.actions.move_to_element_with_offset(self._target_page.canvas, 50, 50)\
                                     .click(self._target_page.canvas) \
                                     .send_keys(Keys.RETURN) \
                                     .perform()
            self._target_page.actions.pause(1) \
                                     .send_keys(Keys.RETURN + Keys.RETURN) \
                                     .pause(1) \
                                     .send_keys(Keys.RETURN + Keys.RETURN) \
                                     .perform()
            self.logger.warning("Double ENTER clicked")

    def draw_keypoints(self, image, *args):
        for keypoint in args:
            if keypoint == self._keypoints_player:
                point_color = Colors.GREEN.value
            elif keypoint == self._keypoints_enemy:
                point_color = Colors.RED.value
            else:
                point_color = Colors.BLACK.value
            image = cv2.drawKeypoints(
                image, keypoint, np.array([]), point_color,
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
        return image

    def lowest_enemy_location(self):
        lowest_enemy_y_axis = 0
        lowest_enemy_x_axis = 0
        lowest_enemy_x = 0
        j = 0
        while j < len(self._keypoints_enemy):
            enemy_axis_y = self._keypoints_enemy[j].pt[0]
            enemy_axis_x = self._keypoints_enemy[j].pt[1]
            if enemy_axis_x > lowest_enemy_x:
                lowest_enemy_x_axis = enemy_axis_x
                lowest_enemy_y_axis = enemy_axis_y
            j += 1
        return lowest_enemy_y_axis, lowest_enemy_x_axis

    def evasion_manever_alpha(self, lowest_enemy_y_axis):
        if constants.PLAYER_AXIS_Y > lowest_enemy_y_axis:
            # pyautogui.keyDown('right')
            # pyautogui.keyDown('x')
            self._target_page.actions.key_down(Keys.RIGHT)\
                                     .key_down('x')\
                                     .perform()
        if constants.PLAYER_AXIS_Y < lowest_enemy_y_axis:
            # pyautogui.keyDown('left')
            # pyautogui.keyDown('x')
            self._target_page.actions.key_down(Keys.LEFT)\
                                     .key_down('x')\
                                     .perform()

    def follow_and_destroy(self, lowest_enemy_y_axis, lowest_enemy_x_axis):
        i = 0
        while i < len(self._keypoints_player):
            constants.PLAYER_AXIS_Y = self._keypoints_player[i].pt[0]
            player_axis_x = self._keypoints_player[i].pt[1]
            self.logger.critical(constants.PLAYER_AXIS_Y)
            i += 1
            if lowest_enemy_x_axis > 130:
                self.evasion_manever_alpha(lowest_enemy_y_axis)
            if constants.PLAYER_AXIS_Y > lowest_enemy_y_axis:
                # pyautogui.keyDown('left')
                # pyautogui.keyDown('x')
                self._target_page.actions.key_down(Keys.LEFT)\
                                         .key_down('x')\
                                         .perform()
                self.logger.critical('DOWN: left + x')
            else:
                # pyautogui.keyUp('left')
                # pyautogui.keyUp('x')
                self._target_page.actions.key_up(Keys.LEFT)\
                                         .key_up('x')\
                                         .perform()
                self.logger.critical('UP: left + x')
            if constants.PLAYER_AXIS_Y < lowest_enemy_y_axis:
                # pyautogui.keyDown('right')
                # pyautogui.keyDown('x')
                self._target_page.actions.key_down(Keys.RIGHT)\
                                         .key_down('x')\
                                         .perform()
                self.logger.critical('DOWN: right + x')
            else:
                # pyautogui.keyUp('right')
                # pyautogui.keyUp('x')
                self._target_page.actions.key_up(Keys.RIGHT)\
                                         .key_up('x')\
                                         .perform()
                self.logger.critical('UP: right + x')

    def __get_keypoints(self, threshold):
        self._keypoints_player = DetectorFactory.create_detector(DetectorsEnum.Player)\
                                                .detect(threshold)
        self._keypoints_enemy = DetectorFactory.create_detector(DetectorsEnum.Enemy)\
                                               .detect(threshold)
        self._keypoints_missile = DetectorFactory.create_detector(DetectorsEnum.Missile)\
                                                 .detect(threshold)

    def run_game_loop(self):
        while True:
            self.__get_keypoints(self._target_page.image.threshold)
            if constants.DEBUG_MODE:
                im_with_keypoints = self.draw_keypoints(self._target_page.image.original,
                                                        self._keypoints_player,
                                                        self._keypoints_enemy,
                                                        self._keypoints_missile)
            lowest_enemy_y_axis, lowest_enemy_x_axis = self.lowest_enemy_location()
            self.follow_and_destroy(lowest_enemy_y_axis, lowest_enemy_x_axis)
            if constants.DEBUG_MODE:
                cv2.imshow("Galaga", im_with_keypoints)
                if cv2.waitKey(1) == ord('q'):
                    break
