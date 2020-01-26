import unittest
import io


class _ResultsPrinter(unittest.TestCase):
    def setUp(self):
        self.sio = io.StringIO()

    def print(self, *args, file=None, **kwds):
        print(*args, **kwds, file=self.sio)

    def results(self):
        return self.sio.getvalue().splitlines()
