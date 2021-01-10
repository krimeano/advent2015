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
    sorted_wires = []

    @staticmethod
    def get_wire(line):
        if '->' not in line:
            return Wire.make_wire(line)

        cmd = line.split(' -> ')
        return Wire.make_wire(cmd.pop()).connect(cmd.pop().split(' '))

    @staticmethod
    def make_wire(name: str):
        if re.match(r'^\d+$', name):
            return Wire(name, int(name))
        if name not in Wire.wires:
            Wire.wires[name] = Wire(name)
        return Wire.wires[name]

    @staticmethod
    def reset():
        Wire.wires = {}
        Wire.sorted_wires = []

    @staticmethod
    def sort_wires():
        all_wires = [Wire.wires[ix] for ix in Wire.wires]
        Wire.sorted_wires = []

        while all_wires:
            all_wires = sorted(all_wires, key=lambda x: x.count_in)
            wire = all_wires.pop(0)
            if wire.count_in != 0:
                print(wire)
                print([x.name for x in Wire.sorted_wires])
                print([x.name + str(x.count_in) for x in all_wires])
                raise Exception('non zero count in = %s' % wire.count_in)

            for x in wire.next:
                x.count_in -= 1

            Wire.sorted_wires.append(wire)

        return Wire.sorted_wires

    def __init__(self, name: str, value=0):
        self.name = name
        self.value = value
        self.prev = []
        self.next = []
        self.operator = Operator.SIGNAL
        self.count_in = 0

    def __str__(self):
        s = short[self.operator]
        pp = [x.name for x in self.prev]
        qq = [str(x.value) for x in self.prev]
        if len(pp) == 1:
            pp.insert(0, '')
            qq.insert(0, '')
        return '{n} ({p}) = ({q}) = {v}'.format(n=self.name, p=s.join(pp), q=s.join(qq), v=self.value)

    def __int__(self):
        return self.value

    def connect(self, params):
        if len(params) == 1:
            self.operator = Operator.SIGNAL
        else:
            self.operator = Operator(params.pop(-2))

        while params:
            prev = Wire.get_wire(params.pop(0))
            self.prev.append(prev)

            prev.next.append(self)
            if str(prev.value) != prev.name:
                self.count_in += 1

        return self

    def resolve(self):
        x = self.prev[0].value

        if self.operator == Operator.SIGNAL:
            self.value = x
            return self

        if self.operator == Operator.NOT:
            self.value = ONE ^ x
            return self

        y = len(self.prev) > 1 and self.prev[1].value or 0

        if self.operator == Operator.AND:
            self.value = x & y
        elif self.operator == Operator.OR:
            self.value = x | y
        elif self.operator == Operator.LSHIFT:
            self.value = (x << y) & ONE
        elif self.operator == Operator.RSHIFT:
            self.value = (x >> y) & ONE

        return self


class Part1(aoc.Part):
    def solve(self, data, measure_at='a') -> int:
        Wire.reset()
        for x in data:
            Wire.get_wire(x)

        for x in Wire.sort_wires():
            x.resolve()

        return measure_at in Wire.wires and int(Wire.wires[measure_at]) or 0


class Part2(aoc.Part):

    def solve(self, data, *args) -> int:
        a = Wire.get_wire('a')
        b = Wire.get_wire('b')
        print(b)
        b.prev = [Wire.get_wire(str(int(a)))]
        print(b)
        for x in Wire.sorted_wires:
            x.resolve()
        return int(a)


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
    Part2([])
]).solve())
