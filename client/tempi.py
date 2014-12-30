__author__ = 'kirillov'

import random
import time
import urllib2 as u2
import logging

from daemonize import Daemonize
from optparse import OptionParser

PID = "/tmp/tempi.pid"
BASE_HOST = "tin-bronze2.appspot.com"

_LOGGER = None

parser = OptionParser()
parser.add_option("-d", "--daemonize", dest="daemonize", action="store_true",
                  help="Daemonize TemPi (default True) or run in foreground")

parser.add_option("-s", "--sleep_seconds", default=10, dest="sleep_seconds",
                  help="Sleep for this number of seconds")

parser.add_option("-f", "--log_file", default="/var/log/tempi.log", dest="log_file",
                  help="Logfile for application to use. Defaults to /var/log/tempi.log")


def get_current_temperature():
    """
    :rtype : float
    :return: current temperature from the sensor.
    """
    return 17 + 5 * random.random()

def report_temperature(temperature, base_host):
    url = "http://" + base_host + "/submit?temp=" + str(temperature)
    _LOGGER.info("Opening %s", url)
    u = u2.urlopen(url)

    _LOGGER.info("Code: %d, text: %s", u.code, u.read())


def configure_logger(options):
    global _LOGGER
    my_logger = logging.getLogger('tempi')
    my_logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(options.log_file,
                                                   maxBytes=20 * 1024 * 1024,
                                                   backupCount=5)

    my_logger.addHandler(handler)
    _LOGGER = my_logger

def run():
    global _LOGGER

    (options, args) = parser.parse_args()
    configure_logger(options)

    while True:
        report_temperature(get_current_temperature(), BASE_HOST)
        time.sleep(float(options.sleep_seconds))


def main():
    (options, args) = parser.parse_args()

    print options
    if not options.daemonize:
        logging.info("Running in foreground")
        run()
    else:
        daemon = Daemonize(app="TemPi", pid=PID, action=run)
        daemon.start()


if __name__ == '__main__':
    main()