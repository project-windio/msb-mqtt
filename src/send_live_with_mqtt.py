import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl
import json
import pytz
from datetime import datetime
import zmq, socket, sys, logging, pickle

from example_send_logfile.login_details import url, port, user, password

# Set IDs and topic according to the WindIO specification.
edge_id = "urn:uni-bremen:bik:wio:1:1:msb:0001" # MSB in Krogmann nacelle (gateway)
device_id = "urn:uni-bremen:bik:wio:1:1:nacs:0001" # Acceleration of MSB in Krogmann nacelle
mqtt_topic = "ppmpv3/3/DDATA/" + edge_id + "/" + device_id

def create_mqtt_payload(unix_epoch=0, acc_x=0, acc_y=0, acc_z=0, id=None):
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
    time = datetime.fromtimestamp(float(unix_epoch), tz=pytz.utc).isoformat()
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

client = mqtt.Client()
print("Working with user: " + user)
client.username_pw_set(user, password)
client.connect(url, port)
print("Successfully connected.")
client.tls_set_context(mqtt_ssl.create_default_context())
client.loop_start()


# Receive data using ZMQ.
ipc_protocol = 'tcp://127.0.0.1'
ipc_port = '5556'
connect_to = f'{ipc_protocol}:{ipc_port}'
print(f'Trying to bind zmq to {connect_to}')

ctx = zmq.Context()
zmq_socket = ctx.socket(zmq.SUB)

try:
    zmq_socket.connect(connect_to)
except Exception as e:
    logging.fatal(f'Failed to bind to zeromq socket: {e}')
    sys.exit(-1)

# Subscribe to all available data.
zmq_socket.setsockopt(zmq.SUBSCRIBE, b'')

print('Successfully bound to zeroMQ receiver socket as subscriber')


while True:
    print('Entered the infinite loop.')
    try:
        print('Trying to receive data.')
        (zmq_topic, data) = zmq_socket.recv_multipart()
        zmq_topic = zmq_topic.decode('utf-8')
        data = pickle.loads(data)
        print(f'Received first data: {data}')
        print(f'From topic: {zmq_topic}')
        break
    except KeyboardInterrupt:
        print('Interrupted!')
    #except Exception as e:
    #    print(f'Failed to receive message: {e} ({topic} : {data})')
    #    continue

payload = create_mqtt_payload(unix_epoch=data[0], acc_x=data[2], acc_y=data[3], acc_z=data[4])
client.publish(mqtt_topic, payload)


client.loop_stop()

#client.close()
