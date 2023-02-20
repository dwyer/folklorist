import os


def redirector(handler_method):
  """A decorator to redirect from trad.appspot.com to www.folklorist.org.

  To use it, decorate your get() method like this:

    @redirector
    def get(self):
      user = users.get_current_user(self)
      self.response.out.write('Hello, ' + user.nickname())
  """
  def check_host(self, *args):
    old = 'trad.appspot.com'
    new = 'www.folklorist.org'
    host = os.environ.get('HTTP_HOST')
    query = os.environ.get('QUERY_STRING')
    if host == old:
      path = os.environ.get('PATH_INFO')
      url = 'http://%s%s' % (new, path)
      if query:
        url = '%s?%s' % (url, query)
      self.redirect(url, permanent=True)
      return
    else:
      handler_method(self, *args)
  return check_host


def alphabet():
  from string import ascii_uppercase as letters
  links = ['<a href="/search?q=startswith:%s">%s</a>' % (c, c) for c in letters]
  return ' &middot; '.join(links)


def query_to_words(query):
  import re
  query = re.sub(r'[-/]', ' ', query)
  query = re.sub(r'[^\w\s\':]', '', query)
  return list(set(query.split()))
