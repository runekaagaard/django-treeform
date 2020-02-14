import pytest
from testproj.movies.models import Movie

from django.core.management import call_command
from treeform import comp, field, one, many


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_fixtures.json')


@pytest.mark.django_db
def test_basic():
    assert Movie.objects.count() == 1
    source = Movie.objects.get(pk=1)
    dest = {}
    args, kwargs = comp(
        [
            field("title"),
            one("director", [
                field("name"),
                field("age"),
            ]),
            many("actors", [field("name"), field("education")])
        ],
        source,
        dest, )
    source, dest = args
    assert dest == {
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
