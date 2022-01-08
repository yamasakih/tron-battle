import unittest
import contextlib

import tron_battle
from tron_battle.main import update_information
from tron_battle.main import Player

i = 0


class TestUpdateInformation:
    def setup_method(self, method):
        global i
        i = 0

    def teardown_method(self, method):
        global i
        i = 0

    def test_run(self, monkeypatch):
        def mock_input_n_p():
            return 2, 0

        def mock_input_coordinate():
            global i
            if i == 0:
                i += 1
                return 0, 0, 0, 0
            else:
                return 2, 1, 2, 1

        monkeypatch.setattr(tron_battle.main, "_input_n_p", mock_input_n_p)
        monkeypatch.setattr(
            tron_battle.main, "_input_coordinate", mock_input_coordinate
        )

        height = 3
        width = 4
        map_ = [[-1] * width for _ in range(height)]
        n = 2
        p = 0
        i = 0
        me, enemies, map_ = update_information(n, p, map_)

        expect = [
            [0, -1, -1, -1],
            [-1, -1, 1, -1],
            [-1, -1, -1, -1],
        ]

        assert map_ == expect

        expect = Player(y=0, x=0, idx=0)
        assert me == expect

        expect = [Player(y=1, x=2, idx=1)]
        assert enemies == expect
