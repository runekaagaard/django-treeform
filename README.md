# Why?

My primary motivation for this library is to make a declarative way of getting data out of the Django ORM and into a nested dict of dicts, lists and scalar values. The declarative property is important because it allows for asking questions about the transformation without actually running it. In the context of Django, that is useful for:

- getting metadata about the used fields such as labels, datatypes and validators.
- calculating a hash for the transformation, thus enabling caching.
- solving the N+1 problem by knowing what to select based on child nodes.
- serialization.
- separating the structure of the data from the actual data.

# How?

The most basic building block of `treeform` is the compose function `comp`. It takes an iterable of callables as the first argument. Then it takes an arbitrary number of arguments and keywords who are applied on the first callable. Subsequent callables receives the output of the previous callable as input. Finally the output of the last callable are returned.

`comp` looks likes this:

    def comp(fns, *args, **kwargs):
        """Composes an iterable of callables."""
        for fn, opts in fns:
            args, kwargs = fn(opts, *args, **kwargs)

        return Return(args, kwargs)
