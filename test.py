import paho.mqtt.client as mqtt
import time
from datetime import datetime
import random


mqttBroker = "0.tcp.ap.ngrok.io:18474"
mqttBroker = "test.mosquitto.org"
port = 1883
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker,port)

while True:
    # payload = str(datetime.utcnow())
    device = "iCobanov"
    timestamp = datetime.utcnow()
    value = random.random()
    payload = "{},{},{}".format(device, timestamp, value)

    client.publish("temp/esp32", "Duong an com")
    print(payload)
    time.sleep(2.0)