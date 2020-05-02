from nc.__main__ import main
from . import results_printer


class TestMain(results_printer._ResultsPrinter):
    def main(self, expected, *args, color_count=0, **kwds):
        result = main(args, self.print, color_count=color_count, **kwds)
        assert expected == self.results()[:8]
        return result

    def test_color(self):
        expected = ['Red: (255, 0, 0)', 'Cyan: (0, 255, 255)']
        self.main(expected, 'color', 'red', '(0, 0xff, 0xff)')

    def test_all(self):
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

    def test_all8(self):
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

    def test_terminal(self):
        expected = [
            '\x1b[30;40m',
            'Black, Black\x1b[m\x1b[31;40m',
            'Red, Black\x1b[m\x1b[32;40m',
            'Green, Black\x1b[m\x1b[33;40m',
            'Yellow, Black\x1b[m\x1b[34;40m',
            'Blue, Black\x1b[m\x1b[35;40m',
            'Magenta, Black\x1b[m\x1b[36;40m',
            'Cyan, Black\x1b[m\x1b[37;40m',
        ]
        self.main(expected, 'terminal', '-s0', '-c16')

    def test_errors(self):
        expected = [
            'Do not understand: rod groan',
            'No valid colors specified!',
        ]
        result = self.main(expected, 'color', 'rod', 'groan')
        assert result
