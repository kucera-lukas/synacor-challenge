from __future__ import annotations

import logging
import sys
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from synacor.vm import VM


logger = logging.getLogger(__name__)


class Opcode(ABC):
    opcode: int
    name: str
    argument_count: int

    def __init__(self, vm: VM) -> None:
        self.vm = vm

    @abstractmethod
    def execute(self) -> None:
        if self.vm.debug:
            self.log_debug()

    def log_debug(self) -> None:
        arguments = [
            f'{self.vm.read_memory(self.vm.address + i)}'
            f'={self.vm.load(self.vm.address + i)}'
            for i in range(1, self.argument_count + 1)
        ]
        message = (
            f'[{self.vm.address}]: Executing {self.name} with {arguments=}'
        )
        logger.info(message)


class HaltOpcode(Opcode):
    opcode = 0
    name = 'halt'
    argument_count = 0

    def execute(self) -> None:
        logger.info('halting VM')
        raise SystemExit(0)


class SetOpcode(Opcode):
    opcode = 1
    name = 'set'
    argument_count = 2

    def execute(self) -> None:
        super().execute()
        value_a = self.vm.load(self.vm.address + 2)
        self.vm.store(self.vm.address + 1, value_a)
        self.vm.address += 3


class PushOpcode(Opcode):
    opcode = 2
    name = 'push'
    argument_count = 1

    def execute(self) -> None:
        super().execute()
        value_a = self.vm.load(self.vm.address + 1)
        self.vm.stack.append(value_a)
        self.vm.address += 2


class PopOpcode(Opcode):
    opcode = 3
    name = 'pop'
    argument_count = 1

    def execute(self) -> None:
        super().execute()
        value = self.vm.stack.pop()
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 2


class EqOpcode(Opcode):
    opcode = 4
    name = 'eq'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = 1 if value_b == value_c else 0
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class GtOpcode(Opcode):
    opcode = 5
    name = 'gt'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = 1 if value_b > value_c else 0
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class JmpOpcode(Opcode):
    opcode = 6
    name = 'jmp'
    argument_count = 1

    def execute(self) -> None:
        super().execute()
        self.vm.address = self.vm.load(self.vm.address + 1)


class JtOpcode(Opcode):
    opcode = 7
    name = 'jt'
    argument_count = 2

    def execute(self) -> None:
        super().execute()
        value_a = self.vm.load(self.vm.address + 1)
        if value_a != 0:
            self.vm.address = self.vm.load(self.vm.address + 2)
        else:
            self.vm.address += 3


class JfOpcode(Opcode):
    opcode = 8
    name = 'jf'
    argument_count = 2

    def execute(self) -> None:
        super().execute()
        value_a = self.vm.load(self.vm.address + 1)
        if value_a == 0:
            self.vm.address = self.vm.load(self.vm.address + 2)
        else:
            self.vm.address += 3


class AddOpcode(Opcode):
    opcode = 9
    name = 'add'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = (value_b + value_c) % 32768
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class MultOpcode(Opcode):
    opcode = 10
    name = 'mult'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = (value_b * value_c) % 32768
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class ModOpcode(Opcode):
    opcode = 11
    name = 'mod'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = value_b % value_c
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class AndOpcode(Opcode):
    opcode = 12
    name = 'and'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = value_b & value_c
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class OrOpcode(Opcode):
    opcode = 13
    name = 'or'
    argument_count = 3

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = value_b | value_c
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class NotOpcode(Opcode):
    opcode = 14
    name = 'not'
    argument_count = 2

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        value = ~value_b & 0x7FFF
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 3


class RmemOpcode(Opcode):
    opcode = 15
    name = 'rmem'
    argument_count = 2

    def execute(self) -> None:
        super().execute()
        value_b = self.vm.load(self.vm.address + 2)
        memory = self.vm.load(value_b)
        self.vm.store(self.vm.address + 1, memory)
        self.vm.address += 3


class WmemOpcode(Opcode):
    opcode = 16
    name = 'wmem'
    argument_count = 2

    def execute(self) -> None:
        super().execute()
        value_a = self.vm.load(self.vm.address + 1)
        value_b = self.vm.load(self.vm.address + 2)
        self.vm.memory[value_a] = value_b
        self.vm.address += 3


class CallOpcode(Opcode):
    opcode = 17
    name = 'call'
    argument_count = 1

    def execute(self) -> None:
        super().execute()
        self.vm.stack.append(self.vm.address + 2)
        self.vm.address = self.vm.load(self.vm.address + 1)


class RetOpcode(Opcode):
    opcode = 18
    name = 'ret'
    argument_count = 0

    def execute(self) -> None:
        super().execute()
        try:
            top = self.vm.stack.pop()
        except IndexError:
            logger.warning('attempted to return from empty stack')
            raise SystemExit(0)

        self.vm.address = top


class OutOpcode(Opcode):
    opcode = 19
    name = 'out'
    argument_count = 1

    def execute(self) -> None:
        super().execute()
        value = self.vm.load(self.vm.address + 1)
        print(chr(value), end='')
        self.vm.address += 2


def use_breakpoint(vm: VM) -> None:
    logger.info('using breakpoint')
    # stdin might be piped, so we need to reopen /dev/tty
    sys.stdin = open('/dev/tty')
    breakpoint()


def set_debug(vm: VM) -> None:
    logger.info('setting debug to %s', not vm.debug)
    vm.debug = not vm.debug


def fix_teleporter(vm: VM) -> None:
    logger.info('fixing teleporter')

    # let program set register 0 to 6 to pass the check
    vm.memory[5507] = 6

    # remove calibration process call
    vm.memory[5511] = 21
    vm.memory[5512] = 21

    # set register 7 to the calculated energy level
    vm.registers[32775] = 25734


class InOpcode(Opcode):
    opcode = 20
    name = 'in'
    argument_count = 1

    custom_commands: dict[str, Callable[[VM], None]] = {
        'use breakpoint': use_breakpoint,
        'set debug': set_debug,
        'fix teleporter': fix_teleporter,
    }

    def execute(self) -> None:
        super().execute()

        if self.vm.buffer is None:
            try:
                command = input('Enter command: ')
            except EOFError:
                logger.info('exiting due to EOF')
                raise SystemExit(0)

            if command in self.custom_commands:
                logger.info('executing custom command: %r', command)
                self.custom_commands[command](self.vm)

                print('\n')
                InOpcode(self.vm).execute()
                return

            self.vm.buffer = iter(command)

        try:
            value = next(self.vm.buffer)
        except StopIteration:
            value = '\n'
            self.vm.buffer = None

        self.vm.store(self.vm.address + 1, ord(value))
        self.vm.address += 2


class NoopOpcode(Opcode):
    opcode = 21
    name = 'noop'
    argument_count = 0

    def execute(self) -> None:
        super().execute()
        self.vm.address += 1


OPCODES: dict[int, type[Opcode]] = {
    0: HaltOpcode,
    1: SetOpcode,
    2: PushOpcode,
    3: PopOpcode,
    4: EqOpcode,
    5: GtOpcode,
    6: JmpOpcode,
    7: JtOpcode,
    8: JfOpcode,
    9: AddOpcode,
    10: MultOpcode,
    11: ModOpcode,
    12: AndOpcode,
    13: OrOpcode,
    14: NotOpcode,
    15: RmemOpcode,
    16: WmemOpcode,
    17: CallOpcode,
    18: RetOpcode,
    19: OutOpcode,
    20: InOpcode,
    21: NoopOpcode,
}
