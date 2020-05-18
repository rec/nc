from .print_mocker import print_mocker
from nc.__main__ import main
from unittest import mock, TestCase


class TestMain(TestCase):
    def _run(self, *args, **kwds):
        with print_mocker() as results:
            return main(list(args), **kwds), results

    def main(self, expected, *args, color_count=0, **kwds):
        returncode, results = self._run(*args, color_count=color_count, **kwds)
        actual = results[:8]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
        assert actual == expected
        return returncode

    def test_color(self):
        expected = ['Red: (255, 0, 0)', 'Cyan: (0, 255, 255)']
        self.main(expected, 'color', 'red', '(0, 0xff, 0xff)', color_count=0)

    def test_all_unique(self):
        _, results = self._run('all')
        assert len(results) > 1300
        assert len(results) == len(set(results))

    def test_dupes_in_all(self):
        _, results = self._run('all')
        assert len(results) > 200

    @mock.patch('time.sleep', return_value=None)
    def test_all8(self, sleep):
        expected = [
            '\x1b[34;47mAbsolute Zero: (0, 72, 186)\x1b[m\x1b[33;40m',
            'Acid green: (176, 191, 26)\x1b[m\x1b[36;40m',
            'Aero: (124, 185, 232)\x1b[m\x1b[37;40m',
            'Aero blue: (201, 255, 229)\x1b[m\x1b[37;40m',
            'African violet: (178, 132, 190)\x1b[m\x1b[36;40m',
            'Air superiority blue: (114, 160, 193)\x1b[m\x1b[37;40m',
            'Alabaster: (237, 234, 224)\x1b[m\x1b[37;40m',
            'Alice blue: (240, 248, 255)\x1b[m\x1b[31;47m',
        ]
        self.main(expected, color_count=8)

    maxDiff = 10000

    @mock.patch('time.sleep', return_value=None)
    def test_terminal(self, sleep):
        expected = [
            '',
            'None, None\x1b[30m',
            'Black, None\x1b[m\x1b[31m',
            'Red, None\x1b[m\x1b[32m',
            'Green, None\x1b[m\x1b[33m',
            'Yellow, None\x1b[m\x1b[34m',
            'Blue, None\x1b[m\x1b[35m',
            'Magenta, None\x1b[m\x1b[36m',
        ]
        self.main(expected, 'terminal', '-c16', '-l')

    def test_errors(self):
        expected = [
            'Do not understand: rod groan',
            'No valid colors specified!',
        ]
        result = self.main(expected, 'color', 'rod', 'groan')
        assert result
