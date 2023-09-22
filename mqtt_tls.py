import time
from datetime import datetime
import paho.mqtt.client as mqtt
import ssl
import data
import streamlit as st
import pytz
timezone = pytz.timezone("Asia/Ho_Chi_Minh")  # Replace with your desired timezone
def parsetime(timestamp):
  
  timestamp_datetime = datetime.fromtimestamp(timestamp, tz=pytz.utc)
  
  localized_datetime = timestamp_datetime.astimezone(tz=timezone)
  formatted_datetime = localized_datetime.strftime("%Y-%m-%d %H:%M:%S %z")
 

  return formatted_datetime
def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("Connected with result code " + str(rc))   
  else:
    print("connection failed with rc: "+ str(rc))
  client.subscribe("temp/esp32")
def on_message(client,userdata,msg):

  print(str(msg.payload.decode("utf-8")))
  string = str(msg.payload.decode("utf-8")).split(" ")
  
  if msg.topic == "LED_Data":
    
    lampid = int(string[0])
    timed = parsetime(int(string[1]))
    state = int(string[2])
    dimming = int(string[3])
    flow = int(string[4])
    fake_time = datetime.strptime(timed,"%Y-%m-%d %H:%M:%S %z").replace(tzinfo= timezone)-datetime.now().astimezone(tz= timezone)
    if abs(fake_time.total_seconds())>=3600:
      data.supabase.table("Fake").insert({"lampid" :lampid,"timestamp": timed,"state":state,"dimming":dimming,"flow":flow }).execute()
    else:
      data.supabase.table("Events").insert({"lampid" :lampid,"timestamp": timed,"state":state,"dimming":dimming,"flow":flow }).execute()
      data.supabase.table("Light").update({'bright':dimming}).eq('id',lampid).execute()
  elif msg.topic == "Node_Dead":
    #timed = timezone.localize(datetime.utcfromtimestamp(int(string[0])).strftime('%Y-%m-%d %H:%M:%S'))
    times = parsetime(int(string[0])) 
    lampid = int(string[1])
    status = int(string[2])
    data.supabase.table("NodeDeath").insert({"time": times,"address":lampid,"status":status}).execute()   
  elif msg.topic == "Gateway_Alive":
    timed = parsetime(int(string[0]))
  
    node = int(string[1])
    data.supabase.table("GateAlive").insert({"time": timed,"status":node}).execute()
      
ca_cert = "ca.crt"   
broker_address = "xemdoan2408.duckdns.org"
broker_port = 1234  

temp_broker = "broker.emqx.io"
temp_port = 1883

topic_to_subscribe = "LED_Data"
client=mqtt.Client()

#client.tls_set(ca_certs=ca_cert,tls_version=ssl.PROTOCOL_TLSv1_2)
#client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

t = True

try :
    client.connect(temp_broker,port=temp_port)
    t = False
except:
    pass  
client.subscribe(topic_to_subscribe)
client.subscribe("Gateway_Alive")
client.subscribe("Node_Dead")
def on_off_client(s):
  client.publish("LED_Control/On_off", s)
def bright_client(s):
  client.publish("LED_Control/Dimming",s)
def time_setting(s):
  client.publish("LED_Control/Set_Time",s)
def fake_time(s):
  client.publish("NODE_Fake_time",s)
def start():
  client.loop_start()
def stop():
  client.loop_stop()





