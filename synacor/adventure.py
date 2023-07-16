from __future__ import annotations

import logging
import subprocess
from typing import IO

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
    'north',
    'north',
    'north',
    'north',
    'north',
    'north',
    'north',
    'east',
    'take journal',
    'look journal',
    'west',
    'north',
    'north',
    'take orb',
    'look',
    'north',
    'east',
    'east',
    'north',
    'west',
    'south',
    'east',
    'east',
    'west',
    'north',
    'north',
    'east',
    'vault',
    'take mirror',
    'use mirror',
]


def main(interactive: bool) -> int:
    with subprocess.Popen(CMD, stdin=subprocess.PIPE) as proc:
        if proc.stdin is None:
            logger.error('Failed to start process')
            return 1

        stdin: IO[bytes] = proc.stdin

        def write(s: str) -> None:
            stdin.write(f'{s}\n'.encode())
            stdin.flush()

        for step in STEPS:
            write(step)

        if interactive:
            while proc.poll() is None:
                try:
                    command = input()
                except EOFError:
                    break

                write(command)

    returncode = proc.poll()
    return returncode if isinstance(returncode, int) else 1


if __name__ == '__main__':
    raise SystemExit(main(interactive=False))
