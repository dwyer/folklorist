import re

from urllib2 import urlopen

from google.appengine.ext import db


def _title_to_url(title):
    return '/song/%s' % title.replace(' ', '_').replace('"', '%22').replace('&', '%26').replace(';', '%3B').replace('?', '%3F')


class Ballad(db.Model):
    name = db.StringProperty() # indexed
    description = db.StringProperty(multiline=True) # indexed
    author = db.StringProperty() # indexed
    earliest_date = db.StringProperty(multiline=True) # indexed
    long_description = db.TextProperty()
    keywords = db.StringListProperty(default=[]) # indexed
    historical_references = db.ListProperty(db.Text, default=[])
    found_in = db.StringProperty() # indexed
    references = db.ListProperty(db.Text, default=[])
    recordings = db.ListProperty(db.Text, default=[])
    broadsides = db.ListProperty(db.Text, default=[])
    cross_references = db.StringListProperty(default=[]) # indexed
    same_tune = db.ListProperty(db.Text, default=[])
    alternate_titles = db.StringListProperty(default=[]) # indexed
    notes = db.TextProperty()
    file = db.StringProperty() # indexed

    def url(self):
        return '/song/%s' % self.title().replace(' ', '_').replace('"', '%22').replace(';', '%3B')

    def title(self):
        title = self.name
        title = re.sub(r' \[.*\]$', '', title)
        # articles
        articles = '|'.join(['A', 'An', 'El', 'Le', 'Ta', 'The'])
        title = re.sub(r'^(.*), (%s)$' % articles, r'\2 \1', title)
        title = re.sub(r'^(.*), (%s) (\(.*\))$' % articles, r'\2 \1 \3', title)
        return title

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
                #url = _title_to_url(title)
                ballad_name = BalladName.all().filter('title =', title).get()
                if ballad_name:
                    url = ballad_name.url()
                    s = s.replace(title, '<a href="%s">%s</a>' % (url, title))
            yield s

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
                url = 'http://sniff.numachi.com/pages/ti%s.html' % match.group(1)
                file = urlopen(url)
                text = file.read()
                file.close()
                match = re.search(r'<PRE>(.*)</PRE>', text, re.DOTALL)
                if match:
                    return match.group(1)
                return


class BalladName(db.Model):
    name = db.StringProperty(required=True)
    title = db.StringProperty(required=True)

    def url(self):
        return '/song/%s' % self.title.replace(' ', '_').replace('"', '%22').replace('&', '%26').replace(';', '%3B').replace('?', '%3F')


class BalladIndex(db.Model):
    name = db.StringProperty(required=True)
    index = db.StringListProperty(required=True)

    def title(self):
        title = self.name
        title = re.sub(r' \[.*\]$', '', title)
        # articles
        articles = '|'.join(['A', 'An', 'El', 'Le', 'Ta', 'The'])
        title = re.sub(r'^(.*), (%s)$' % articles, r'\2 \1', title)
        title = re.sub(r'^(.*), (%s) (\(.*\))$' % articles, r'\2 \1 \3', title)
        return title

    def url(self):
        return '/song/%s' % self.title().replace(' ', '_').replace('"', '%22').replace('&', '%26').replace(';', '%3B').replace('?', '%3F')


class SuppTradFile(db.Model):
    name = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    file = db.StringProperty(required=True)
