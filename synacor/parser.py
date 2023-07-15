from __future__ import annotations

import argparse
import logging

from synacor import adventure
from synacor import coins
from synacor import vm


logger = logging.getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='synacor',
        description='Play the Synacor Challenge!',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('adventure', help='Play the adventure game')

    vm_parser = subparsers.add_parser(
        'vm', help='Run the Synacor Challenge binary',
    )
    vm_parser.add_argument('filepath', help='Path to the binary file')

    subparsers.add_parser('coins', help='Solve the coins puzzle')

    dissasemble_parser = subparsers.add_parser(
        'disassemble', help='Disassemble the Synacor Challenge binary',
    )
    dissasemble_parser.add_argument('filepath', help='Path to the binary file')

    return parser


def main() -> int:
    parser = get_parser()
    args = parser.parse_args()

    command: str = args.command
    filepath: str

    if command == 'adventure':
        return adventure.main()
    elif command == 'vm':
        filepath = args.filepath
        return vm.main(filepath)
    elif command == 'disassemble':
        filepath = args.filepath
        vm.disassemble(filepath)
        return 0
    elif command == 'coins':
        return coins.main()

    logger.error(f'Unknown command {command}')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
