from collections import Mapping


def comp(fns, *args, **kwargs):
    """Composes an iterable of callables."""
    for fn in fns:
        args, kwargs = fn(*args, **kwargs)

    return args, kwargs


### General ###


def gets(thing, key):
    """Get value in both dict and object things."""
    if isinstance(thing, Mapping):
        return thing[key]
    else:
        return getattr(thing, key)


def sets(thing, key, value):
    """Set value in both dict and object things."""
    if isinstance(thing, Mapping):
        thing[key] = value
    else:
        setattr(thing, key, value)

    return thing


def copies(k):
    """Transfers a key/value pair from the source to the target."""

    def copier(source, dest):
        sets(dest, k, gets(source, k))

        return (source, dest), {}  # (args, kwargs)

    return copier


def applies(k, fns):
    """Composes fns over the value of k and copies it to the target."""

    def applier(source, dest):
        # 0 gets the args, 1 the dest.
        sets(dest, k, comp(fns, gets(source, k), {})[0][1])

        return (source, dest), {}  # (args, kwargs)

    return applier


def maps(k, fns):
    """Composes fns for each of the value of k and copies it to the target."""

    def mapper(source, dest):
        # 0 gets the args, 1 the dest.
        sets(dest, k, [comp(fns, x, {})[0][1] for x in gets(source, k)])

        return (source, dest), {}  # (args, kwargs)

    return mapper


### Django ###

# Mode
READ = "read"
WRITE = "write"
META = "meta"


def dcomp(mode, fns, *args, **kwargs):
    """Django version of comp."""
    for fn in fns:
        args, kwargs = getattr(fn, mode)(*args, **kwargs)

    return args, kwargs


def dgets(thing, key):
    """Django version of gets."""
    if isinstance(thing, Mapping):
        return thing[key]
    else:
        val = getattr(thing, key)
        if "RelatedManager" in repr(val.__class__):
            return val.all()
        else:
            return val


def dsets(thing, key, value):
    """Django version of sets."""
    if isinstance(thing, Mapping):
        thing[key] = value
    else:
        setattr(thing, key, value)

    return thing


class field(object):
    """Django model field."""

    def __init__(self, k):
        self.k = k

    def read(self, source, dest):
        dsets(dest, self.k, dgets(source, self.k))

        return (source, dest), {}


class one(object):
    """Django one-2-one relation."""

    def __init__(self, k, fns):
        self.k = k
        self.fns = fns

    def read(self, source, dest):
        # 0 gets the args, 1 the dest.
        dsets(dest, self.k,
              dcomp(READ, self.fns, dgets(source, self.k), {})[0][1])

        return (source, dest), {}  # (args, kwargs)


class many(object):
    """Django one-2-many or many-2-many mapping."""

    def __init__(self, k, fns):
        self.k = k
        self.fns = fns

    def read(self, source, dest):
        # 0 gets the args, 1 the dest.
        dsets(dest, self.k, [
            dcomp(READ, self.fns, x, {})[0][1] for x in dgets(source, self.k)
        ])

        return (source, dest), {}  # (args, kwargs)


if __name__ == "__main__":
    source = {
        "title":
            "The Matrix",
        "director": {
            "name": "Wachowski Sisters",
            "age": 52,
        },
        "actors": [{
            "name": "Keanu Reeves",
            "education": "The best"
        }, {
            "name": "Carrie-Anne Moss",
            "education": "Also good"
        }]
    }
    dest = {}
    args, kwargs = comp([
        copies("title"),
        applies("director", [
            copies("name"),
            copies("age"),
        ]),
        maps("actors", [copies("name"), copies("education")])
    ], source, dest)
    source, dest = args
    import json
    print(json.dumps(dest, indent=4))
