from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from synacor.vm import VM


class Opcode(ABC):
    opcode: int
    name: str

    def __init__(self, vm: VM) -> None:
        self.vm = vm

    @abstractmethod
    def execute(self) -> None:
        pass


class HaltOpcode(Opcode):
    opcode = 0
    name = 'halt'

    def execute(self) -> None:
        raise SystemExit(0)


class SetOpcode(Opcode):
    opcode = 1
    name = 'set'

    def execute(self) -> None:
        value_a = self.vm.load(self.vm.address + 2)
        self.vm.store(self.vm.address + 1, value_a)
        self.vm.address += 3


class PushOpcode(Opcode):
    opcode = 2
    name = 'push'

    def execute(self) -> None:
        value_a = self.vm.load(self.vm.address + 1)
        self.vm.stack.append(value_a)
        self.vm.address += 2


class PopOpcode(Opcode):
    opcode = 3
    name = 'pop'

    def execute(self) -> None:
        value = self.vm.stack.pop()
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 2


class EqOpcode(Opcode):
    opcode = 4
    name = 'eq'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = 1 if value_b == value_c else 0
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class GtOpcode(Opcode):
    opcode = 5
    name = 'gt'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = 1 if value_b > value_c else 0
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class JmpOpcode(Opcode):
    opcode = 6
    name = 'jmp'

    def execute(self) -> None:
        self.vm.address = self.vm.load(self.vm.address + 1)


class JtOpcode(Opcode):
    opcode = 7
    name = 'jt'

    def execute(self) -> None:
        value_a = self.vm.load(self.vm.address + 1)
        if value_a != 0:
            self.vm.address = self.vm.load(self.vm.address + 2)
        else:
            self.vm.address += 3


class JfOpcode(Opcode):
    opcode = 8
    name = 'jf'

    def execute(self) -> None:
        value_a = self.vm.load(self.vm.address + 1)
        if value_a == 0:
            self.vm.address = self.vm.load(self.vm.address + 2)
        else:
            self.vm.address += 3


class AddOpcode(Opcode):
    opcode = 9
    name = 'add'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = (value_b + value_c) % 32768
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class MultOpcode(Opcode):
    opcode = 10
    name = 'mult'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = (value_b * value_c) % 32768
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class ModOpcode(Opcode):
    opcode = 11
    name = 'mod'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = value_b % value_c
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class AndOpcode(Opcode):
    opcode = 12
    name = 'and'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = value_b & value_c
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class OrOpcode(Opcode):
    opcode = 13
    name = 'or'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value_c = self.vm.load(self.vm.address + 3)
        value = value_b | value_c
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 4


class NotOpcode(Opcode):
    opcode = 14
    name = 'not'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        value = ~value_b & 0x7FFF
        self.vm.store(self.vm.address + 1, value)
        self.vm.address += 3


class RmemOpcode(Opcode):
    opcode = 15
    name = 'rmem'

    def execute(self) -> None:
        value_b = self.vm.load(self.vm.address + 2)
        memory = self.vm.load(value_b)
        self.vm.store(self.vm.address + 1, memory)
        self.vm.address += 3


class WmemOpcode(Opcode):
    opcode = 16
    name = 'wmem'

    def execute(self) -> None:
        value_a = self.vm.load(self.vm.address + 1)
        value_b = self.vm.load(self.vm.address + 2)
        self.vm.memory[value_a] = value_b
        self.vm.address += 3


class CallOpcode(Opcode):
    opcode = 17
    name = 'call'

    def execute(self) -> None:
        self.vm.stack.append(self.vm.address + 2)
        self.vm.address = self.vm.load(self.vm.address + 1)


class RetOpcode(Opcode):
    opcode = 18
    name = 'ret'

    def execute(self) -> None:
        try:
            top = self.vm.stack.pop()
        except IndexError:
            raise SystemExit(0)

        self.vm.address = top


class OutOpcode(Opcode):
    opcode = 19
    name = 'out'

    def execute(self) -> None:
        value = self.vm.load(self.vm.address + 1)
        print(chr(value), end='')
        self.vm.address += 2


class InOpcode(Opcode):
    opcode = 20
    name = 'in'

    def execute(self) -> None:
        value = input()
        self.vm.store(self.vm.address + 1, ord(value[0]))
        self.vm.address += 2


class NoopOpcode(Opcode):
    opcode = 21
    name = 'noop'

    def execute(self) -> None:
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
    # 20: InOpcode,
    21: NoopOpcode,
}
