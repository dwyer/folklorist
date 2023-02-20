import re

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

    def title(self):
        title = self.name
        title = re.sub(r' \[.*\]$', '', title)
        # articles
        articles = '|'.join(['A', 'An', 'El', 'Le', 'Ta', 'The'])
        title = re.sub(r'^(.*), (%s)$' % articles, r'\2 \1', title)
        title = re.sub(r'^(.*), (%s) (\(.*\))$' % articles, r'\2 \1 \3', title)
        return title

    def urlencoded_title(self):
        return (self.title().replace(' ', '_').replace('"', '%22')
                .replace(';', '%3B'))

    def url(self):
        return '/song/%s' % self.urlencoded_title()


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
