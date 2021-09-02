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

device_id = "test-device"
client = mqtt.Client()
client.tls_set_context(mqtt_ssl.create_default_context())
client.username_pw_set(user, password)
client.connect(url, port)
client.tls_set_context(mqtt_ssl.create_default_context())

client.loop_start()

# Publish data
for count, line in enumerate(Lines):
    client.publish(topic="none/test-device/telemetry", payload=line.strip(), qos=0, retain=False)
    if count >= 10:
        break

client.loop_stop()

client.close()
