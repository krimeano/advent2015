from aoc import Part, Day, Exp


class Part1(Part):
    def solve(self, data) -> int:
        out = 0
        for box in data:
            edges = sorted(int(edge) for edge in box.split('x'))
            d = len(edges)
            s = sum((ix and 2 or 3) * edges[ix] * edges[(ix + 1) % d] for ix in range(d))
            out += s
        return out


class Part2(Part):
    def solve(self, data) -> int:
        out = 0
        for box in data:
            x, y, z = sorted(int(edge) for edge in box.split('x'))
            r = 2 * (x + y) + x * y * z
            out += r
        return out


if __name__ == '__main__':
    day = Day([
        Part1([Exp(43 + 58)]),
        Part2([Exp(34 + 14)])
    ])
    print(day.solve())
