import pytest
from testproj.movies.models import Movie, Actor, Director

from django.core.management import call_command
from treeform import dcomp, field, one, many, read, meta, pp


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
    meta_data = meta(Movie, VIEW_MOVIE_SCHEMA)
    print(meta_data)
    assert meta_data == {
        'actors': {
            'fields': ['name', 'education'],
            'model': Actor
        },
        'director': {
            'fields': ['name', 'age'],
            'model': Director,
            'movie_set': {
                'fields': ['title'],
                'model': Movie,
            },
        },
        'fields': ['title'],
        'model': Movie
    }
    assert 0
