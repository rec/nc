from .colors import Colors as _Colors

_DEFAULT_SCHEMES = 'html', 'pwg', 'juce', 'wikipedia'


class _NC:
    Colors = _Colors

    @property  # noqa: F811
    def COLORS(self):
        if not hasattr(self, '_COLORS'):
            self._COLORS = self.Colors(*_DEFAULT_SCHEMES)

        return self._COLORS


nc = _NC()
