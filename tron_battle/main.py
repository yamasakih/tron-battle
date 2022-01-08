import sys
import math
from copy import deepcopy
from collections import deque
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Player:
    y: int
    x: int
    idx: int


width = 30
height = 20
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
directions = [LEFT, UP, RIGHT, DOWN]
direction_strings = ["LEFT", "UP", "RIGHT", "DOWN"]
MARGIN = 0


def debug(*args, end="\n"):
    print(*args, end=end, file=sys.stderr, flush=True)


def search():
    best = (-3, -3)
    for i, d in enumerate(directions):
        dx, dy = d
        nx = px + dx
        ny = py + dy
        if not (0 <= nx < width and 0 <= ny < height):
            continue
        if been[ny][nx] != -1:
            continue
        v = bfs(ny, nx)
        if best[0] < v:
            best = (v, i)
    return best[1]


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
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < width and 0 <= ny < height and map_[ny][nx] == -1:
                if D[ny][nx] != -1:
                    continue
                D[ny][nx] = depth + 1
                max_depth = max(depth + 1, max_depth)
                q.append((ny, nx, depth + 1))
    return max_depth


if __name__ == "__main__ ":
    n, p = [int(i) for i in input().split()]
    map_ = [[-1] * width for _ in range(height)]
    me, enemies, map_ = update_information(n=n, p=p, map_=map_, skip_n_p=True)

    idx = search()
    print(direction_strings[idx])

    print(f"{enemies=}", file=sys.stderr, flush=True)
    while True:
        me, enemies, map_ = update_information(n=n, p=p, map_=map_)

        for ex, ey, idx in enemies:
            for dx, dy in directions:
                nx = ex + dx
                ny = ey + dy
                if nx < 0 or width <= nx or ny < 0 or height <= ny:
                    continue
                v = (1 << idx) * 10
                print(v, file=sys.stderr, flush=True)
                if been[ny][nx] == -1:
                    been[ny][nx] = v
                elif been[ny][nx] >= 10:
                    been[ny][nx] += v
        for b in been:
            print(b, file=sys.stderr, flush=True)
        idx = search()
        for ex, ey, i in enemies:
            for dx, dy in directions:
                nx = ex + dx
                ny = ey + dy
                if nx < 0 or width <= nx or ny < 0 or height <= ny:
                    continue
                # v = (1 << i) * 10
                if been[ny][nx] >= 10:
                    been[ny][nx] = -1

        print(direction_strings[idx])
