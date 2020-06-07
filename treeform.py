import json
from collections import Mapping

from django.db.models.fields import NOT_PROVIDED
from django.db.models import Model


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


def read(source, schema):
    return dcomp(READ, schema, source, {})[0][1]


def meta(source, schema):
    return dcomp(META, schema, source, {})[0][1]


NULL = "__NULL__"
META_ATTRS = (("blank", NULL), ("hidden", NULL), ("help_text", NULL),
              ("max_length", None), ("null", NULL), ("verbose_name", None),
              ("default", NOT_PROVIDED))


class field(object):
    """Django model field."""

    def __init__(self, k):
        self.k = k

    def read(self, source, dest):
        dsets(dest, self.k, dgets(source, self.k))

        return (source, dest), {}

    def meta(self, source, dest):
        if "model" not in dest:
            dest["model"] = source
            dest["fields"] = []
        dest["fields"].append(self.k)
        # metadata = {"type": type(field)}
        # for key, null in META_ATTRS:
        #     val = getattr(field, key, NULL)
        #     if val != null:
        #         metadata[key] = val
        # dsets(dest, self.k, metadata)

        return (source, dest), {}


class one(object):
    """Django one-2-one relation."""

    def __init__(self, k, fns):
        self.k = k
        self.fns = fns

    def read(self, source, dest):
        dsets(dest, self.k, read(dgets(source, self.k), self.fns))

        return (source, dest), {}

    def meta(self, source, dest):
        dsets(dest, self.k,
              meta(dgets(source, self.k).field.related_model, self.fns))

        return (source, dest), {}


class many(object):
    """Django one-2-many or many-2-many mapping."""

    def __init__(self, k, fns):
        self.k = k
        self.fns = fns

    def read(self, source, dest):
        dsets(dest, self.k, [
            dcomp(READ, self.fns, x, {})[0][1] for x in dgets(source, self.k)
        ])

        return (source, dest), {}

    def meta(self, source, dest):
        dsets(dest, self.k, meta(dgets(source, self.k).rel.model, self.fns))

        return (source, dest), {}


### Other ###

CUSTOM_DATA_TYPE = "__CDT__"
DATA_TYPE_CLASS = "treeform.1"


def pp(data):
    from pprint import pprint
    pprint(data, indent=4, depth=10)
    # print(serialize(data, indent=4))


def default(thing):
    print(thing, isinstance(thing, Model), type(thing) is type)
    if type(thing) is type:
        return (CUSTOM_DATA_TYPE, DATA_TYPE_CLASS,
                str(thing.__module__) + "." + thing.__class__.__name_)
    elif isinstance(thing, Model):
        return str(thing)
    else:
        raise TypeError("DONT KNOW" + repr(thing))


def serialize(data, indent=None):
    return json.dumps(data, default=default, indent=indent)


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
    print(json.dumps(dest, indent=4))
