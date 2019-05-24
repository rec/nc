from . import _util
import importlib
import string

_ALLOWED = set(string.ascii_letters + string.digits)


class Colors:
    def __init__(self, *schemes, canonicalize_gray=True):
        self._canonicalize_gray = bool(canonicalize_gray)
        self._schemes = schemes
        self._name_to_rgb = {}
        self._rgb_to_name = {}

        for s in schemes:
            self._add_scheme(s)

        self._canonical_to_rgb = {
            self._canonical_name(k): v for k, v in self._name_to_rgb.items()
        }

    def to_color(self, c):
        """Try to coerce the argument into an rgb color"""
        try:
            return self[c]
        except Exception:
            return _util.to_color(c)

    def to_string(self, c):
        """Convert a tuple to a string name"""
        try:
            return self._rgb_to_name[c]
        except Exception:
            return str(c)

    def items(self):
        return self._name_to_rgb.items()

    def __getitem__(self, name):
        """Try to convert  string item into a color"""
        canonical = self._canonical_name(name)
        rgb = self._canonical_to_rgb.get(canonical)
        if rgb is None:
            raise KeyError(name)
        return rgb

    def __setitem__(self, name, rgb):
        raise KeyError(name)

    def __contains__(self, x):
        """Return true if this string name appears in the table canonically"""
        return self._canonical_name(x) in self._canonical_to_rgb

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            return super().__setattr__(name, value)
        raise AttributeError(name)

    def __len__(self):
        return len(self._name_to_rgb)

    def __iter__(self):
        return iter(self._name_to_rgb)

    def __eq__(self, x):
        return __class__ == x.__class__ and self._name_to_rgb == x._name_to_rgb

    def __ne__(self, x):
        return not (self == x)

    def __add__(self, x):
        if not isinstance(x, __class__):
            x = __class__(x, canonicalize_gray=self._canonicalize_gray)
        elif self._canonicalize_gray != x._canonicalize_gray:
            raise ValueError('canonicalize_gray must be the same')
        return __class__(
            *(self._schemes + x._schemes),
            canonicalize_gray=self._canonicalize_gray,
        )

    def __radd__(self, x):
        return __class__(x, canonicalize_gray=self._canonicalize_gray) + self

    def _add_scheme(self, scheme):
        if isinstance(scheme, str):
            if '.' not in scheme:
                scheme = 'nc.schemes.' + scheme
            scheme = importlib.import_module(scheme)

        if not isinstance(scheme, dict):
            scheme = scheme.__dict__

        if 'COLORS' in scheme:
            colors = scheme['COLORS']
            primary_names = scheme.get('PRIMARY_NAMES', ())
        else:
            colors = scheme
            primary_names = ()

        colors = {k: _util.to_color(v) for k, v in colors.items()}
        self._name_to_rgb.update(colors)

        def best_name(names):
            names.sort(key=lambda n: (len(n), n.lower()))
            pnames = (n for n in names if n in primary_names)
            return next(pnames, names[0])

        names = {}
        for name, color in colors.items():
            names.setdefault(color, []).append(name)

        self._rgb_to_name.update((k, best_name(v)) for k, v in names.items())

    def _canonical_name(self, name):
        name = name.lower()
        if self._canonicalize_gray:
            name = name.replace('grey', 'gray')
        return ''.join(i for i in name if i in _ALLOWED)


"""Some colors have multiple names; a best name needs to be chosen.
   scheme.PRIMARY_NAMES is a list of names to use by preference.
   Otherwise the shortest color name is chosen, and in a tie, the
   alphabetically first one.
"""
