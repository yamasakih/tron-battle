from copy import deepcopy
import tron_battle
from tron_battle.main import (
    _reset_map,
    BehaviorFactory,
    BehaviorName,
    BfsBehavior,
    BfsMeAndEnemiesBehavior,
    BfsNotGoNextToEnemiesBehavior,
    BfsTwoStepBehavior,
    Player,
    bfs,
    update_information,
)

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
        monkeypatch.setattr(
            tron_battle.main, "_input_n_p", self.mock_input_n_p
        )
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

    def test_run_at_first(self, monkeypatch):
        monkeypatch.setattr(
            tron_battle.main, "_input_n_p", self.mock_input_n_p
        )
        monkeypatch.setattr(
            tron_battle.main, "_input_coordinate", self.mock_input_coordinate
        )

        height = 3
        width = 4
        map_ = [[-1] * width for _ in range(height)]
        n = 2
        p = 0
        i = 0
        me, enemies, map_ = update_information(n, p, map_, first=True)

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


class TestBfs:
    def test_run1(self):
        map_ = [
            [0, -1, -1, -1, 0],
            [0, -1, 0, 0, 0],
            [0, -1, 0, -1, 0],
            [0, -1, -1, -1, 0],
        ]

        actual = bfs(0, 1, map_)
        expect = 6
        assert actual == expect

        actual = bfs(0, 3, map_)
        expect = 8
        assert actual == expect

        actual = bfs(3, 1, map_)
        expect = 5
        assert actual == expect

    def test_run2(self):
        map_ = [
            [-1, 2, 2, 2, 2, 2],
            [-1, 2, -1, -1, -1, -1],
            [-1, 2, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1],
        ]

        actual = bfs(2, 0, map_)
        expect = 2
        assert actual == expect

        actual = bfs(1, 3, map_)
        expect = 6
        assert actual == expect

        actual = bfs(3, 3, map_)
        expect = 4
        assert actual == expect

    def test_run3(self):
        map_ = [
            [-1, -1, 10],
            [0, 0, -1],
            [0, 0, -1],
        ]

        actual = bfs(0, 1, map_)
        expect = 1
        assert actual == expect

        actual = bfs(0, 1, map_, tmp_idx=10)
        expect = 3
        assert actual == expect

        actual = bfs(0, 1, map_, tmp_idx=20)
        expect = 1
        assert actual == expect


class TestBfsBehavior:
    def test_run1(self):
        map_ = [
            [0, -1, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsBehavior()

        me = Player(y=0, x=0, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

        me = Player(y=3, x=4, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "LEFT"
        assert actual == expect

    def test_run2(self):
        map_ = [
            [0, 0, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsBehavior()

        me = Player(y=0, x=1, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "DOWN"
        assert actual == expect

        me = Player(y=2, x=2, idx=1)
        enemies = [Player(y=0, x=3, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

    def test_run3(self):
        map_ = [
            [0, -1, -1, -1, 2],
            [0, 1, 1, 2, 2],
            [0, 1, -1, -1, 2],
            [2, 2, 2, -1, -1],
        ]
        behavior = BfsBehavior()

        me = Player(y=1, x=2, idx=0)
        enemies = [Player(y=0, x=0, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "DOWN"
        assert actual == expect

    def test_run4(self):
        map_ = [
            [1, 1, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, 0, 0, 0, 0],
        ]
        behavior = BfsBehavior()

        me = Player(y=3, x=2, idx=0)
        enemies = [Player(y=0, x=0, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "LEFT"
        assert actual == expect


class TestBfsMeAndEnemiesBehavior:
    def test_run1(self):
        map_ = [
            [0, -1, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsMeAndEnemiesBehavior()

        me = Player(y=0, x=0, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

        me = Player(y=3, x=4, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "LEFT"
        assert actual == expect

    def test_run2(self):
        map_ = [
            [0, 0, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsMeAndEnemiesBehavior()

        me = Player(y=0, x=1, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "DOWN"
        assert actual == expect

        me = Player(y=2, x=2, idx=1)
        enemies = [Player(y=0, x=3, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

    def test_run3(self):
        map_ = [
            [0, -1, -1, -1, 2],
            [0, 1, 1, 2, 2],
            [0, 1, -1, -1, 2],
            [2, 2, 2, -1, -1],
        ]
        behavior = BfsMeAndEnemiesBehavior()

        me = Player(y=1, x=2, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "UP"
        assert actual == expect

    def test_run4(self):
        map_ = [
            [0, -1, -1, -1, 2],
            [0, 1, 2, 2, 2],
            [0, -1, -1, -1, 2],
            [2, 2, 2, -1, -1],
        ]
        behavior = BfsMeAndEnemiesBehavior()

        me = Player(y=1, x=1, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "UP"
        assert actual == expect


class TestBehaviorFactory:
    def test_run1(self):
        factory = BehaviorFactory()
        behavior = factory.make(BehaviorName.BfsBehavior)

        actual = type(behavior)
        expect = BfsBehavior
        assert actual == expect

    def test_run2(self):
        factory = BehaviorFactory()
        behavior = factory.make(BehaviorName.BfsMeAndEnemiesBehavior)

        actual = type(behavior)
        expect = BfsMeAndEnemiesBehavior
        assert actual == expect


class TestPlayer:
    def test_run(self):
        player = Player(y=0, x=0, idx=0)
        actual = player.get_tmp_idx()
        expect = 10
        assert actual == expect

        player = Player(y=0, x=0, idx=2)
        actual = player.get_tmp_idx()
        expect = 40
        assert actual == expect


class TestBfsNotGoNextToEnemiesBehavior:
    def test_run1(self):
        map_ = [
            [0, -1, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsNotGoNextToEnemiesBehavior()

        me = Player(y=0, x=0, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

        me = Player(y=3, x=4, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "LEFT"
        assert actual == expect

    def test_run2(self):
        map_ = [
            [0, 0, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsNotGoNextToEnemiesBehavior()

        me = Player(y=0, x=1, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "DOWN"
        assert actual == expect

        me = Player(y=2, x=2, idx=1)
        enemies = [Player(y=0, x=3, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

    def test_run3(self):
        map_ = [
            [0, -1, -1, -1, 2],
            [0, 1, 1, 2, 2],
            [0, 1, -1, -1, 2],
            [2, 2, 2, -1, -1],
        ]
        behavior = BfsNotGoNextToEnemiesBehavior()

        me = Player(y=1, x=2, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "UP"
        assert actual == expect

    def test_run4_push_the_latter_enemy_to_the_side(self):
        map_ = [
            [1, -1, -1, -1, 2],
            [1, 0, 2, 2, 2],
            [1, -1, -1, -1, 2],
            [2, 2, 2, -1, -1],
        ]
        behavior = BfsNotGoNextToEnemiesBehavior()

        me = Player(y=1, x=1, idx=0)
        enemies = [Player(y=0, x=0, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "UP"
        assert actual == expect

    def test_run5_dont_push_the_former_enemy_to_the_side(self):
        map_ = [
            [0, -1, -1, -1, 2],
            [0, 1, 2, 2, 2],
            [0, -1, -1, -1, 2],
            [2, 2, 2, -1, -1],
        ]
        behavior = BfsNotGoNextToEnemiesBehavior()

        me = Player(y=1, x=1, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "DOWN"
        assert actual == expect

    def test_rollback_next_to_enemies(self):
        me = Player(y=0, x=0, idx=2)
        enemies = [Player(y=0, x=0, idx=0)]
        behavior = BfsNotGoNextToEnemiesBehavior()
        behavior.me = me
        behavior.enemies = enemies
        behavior.height = 3
        behavior.width = 3

        map_ = [
            [10, 10, 10],
            [10, 10, 10],
            [10, 10, 10],
        ]
        behavior.map_ = map_
        behavior.rollback_next_to_enemies()
        actual = behavior.map_
        expect = [
            [10, -1, 10],
            [-1, 10, 10],
            [10, 10, 10],
        ]
        assert actual == expect

        map_ = [
            [10, 30, 10],
            [10, 10, 10],
            [10, 10, 10],
        ]
        behavior.map_ = map_
        behavior.rollback_next_to_enemies()
        actual = behavior.map_
        expect = [
            [10, 30, 10],
            [-1, 10, 10],
            [10, 10, 10],
        ]
        assert actual == expect

        enemies = [Player(y=1, x=2, idx=0)]
        behavior.enemies = enemies
        map_ = [
            [10, 10, 10],
            [10, 10, 10],
            [10, 10, 10],
        ]
        behavior.map_ = map_
        behavior.rollback_next_to_enemies()
        actual = behavior.map_
        expect = [
            [10, 10, -1],
            [10, -1, 10],
            [10, 10, -1],
        ]
        assert actual == expect

    def test_run6(self):
        map_ = [
            [1, -1, -1, -1],
            [1, -1, -1, -1],
            [-1, 0, 0, 0],
        ]
        behavior = BfsNotGoNextToEnemiesBehavior()

        me = Player(y=2, x=1, idx=0)
        enemies = [Player(y=1, x=0, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "UP"
        assert actual == expect


class TestBfsTwoStepBehavior:
    def test_run1(self):
        map_ = [
            [0, -1, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        behavior = BfsTwoStepBehavior()

        me = Player(y=0, x=0, idx=0)
        enemies = [Player(y=3, x=4, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "RIGHT"
        assert actual == expect

        me = Player(y=3, x=4, idx=1)
        enemies = [Player(y=0, x=0, idx=0)]
        actual = behavior.think(me, enemies, map_)
        expect = "LEFT"
        assert actual == expect

    def test_run2(self):
        map_ = [
            [1, 1, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, 0, 0, 0, 0],
        ]
        behavior = BfsBehavior()

        me = Player(y=3, x=2, idx=0)
        enemies = [Player(y=0, x=0, idx=1)]
        actual = behavior.think(me, enemies, map_)
        expect = "LEFT"
        assert actual == expect


class TestBfsTwoStepBehavior:
    def test_run1(self):
        map_ = [
            [0, -1, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, 2, 1, -1, 1],
            [0, 2, 2, 2, 1],
        ]

        actual = _reset_map(deepcopy(map_), 0)
        expect = [
            [-1, -1, -1, -1, 1],
            [-1, -1, 1, 1, 1],
            [-1, 2, 1, -1, 1],
            [-1, 2, 2, 2, 1],
        ]
        assert actual == expect

        actual = _reset_map(deepcopy(map_), 1)
        expect = [
            [0, -1, -1, -1, -1],
            [0, -1, -1, -1, -1],
            [0, 2, -1, -1, -1],
            [0, 2, 2, 2, -1],
        ]
        assert actual == expect

        actual = _reset_map(deepcopy(map_), 2)
        expect = [
            [0, -1, -1, -1, 1],
            [0, -1, 1, 1, 1],
            [0, -1, 1, -1, 1],
            [0, -1, -1, -1, 1],
        ]
        assert actual == expect
