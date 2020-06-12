from django.db import models as m


class SchemaVersion(m.Model):
    schema = m.TextField("Unique name of the schema", db_index=True)
    version = m.PositiveIntegerField(
        "Current version of the schema for given object_id", db_index=True)
    object_id = m.PositiveIntegerField("Id of object", db_index=True)


"""
schema_hash = m.TextField(
        "Meta data hash value of the schema", db_index=True)
content_type_id = m.PositiveIntegerField(
        "Content type id of object", db_index=True)
"""
