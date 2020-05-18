from unittest import mock
import contextlib
import io


@contextlib.contextmanager
def print_mocker():
    results = []

    with mock.patch('builtins.print') as mp:
        yield results

    sio = io.StringIO()
    for args, kwargs in mp.call_args_list:
        kwargs.pop('file', None)
        print(*args, **kwargs, file=sio)

    results[:] = sio.getvalue().splitlines()
