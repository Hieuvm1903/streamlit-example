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
  print(msg.topic + ":" + str(msg.payload))


ca_cert = "ca.crt"   
broker_address = "xemdoan2408.duckdns.org"
broker_port = 1234  # Default port for MQTT with TLS
topic_to_subscribe = "test_topic"
client=mqtt.Client()
client.tls_set(ca_certs=ca_cert,tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port=broker_port)
client.subscribe(topic_to_subscribe)
def test():
  t=0
  while t<=20:
    
    client.publish("test_topic", "From HieuVM")
    t+=1
    time.sleep(1)
# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
  
  #print(t)





