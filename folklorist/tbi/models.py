from django.db import models
from django.contrib.postgres.fields import ArrayField


class IndexableCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 255)
        super().__init__(*args, **kwargs)


class Ballad(models.Model):
    name = IndexableCharField()
    description = IndexableCharField()
    author = IndexableCharField(max_length=300)
    earliest_date = IndexableCharField()
    long_description = models.TextField()
    keywords = ArrayField(IndexableCharField(), null=True)
    historical_references = ArrayField(models.TextField(), null=True)
    found_in = IndexableCharField()
    references = ArrayField(models.TextField(), null=True)
    recordings = ArrayField(models.TextField(), null=True)
    broadsides = ArrayField(models.TextField(), null=True)
    cross_references = ArrayField(IndexableCharField(), null=True)
    same_tune = ArrayField(models.TextField(), null=True)
    alternate_titles = ArrayField(IndexableCharField(), null=True)
    notes = models.TextField()
    file = IndexableCharField()


class BalladIndex(models.Model):
    name = IndexableCharField(blank=False)
    index = ArrayField(IndexableCharField())


class BalladName(models.Model):
    name = IndexableCharField(blank=False)
    title = IndexableCharField(blank=False)


class SuppTradFile(models.Model):
    name = IndexableCharField(blank=False)
    text = models.TextField(blank=False)
    file = IndexableCharField(blank=False)
