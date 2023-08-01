import requests
import time
import random
import json
import paho.mqtt.client as mqtt
#broker_address ="0.tcp.ap.ngrok.io"
broker_address = "test.mosquitto.org"
port= 1883
t=''
def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("Connected with result code " + str(rc))
    
  else:
    print("connection failed with rc: "+ str(rc))
  client.subscribe("temp/esp32")
def on_message(client,userdata,msg):
  print("da vao")
  print(msg.topic + ":" + str(msg.payload.decode("utf-8")))
  
while True:
  client=mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(broker_address,port=port)
  
  
  #print(t)
  



