import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl
import json
import os.path
from .utils import log_to_mqtt_payload


# Read the config.
with open(os.path.dirname(__file__) + '/../msb_mqtt.json') as json_file:
    config = json.load(json_file)
    print('Working with config:')
    print(config)
    user = config['user']
    password = config['password']
    url = config['url']
    port = config['port']
    edge_id = config['edge_id']
    device_id = config['device_id']
    mqtt_topic = "ppmpv3/3/DDATA/" + edge_id + "/" + device_id

client = mqtt.Client()
print("Working with user: " + user)
client.username_pw_set(user, password)
client.connect(url, port)
print("Successfully connected.")
client.tls_set_context(mqtt_ssl.create_default_context())

client.loop_start()

# Load data.
file1 = open("test.log", "r")
Lines = file1.readlines()
send_n_lines = 5

# Print data.
count = 0
for count, line in enumerate(Lines):
    #print("Line {}: {}".format(count + 1, line.strip())) # Strips the newline character.
    if count >= send_n_lines - 1:
        break
#print("Successfully printed the logfile.")

# Publish data.
print("topic: " + mqtt_topic)
for count, line in enumerate(Lines):
    payload = log_to_mqtt_payload(line.strip(), device_id)
    print("payload:")
    print(payload)
    client.publish(mqtt_topic, payload)
    if count >= send_n_lines - 1:
        break

client.loop_stop()
#client.close()
