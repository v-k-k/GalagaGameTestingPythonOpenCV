from utils import Base
from time import sleep


class Tester(Base):

    def __init__(self, game):
        self.game = game
        self.logger.info("Tester instance successfully created")

    def check_initial_screen(self):
        self.game.check_initial_screen(attempts=1000)

    def __check(self, test_producer):
        while True:
            try:
                self.logger.debug(dir(test_producer))
                next(test_producer)
                sleep(1)
            except StopIteration:
                break

    def check_lives_visible(self):
        # TODO
        pass

    def check_fighter_moved(self):
        return self.__check(test_producer=self.game.check_fighter_movements())

    def check_missile_launched(self):
        return self.__check(test_producer=self.game.check_missile_launched())

    def check_game_over(self):
        # TODO
        pass
