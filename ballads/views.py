import logging
import os
import urllib

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from django.core.paginator import Paginator

from models import *
from hacks import *


# TODO put this in /settings.py and make it an absolute path
TEMPLATES_DIR = 'templates'


class _RequestHandler(webapp.RequestHandler):
  template_dir = 'templates'
  
  def __init__(self):
    webapp.RequestHandler.__init__(self)
  
  def write(self, filename='base.html'):
    path = os.path.join(self.template_dir, filename)
    self.response.out.write(template.render(path, dict(self=self)))
  
  def not_found(self):
    self.error(404)
    self.message = '404: Page not found.'
    self.title = 'Page not found.'
    self.write('error.html')


class HomePage(webapp.RequestHandler):
  @redirector
  def get(self):
    path = os.path.join(TEMPLATES_DIR, 'home.html')
    context = {'vols': alphabet()}
    self.response.out.write(template.render(path, context))


class SearchPage(webapp.RequestHandler):
  limit = 30
  
  @redirector
  def get(self):
    self.query = self.request.get('q')
    self.page = int(self.request.get('p', 1))
    self.start = int(self.request.get('start', 1))
    
    info = None
    error = None
    
    if self.query:
      self.query = self.query.strip()
      self.title = 'Search for %s - Folklorist' % self.query
      self.results = BalladIndex.all(keys_only=True)
      for word in query_to_words(self.query):
        self.results.filter('index =', word.lower())
      #self.num_results = '?'
      self.num_results = self.results.count()
      offset = (self.page-1) * self.limit
      self.results = self.results.fetch(self.limit, offset)
      self.results = db.get(self.results)
      #self.results = [child.parent() for child in self.results]
      
      if self.results:
        # pagination
        self.pages = []
        if self.page > 1:
          self.pages.append('<a href="/search?q=%s&p=%d">&lt; Previous</a>'
              % (self.query, self.page-1))
        if len(self.results) == self.limit:
          self.pages.append('<a href="/search?q=%s&p=%d">Next &gt;</a>'
              % (self.query, self.page+1))
        self.pages = ' &middot; '.join(self.pages)
        # love!
        self.start = offset + 1
        self.finish = offset + self.limit
    #self.write('search.html')
    path = os.path.join(TEMPLATES_DIR, 'search.html')
    context = {'self': self, 'vols': alphabet(), 'error': error, 'info': info}
    self.response.out.write(template.render(path, context))


class BalladPage(_RequestHandler):
  @redirector
  def get(self, title):
    title = urllib.unquote(title.replace('_', ' '))
    query = BalladName.all(keys_only=True).filter('title =', title).get()
    # get ballad
    self.ballad = None
    if query:
      key = query.parent()
      self.ballad = Ballad.get(key)
    # got ballad
    if self.ballad:
      self.title = self.ballad.title()
      self.supptrad = SuppTradFile.get_by_key_name(self.ballad.file, self.ballad)
    else: # handle broken links
      self.ballad = Ballad.all().filter('name =', title).get()
      if self.ballad:
        self.redirect(self.ballad.url(), permanent=True)
      else:
        self.not_found()
      return
    self.write('ballad.html')


class SitemapPage(webapp.RequestHandler):
  @redirector
  def get(self, start):
    memkey = 'sitemap_%s' % start
    output = memcache.get(memkey)
    if output is None:
      list = BalladName.all().order('name')
      list.filter('name >=', start)
      list.filter('name <', start+chr(127))
      output = template.render('templates/sitemap.xml', dict(list=list))
      memcache.set(memkey, output)
    self.response.headers['content-type'] = 'text/xml'
    self.response.out.write(output)


class ErrorPage(_RequestHandler):
  url = '/.*'
  def get(self):
    self.not_found()
