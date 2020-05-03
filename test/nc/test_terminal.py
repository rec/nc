from .print_mocker import print_mocker
from nc import demo
from nc import terminal
from unittest import mock, TestCase
import nc


@mock.patch('time.sleep', return_value=None)
class TerminalTest(TestCase):
    def test_context256(self, sleep):
        context = terminal.Context(256)
        assert context

    def test_demo16(self, sleep):
        with print_mocker() as actual:
            demo.demo(16, reverse=False, long=True, steps=9)
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
            'White, None\x1b[m',
        ]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
        self.assertEqual(expected, actual)

    maxDiff = 10000

    def test_demo256(self, sleep):
        with print_mocker() as results:
            demo.demo(256, reverse=False, long=True, steps=512)
        actual = results[:8]

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
        self.assertEqual(expected, actual)

        actual = results[252:260]
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
        self.assertEqual(expected, actual)

    def test_color_context(self, sleep):
        context = terminal.Context(16)
        actual = []

        def pr(*args, **kwds):
            actual.extend(args)

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
        self.assertEqual(''.join(expected), ''.join(actual))

    def test_color_context_256(self, sleep):
        context = terminal.Context(256)
        assert len(context) == 256
