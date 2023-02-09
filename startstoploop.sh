#!/bin/bash
echo "startstoploop.sh is starting."
RESTART_TIME=5 # in seconds
WAIT_TIME_DISPLAY_MSG=0.5 # in seconds
while true
do
    sleep $WAIT_TIME_DISPLAY_MSG
    echo "Running msb_mqtt.py"
    python src/msb_mqtt.py
    sleep $RESTART_TIME
    echo "Terminating msb_mqtt.py"
    pkill -9 -f msb_mqtt.py.py # Kill unix process, thanks to: https://superuser.com/questions/446808/how-to-manually-stop-a-python-script-that-runs-continuously-on-linux
done
echo "startstoploop.sh is terminating."
sleep $WAIT_TIME_DISPLAY_MSG
