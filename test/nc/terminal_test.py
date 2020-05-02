from . import results_printer
from nc import terminal
import nc


class TerminalTest(results_printer._ResultsPrinter):
    def test_context256(self):
        context = terminal.Context(256)
        assert context

    def test_demo16(self):
        with self.print_until(10):
            terminal.demo(print=self.print, sleep=None, count=16)

        actual = self.results()
        expected = [
            '\x1b[30;40m',
            'Black, Black\x1b[m\x1b[31;40m',
            'Red, Black\x1b[m\x1b[32;40m',
            'Green, Black\x1b[m\x1b[33;40m',
            'Yellow, Black\x1b[m\x1b[34;40m',
            'Blue, Black\x1b[m\x1b[35;40m',
            'Magenta, Black\x1b[m\x1b[36;40m',
            'Cyan, Black\x1b[m\x1b[37;40m',
            'White, Black\x1b[m\x1b[90;40m',
            'Bright black, Black\x1b[m\x1b[91;40m',
        ]
        self.assertEqual(actual, expected)

    maxDiff = 10000

    def test_demo256(self):
        with self.print_until(512):
            terminal.demo(print=self.print, sleep=None, count=256)

        actual = self.results()[:8]
        expected = [
            '\x1b[38;5;16;48;5;16m',
            'Black, Black\x1b[m\x1b[38;5;1;48;5;16m',
            'Red, Black\x1b[m\x1b[38;5;2;48;5;16m',
            'Green, Black\x1b[m\x1b[38;5;3;48;5;16m',
            'Yellow, Black\x1b[m\x1b[38;5;4;48;5;16m',
            'Blue, Black\x1b[m\x1b[38;5;5;48;5;16m',
            'Magenta, Black\x1b[m\x1b[38;5;6;48;5;16m',
            'Cyan, Black\x1b[m\x1b[38;5;7;48;5;16m',
        ]
        self.assertEqual(actual, expected)

        actual = self.results()[252:260]
        expected = [
            'Snow 3 B, Black\x1b[m\x1b[38;5;252;48;5;16m',
            'Light gray, Black\x1b[m\x1b[38;5;253;48;5;16m',
            'Gainsboro, Black\x1b[m\x1b[38;5;254;48;5;16m',
            'Snow 2, Black\x1b[m\x1b[38;5;255;48;5;16m',
            'White smoke, Black\x1b[m\x1b[38;5;16;48;5;1m',
            'Black, Red\x1b[m\x1b[38;5;1;48;5;1m',
            'Red, Red\x1b[m\x1b[38;5;2;48;5;1m',
            'Green, Red\x1b[m\x1b[38;5;3;48;5;1m',
        ]
        self.assertEqual(actual, expected)

    def test_color_context(self):
        context = terminal.Context(count=16)
        pr = self.print
        with context(print=pr):
            pr('one')
        with context(fg=nc.red, print=pr):
            pr('two')
        with context(bg=nc.yellow, print=pr):
            pr('three')
        with context(fg=nc.cyan, bg=nc.green, print=pr):
            pr('four')

        expected = [
            'one',
            '\x1b[91mtwo',
            '\x1b[m\x1b[103mthree',
            '\x1b[m\x1b[96;102mfour',
            '\x1b[m',
        ]
        self.assertEqual(self.results(), expected)

    def test_color_context_256(self):
        context = terminal.Context(count=256)
        assert context.count == 256
        assert context.colors
