import paho.mqtt.client as mqtt
import json
import os.path


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Read the login data
with open(os.path.dirname(__file__) + '/example_with_certificate_login.json') as json_file:
    config = json.load(json_file)
    print('Working with login data:')
    print(config)
    user = config['user']
    password = config['password']


client.tls_set(os.path.dirname(__file__) + "/server.pem", os.path.dirname(__file__) + "/client-cert-bikbox.pem",
                os.path.dirname(__file__) + "/decrypted-client-key-bikbox.pem")
client.username_pw_set(user, password)

client.connect("mqtt.brementestturbine.science", 8883, 60)

client.loop_forever()
