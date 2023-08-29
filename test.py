import paho.mqtt.client as mqtt
import time
from datetime import datetime
import random


mqttBroker = "xemdoan2408.duckdns.org"
port = 1234
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker,port)

while True:
    # payload = str(datetime.utcnow())
    device = "iCobanov"
    timestamp = datetime.utcnow()
    value = random.random()
    payload = "{},{},{}".format(device, timestamp, value)

    client.publish("temp/esp32", "hieu vm")
    print(payload)
    time.sleep(2.0)