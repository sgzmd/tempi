import webapp2

from datetime import datetime

from data import *
from google.appengine.ext import ndb
from google.appengine.api.mail import send_mail
import logging
import itertools

from google.appengine.api import mail

import pprint

THERMOMETER = ndb.Key("Thermometer", "1")
MAX_DELTA_SECONDS = 10 * 60 # 10 minutes
EMAIL_BODY = """
Last activity registered {0} seconds ago.
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        data = DataPoint.query(ancestor=THERMOMETER).order(-DataPoint.timestamp).fetch(1)
        for dp in data:
            self.response.out.write('<p>' + str(dp.timestamp) + '&nbsp;' + str(dp.temperature) + '</p>')


class SubmitDataHandler(webapp2.RequestHandler):
    def get(self):
        temperature = self.request.get('temp')
        if not temperature:
            self.error(400)
        else:
            dp = DataPoint(parent=THERMOMETER)
            dp.temperature = float(temperature)
            dp.put()


class AggregateTask(webapp2.RequestHandler):
    def get(self):
        def chop_off_minutes(timestamp):
            return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)

        def cronlog(message):
            self.response.out.write(message + "\n")
            logging.info(message)

        # ignoring the very first timestamp for watchdog to use
        data = list(itertools.islice(DataPoint.query(ancestor=THERMOMETER)
                                              .order(-DataPoint.timestamp)
                                              .fetch(), 1, None))

        self.response.content_type = "text/plain"

        if not data:
            cronlog("No DataPoint stored")
            return

        # data is sorted by timestamp
        hour_only = set([chop_off_minutes(x.timestamp) for x in data])
        data_hour_only = dict()
        for timestamp in hour_only:
            cronlog("Processing timestamp: " + str(timestamp))
            temps = [y.temperature
                     for y in filter(lambda x:
                                     chop_off_minutes(x.timestamp) == timestamp,
                                     data)]
            if not temps:
                cronlog("No temp datapoints for " + str(timestamp))
                continue

            data_hour_only[timestamp] = sum(temps) / len(temps)
            cronlog(
                "Calculated average temperature: " +
                str(data_hour_only[timestamp]))

        for k in data_hour_only.keys():
            if not HourPoint.query(HourPoint.timestamp == k).fetch():
                cronlog("Writing HourPoint for " + str(k))
                HourPoint(timestamp=k, temperature=data_hour_only[k]).put()
            else:
                cronlog("HourPoint already exists for " + str(k))

        for d in data:
            d.key.delete()


class WatchdogTask(webapp2.RequestHandler):
    def cronlog(self, message):
        logging.info(message)

    def notify(self, last_update_delta):
        if last_update_delta.total_seconds() < MAX_DELTA_SECONDS:
            logging.info("Last update was only %d seconds OK which is OK",
                         last_update_delta.total_seconds())
            return

        last_notification = Notification.query(ancestor=THERMOMETER).order(-Notification.timestamp).fetch(1)
        if last_notification:
            notification_delta = datetime.now() - last_notification[0].timestamp
            if notification_delta.total_seconds() < 10*MAX_DELTA_SECONDS:
                logging.info("Last notification sent %d seconds ago, not resending",
                             notification_delta.total_seconds())
                return

        send_mail(sender="TemPi <sigizmund@gmail.com>",
                  to="Roman Kirillov <sigizmund@gmail.com>",
                  subject="No TemPi activity for too long",
                  body=format(EMAIL_BODY, str(last_update_delta.total_seconds())))

        Notification(parent=THERMOMETER).put()

    def get(self):
        try:
            self.response.out.content_type = "text/plain"
            last = DataPoint.query(ancestor=THERMOMETER).order(-DataPoint.timestamp).fetch(1)[0]
            if not last:
                pass
            delta = datetime.now() - last.timestamp
            self.response.out.write("No events for " + str(delta.total_seconds()) + " seconds\n")
            self.notify(delta)
        except Exception as inst:
            send_mail(sender="TemPi <sigizmund@gmail.com>",
                      to="Roman Kirillov <sigizmund@gmail.com>",
                      subject="TemPi critical error",
                      body=inst.message)



app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/submit', SubmitDataHandler),
                                  ('/tasks/aggregate', AggregateTask),
                                  ('/tasks/watchdog', WatchdogTask)
                              ], debug=True)
