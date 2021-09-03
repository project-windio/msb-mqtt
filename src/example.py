import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl
import json

from login_details import url, port, user, password, topic

def log_to_mqtt_payload(log_line, id="urn:uni-bremen:bik:wio:0:1:msb:0001"):
    """
    Creates a WindIO MQTT payload based on a motion sensor box log file line.

    Example for payload from WindIO documentation:
    {
    "content-spec": "urn:spec://eclipse.org/unide/measurement-message#v3",
    "device": {
        "id": "urn:uni-bremen:bik:wio:1:1:wind:1234"
    },
    "measurements": [
        {
        "context": {
            "temperature":  {
            "unit": "Cel"
            }
        },
        "ts": "2021-05-18T07:43:16.969Z",
        "series": {
            "time": [
            0
            ],
            "temperature": [
            35.4231
            ]
        }
        }
    ]
    }

    """
    dict = {
        "content-spec": "urn:spec://eclipse.org/unide/measurement-message#v3",
        "device": {
            "id": id
        },
        "measurements": [
            {
            "context": {
                "acceleration in x":  {
                "unit": "m s-2"
                }
            },
            "ts": "2021-05-18T07:43:16.969Z",
            "series": {
                "time": [
                0
                ],
                "temperature": [
                log_line[9:28:1]
                ]
            }
            }
        ]
    }
    payload = json.dumps(dict, indent=4) 
    return payload


# Print log file.
file1 = open("test.log", "r")
Lines = file1.readlines()
count = 0
for count, line in enumerate(Lines):
    print("Line {}: {}".format(count + 1, line.strip())) # Strips the newline character.
    if count >= 10:
        break
print("Successfully printed the logfile.")

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(url, port)
client.tls_set_context(mqtt_ssl.create_default_context())



client.loop_start()

# Publish data
for count, line in enumerate(Lines):
    payload = log_to_mqtt_payload(line.strip())
    client.publish(topic=topic, payload="count " + str(count) + " " + payload)
    if count >= 10:
        break

client.loop_stop()

#client.close()
