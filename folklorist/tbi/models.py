import re
import urllib.parse

from django.db import models
from django.contrib.postgres.fields import ArrayField

from .utils import title_quote


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

    def url(self):
        return '/song/' + title_quote(self.title())

    def index(self):
        title = self.title().lower()
        title = re.sub(r'[-/]', ' ', title)
        title = re.sub(r'[^\w\s\']', '', title)
        words = []
        for word in title.split():
            if word not in words:
                words.append(word)
        words.append('startswith:%s' % self.name[0].lower())
        words.extend(['keyword:%s' % w.lower() for w in self.keywords])
        return words

    def references_ex(self):
        res = [
            (r'^DT(?: \d+)?, (?:(\w+)+\*?\s?)+$', r'<u>\1</u>'),
            (r'^Roud #(\d+)$', r'<a href="http://library.efdss.org/cgi-bin/query.cgi?query=\1&field=20&output=List&length=5" target="_blank">\1</a>'),
        ]
        for s in self.references:
            for x, y in res:
                m = re.match(x, s)
                if m:
                    for g in m.groups():
                        s = re.sub('(%s)' % g, y, s)
                    break
            yield s

    def cross_references_ex(self):
        for s in self.cross_references:
            m = re.match(r'^cf. "(?P<title>.+)"', s)
            if m:
                title = m.group('title')
                try:
                    ballad_name = BalladName.objects.get(title=title)
                    url = ballad_name.url()
                    s = s.replace(title, '<a href="%s">%s</a>' % (url, title))
                except BalladName.DoesNotExist:
                    pass
            yield s

    def score(self):
        prog = re.compile('^DT, (.*)\*$')
        for ref in self.references:
            match = prog.match(ref)
            if match:
                return 'http://sniff.numachi.com/scores/%s.png' % match.group(1)

    def lyrics(self):
        prog = re.compile(r'^DT, (.*)\*$')
        for ref in self.references:
            match = prog.match(ref)
            if match:
                from urllib2 import urlopen
                url = 'http://sniff.numachi.com/pages/ti%s.html' % match.group(1)
                file = urlopen(url)
                text = file.read()
                file.close()
                match = re.search(r'<PRE>(.*)</PRE>', text, re.DOTALL)
                if match:
                    return match.group(1)
                return


class BalladName(models.Model):
    name = IndexableCharField(blank=False)
    title = IndexableCharField(blank=False)
    parent = models.ForeignKey(Ballad, on_delete=models.CASCADE, null=True)

    def url(self):
        return '/song/' + title_quote(self.title)


class BalladIndex(models.Model):
    name = IndexableCharField(blank=False)
    index = ArrayField(IndexableCharField())
    parent = models.ForeignKey(BalladName, on_delete=models.CASCADE, null=True)

    def title(self):
        title = self.name
        title = re.sub(r' \[.*\]$', '', title)
        # articles
        articles = '|'.join(['A', 'An', 'El', 'Le', 'Ta', 'The'])
        title = re.sub(r'^(.*), (%s)$' % articles, r'\2 \1', title)
        title = re.sub(r'^(.*), (%s) (\(.*\))$' % articles, r'\2 \1 \3', title)
        return title

    def url(self):
        return '/song/' + title_quote(self.title())


class SuppTradFile(models.Model):
    name = IndexableCharField(blank=False)
    text = models.TextField(blank=False)
    file = IndexableCharField(blank=False)
    parent = models.ForeignKey(Ballad, on_delete=models.CASCADE, null=True)
