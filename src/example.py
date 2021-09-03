import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl

from login_details import url, port, user, password

# Print log file.
file1 = open("test.log", "r")
Lines = file1.readlines()
count = 0
for count, line in enumerate(Lines):
    print("Line {}: {}".format(count + 1, line.strip())) # Strips the newline character.
    if count >= 10:
        break
print("Successfully printed the logfile.")

# Set ID according to the WindIO specification.
device_id = "urn:uni-bremen:bik:wio:0:1:msb:0001"

client = mqtt.Client()
#client.tls_set_context(mqtt_ssl.create_default_context())
#client.username_pw_set(user, password)
client.connect(url, port)
client.tls_set_context(mqtt_ssl.create_default_context())

client.loop_start()

# Publish data
for count, line in enumerate(Lines):
    client.publish(topic="encyclopedia/windio", payload=line.strip())
    if count >= 10:
        break

client.loop_stop()

#client.close()
