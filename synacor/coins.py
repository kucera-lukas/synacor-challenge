from __future__ import annotations

import itertools
import logging

logger = logging.getLogger(__name__)


RESULT = 399

COINS = {
    'red': 2,
    'corroded': 3,
    'shiny': 5,
    'concave': 7,
    'blue': 9,
}


def compute(a: int, b: int, c: int, d: int, e: int) -> int:
    return a + b * c**2 + d**3 - e


def main() -> int:
    for combination in itertools.permutations(COINS.items()):
        if compute(*(c[1] for c in combination)) == RESULT:
            logger.info(f'Solution is {combination}')
            break
    else:
        logger.error('No solution found')
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
