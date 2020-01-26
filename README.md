# Why?

My primary motivation for this library is to make a declarative way of getting data out the Django ORM and into a nested dict of dicts, lists and scalar values. The declarative property is important because it allows for asking questions about the transformation without actually running it. In the context of Django, that is useful for:

- getting metadata about the used fields such as labels, datatypes and validators.
- calculating a hash for the transformation, thus enabling caching.
- solving the N+1 problem by knowing what to select based on child nodes.
- serialization.
- separating the structure of the data from the actual data.

# How?

The most basic building block of `treeform` is the compose function `comp`. It takes an iterable of `(callable, options)` pairs as the first argument. It then takes an optional number of arguments and keyword arguments. Each callable is called with the `options` of the`(callable, options)` pair, then the output of the previous function as input. The first callable in the iterable receives the input to `comp` as input. `comp` returns the output of the last callable. `comp` looks likes this:

    def comp(fns, *args, **kwargs):
    """Composes an iterable of callables."""
    for fn, opts in fns:
        args, kwargs = fn(opts, *args, **kwargs)

    return Return(args, kwargs)
