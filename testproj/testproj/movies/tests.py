import pytest
from testproj.movies.models import Movie

from django.core.management import call_command
from treeform import dcomp, field, one, many, read, meta, pp


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_fixtures.json')


@pytest.mark.django_db
def test_read():
    assert read(
        Movie.objects.get(pk=1), [
            field("title"),
            one("director", [
                field("name"),
                field("age"),
            ]),
            many("actors", [field("name"), field("education")])
        ]) == {
            'director': {
                'age': 52,
                'name': 'Wachowski Sisters'
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
    pp(
        meta(
            Movie.objects.get(pk=1),
            [
                field("title"),
                one("director", [
                    field("name"),
                    field("age"),
                ]),
                many("actors", [field("name"),
                                field("education")])
            ], ))
    assert 0
