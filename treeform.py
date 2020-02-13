from collections import Mapping


def comp(fns, *args, **kwargs):
    """Composes an iterable of callables."""
    for fn in fns:
        args, kwargs = fn(*args, **kwargs)

    return args, kwargs


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
