# Why?

My primary motivation for this library is to make a declarative way of getting data out the Django ORM and into a nested dict of dicts, lists and scalar values. The declarative property is important because it allows for asking questions about the transformation without actually running the transformation. In the context of Django, that is useful for:

- getting metadata about the used fields such as labels, datatypes and validators.
- calculating a hash for the transformation, thus enabling caching.
- solving the N+1 problem.
- serialization.
- separating the structure of the data from the actual data.

# How?

Stub.
