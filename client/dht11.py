import Adafruit_DHT

def read_sensor_data():
    sensor = Adafruit_DHT.DHT11
    pin = 4
    return Adafruit_DHT.read_retry(sensor, pin)
