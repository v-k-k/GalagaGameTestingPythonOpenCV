import pyautogui
from time import sleep

from .image_control import ImageControl
from utils import Base, coroutine, Coordinates
from utils.timeouts import Timeouts


class GameControl(Base):
    __image = None
    __game = None
    __game_loop = None
    __CURRENT_PLAYER_AXIS_Y_POSITION = 0

    def __init__(self, target):
        self.__game = target
        self.__image = ImageControl(self.__game.canvas_image)
        self.__game.pass_through_initial_screen(
            self.__image.is_initial_screen_visible
        )

    def check_initial_screen(self, attempts):
        self.__game.pause_game()
        for _ in range(attempts):
            content = self.__image.text_content
            if "start" in content or "stage 1" in content:
                break
            self.logger.error("No initial messages")
            if not _ % 50:
                self.__game.pause_game()
                self.__game.pause_game()
            sleep(Timeouts.MIN.value)
        else:
            raise AssertionError("Game wasn't initialized")

    @property
    def _game_loop(self):
        if not self.__game_loop:
            self.__game_loop = coroutine(self.__game.run_game_loop)(self.follow_and_destroy,
                                                                    self.__image,
                                                                    self.prevent_pause_click)
        return self.__game_loop

    def check(self, criteria: tuple):
        a = 10  # # #
        while True:
            try:
                self._game_loop.send(a)  # # #
                yield
            except StopIteration:
                break
            a -= 1  # # #

    @property
    def lowest_enemy_location(self):
        lowest_enemy_y_axis = 0
        lowest_enemy_x_axis = 0
        lowest_enemy_x = 0
        j = 0
        while j < len(self.__image.keypoints.enemy):
            enemy_axis_y = self.__image.keypoints.enemy[j].pt[0]
            enemy_axis_x = self.__image.keypoints.enemy[j].pt[1]
            if enemy_axis_x > lowest_enemy_x:
                lowest_enemy_x_axis = enemy_axis_x
                lowest_enemy_y_axis = enemy_axis_y
            j += 1
        return Coordinates(lowest_enemy_y_axis, lowest_enemy_x_axis)

    def prevent_pause_click(self):
        if "pause" in self.__image.text_content:
            self.logger.warning("PAUSE occurred !!!")
            self.__game.pause_game()
            self.logger.warning("pressed ENTER")

    def evasion_maneuver_alpha(self, lowest_enemy_y_axis):
        if self.__CURRENT_PLAYER_AXIS_Y_POSITION > lowest_enemy_y_axis:
            self.__game.move_right_and_shoot()
        if self.__CURRENT_PLAYER_AXIS_Y_POSITION < lowest_enemy_y_axis:
            self.__game.move_left_and_shoot()
        self.prevent_pause_click()

    def follow_and_destroy(self):
        closest_enemy = self.lowest_enemy_location
        i = 0
        while i < len(self.__image.keypoints.player):
            self.__CURRENT_PLAYER_AXIS_Y_POSITION = self.__image.keypoints.player[i].pt[0]
            player_axis_x = self.__image.keypoints.player[i].pt[1]
            self.logger.debug(self.__CURRENT_PLAYER_AXIS_Y_POSITION)
            i += 1
            if closest_enemy.x_coord > 130:
                self.evasion_maneuver_alpha(closest_enemy.y_coord)
            if self.__CURRENT_PLAYER_AXIS_Y_POSITION > closest_enemy.y_coord:
                self.__game.move_left_and_shoot()
            else:
                self.__game.idle_on_left()
            self.prevent_pause_click()
            if self.__CURRENT_PLAYER_AXIS_Y_POSITION < closest_enemy.y_coord:
                self.__game.move_right_and_shoot()
            else:
                self.__game.idle_on_right()
            self.prevent_pause_click()

    def alternative_press_left_x(self):
        self.logger.warning("Alternative pressing down LEFT + X")
        pyautogui.keyDown('left')
        pyautogui.keyDown('x')
        return self

    def alternative_release_left_x(self):
        self.logger.warning("Alternative releasing LEFT + X")
        pyautogui.keyUp('left')
        pyautogui.keyUp('x')
        return self

    def alternative_press_right_x(self):
        self.logger.warning("Alternative pressing down RIGHT + X")
        pyautogui.keyDown('right')
        pyautogui.keyDown('x')
        return self

    def alternative_release_right_x(self):
        self.logger.warning("Alternative releasing RIGHT + X")
        pyautogui.keyUp('right')
        pyautogui.keyUp('x')
        return self
