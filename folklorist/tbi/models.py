from django.db import models
from django.contrib.postgres.fields import ArrayField


class IndexableCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 254)
        super().__init__(*args, **kwargs)


class Ballad(models.Model):
    name = IndexableCharField()
    description = IndexableCharField()
    author = IndexableCharField()
    earliest_date = IndexableCharField()
    long_description = models.TextField()
    keywords = ArrayField(IndexableCharField())
    historical_references = ArrayField(models.TextField())
    found_in = IndexableCharField()
    references = ArrayField(models.TextField())
    recordings = ArrayField(models.TextField())
    broadsides = ArrayField(models.TextField())
    cross_references = ArrayField(IndexableCharField())
    same_tune = ArrayField(models.TextField())
    alternate_titles = ArrayField(IndexableCharField())
    notes = models.TextField()
    file = IndexableCharField()
