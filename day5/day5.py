import aoc


class Validator:
    def validate(self, string):
        return True


class FirstValidator(Validator):
    VOWELS = 'aeiou'
    FORBIDDEN = {'b': 'a', 'd': 'c', 'q': 'p', 'y': 'x'}

    def validate(self, string: str):
        vowels_count = 0
        has_double = False
        w = ''
        for x in string:
            if x in self.FORBIDDEN and self.FORBIDDEN[x] == w:
                return False
            has_double = has_double or x == w
            vowels_count += x in self.VOWELS
            w = x
        return has_double and vowels_count > 2


class SecondValidator(Validator):
    """
    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
    """

    def validate(self, string):
        pairs = {}
        w = ''
        v = ''
        pairs_found = False
        triplet_found = False

        for ix in range(len(string)):
            x = string[ix]

            triplet_found = triplet_found or v == x

            if not pairs_found:
                wx = w + x
                if wx in pairs:
                    pairs_found = pairs_found or ix - pairs[wx] > 1
                else:
                    pairs[wx] = ix

            if pairs_found and triplet_found:
                return True

            v = w
            w = x

        return False


class Part1(aoc.Part):
    def __init__(self, validator: Validator, expectations):
        self.validator = validator
        super().__init__(expectations)

    def solve(self, data) -> int:
        out = 0
        for line in data:
            out += self.validator.validate(line)
        return out


print(aoc.Day([
    Part1(FirstValidator(), [aoc.Exp(2)]),
    Part1(SecondValidator(), [aoc.Exp(2, suffix='2')])
]).solve())
