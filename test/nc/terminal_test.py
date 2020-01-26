from nc import terminal
import nc
import io
import unittest


class TestTerminal(unittest.TestCase):
    def test_demo(self):
        results, printer = _results_printer()
        terminal.demo(print=printer, sleep=lambda x: None)
        lines = results()
        expected = [
            '\x1b[30;40m',
            'Black, Black\x1b[0;0m\x1b[31;40m',
            'Red, Black\x1b[0;0m\x1b[32;40m',
            'Green, Black\x1b[0;0m\x1b[33;40m',
            'Yellow, Black\x1b[0;0m\x1b[34;40m',
            'Blue, Black\x1b[0;0m\x1b[35;40m',
            'Magenta, Black\x1b[0;0m\x1b[36;40m',
            'Cyan, Black\x1b[0;0m\x1b[37;40m',
            'White, Black\x1b[0;0m\x1b[90;40m',
            'Bright black, Black\x1b[0;0m\x1b[91;40m',
        ]
        self.assertEqual(lines[:10], expected)

    def test_color_context(self):
        results, printer = _results_printer()

        with terminal.color_context(print=printer):
            printer('one')
        with terminal.color_context(fg=nc.red, print=printer):
            printer('two')
        with terminal.color_context(bg=nc.yellow, print=printer):
            printer('three')
        with terminal.color_context(fg=nc.cyan, bg=nc.green, print=printer):
            printer('four')

        expected = [
            'one',
            '\x1b[91;0mtwo',
            '\x1b[0;0m\x1b[0;103mthree',
            '\x1b[0;0m\x1b[96;102mfour',
            '\x1b[0;0m',
        ]
        self.assertEqual(results(), expected)


def _results_printer():
    sio = io.StringIO()

    def printer(*args, **kwds):
        print(*args, **kwds, file=sio)

    def results():
        return sio.getvalue().splitlines()

    return results, printer
