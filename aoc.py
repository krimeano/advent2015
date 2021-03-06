import os


class Exp:
    def __init__(self, val: int, *args, suffix='', data=None):
        """
        :param int val:
        :param str suffix:
        :param list[str|int] data:
        :param args:
        """
        self.val = val
        self.args = args
        self.suffix = suffix
        self.data = data


class InputReader:
    prefix = 'input'

    def __init__(self, suffix=''):
        self.path = '{p}{s}'.format(p=self.prefix, s=suffix)
        if suffix and not os.path.exists(self.path):
            self.path = '{p}'.format(p=self.prefix)

    def read(self):
        with open(self.path) as f:
            return [x.strip() for x in f.readlines()]


class ExampleReader(InputReader):
    prefix = 'example'

    def __init__(self, exp: Exp):
        super().__init__(exp.suffix)


class Part:
    def __init__(self, expectations):
        """
        :param list(Exp) expectations:
        """
        self.expectations = expectations
        self.data = []
        pass

    def run(self):
        for e in self.expectations:
            data = e.data or ExampleReader(e).read()
            v = self.solve(data, *e.args)
            if v != e.val:
                args_txt = e.args and (' AND ARGUMENTS %s' % e.args) or ''
                print('EXPECTED', e.val, 'RECEIVED', v, 'WITH DATA', data, args_txt)
                return False

        return self.solve(InputReader().read(), )

    def solve(self, data, *args) -> int:
        """
        :param list[str] data:
        :param list args:
        :return:
        """
        return 0


class Day:
    def __init__(self, parts):
        """
        :param list(Part) parts:
        :return:
        """
        self.parts = parts
        pass

    def solve(self):
        return tuple(x.run() for x in self.parts)
