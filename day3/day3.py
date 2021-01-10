from aoc import Day, Exp, Part


class Part1(Part):
    shifts = {
        '>': [1, 0],
        '^': [0, 1],
        '<': [-1, 0],
        'v': [0, -1]
    }

    def solve(self, data, *args) -> int:
        f = (0, 0)
        houses = {f}
        for x in data[0]:
            h = tuple(f[ix] + self.shifts[x][ix] for ix in range(len(f)))
            if h not in houses:
                houses.add(h)
            f = h
        return len(houses)


class Part2(Part1):
    def solve(self, data, *args) -> int:
        f = g = (0, 0)
        houses = {f}
        for x in data[0]:
            h = tuple(f[ix] + self.shifts[x][ix] for ix in range(len(f)))
            if h not in houses:
                houses.add(h)
            f = g
            g = h
        return len(houses)


if __name__ == '__main__':
    day = Day([
        Part1([
            Exp(2, data=['>']),
            Exp(4, data=['^>v<']),
            Exp(2, data=['^v^v^v^v^v']),
        ]),
        Part2([
            Exp(3, data=['^v']),
            Exp(3, data=['^>v<']),
            Exp(11, data=['^v^v^v^v^v']),
        ]),
    ])

    print(day.solve())
