from .colors import COLORS, COLORS_255  # noqa: F401
from .colors2 import Colors as Colors2

_DEFAULT_SCHEMES = 'html', 'pwg', 'juce'


class _NC:
    Colors = Colors2

    @property  # noqa: F811
    def COLORS(self):
        if not hasattr(self, '_COLORS'):
            self._COLORS = self.Colors(*_DEFAULT_SCHEMES)

        return self._COLORS


nc = _NC()
