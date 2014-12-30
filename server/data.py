__author__ = 'kirillov'

from google.appengine.ext import ndb

class DataPoint(ndb.Model):
  temperature = ndb.FloatProperty()
  timestamp = ndb.DateTimeProperty(auto_now_add=True)

class HourPoint(ndb.Model):
  timestamp = ndb.DateTimeProperty()
  temperature = ndb.FloatProperty()