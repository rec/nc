from nc import terminal
from unittest import mock, TestCase
import functools
import nc


@mock.patch('time.sleep', return_value=None)
class TerminalTest(TestCase):
    def test_context256(self, sleep):
        context = terminal.Context(256)
        assert context

    def test_color_context(self, sleep):
        actual = []

        def pr(*args, **kwds):
            actual.extend(args)

        context = functools.partial(terminal.context, count=16, print=pr)

        with context():
            pr('one')
        with context(fg=nc.red):
            pr('two')
        with context(bg=nc.yellow, print=pr, count=16):
            pr('three')
        with context(fg=nc.cyan, bg=nc.green):
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
