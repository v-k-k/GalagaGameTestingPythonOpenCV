import pytest


class TestBasics:

    @pytest.mark.initial
    def test_initial_screen(self, tester):
        tester.check_initial_screen()

    @pytest.mark.simple
    @pytest.mark.missile
    def test_missile_launched(self, tester):
        tester.check_missile_launched()

    @pytest.mark.simple
    @pytest.mark.movements
    def test_fighter_movements(self, tester):
        tester.check_fighter_moved()

