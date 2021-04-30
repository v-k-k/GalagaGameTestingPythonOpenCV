import cv2
import pytesseract
from time import sleep
import constants
from utils import Base
from utils.timeouts import Timeouts


class Game(Base):
    _keypoints_player = None
    _keypoints_enemy = None
    _keypoints_missile = None
    _target_page = None

    def __init__(self, target):
        pytesseract.pytesseract.tesseract_cmd = constants.TESSERACT_EXE
        self._target_page = target
        sleep(Timeouts.MAX.value)
        self.logger.warning("Page opened")

    def canvas_image(self):
        return self._target_page.canvas_image

    def pass_through_initial_screen(self, get_flag_callback):
        while get_flag_callback():
            self.logger.warning("Initial screen visible")
            self._target_page.perform_canvas_click_with_enter() \
                             .perform_double_enter_click()

    def move_left_and_shoot(self):
        self._target_page.press_left_x()

    def idle_on_left(self):
        self._target_page.release_left_x()

    def move_right_and_shoot(self):
        self._target_page.press_right_x()

    def idle_on_right(self):
        self._target_page.release_right_x()

    def pause_game(self):
        self._target_page.perform_single_enter_click()

    def run_game_loop(self, injected_action, image, pause_solver):
        while True:
            image.load_keypoints()
            pause_solver()
            im_with_keypoints = image.draw_keypoints() if constants.DEBUG_MODE else None
            injected_action()
            pause_solver()
            if constants.DEBUG_MODE:
                cv2.imshow("Galaga", im_with_keypoints)
                if cv2.waitKey(1) == ord('q'):
                    break
            test_passed = yield
            self.logger.error(f"Test pass status is --> {bool(test_passed)}")
            if test_passed:
                break

