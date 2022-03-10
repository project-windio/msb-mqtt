# Thanks to https://www.hivemq.com/blog/mqtt-client-library-paho-python/
# See example titled "Subscribe"

import paho.mqtt.client as paho
import sys, os.path
sys.path.append(os.path.abspath('../'))
from login_details import url, port, user, password
from example import topic

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.username_pw_set(user, password)
client.connect(url, port)
client.subscribe(topic, qos=1)

client.loop_forever()