import os
import random
import Adafruit_DHT

def read_sensor_data():
    sensor = Adafruit_DHT.DHT11
    pin = 4

    # yeah yeah I know about other architectures.
    # I will fix this at some point.
    if os.uname().machine == 'armv6l':
        return Adafruit_DHT.read_retry(sensor, pin)
    else:
        return (30*(1+random.random()), 15*(1+random.random()))
