# MQTT client for Motion Sensor Box in project WindIO

In the project WindIO measurements are conducted using motion sensor boxes. They send their data to a digital twin using the MQTT protocol.

WindIO's digital twin is being developed at https://github.com/project-windio/wt-digital-twin .
Motion Sensor Box is an open-source design: https://github.com/flucto-gmbh/motion-sensor-box

## Concept of client

Motion Sensor Box uses ZMQ for internal datastreams.
The MQTT client will listen to ZMQ to get live data and will send them.
It will be implemented as a service.

This issue describes the idea: https://github.com/flucto-gmbh/motion-sensor-box/issues/27
