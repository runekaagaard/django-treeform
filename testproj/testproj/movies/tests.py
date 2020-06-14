import pytest
from testproj.movies.models import Movie, Actor, Director

from django.core.management import call_command
from django.db.models.fields import NOT_PROVIDED
from django.db.models import fields

from treeform.treeform import (dcomp, field, one, many, read, meta, pp,
                               serialize)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_fixtures.json')


VIEW_MOVIE_SCHEMA = [
    field("title"),
    one("director",
        [field("name"),
         field("age"),
         many("movie_set", [field("title")])]),
    many("actors", [field("name"), field("education")])
]


@pytest.mark.django_db
def test_read():
    assert read(
        Movie.objects.get(pk=1), VIEW_MOVIE_SCHEMA) == {
            'director': {
                'age': 52,
                'name': 'Wachowski Sisters',
                'movie_set': [{
                    'title': 'The Matrix'
                }],
            },
            'actors': [{
                'name': 'Keanu Reeves',
                'education': 'The best',
            }, {
                'name': 'Carrie-Anne Moss',
                'education': 'Also good',
            }],
            'title':
                'The Matrix'
        }


@pytest.mark.django_db
def test_meta():
    meta_data = serialize(meta(Movie, VIEW_MOVIE_SCHEMA), indent=4)
    assert meta_data == """
{
    "model": [
        "__CDT__",
        "treeform.django_model",
        "movies.movie"
    ],
    "ordering": [
        "title"
    ],
    "fields": {
        "title": {
            "type": [
                "__CDT__",
                "treeform.django_model_field",
                "django.db.models.fields.TextField"
            ],
            "blank": false,
            "hidden": false,
            "help_text": "",
            "max_length": null,
            "null": false,
            "verbose_name": "Movie Title",
            "default": [
                "__CDT__",
                "treeform.not_provided"
            ]
        }
    },
    "director": {
        "model": [
            "__CDT__",
            "treeform.django_model",
            "movies.director"
        ],
        "ordering": [
            "name",
            "age"
        ],
        "fields": {
            "name": {
                "type": [
                    "__CDT__",
                    "treeform.django_model_field",
                    "django.db.models.fields.TextField"
                ],
                "blank": false,
                "hidden": false,
                "help_text": "",
                "max_length": null,
                "null": false,
                "verbose_name": "name",
                "default": [
                    "__CDT__",
                    "treeform.not_provided"
                ]
            },
            "age": {
                "type": [
                    "__CDT__",
                    "treeform.django_model_field",
                    "django.db.models.fields.IntegerField"
                ],
                "blank": false,
                "hidden": false,
                "help_text": "",
                "max_length": null,
                "null": false,
                "verbose_name": "age",
                "default": [
                    "__CDT__",
                    "treeform.not_provided"
                ]
            }
        },
        "movie_set": {
            "model": [
                "__CDT__",
                "treeform.django_model",
                "movies.movie"
            ],
            "ordering": [
                "title"
            ],
            "fields": {
                "title": {
                    "type": [
                        "__CDT__",
                        "treeform.django_model_field",
                        "django.db.models.fields.TextField"
                    ],
                    "blank": false,
                    "hidden": false,
                    "help_text": "",
                    "max_length": null,
                    "null": false,
                    "verbose_name": "Movie Title",
                    "default": [
                        "__CDT__",
                        "treeform.not_provided"
                    ]
                }
            },
            "version_hash": "e377fa0c879470efb735231ce6806f8b"
        },
        "version_hash": "315e9b956204acf65c1fc7d86a58bd9f"
    },
    "actors": {
        "model": [
            "__CDT__",
            "treeform.django_model",
            "movies.actor"
        ],
        "ordering": [
            "name",
            "education"
        ],
        "fields": {
            "name": {
                "type": [
                    "__CDT__",
                    "treeform.django_model_field",
                    "django.db.models.fields.TextField"
                ],
                "blank": false,
                "hidden": false,
                "help_text": "Actor Name",
                "max_length": null,
                "null": false,
                "verbose_name": "name",
                "default": [
                    "__CDT__",
                    "treeform.not_provided"
                ]
            },
            "education": {
                "type": [
                    "__CDT__",
                    "treeform.django_model_field",
                    "django.db.models.fields.TextField"
                ],
                "blank": false,
                "hidden": false,
                "help_text": "",
                "max_length": null,
                "null": false,
                "verbose_name": "education",
                "default": [
                    "__CDT__",
                    "treeform.not_provided"
                ]
            }
        },
        "version_hash": "73e8b5532945734f9dd37b4327cb3707"
    },
    "version_hash": "1680b821b17a3ea498a057c378f9776f"
}
""".strip()
