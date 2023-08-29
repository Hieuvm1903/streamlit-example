import requests
import time
import random
import json
import paho.mqtt.client as mqtt
import ssl
#broker_address ="0.tcp.ap.ngrok.io"

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


ca_cert = "C:\Users\Admin\Documents\GitHub\streamlit-example\ca.crt"   
broker_address = "xemdoan2408.duckdns.org"
broker_port = 1234  # Default port for MQTT with TLS
def test():
  while True:
    client=mqtt.Client()
    client.tls_set(ca_certs=ca_cert,tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address,port=broker_port)
    client.publish("test_topic", "From HieuVM")
    print("abc")
    time.sleep(1)



  
  
  #print(t)





