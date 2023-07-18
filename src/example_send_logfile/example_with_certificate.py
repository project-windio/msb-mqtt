import paho.mqtt.client as mqtt
import json
import os.path
from utils import log_to_mqtt_payload
from os.path import dirname, abspath


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Read the login data
with open(os.path.dirname(__file__) + '/certificate_login.json') as json_file:
    config = json.load(json_file)
    print('Working with login data:')
    print(config)
    user = config['user']
    password = config['password']
    url = config['url']
    port = config['port']


client.tls_set(os.path.dirname(__file__) + "/server.pem", os.path.dirname(__file__) + "/client-cert-bikbox.pem",
                os.path.dirname(__file__) + "/decrypted-client-key-bikbox.pem")
client.username_pw_set(user, password)

client.connect(host=url, port=port, keepalive=60)

client.loop_start()

# Load data.
file = open(os.path.dirname(__file__) + "/test.log", "r")
lines = file.readlines()
send_n_lines = 5

# Print data.
count = 0
for count, line in enumerate(lines):
    print("Line {}: {}".format(count + 1, line.strip())) # Strips the newline character.
    if count >= send_n_lines - 1:
        break
print("Successfully printed the logfile.")

# Publish data.
mqtt_topic = "Example topic"
device_id = "424242"
print("topic: " + mqtt_topic)
for count, line in enumerate(lines):
    payload = log_to_mqtt_payload(line.strip(), device_id)
    print("payload:")
    print(payload)
    client.publish(mqtt_topic, payload)
    if count >= send_n_lines - 1:
        break

client.loop_end()
