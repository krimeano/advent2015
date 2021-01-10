import aoc
from enum import Enum

SIZE = 1000


class InstructionType(Enum):
    ON = 1
    OFF = -1
    TOGGLE = 0


class Instruction:
    type = None

    prefixes = {
        'turn on': InstructionType.ON,
        'turn off': InstructionType.OFF,
        'toggle': InstructionType.TOGGLE,
    }

    @staticmethod
    def get_instance(line):
        t, corners = Instruction.define_type_and_corners(line)

        if t == InstructionType.ON:
            return InstructionOn(corners)

        if t == InstructionType.OFF:
            return InstructionOff(corners)

        if t == InstructionType.TOGGLE:
            return InstructionToggle(corners)

    @staticmethod
    def define_type_and_corners(line):
        for p in Instruction.prefixes:
            if p in line:
                t = Instruction.prefixes[p]
                corners = [[int(c.strip()) for c in cc.split(',')] for cc in line[len(p):].split('through')]
                return t, corners
        else:
            raise Exception('instruction is not recognized: ' + line)

    def __init__(self, corners):
        """
        :param list[list[int]] corners:
        """
        self.corners = corners

    def apply(self, light: int) -> int:
        return light

    def __str__(self):
        return '{t} from {xy0} to {xy1}'.format(t=self.type, xy0=self.corners[0], xy1=self.corners[1])


class InstructionOff(Instruction):
    type = InstructionType.OFF

    def apply(self, light: int) -> int:
        return 0


class InstructionToggle(Instruction):
    type = InstructionType.TOGGLE

    def apply(self, light: int) -> int:
        return 1 - light


class InstructionOn(Instruction):
    type = InstructionType.ON

    def apply(self, light: int) -> int:
        return 1


class InstructionFixed(Instruction):
    type = None

    @staticmethod
    def get_instance(line):
        t, corners = Instruction.define_type_and_corners(line)

        if t == InstructionType.ON:
            return InstructionFixedOn(corners)

        if t == InstructionType.OFF:
            return InstructionFixedOff(corners)

        if t == InstructionType.TOGGLE:
            return InstructionFixedToggle(corners)


class InstructionFixedOff(InstructionOff):
    def apply(self, light: int) -> int:
        return light and light - 1


class InstructionFixedToggle(InstructionToggle):
    def apply(self, light: int) -> int:
        return light + 2


class InstructionFixedOn(InstructionOn):
    def apply(self, light: int) -> int:
        return light + 1


class Part1(aoc.Part):
    lights = []

    def solve(self, data) -> int:
        self.init_lights()
        for line in data:
            self.apply_instruction(self.get_instruction(line))
        return int(self)

    def get_instruction(self, line):
        return Instruction.get_instance(line)

    def init_lights(self):
        self.lights = [[0 for y in range(SIZE)] for x in range(SIZE)]

    def apply_instruction(self, instruction: Instruction):
        [x0, y0], [x1, y1] = instruction.corners
        for ix in range(x0, x1 + 1):
            for jy in range(y0, y1 + 1):
                self.lights[ix][jy] = instruction.apply(self.lights[ix][jy])

    def __str__(self):
        return '\n'.join([' '.join([str(y) for y in x]) for x in self.lights])

    def __int__(self):
        return sum([sum(x) for x in self.lights])


class Part2(Part1):
    def get_instruction(self, line):
        return InstructionFixed.get_instance(line)


print(aoc.Day([
    Part1([]),
    Part2([])
]).solve())
