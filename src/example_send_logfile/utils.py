import pytz
import json
from datetime import datetime

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

