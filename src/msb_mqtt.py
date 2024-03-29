import paho.mqtt.client as mqtt
from paho.mqtt.client import ssl as mqtt_ssl
import pytz, zmq, sys, logging, pickle, json
from datetime import datetime
from os import path
import time


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

# The  complete script is restarted in regular intervals
restart_after_seconds = 60

while True:
    elapsed_time_seconds = 0
    start_time = datetime.now()
    # Read config.
    with open(path.join("src", "msb_mqtt.json")) as json_file:
        config = json.load(json_file)
        print(config)
        user = config['user']
        password = config['password']
        url = config['url']
        port = config['port']
        edge_id = config['edge_id']
        device_id = config['device_id']
        mqtt_topic = "ppmpv3/3/DDATA/" + edge_id + "/" + device_id
        do_print = config['print']
        
    client = mqtt.Client()
    print("Working with user: " + user)
    client.username_pw_set(user, password)
    client.connect(url, port=port, keepalive=60*60*12)
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

    is_first_data = True
    print('Trying to receive data.')
    while elapsed_time_seconds < restart_after_seconds:
        try:
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
            (zmq_topic, data) = zmq_socket.recv_multipart(flags=zmq.NOBLOCK)
            zmq_topic = zmq_topic.decode('utf-8')
            data = pickle.loads(data)
            if is_first_data:
                print(f'Received first data: {data}')
                print(f'From topic: {zmq_topic}')
                is_first_data = False
            if zmq_topic == 'imu':
                if do_print:
                    print(f'Will send data via MQTT: {data}')
                payload = create_mqtt_payload(unix_epoch=data[0], acc_x=data[2], acc_y=data[3], acc_z=data[4])
                client.publish(mqtt_topic, payload)
            else:
                print(f'Only topic "imu" is used, however I received data on topic: {zmq_topic}')
            continue
        except KeyboardInterrupt:
            client.loop_stop()
            print('Interrupted!')
            pass
        except Exception as e:
            print(f'Error: {e}')
            print("Continuing in 1 second")
            time.sleep(1.0)
            continue
    continue
