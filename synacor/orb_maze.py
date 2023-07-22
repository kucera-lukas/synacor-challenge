from __future__ import annotations

import collections
import logging
import operator
from typing import Callable
from typing import TypeAlias

logger = logging.getLogger(__name__)


MIN = 0
MAX = 32768

START = (3, 0)
END = (0, 3)

RESULT = 30

MAZE: list[list[Callable[[int, int], int] | int]] = [
    [operator.mul, 8, operator.sub, 1],  # type: ignore[misc]
    [4, operator.mul, 11, operator.mul],  # type: ignore[misc]
    [operator.add, 4, operator.sub, 18],  # type: ignore[misc]
    [22, operator.sub, 9, operator.mul],  # type: ignore[misc]
]

STEPS = ((0, 1, 'east'), (1, 0, 'south'), (0, -1, 'west'), (-1, 0, 'north'))

StepType: TypeAlias = 'Callable[[int, int], int] | int'


def calculate(path: list[StepType]) -> int:
    start, *path = path

    assert isinstance(start, int), 'First step must be an integer'
    value: int = start

    op: Callable[[int, int], int]

    for i in path:
        if isinstance(i, int):
            value = op(value, i)
        else:
            op = i

    return value


def bfs() -> list[str]:
    queue: collections.deque[
        tuple[
            tuple[int, int], list[StepType], list[str],
        ]
    ] = collections.deque()
    queue.append((START, [MAZE[START[0]][START[1]]], []))

    while queue:
        nxt, path, steps = queue.popleft()

        if len(path) > 1 and nxt == START:
            continue

        if len(path) > 13:
            continue

        res = calculate(path)

        if res < MIN or res > MAX:
            continue

        if nxt == END:
            if res == RESULT:
                return steps
            else:
                continue

        for i, j, direction in STEPS:
            x, y = nxt
            x += i
            y += j

            if x < 0 or y < 0:
                continue

            if x >= len(MAZE) or y >= len(MAZE[x]):
                continue

            queue.append(((x, y), path + [MAZE[x][y]], steps + [direction]))

    raise RuntimeError('No path found')


def main() -> int:
    steps = bfs()
    logger.info('Found correct steps: %s', steps)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
