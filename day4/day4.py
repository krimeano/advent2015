import aoc
import hashlib


class Part1(aoc.Part):
    zeroes = 5

    def solve(self, data, *args) -> int:
        ix = 0
        print()
        while ix < 10 ** (self.zeroes + 2):
            ix += 1
            s = data[0] + str(ix)
            m = hashlib.md5(s.encode('utf-8')).hexdigest()
            if m[:self.zeroes - 1] == '0' * (self.zeroes - 1) or not ix % 10 ** self.zeroes:
                print(ix, s, m)
            if m[:self.zeroes] == '0' * self.zeroes:
                return ix
        return 0


class Part2(Part1):
    zeroes = 6


print(aoc.Day([
    Part1([
        aoc.Exp(609043, data=['abcdef']),
        aoc.Exp(1048970, data=['pqrstuv']),
    ]),
    Part2([])
]).solve())
