import logging, os, urllib

from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class BalladFile(db.Model):
  pass


class DeleteBalladFiles(webapp.RequestHandler):
  def get(self):
    taskqueue.add(url='/queue/delete')
  
  def post(self):
    ballads = BalladFile.all(keys_only=True).fetch(100)
    if ballads:
      db.delete(ballads)
      taskqueue.add(url='/queue/delete')


def main():
  urls = [
      ('/queue/delete', DeleteBalladFiles),
  ]
  application = webapp.WSGIApplication(urls, debug=True)
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
