from pages import GalagaPage
import pytest
from game import Game


class TestBasics:

    def test_shit(self, init_driver):
        game = Game(GalagaPage(init_driver))
        game.run_game_loop()

