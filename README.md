# Why?

My primary motivation for this library is to make a declarative way of getting data out of the Django ORM and into a nested dict of dicts, lists and scalar values. The declarative property is important because it allows for asking questions about the transformation without actually running it. In the context of Django, that is useful for:

- getting metadata about the used fields such as labels, datatypes and validators.
- calculating a hash for the transformation, thus enabling caching.
- solving the N+1 problem by knowing what to select based on child nodes.
- serialization.
- separating the structure of the data from the actual data.

# How?

The most basic building block of `treeform` is the compose function `comp`. It's works like a recipy where each step adds a new thing to the dish.

It takes an iterable of callables as the first argument. Then it takes an arbitrary number of arguments and keywords who are applied on the first callable. Subsequent callables receives the output of the previous callable as input. Finally the output of the last callable are returned.

`comp` looks likes this:

```python
def comp(fns, *args, **kwargs):
    """Composes an iterable of callables."""
    for fn in fns:
        args, kwargs = fn(opts, *args, **kwargs)

    return args, kwargs
```

Treeform uses `comp` to transform a tree into another tree which can be handled by three basic operations:

## Copy

Read value for given key at the source and write it to the destination. In normal Django code that would look like:

```python
movie = get_movie()
{
    # COPY
    "title": movie.title
}
```

The `copies` functions with some details glossed over, looks like:

```python
def copies(k):
    def copier(source, dest):
        dest[k] = source[k]

        return (source, dest), {}  # (args, kwargs)

    return copier
```

The Django example above can be written as:

```python
movie = get_movie()
#                       ↓ source ↓ dest
comp([copies("title")], movie,   {})
```

## Apply

Read value for given key at the source, apply a given `comp` transformation to the value and write the result to the destination. In normal django code that would look like:

```python
director = get_director(movie)
{
    # APPLY
    #            ↓ COPY                 ↓ COPY
    "director": {"name": director.name, "age": director.age},
}
```

In database terms `apply` is similar to a one-to-one relation.

The `applies` functions with some details glossed over, looks like:

```python
def applies(k, fns):
    def applier(source, dest):
        # 0 gets the args, 1 the dest.
        dest[k] = comp(fns, source[k], {})[0][1]

        return (source, dest), {}  # (args, kwargs)

    return applier
```

The Django example above can be written as:

```python
director = get_director(movie)
#                                                            ↓ source   ↓ dest
comp([applies("director", [copies("name"), copies("age")])], director,  {})
```

## Map

For each item at the source apply a given `comp` transformation and save the result to the destination. In normal django code that would look like:

```python
{
    # MAP
    "actors": [
        ↓ APPLY
         ↓ COPY          ↓ COPY                   
        {"name": x.name, "education": x.education} for x in movie.actors.all()
    ]
}
```

In database terms `map` is similar to a one-to-many or many-to-many relation.

The `maps` functions with some details glossed over, looks like:

```python
def maps(k, fns):
    def mapper(source, dest):
        # 0 gets the args, 1 the dest.
        dest[k] = [comp(fns, x, {})[0][1] for x in source[k]]

        return (source, dest), {}  # (args, kwargs)

    return mapper
```

The Django example above can be written as:

```python
comp(
    [maps("actors", [copies("name"), copies("education")])],
    # source
    movie.actors.all(),
    # dest
    {},
)
```
