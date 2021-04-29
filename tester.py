from utils import Base
from time import sleep


class Tester(Base):

    def __init__(self, game):
        self.game = game
        self.logger.info("Tester instance successfully created")

    def check_initial_screen(self):
        self.game.check_initial_screen(attempts=1000)

    def check(self):
        p = self.game.check(criteria=None)
        while True:
            try:
                next(p)
                sleep(1)
            except StopIteration:
                break

