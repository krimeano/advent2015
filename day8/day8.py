import aoc


class Parser:
    QUOTE = '"'
    BACKSLASH = '\\'
    HEX = 'x'
    ESCAPED = (BACKSLASH, QUOTE, HEX)
    total = 0
    meaningful = 0
    is_started = False
    is_finished = False
    is_escaped = False
    is_hex = False
    chunk = ''

    def __init__(self, string):
        self.string = string

    def __int__(self):
        return self.total - self.meaningful

    def process(self):
        self.total = len(self.string)
        for x in self.string:
            self.process_char(x)
        return self

    def process_char(self, char):
        if self.is_escaped:
            return self.process_escaped(char)

        if char == self.BACKSLASH:
            self.is_escaped = True
            return

        if char == self.QUOTE:
            if self.is_started:
                self.is_finished = True
                return
            self.is_started = True
            return

        self.meaningful += 1

    def process_escaped(self, char):
        if self.is_hex:
            return self.process_hex(char)

        if char == self.HEX:
            self.is_hex = True
            return

        self.is_escaped = False

        if char in self.ESCAPED:
            self.meaningful += 1
        else:
            self.meaningful += 2
            raise Exception('not escaped', char, 'at', self.string)

    def process_hex(self, char):

        if char not in '1234567890abcdefABCDEF':
            raise Exception('not hex', char, 'at', self.string)

        if len(self.chunk):
            self.chunk = ''
            self.is_hex = False
            self.is_escaped = False
            self.meaningful += 1
            return

        self.chunk += char


class Part1(aoc.Part):
    def solve(self, data, *args) -> int:
        out = 0
        for line in data:
            out += int(Parser(line).process())
        return out


class Encoder(Parser):
    def process(self):
        self.meaningful = len(self.string)
        self.total = 2
        for x in self.string:
            self.total += x in (self.BACKSLASH, self.QUOTE) and 2 or 1
        return self


class Part2(aoc.Part):
    def solve(self, data, *args) -> int:
        out = 0
        for line in data:
            out += int(Encoder(line).process())
        return out


print(aoc.Day([
    Part1([
        aoc.Exp(12)
    ]),
    Part2([
        aoc.Exp(19)
    ])
]).solve())
