from nc import Colors
import unittest

HTML = Colors('html')
TERMINAL_8 = Colors('terminal8')
TERMINAL_16 = Colors('terminal16')
TERMINAL_256 = Colors('terminal256')
WIKIPEDIA = Colors('wikipedia')
X11 = Colors('x11')


class PaletteTest(unittest.TestCase):
    def test_terminal256(self):
        assert len(TERMINAL_256) == 256

        s256 = set(TERMINAL_256.items())
        assert len(s256.intersection(X11.items())) == 4
        assert len(s256.intersection(HTML.items())) == 3
        assert len(s256.intersection(WIKIPEDIA.items())) == 2
        assert len(s256.intersection(TERMINAL_8.items())) == 1
        assert len(s256.intersection(TERMINAL_16.items())) == 1

    def test_terminal16(self):
        assert len(TERMINAL_16) == 16

        s16 = set(TERMINAL_16.items())
        assert len(s16.intersection(X11.items())) == 1
        assert len(s16.intersection(HTML.items())) == 1
        assert len(s16.intersection(WIKIPEDIA.items())) == 1
        assert len(s16.intersection(TERMINAL_8.items())) == 1
        assert len(s16.intersection(TERMINAL_256.items())) == 1
