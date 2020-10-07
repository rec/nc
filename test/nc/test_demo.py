from .print_mocker import print_mocker
from nc import demo
from unittest import mock, TestCase


@mock.patch('time.sleep', return_value=None)
class DemoTest(TestCase):
    def test_demo0(self, sleep):
        with print_mocker() as actual:
            returncode = demo.demo(0, reverse=False, long=True, steps=9)
        assert returncode == -1
        assert actual[0].startswith('Your terminal')

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

    def test_short_demo(self, sleep):
        with print_mocker() as actual:
            demo.demo(16, reverse=False, long=False, steps=9)
        expected = [
            '\x1b[30;40m•'
            '\x1b[m'
            '\x1b[31;40m•'
            '\x1b[m'
            '\x1b[32;40m•'
            '\x1b[m'
            '\x1b[33;40m•'
            '\x1b[m'
            '\x1b[34;40m•'
            '\x1b[m'
            '\x1b[35;40m•'
            '\x1b[m'
            '\x1b[36;40m•'
            '\x1b[m'
            '\x1b[37;40m•'
            '\x1b[m'
            '\x1b[90;40m•\x1b[m'
        ]
        if expected != actual:
            print(*map(repr, actual), sep='\n')
        self.assertEqual(expected, actual)

    @mock.patch('subprocess.check_output', return_value='5 7')
    def test_thin_columns(self, sleep, check_output):
        with print_mocker() as actual:
            demo.demo(256, reverse=False, long=False, steps=256)
        actual = actual[:8]
        expected = [
            (
                '\x1b[38;5;16;48;5;16m•\x1b[m'
                '\x1b[38;5;1;48;5;16m•\x1b[m'
                '\x1b[38;5;2;48;5;16m•\x1b[m'
                '\x1b[38;5;3;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;4;48;5;16m•'
                '\x1b[m\x1b[38;5;5;48;5;16m•'
                '\x1b[m\x1b[38;5;6;48;5;16m•'
                '\x1b[m\x1b[38;5;7;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;8;48;5;16m•'
                '\x1b[m\x1b[38;5;196;48;5;16m•'
                '\x1b[m\x1b[38;5;46;48;5;16m•'
                '\x1b[m\x1b[38;5;226;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;12;48;5;16m•'
                '\x1b[m\x1b[38;5;201;48;5;16m•'
                '\x1b[m\x1b[38;5;51;48;5;16m•'
                '\x1b[m\x1b[38;5;231;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;16;48;5;16m•'
                '\x1b[m\x1b[38;5;17;48;5;16m•'
                '\x1b[m\x1b[38;5;18;48;5;16m•'
                '\x1b[m\x1b[38;5;19;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;20;48;5;16m•'
                '\x1b[m\x1b[38;5;21;48;5;16m•'
                '\x1b[m\x1b[38;5;22;48;5;16m•'
                '\x1b[m\x1b[38;5;23;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;24;48;5;16m•'
                '\x1b[m\x1b[38;5;25;48;5;16m•'
                '\x1b[m\x1b[38;5;26;48;5;16m•'
                '\x1b[m\x1b[38;5;27;48;5;16m•\x1b[m'
            ),
            (
                '\x1b[m\x1b[38;5;28;48;5;16m•'
                '\x1b[m\x1b[38;5;29;48;5;16m•'
                '\x1b[m\x1b[38;5;30;48;5;16m•'
                '\x1b[m\x1b[38;5;31;48;5;16m•\x1b[m'
            ),
        ]
        assert actual == expected
