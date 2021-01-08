from aoc import Part, Day, Exp


class Part1(Part):
    shifts = {
        '(': 1,
        ')': -1
    }

    def solve(self, data) -> int:
        out = sum(self.shifts[x] for x in data[0])
        return out


class Part2(Part1):
    basement = -1
    ground_floor = 0

    def solve(self, data) -> int:
        floor = self.ground_floor
        ix = 0
        for x in data[0]:
            ix += 1
            floor += self.shifts[x]
            if floor == self.basement:
                return ix
        return -1


if __name__ == '__main__':
    day = Day([
        Part1([
            Exp(0, data=['(())']),
            Exp(0, data=['()()']),
            Exp(3, data=['(((']),
            Exp(3, data=['(()(()(']),
            Exp(-1, data=['())']),
            Exp(-1, data=['))(']),
            Exp(-3, data=[')))']),
            Exp(-3, data=[')())())']),
        ]),
        Part2([
            Exp(1, data=[')']),
            Exp(5, data=['()())'])
        ])
    ])
    print(day.solve())
