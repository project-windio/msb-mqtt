import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl
import json
import pytz
from datetime import datetime
import sys, os.path
sys.path.append(os.path.abspath('../'))
from login_details import url, port, user, password

# Set IDs and topic according to the WindIO specification.
edge_id = "urn:uni-bremen:bik:wio:1:1:msb:0001" # MSB in Krogmann nacelle (gateway)
device_id = "urn:uni-bremen:bik:wio:1:1:nacs:0001" # Acceleration of MSB in Krogmann nacelle
topic = "ppmpv3/3/DDATA/" + edge_id + "/" + device_id

def log_to_mqtt_payload(log_line, id=None):
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
    time = log_line.split(",")[0]
    time = time.split("[")[1]
    time = datetime.fromtimestamp(float(time), tz=pytz.utc).isoformat()
    acc_x = log_line.split(",")[2].strip()
    acc_y = log_line.split(",")[3].strip()
    acc_z = log_line.split(",")[4].strip()
    g = 9.81 # Acceleration due to gravity.
    dict = {
        "content-spec": "urn:spec://eclipse.org/unide/measurement-message#v3",
        "device": {
            "id": id
        },
        "measurements": [
            {
            "context": {
                "acc_x":  {
                    "unit": "m s-2"
                },
                "acc_y":  {
                    "unit": "m s-2"
                },
                "acc_z":  {
                    "unit": "m s-2"
                }
            },
            "ts": time,
            "series": {
                "time": [
                0
                ],
                "acc_x": [
                    float(acc_x) * g
                ],
                "acc_y": [
                    float(acc_y) * g
                ],
                "acc_z": [
                    float(acc_z) * g
                ]
            }
            }
        ]
    }
    payload = json.dumps(dict, indent=4) 
    return payload


# Print log file.
send_n_lines = 5
file1 = open("test.log", "r")
Lines = file1.readlines()
count = 0
for count, line in enumerate(Lines):
    #print("Line {}: {}".format(count + 1, line.strip())) # Strips the newline character.
    if count >= send_n_lines - 1:
        break
#print("Successfully printed the logfile.")

client = mqtt.Client()
print("Working with user: " + user)
client.username_pw_set(user, password)
client.connect(url, port)
print("Successfully connected.")
client.tls_set_context(mqtt_ssl.create_default_context())



client.loop_start()

# Publish data
print("topic: " + topic)
for count, line in enumerate(Lines):
    payload = log_to_mqtt_payload(line.strip(), device_id)
    print("payload:")
    print(payload)
    client.publish(topic, payload)
    if count >= send_n_lines - 1:
        break

client.loop_stop()

#client.close()
