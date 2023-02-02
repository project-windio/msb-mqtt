#!/bin/bash
echo "startstoploop.sh is starting."
for i in {1..5}
do
    sleep .5 # Waits 0.5 second.
    echo "Running msb_mqtt.py"
    python src/msb_mqtt.py
    sleep 5 # Waits 5 second.
    echo "Terminating msb_mqtt.py"
    pkill -9 -f msb_mqtt.py.py #Thanks to: https://superuser.com/questions/446808/how-to-manually-stop-a-python-script-that-runs-continuously-on-linux
done
echo "startstoploop.sh is terminating."
sleep .5 # Waits 0.5 second.
