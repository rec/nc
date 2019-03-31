from . import table


class Colors:
    """
    Colors is a "magic" color name object.

     To get a color from a name, use ``COLORS.<colorname>`` - for example

    ::

        COLORS.red
        COLORS.ochre

    or if the name is a variable or has a space in it,

    ::

        COLORS['violet red 4']

    To get a name from a color, use

    ::

        COLOR((0, 255, 255))
    """

    def __init__(self, table):
        super().__setattr__('_table', table)

    def to_string(self, color):
        return self._table.to_string(color)

    def __getitem__(self, name):
        try:
            return self._table.to_color(name)
        except ValueError:
            raise KeyError(name)

    def __getattr__(self, name):
        try:
            return self._table.to_color(name)
        except ValueError:
            raise AttributeError(name)

    def __setitem__(self, name, value):
        raise KeyError(name)

    def __setattr__(self, name, value):
        raise AttributeError(name)

    def __iter__(self):
        return iter(self._table)

    def __contains__(self, x):
        return x in self._table


COLORS = Colors(table.Table())
COLORS_255 = Colors(table.Table(normal=False))
