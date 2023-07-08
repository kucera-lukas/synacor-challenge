from __future__ import annotations

import argparse

from synacor import adventure
from synacor import coins
from synacor import vm


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

    return parser


def main() -> int:
    parser = get_parser()
    args = parser.parse_args()

    command: str = args.command

    if command == 'adventure':
        return adventure.main()
    elif command == 'vm':
        filepath: str = args.filepath
        return vm.main(filepath)
    elif command == 'coins':
        return coins.main()

    print(f'Unknown command {command}')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
