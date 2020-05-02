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
            '',
            'None, None\x1b[30m',
            'Black, None\x1b[m\x1b[31m',
            'Red, None\x1b[m\x1b[32m',
            'Green, None\x1b[m\x1b[33m',
            'Yellow, None\x1b[m\x1b[34m',
            'Blue, None\x1b[m\x1b[35m',
            'Magenta, None\x1b[m\x1b[36m',
            'Cyan, None\x1b[m\x1b[37m',
            'White, None\x1b[m\x1b[90m',
        ]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
        self.assertEqual(actual, expected)

    maxDiff = 10000

    def test_demo256(self):
        with self.print_until(512):
            terminal.demo(print=self.print, sleep=None, count=256)

        actual = self.results()[:8]
        expected = [
            '',
            'None, None\x1b[38;5;16m',
            'Black, None\x1b[m\x1b[38;5;1m',
            'Red, None\x1b[m\x1b[38;5;2m',
            'Green, None\x1b[m\x1b[38;5;3m',
            'Yellow, None\x1b[m\x1b[38;5;4m',
            'Blue, None\x1b[m\x1b[38;5;5m',
            'Magenta, None\x1b[m\x1b[38;5;6m',
        ]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
        self.assertEqual(actual, expected)

        actual = self.results()[252:260]
        expected = [
            'Silver, None\x1b[m\x1b[38;5;251m',
            'Snow 3 B, None\x1b[m\x1b[38;5;252m',
            'Light gray, None\x1b[m\x1b[38;5;253m',
            'Gainsboro, None\x1b[m\x1b[38;5;254m',
            'Snow 2, None\x1b[m\x1b[38;5;255m',
            'White smoke, None\x1b[m\x1b[48;5;16m',
            'None, Black\x1b[m\x1b[38;5;16;48;5;16m',
            'Black, Black\x1b[m\x1b[38;5;1;48;5;16m',
        ]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
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
