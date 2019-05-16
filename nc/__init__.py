from . import colors
import sys

_DEFAULT_SCHEMES = 'html', 'pwg', 'juce', 'wikipedia'


class _NC:
    Colors = colors.Colors
    _COLORS = None

    @property  # noqa: F811
    def COLORS(self):
        if not self._COLORS:
            self._COLORS = self.Colors(*_DEFAULT_SCHEMES)

        return self._COLORS

    def __getattr__(self, name):
        return globals()[name]


sys.modules[__name__] = _NC()
