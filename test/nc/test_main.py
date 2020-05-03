from nc.__main__ import main
from unittest import mock, TestCase
from .print_mocker import print_mocker


@mock.patch('time.sleep', return_value=None)
class TestMain(TestCase):
    def main(self, expected, *args, color_count=0, **kwds):
        with print_mocker() as results:
            result = main(list(args), color_count=color_count, **kwds)
        actual = results[:8]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
        assert expected == actual
        return result

    def test_color(self, sleep):
        expected = ['Red: (255, 0, 0)', 'Cyan: (0, 255, 255)']
        self.main(expected, 'color', 'red', '(0, 0xff, 0xff)')

    def test_all(self, sleep):
        expected = [
            'Absolute Zero: (0, 72, 186)',
            'Acid green: (176, 191, 26)',
            'Aero: (124, 185, 232)',
            'Aero blue: (201, 255, 229)',
            'African violet: (178, 132, 190)',
            'Air superiority blue: (114, 160, 193)',
            'Alabaster: (237, 234, 224)',
            'Alice blue: (240, 248, 255)',
        ]
        self.main(expected, 'all')

    def test_all8(self, sleep):
        expected = [
            '\x1b[34;47m',
            'Absolute Zero: (0, 72, 186)\x1b[m\x1b[33;40m',
            'Acid green: (176, 191, 26)\x1b[m\x1b[36;40m',
            'Aero: (124, 185, 232)\x1b[m\x1b[37;40m',
            'Aero blue: (201, 255, 229)\x1b[m\x1b[37;40m',
            'African violet: (178, 132, 190)\x1b[m\x1b[36;40m',
            'Air superiority blue: (114, 160, 193)\x1b[m\x1b[37;40m',
            'Alabaster: (237, 234, 224)\x1b[m\x1b[37;40m',
        ]
        self.main(expected, 'all', color_count=8)

    maxDiff = 10000

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

    def test_errors(self, sleep):
        expected = [
            'Do not understand: rod groan',
            'No valid colors specified!',
        ]
        result = self.main(expected, 'color', 'rod', 'groan')
        assert result
