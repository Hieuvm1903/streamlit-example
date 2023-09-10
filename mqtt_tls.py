import time
from datetime import datetime
import paho.mqtt.client as mqtt
import ssl
import data
import streamlit as st

def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("Connected with result code " + str(rc))
    
  else:
    print("connection failed with rc: "+ str(rc))
  client.subscribe("temp/esp32")
def on_message(client,userdata,msg):
  
  string = str(msg.payload.decode("utf-8")).split(" ")
  
  if msg.topic == "LED_Data":
    
    lampid = int(string[0])
    time = datetime.utcfromtimestamp(int(string[1])).strftime('%Y-%m-%d %H:%M:%S')
    state = int(string[2])
    dimming = int(string[3])
    flow = int(string[4])
    data.supabase.table("Events").insert({"lampid" :lampid,"timestamp": time,"state":state,"dimming":dimming,"flow":flow }).execute()
  elif msg.topic == "Node_Dead":
    time = datetime.utcfromtimestamp(int(string[0])).strftime('%Y-%m-%d %H:%M:%S')
    lampid = int(string[1])
    status = int(string[2])
    data.supabase.table("NodeDeath").insert({"time": time,"address":lampid,"status":status}).execute()
  elif msg.topic == "Gateway_Alive":
    time = datetime.utcfromtimestamp(int(string[0])).strftime('%Y-%m-%d %H:%M:%S')
    node = int(string[1])
    data.supabase.table("GateAlive").insert({"time": time,"status":node}).execute()


ca_cert = "ca.crt"   
broker_address = "xemdoan2408.duckdns.org"
broker_port = 1234  
topic_to_subscribe = "LED_Data"
client=mqtt.Client()

client.tls_set(ca_certs=ca_cert,tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message
t = True
while t:
  try :
    client.connect(broker_address,port=broker_port)
    t = False
  except:
    pass
client.subscribe(topic_to_subscribe)
client.subscribe("Gateway_Alive")
client.subscribe("Node_Dead")
client.loop_start()
def on_off_client(s):
  client.publish("LED_Control/On_off", s)
def bright_client(s):
  client.publish("LED_Control/Dimming",s)
def time_setting(s):
  client.publish("LED_Control/Set_Time",s)
def start():
  client.loop_start()
def stop():
  client.loop_stop()






