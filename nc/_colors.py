from . import _util
import importlib
import string

_ALLOWED = set(string.ascii_letters + string.digits)


class Colors:
    def __init__(self, *modules, canonicalize_gray=True):
        self._modules = modules
        self._canonicalize_gray = bool(canonicalize_gray)
        self._initialize()

    def to_color(self, c):
        """Try to coerce the argument into an rgb color"""
        try:
            return self[c]
        except Exception:
            return _util.to_color(c)

    def to_string(self, c):
        """Convert a tuple to a string name"""
        try:
            return self._to_name[c]
        except Exception:
            return str(c)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, name):
        """Try to convert  string item into a color"""
        try:
            return self._to_rgb[self._canonical_name(name)]
        except KeyError:
            raise KeyError(name)

    def __setitem__(self, name, rgb):
        raise KeyError(name)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            raise AttributeError(name)
        super().__setattr__(name, value)

    def __contains__(self, x):
        """Return true if this string name appears in the table canonically"""
        return self._canonical_name(x) in self._to_rgb

    def __add__(self, other):
        modules = self._combine(other)
        return __class__(*modules, canonicalize_gray=self._canonicalize_gray)

    def __iadd__(self, other):
        self.modules = self._combine(other)
        self._initialize()
        return self

    def __radd__(self, other):
        self.modules = self._combine(other)
        self._initialize()
        return self

    def __eq__(self, other):
        return self._modules == other._modules

    def __ne__(self, other):
        return not (self == other)

    def _combine(self, other):
        if not isinstance(other, __class__):
            other = __class__(other)

        if self._canonicalize_gray != other._canonicalize_gray:
            raise ValueError('canonicalize_gray must be the same')
        modules = tuple(m for m in other._modules if m not in self._modules)
        return self._modules + modules

    def _initialize(self):
        self._items = {}
        self._to_name = {}
        self._to_rgb = {}

        for module in self._modules:
            self._add_module(module)

        self._items = sorted(self._items.items())

    def _add_module(self, module):
        to_names = {}
        if isinstance(module, dict):
            mdict = module

        else:
            if isinstance(module, str):
                if '.' not in module:
                    module = 'nc.schemes.' + module
                mdict = importlib.import_module(module).__dict__
            else:
                mdict = module.__dict__

        colors = mdict.get('COLORS', None)
        if colors is None:
            colors = mdict
            mdict = {}

        primary_names = set(mdict.get('PRIMARY_NAMES') or ())
        for name, color in colors.items():
            rgb = color if isinstance(color, tuple) else _util.to_rgb(color)
            to_names.setdefault(rgb, []).append(name)

            cname = self._canonical_name(name)
            self._items[name] = self._to_rgb[cname] = rgb

        def best_name(names):
            names.sort(key=lambda n: (len(n), n.lower()))
            pnames = (n for n in names if n in primary_names)
            return next(pnames, names[0])

        best_names = {k: best_name(v) for k, v in to_names.items()}
        self._to_name.update(best_names)

    def _canonical_name(self, name):
        name = name.lower()
        if self._canonicalize_gray:
            name = name.replace('grey', 'gray')
        return ''.join(i for i in name if i in _ALLOWED)


def _combine(a, b):
    if not isinstance(a, Colors):
        a = Colors(a)
    if not isinstance(b, Colors):
        b = Colors(b)

    if a._canonicalize_gray != b._canonicalize_gray:
        raise ValueError('canonicalize_gray must be the same')
    modules = tuple(m for m in b._modules if m not in a._modules)
    return a._modules + modules


"""Some colors have multiple names; a best name needs to be chosen.
   module.PRIMARY_NAMES is a list of names to use by preference.
   Otherwise the shortest color name is chosen, and in a tie, the
   alphabetically first one.
"""
