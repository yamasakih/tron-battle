import math
import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import List, Tuple, Union


def debug(*args, end="\n"):
    print(*args, end=end, file=sys.stderr, flush=True)


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


def _input_n_p():
    n, p = [int(i) for i in input().split()]
    return n, p


def _input_coordinate():
    x0, y0, x1, y1 = [int(i) for i in input().split()]
    return x0, y0, x1, y1


def update_information(
    n, p, map_, skip_n_p=False
) -> Tuple[Player, List[Player], List[List[int]]]:

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


def bfs(y, x, map_):
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
            if 0 <= nx < width and 0 <= ny < height and map_[ny][nx] == -1:
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
    map_: List[List[int]]
    behaivior: "BaseBehavior"

    def think(self) -> str:
        return self.behaivior.think(self.me, self.enemies, self.map_)

    def update(
        self, me: Player, enemies: List[Player], map_: List[List[int]]
    ) -> None:
        self.me = me
        self.enemies = enemies
        self.map_ = map_


class BaseBehavior:
    def think(
        self, me: Player, enemies: List[Player], map_: List[List[int]]
    ) -> str:
        return "Not implemented"

    def isin(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width


class BfsBehavior(BaseBehavior):
    def think(
        self, me: Player, enemies: List[Player], map_: List[List[int]]
    ) -> str:
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
    def think(
        self, me: Player, enemies: List[Player], map_: List[List[int]]
    ) -> str:
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


if __name__ == "__main__ ":
    n, p = [int(i) for i in input().split()]
    map_ = [[-1] * width for _ in range(height)]
    me, enemies, map_ = update_information(n=n, p=p, map_=map_, skip_n_p=True)

    # behaivior = BfsBehavior()
    behaivior = BfsMeAndEnemiesBehavior()
    brain = Brain(me, enemies, map_, behaivior)

    ans = brain.think()
    print(ans)

    while True:
        me, enemies, map_ = update_information(n=n, p=p, map_=map_)

        brain.update(me, enemies, map_)
        ans = brain.think()
        print(ans)
