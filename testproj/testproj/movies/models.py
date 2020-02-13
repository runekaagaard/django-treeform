from django.db import models as m


class Director(m.Model):
    name = m.TextField()
    age = m.IntegerField()


class Actor(m.Model):
    name = m.TextField()
    education = m.TextField()


class Movie(m.Model):
    title = m.TextField()
    actors = m.ManyToManyField(Actor)
