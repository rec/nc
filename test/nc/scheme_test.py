from nc import Colors
import unittest

HTML = Colors('html')
TERMINAL_256 = Colors('terminal256')
WIKIPEDIA = Colors('wikipedia')
X11 = Colors('x11')


class SchemeTest(unittest.TestCase):
    def test_terminal256(self):
        assert len(TERMINAL_256) == 202

        s256 = set(TERMINAL_256.items())
        assert len(s256.intersection(X11.items())) == 11
        assert len(s256.intersection(HTML.items())) == 13
        assert len(s256.intersection(WIKIPEDIA.items())) == 10
