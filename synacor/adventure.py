from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)

CMD = [
    'python',
    '-m',
    'synacor',
    'vm',
    'spec/challenge.bin',
]

STEPS = [
    'take tablet',
    'use tablet',
    'doorway',
    'north',
    'north',
    'bridge',
    'continue',
    'down',
    'east',
    'take empty lantern',
    'west',
    'west',
    'passage',
    'ladder',
    'west',
    'south',
    'north',
    'take can',
    'use can',
    'use lantern',
    'west',
    'ladder',
    'darkness',
    'continue',
    'west',
    'west',
    'west',
    'west',
    'north',
    'take red coin',
    'north',
    'east',
    'take concave coin',
    'down',
    'take corroded coin',
    'up',
    'west',
    'west',
    'take blue coin',
    'up',
    'take shiny coin',
    'down',
    'east',
    'use blue coin',
    'use red coin',
    'use shiny coin',
    'use concave coin',
    'use corroded coin',
    'north',
    'take teleporter',
    'use teleporter',
    'take business card',
    'take strange book',
    'look strange book',
    'fix teleporter',
    'use teleporter',
]


def main() -> int:
    with subprocess.Popen(CMD, stdin=subprocess.PIPE) as proc:
        if proc.stdin is None:
            logger.error('Failed to start process')
            return 1

        for step in STEPS:
            proc.stdin.write(f'{step}\n'.encode())

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
