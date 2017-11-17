from daemon import runner
import requests
import dht11
import logging
import time

from keyutils import GetKeyOrDie
IFFT_URL = "https://maker.ifttt.com/trigger/tempi/with/key/{}".format(GetKeyOrDie())

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

            r = requests.post(IFFT_URL, data=None, json={
                'value1': temperature,
                'value2': humidity
            })


            time.sleep(5)
        # time.sleep(60 * 60 * 30) # wake up every 30 minutes

app = TempiApp()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
