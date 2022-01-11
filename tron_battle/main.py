import math
import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any, List, NewType, Tuple, Union

Map = NewType("Map", List[List[int]])


def debug(*args, end="\n") -> None:
    print(*args, end=end, file=sys.stderr, flush=True)


def debug_map(map_: Map) -> None:
    height = len(map_)
    width = len(map_[0])
    for y in range(height):
        row = []
        for x in range(width):
            row.append("x" if map_[y][x] == -1 else str(map_[y][x]))
        debug("".join(row))


class Direction(IntEnum):
    LEFT = 0
    UP = auto()
    RIGHT = auto()
    DOWN = auto()

    @classmethod
    def get_name(cls, i: Union[int, "Direction"]) -> str:
        return ["LEFT", "UP", "RIGHT", "DOWN"][i]


width = 30
height = 20

directions = {
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
    Direction.UP: (-1, -0),
    Direction.DOWN: (1, 0),
}
MARGIN = 0


@dataclass
class Player:
    y: int
    x: int
    idx: int

    def get_tmp_idx(self) -> int:
        return (1 << self.idx) * 10


def _input_n_p():
    n, p = [int(i) for i in input().split()]
    return n, p


def _input_coordinate():
    x0, y0, x1, y1 = [int(i) for i in input().split()]
    return x0, y0, x1, y1


def update_information(
    n, p, map_, skip_n_p=False
) -> Tuple[Player, List[Player], Map]:

    if not skip_n_p:
        _ = _input_n_p()

    enemies = []
    for i in range(n):
        x0, y0, x1, y1 = _input_coordinate()
        if p == i:
            me = Player(y=y1, x=x1, idx=i)
        else:
            enemies.append(Player(y=y1, x=x1, idx=i))
        map_[y1][x1] = i
    return me, enemies, map_


def bfs(y, x, map_, tmp_idx=-1):
    height = len(map_)
    width = len(map_[0])
    D = [[-1] * width for _ in range(height)]
    q = deque([])
    q.append((y, x, 0))
    D[y][x] = 0
    max_depth = -1
    while q:
        y, x, depth = q.popleft()
        for dy, dx in directions.values():
            ny = y + dy
            nx = x + dx
            if 0 <= nx < width and 0 <= ny < height:
                if map_[ny][nx] not in [-1, tmp_idx]:
                    continue
                if D[ny][nx] != -1:
                    continue
                D[ny][nx] = depth + 1
                max_depth = max(depth + 1, max_depth)
                q.append((ny, nx, depth + 1))
    return max_depth


@dataclass
class Brain:
    me: Player
    enemies: List[Player]
    map_: Map
    behaivior: "BaseBehavior"

    def think(self) -> str:
        return self.behaivior.think(self.me, self.enemies, self.map_)

    def update(self, me: Player, enemies: List[Player], map_: Map) -> None:
        self.me = me
        self.enemies = enemies
        self.map_ = map_


class BaseBehavior:
    def think(self, me: Player, enemies: List[Player], map_: Map) -> str:
        return "Not implemented"

    def isin(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width


class BfsBehavior(BaseBehavior):
    def think(self, me: Player, enemies: List[Player], map_: Map) -> str:
        self.height = len(map_)
        self.width = len(map_[0])
        best = (None, -(10 ** 10))
        for key, value in directions.items():
            dy, dx = value
            ny = me.y + dy
            nx = me.x + dx
            if not self.isin(ny, nx):
                continue
            if map_[ny][nx] != -1:
                continue
            depth = bfs(ny, nx, map_)
            if best[1] < depth:
                best = (key, depth)
        return Direction.get_name(best[0])


class BfsMeAndEnemiesBehavior(BaseBehavior):
    def think(self, me: Player, enemies: List[Player], map_: Map) -> str:
        self.height = len(map_)
        self.width = len(map_[0])

        enemy = enemies[0]  # TODO: 複数対応

        best = (None, -(10 ** 10))
        for key, value in directions.items():
            dy, dx = value
            ny = me.y + dy
            nx = me.x + dx
            if not self.isin(ny, nx):
                continue
            if map_[ny][nx] != -1:
                continue
            me_depth = bfs(ny, nx, map_)

            map_[ny][nx] = 10

            enemy_depth = bfs(enemy.y, enemy.x, map_)
            score = me_depth - enemy_depth

            if best[1] < score:
                best = (key, score)

            map_[ny][nx] = -1

        return Direction.get_name(best[0])


class BfsNotGoNextToEnemiesBehavior(BaseBehavior):
    def think(self, me: Player, enemies: List[Player], map_: Map) -> str:
        self.height = len(map_)
        self.width = len(map_[0])
        self.me = me
        self.enemies = enemies
        self.map_ = map_

        self.update_next_to_enemies()

        best = self.decide_where_to_go()

        self.rollback_next_to_enemies()

        if best[0] is not None:
            return Direction.get_name(best[0])

        # 隣に行かない制約のせいでどこにもいけない可能性があるので隣もOKで再度探索にする
        best = self.decide_where_to_go()
        if best[0] is not None:
            return Direction.get_name(best[0])

        # どうしようもないけど順番のおかげで勝つかもしれないのでLEFTを返しておく
        return "LEFT"

    def decide_where_to_go(self) -> Tuple[Any, int]:
        enemy = self.enemies[0]  # TODO: 複数対応

        best = (None, -(10 ** 10))
        for key, value in directions.items():
            dy, dx = value
            ny = self.me.y + dy
            nx = self.me.x + dx
            if not self.isin(ny, nx):
                continue
            if self.map_[ny][nx] != -1:
                continue
            me_depth = bfs(ny, nx, self.map_)

            self.map_[ny][nx] = self.me.get_tmp_idx()

            enemy_depth = bfs(enemy.y, enemy.x, self.map_, enemy.get_tmp_idx())
            score = me_depth - enemy_depth

            if best[1] < score:
                best = (key, score)

            self.map_[ny][nx] = -1
        return best

    def update_next_to_enemies(self) -> None:
        for enemy in self.enemies:
            if enemy.idx < self.me.idx:
                # プレイヤーより先に行動し近づくと危ないので隣をすべて-1ではないようにする
                for key, value in directions.items():
                    dy, dx = value
                    ny = enemy.y + dy
                    nx = enemy.x + dx
                    if not self.isin(ny, nx):
                        continue
                    if self.map_[ny][nx] != -1:
                        continue
                    self.map_[ny][nx] = enemy.get_tmp_idx()

    def rollback_next_to_enemies(self) -> None:
        for enemy in self.enemies:
            if enemy.idx < self.me.idx:
                for key, value in directions.items():
                    dy, dx = value
                    ny = enemy.y + dy
                    nx = enemy.x + dx
                    if not self.isin(ny, nx):
                        continue
                    if self.map_[ny][nx] == enemy.get_tmp_idx():
                        self.map_[ny][nx] = -1


class BehaviorName(IntEnum):
    BfsBehavior = auto()
    BfsMeAndEnemiesBehavior = auto()
    BfsNotGoNextToEnemiesBehavior = auto()


class BehaviorFactory:
    @classmethod
    def make(self, name: str) -> BaseBehavior:
        if name == BehaviorName.BfsBehavior:
            return BfsBehavior()
        elif name == BehaviorName.BfsMeAndEnemiesBehavior:
            return BfsMeAndEnemiesBehavior()
        elif name == BehaviorName.BfsNotGoNextToEnemiesBehavior:
            return BfsNotGoNextToEnemiesBehavior()
        raise ValueError(f"Invalid name {name}")


if __name__ == "__main__ ":
    n, p = [int(i) for i in input().split()]
    map_ = [[-1] * width for _ in range(height)]
    me, enemies, map_ = update_information(n=n, p=p, map_=map_, skip_n_p=True)

    behaivior = BehaviorFactory().make(BehaviorName.BfsNotGoNextToEnemiesBehavior)
    brain = Brain(me, enemies, map_, behaivior)

    ans = brain.think()
    print(ans)

    while True:
        me, enemies, map_ = update_information(n=n, p=p, map_=map_)

        brain.update(me, enemies, map_)
        ans = brain.think()
        print(ans)
