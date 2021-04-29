import pytest


class TestBasics:

    @pytest.mark.initial
    def test_initial_screen(self, tester):
        tester.check_initial_screen()

    @pytest.mark.simple
    def test_simple(self, tester):
        tester.check()

