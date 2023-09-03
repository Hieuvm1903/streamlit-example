import time
import paho.mqtt.client as mqtt
import ssl


def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("Connected with result code " + str(rc))
    
  else:
    print("connection failed with rc: "+ str(rc))
  client.subscribe("temp/esp32")
def on_message(client,userdata,msg):
  print("received")
  print(msg.topic + ":" + str(msg.payload.decode("utf-8")))


ca_cert = "ca.crt"   
broker_address = "xemdoan2408.duckdns.org"
broker_port = 1234  
topic_to_subscribe = "LED_Data"
client=mqtt.Client("On/Off")

client.tls_set(ca_certs=ca_cert,tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port=broker_port)
client.on_message = on_message

def test():
  t=0
  client.subscribe(topic_to_subscribe)
  client.loop_start()
  while t == 0:
    #client.publish(topic_to_subscribe, "01 1")
      time.sleep(10)
      try:
        while True:
         pass
      except KeyboardInterrupt:
        client.loop_stop()
#     # 
# 
  






