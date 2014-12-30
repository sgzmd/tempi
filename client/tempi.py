__author__ = 'kirillov'

import random
import time
import urllib2 as u2

import logging

from daemonize import Daemonize

logging.basicConfig()

from optparse import OptionParser

PID = "/tmp/tempi.pid"
BASE_HOST = "tin-bronze2.appspot.com"

parser = OptionParser()
parser.add_option("-d",  "--daemonize",
                  dest="daemonize",
                  action="store_true",
                  help="Daemonize TemPi (default True) or run in foreground")

parser.add_option("-s", "--sleep_seconds", default=10, dest="sleep_seconds",
                  help="Sleep for this number of seconds")


def get_current_temperature():
  return 17 + 5 * random.random()


def report_temperature(temperature, base_host):
  url = "http://" + base_host + "/submit?temp=" + str(temperature)
  print "Opening " + url
  u = u2.urlopen(url)

  print u.code
  print u.read()


def run(sleep_seconds):
  while True:
    report_temperature(get_current_temperature(), BASE_HOST)
    time.sleep(sleep_seconds)

def run_daemon():
  (options, args) = parser.parse_args()
  run(options.sleep_seconds)

def main():
  (options, args) = parser.parse_args()

  print options

  if not options.daemonize:
    logging.info("Running in foreground")
    run(options.sleep_seconds)
  else:
    daemon = Daemonize(app="TemPi", pid=PID, action=run_daemon)
    daemon.start()

if __name__ == '__main__':
  main()