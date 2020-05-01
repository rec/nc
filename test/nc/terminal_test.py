from . import results_printer
from nc import terminal
import nc


class TerminalTest(results_printer._ResultsPrinter):
    def test_demo(self):
        terminal.demo(print=self.print, sleep=None, count=16)
        lines = self.results()
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
        self.assertEqual(lines[:10], expected)

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
