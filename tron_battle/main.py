import sys
import math
from copy import deepcopy
from collections import deque

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

# game loop
width = 30
height = 20
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
directions = [LEFT, UP, RIGHT, DOWN]
direction_strings = ["LEFT", "UP", "RIGHT", "DOWN"]
MARGIN = 0


def bfs(y, x):
    inter = [[-1] * width for _ in range(height)]
    q = deque([])
    q.append((y, x, 0))
    inter[y][x] = 0
    max_ = -1
    while q:
        y, x, depth = q.popleft()
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < width and 0 <= ny < height and been[ny][nx] == -1:
                if inter[ny][nx] != -1:
                    continue
                inter[ny][nx] = depth + 1
                max_ = max(depth + 1, max_)
                q.append((ny, nx, depth + 1))
    return max_


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


# def update():
#     global px
#     global py
#     global been
#     for i in range(n):
#         x0, y0, x1, y1 = [int(j) for j in input().split()]
#         if p == i:
#             px = x1
#             py = y1
#         been[y0][x0] = p

if __name__ == "__main__ ":
    n, p = [int(i) for i in input().split()]
    been = [[-1] * width for _ in range(height)]
    enemies = []
    for i in range(n):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        if p == i:
            px = x1
            py = y1
        else:
            enemies.append((x1, y1, i))
        been[y0][x0] = p
    # update()

    idx = search()
    print(direction_strings[idx])

    print(f"{enemies=}", file=sys.stderr, flush=True)
    while True:
        _ = input()
        # update()
        enemies = []
        for i in range(n):
            x0, y0, x1, y1 = [int(j) for j in input().split()]
            if i == p:
                px = x1
                py = y1
            else:
                enemies.append((x1, y1, i))
            been[y1][x1] = i

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
