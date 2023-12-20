# MQTT client for Motion Sensor Box in project WindIO

In the project WindIO measurements are conducted using motion sensor boxes. They send their data to a digital twin using the MQTT protocol.

WindIO's digital twin is being developed at https://github.com/project-windio/wt-digital-twin .

Motion Sensor Box is an open-source design: https://github.com/flucto-gmbh/motion-sensor-box

## Concept of client

Motion Sensor Box uses ZMQ for internal datastreams.

The MQTT client  listens to ZMQ to receive live data and sends them via MQTT to the WindIO broker.

An example payload is shown in [example_payload.json](example_payload.json).

This issue describes the idea: https://github.com/flucto-gmbh/motion-sensor-box/issues/27

## Installation on sensor box

Clone the package (preferred location: motion-sensor-box/src/mqtt):

```
git clone https://github.com/project-windio/msb-mqtt.git
```

Install the requirements:

```
pip install -r requirements.txt
```

Adapt the config to fit the specific sensor box by opening the JSON config file:

```
nano src/msb_mqtt.json
```

## Run the client

```
python src/msb_mqtt.py
```

To keep it running when you quit ssh:

```
python src/msb_mqtt.py > /dev/null 2>&1 &
```

or

```
nohup python src/msb_mqtt.py &
```


## Troubleshooting

To check wheter msb_mqtt.py is running type:

```
ps -ef
```

You may run intro problems if the MSB SD card runs full.

You can make new room by deleting log files located in home/pi/msb_data.

You may want to copy them first by typing

```
scp -i "LOCATION\TO\.ssh\ssh_key\msb_key" pi@msb-0003-a.local:/home/pi/msb_data/MSB-0003-A/msb-0003-a_20220703* "C:\LOCATION\TO\log-files"
```

Consider not running the fusion log service which creates these log files if you are ok with only storing files on the MQTT remote server.
