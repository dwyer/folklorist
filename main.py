import os

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from ballads.views import *


def main():
  urls = [
      ('/', HomePage),
      ('/search', SearchPage),
      ('/song/(.*)', BalladPage),
      ('/sitemaps/(.+)\.xml', SitemapPage),
      (ErrorPage.url, ErrorPage),
  ]
  application = webapp.WSGIApplication(urls, debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
