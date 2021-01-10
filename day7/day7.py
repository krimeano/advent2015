import aoc
from enum import Enum
import re

ONE = 2 ** 16 - 1


class Operator(Enum):
    SIGNAL = 'SIGNAL'
    OR = 'OR'
    AND = 'AND'
    LSHIFT = 'LSHIFT'
    RSHIFT = 'RSHIFT'
    NOT = 'NOT'


short = {
    Operator.SIGNAL: '=',
    Operator.OR: '|',
    Operator.AND: '&',
    Operator.LSHIFT: '<',
    Operator.RSHIFT: '>',
    Operator.NOT: '!',
}


class Wire:
    wires = {}

    @staticmethod
    def get_wire(line):
        cmd = line.split(' -> ')
        x = cmd.pop(-1)
        if x not in Wire.wires:
            Wire.wires[x] = Wire(x)

        wire = Wire.wires[x]

        if len(cmd):
            wire.connect(cmd[0].split(' '))

        return wire

    @staticmethod
    def reset():
        Wire.wires = {}

    def __init__(self, name: str):
        self.name = name
        self.value = 0
        self.arg = 0
        self.prev = []
        self.next = []
        self.operator = Operator.SIGNAL
        self.count_in = 0

    def __str__(self):
        s = short[self.operator]
        pp = [x.name for x in self.prev] + (self.arg and [str(self.arg)] or [])
        qq = [str(x.value) for x in self.prev] + (self.arg and [str(self.arg)] or [])
        if len(pp) == 1:
            pp.insert(0, '')
            qq.insert(0, '')
        return '{n}({p}) = ({q}) = {v}'.format(n=self.name, p=s.join(pp), q=s.join(qq), v=self.value)

    def __int__(self):
        return self.value

    def connect(self, cmd):
        if len(cmd) == 1:
            self.operator = Operator.SIGNAL
            if re.match(r'^\d+$', cmd[0]):
                self.arg = int(cmd[0])
                return self
        else:
            self.operator = Operator(cmd.pop(-2))

        if self.operator in [Operator.RSHIFT, Operator.LSHIFT]:
            self.arg = int(cmd.pop(-1))
        while cmd:
            prev = Wire.get_wire(cmd.pop(0))
            self.prev.append(prev)
            self.count_in += 1
            prev.next.append(self)

        return self

    def resolve(self):
        if self.operator == Operator.SIGNAL:
            self.value = self.arg
            return self

        x = self.prev[0].value
        y = len(self.prev) > 1 and self.prev[1].value or self.arg

        if self.operator == Operator.AND:
            self.value = x & y
        elif self.operator == Operator.OR:
            self.value = x | y
        elif self.operator == Operator.LSHIFT:
            self.value = (x << y) & ONE
        elif self.operator == Operator.RSHIFT:
            self.value = (x >> y) & ONE
        elif self.operator == Operator.NOT:
            self.value = ONE ^ x
        return self


class Part1(aoc.Part):
    def solve(self, data, measure_at='a') -> int:
        print()
        Wire.reset()
        all_wires = [Wire.get_wire(x) for x in data]
        sorted_wires = []

        while all_wires:
            all_wires = sorted(all_wires, key=lambda x: x.count_in)
            wire = all_wires.pop(0)
            if wire.count_in != 0:
                print(wire)
                print([x.name for x in sorted_wires])
                print([x.name + str(x.count_in) for x in all_wires])
                raise Exception('non zero count in = %s' % wire.count_in)
            for x in wire.next:
                x.count_in -= 1
            sorted_wires.append(wire)

        for x in sorted_wires:
            print(x.resolve(), 'count_in=', x.count_in)

        return measure_at in Wire.wires and int(Wire.wires[measure_at]) or 0


print(ONE)

print(aoc.Day([
    Part1([
        aoc.Exp(123, 'x'),
        aoc.Exp(456, 'y'),
        aoc.Exp(72, 'd'),
        aoc.Exp(507, 'e'),
        aoc.Exp(492, 'f'),
        aoc.Exp(114, 'g'),
        aoc.Exp(65412, 'h'),
        aoc.Exp(65079, 'i'),
    ]),
]).solve())
