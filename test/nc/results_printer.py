import unittest
import io


class _ResultsPrinter(unittest.TestCase):
    def setUp(self):
        self.sio = io.StringIO()
        self.count = self.max_count = 0

    def print(self, *args, file=None, **kwds):
        print(*args, **kwds, file=self.sio)

        self.count += 'end' not in kwds
        if self.max_count and (self.count >= self.max_count):
            raise BufferError

    def print_until(self, max_count):
        self.max_count = max_count
        return self.assertRaises(BufferError)

    def results(self):
        return self.sio.getvalue().splitlines()
