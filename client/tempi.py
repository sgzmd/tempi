from daemon import runner
import requests
import dht11
import logging
import time

from keyutils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IFFT_URL = "https://maker.ifttt.com/trigger/tempi/with/key/{}".format(GetIftttKeyOrDie())
THINGSPEAK_URL = "https://api.thingspeak.com/update?api_key={}".format(GetThingspeakKeyOrDie())

class TempiApp():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = 'log.txt'
        self.stderr_path = 'log.txt'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            (humidity, temperature) = dht11.read_sensor_data()

            logger.info("Temp={}, Humidity={}".format(temperature, humidity))

            # r = requests.post(IFFT_URL, data=None, json={
            #     'value1': temperature,
            #     'value2': humidity
            # })

            requests.get(THINGSPEAK_URL + "&field1={}&field2={}".format(temperature, humidity))


            time.sleep(5)
        # time.sleep(60 * 60 * 30) # wake up every 30 minutes

TempiApp().run()

#app = TempiApp()
#daemon_runner = runner.DaemonRunner(app)
#daemon_runner.do_action()
