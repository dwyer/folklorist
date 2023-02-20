from google.appengine.ext import ndb


def _title_to_url(title):
  return '/song/%s' % title.replace(' ', '_').replace('"', '%22').replace('&', '%26').replace(';', '%3B').replace('?', '%3F') 


class Ballad(ndb.Model):
  name = ndb.StringProperty() # indexed
  description = ndb.StringProperty() # indexed
  author = ndb.StringProperty() # indexed
  earliest_date = ndb.StringProperty() # indexed
  long_description = ndb.TextProperty()
  keywords = ndb.StringProperty(repeated=True) # indexed
  historical_references = ndb.TextProperty(repeated=True)
  found_in = ndb.StringProperty() # indexed
  references = ndb.TextProperty(repeated=True)
  recordings = ndb.TextProperty(repeated=True)
  broadsides = ndb.TextProperty(repeated=True)
  cross_references = ndb.StringProperty(repeated=True) # indexed
  same_tune = ndb.TextProperty(repeated=True)
  alternate_titles = ndb.StringProperty(repeated=True) # indexed
  notes = ndb.TextProperty()
  file = ndb.StringProperty() # indexed
  
  def url(self):
    return '/song/%s' % self.title().replace(' ', '_').replace('"', '%22').replace(';', '%3B')
  
  def title(self):
    import re
    title = self.name
    title = re.sub(r' \[.*\]$', '', title)
    # articles
    articles = '|'.join(['A', 'An', 'El', 'Le', 'Ta', 'The'])
    title = re.sub(r'^(.*), (%s)$' % articles, r'\2 \1', title)
    title = re.sub(r'^(.*), (%s) (\(.*\))$' % articles, r'\2 \1 \3', title)
    return title
  
  def references_ex(self):
    import re
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
    import re
    for s in self.cross_references:
      m = re.match(r'^cf. "(?P<title>.+)"', s)
      if m:
        title = m.group('title')
        #url = _title_to_url(title)
        ballad_name = BalladName.query(BalladName.title==title).get()
        if ballad_name:
          url = ballad_name.url()
          s = s.replace(title, '<a href="%s">%s</a>' % (url, title))
      yield s
  
  def index(self):
    import re
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
    import re
    prog = re.compile('^DT, (.*)\*$')
    for ref in self.references:
      match = prog.match(ref)
      if match:
        return 'http://sniff.numachi.com/scores/%s.png' % match.group(1)
  
  def lyrics(self):
    import re
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


class BalladName(ndb.Model):
  name = ndb.StringProperty(required=True)
  title = ndb.StringProperty(required=True)
  
  def url(self):
    return '/song/%s' % self.title.replace(' ', '_').replace('"', '%22').replace('&', '%26').replace(';', '%3B').replace('?', '%3F')


class BalladIndex(ndb.Model):
  name = ndb.StringProperty(required=True)
  index = ndb.StringProperty(repeated=True)
  
  def title(self):
    import re
    title = self.name
    title = re.sub(r' \[.*\]$', '', title)
    # articles
    articles = '|'.join(['A', 'An', 'El', 'Le', 'Ta', 'The'])
    title = re.sub(r'^(.*), (%s)$' % articles, r'\2 \1', title)
    title = re.sub(r'^(.*), (%s) (\(.*\))$' % articles, r'\2 \1 \3', title)
    return title
  
  def url(self):
    return '/song/%s' % self.title().replace(' ', '_').replace('"', '%22').replace('&', '%26').replace(';', '%3B').replace('?', '%3F')


class SuppTradFile(ndb.Model):
  name = ndb.StringProperty(required=True)
  text = ndb.TextProperty(required=True)
  file = ndb.StringProperty(required=True)
