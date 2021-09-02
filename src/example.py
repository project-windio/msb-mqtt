import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl

from login_details import url, port, user, password

device_id = "test-device"

client = mqtt.Client()

client.tls_set_context(mqtt_ssl.create_default_context())
client.username_pw_set(user, password)
client.connect(url, port)

client.tls_set_context(mqtt_ssl.create_default_context())

client.loop_start()

# Publish example.
client.publish(topic="none/test-device/telemetry", payload='{"test": 42}', qos=0, retain=False)

client.loop_stop()
client.close()
