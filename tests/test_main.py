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

    def mock_input_n_p(self):
        return 2, 0

    def mock_input_coordinate(self):
        global i
        if i == 0:
            i += 1
            return 0, 0, 0, 0
        else:
            return 2, 1, 2, 1

    def test_run(self, monkeypatch):
        monkeypatch.setattr(tron_battle.main, "_input_n_p", self.mock_input_n_p)
        monkeypatch.setattr(
            tron_battle.main, "_input_coordinate", self.mock_input_coordinate
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

    def test_run_with_skip(self, monkeypatch):
        monkeypatch.setattr(tron_battle.main, "_input_n_p", self.mock_input_n_p)
        monkeypatch.setattr(
            tron_battle.main, "_input_coordinate", self.mock_input_coordinate
        )

        height = 3
        width = 4
        map_ = [[-1] * width for _ in range(height)]
        n = 2
        p = 0
        i = 0
        me, enemies, map_ = update_information(n, p, map_, skip_n_p=True)

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

