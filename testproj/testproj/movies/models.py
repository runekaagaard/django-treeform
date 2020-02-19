from django.db import models as m


class Director(m.Model):
    name = m.TextField()
    age = m.IntegerField()


class Actor(m.Model):
    name = m.TextField(help_text="Actor Name")
    education = m.TextField()


class Movie(m.Model):
    title = m.TextField("Movie Title")
    actors = m.ManyToManyField(Actor)
    director = m.ForeignKey(Director, on_delete=m.PROTECT)
