from __future__ import annotations

import argparse
import struct

from synacor.opcode import Opcode
from synacor.opcode import OPCODES


class VM:
    def __init__(self, filepath: str) -> None:
        self.memory = Memory(filepath)
        self.stack: list[int] = []
        self.registers = Registers()
        self.address = 0

    def run(self) -> None:
        while 1:
            opcode = self.get_op(self.read_memory(self.address))

            # print(f"'{opcode.name}'")

            opcode.execute()

    def read_memory(self, address: int) -> int:
        value = self.memory[address]
        return value

    def load(self, address: int) -> int:
        value = self.read_memory(address)

        if value < 32768:
            return value
        elif value < 32776:
            return self.registers[value]
        else:
            raise ValueError(f'Invalid value {value}')

    def get_op(self, opcode: int) -> Opcode:
        try:
            cls = OPCODES[opcode]
        except KeyError:
            raise ValueError(f'Invalid opcode {opcode}')

        return cls(self)

    def is_register(self, register: int) -> int:
        try:
            self.registers[register]
        except ValueError:
            return False
        return True

    def store(self, address: int, new_value: int) -> None:
        value = self.read_memory(address)

        if self.is_register(value):
            self.registers[value] = new_value
        else:
            self.memory[value] = new_value


class Memory:
    def __init__(self, filepath: str) -> None:
        self._memory: list[int] = []
        self.filepath: str = filepath

        self.load_file()

    def __getitem__(self, key: int) -> int:
        return self.memory[key]

    def __setitem__(self, key: int, value: int) -> None:
        self.memory[key] = value

    @property
    def memory(self) -> list[int]:
        if not self._memory:
            self.load_file()
        return self._memory

    def load_file(self) -> None:
        with open(self.filepath, mode='rb') as file:
            chunk = file.read(2)
            while chunk != b'':
                unpacked: tuple[int, ...] = struct.unpack('<H', chunk)
                self._memory.append(unpacked[0])
                chunk = file.read(2)


class Registers:
    def __init__(self) -> None:
        self._registers: dict[int, int] = {
            32768: 0,
            32769: 0,
            32770: 0,
            32771: 0,
            32772: 0,
            32773: 0,
            32774: 0,
            32775: 0,
        }

    def __getitem__(self, key: int) -> int:
        self.validate_register(key)
        return self._registers[key]

    def __setitem__(self, key: int, value: int) -> None:
        self.validate_register(key)
        self._registers[key] = value

    def validate_register(self, register: int) -> None:
        if register not in self._registers:
            raise ValueError(f'Invalid register {register}')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='synacor-vm',
        description='Run the Synacor Challenge binary',
    )
    parser.add_argument('filepath', help='Path to the binary file')
    return parser


def main() -> int:
    parser = get_parser()
    args = parser.parse_args()

    vm = VM(args.filepath)  # type: ignore[misc]

    try:
        vm.run()
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
