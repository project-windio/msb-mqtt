# MQTT client for the motion sensor box

In these examples data from the MSB logfile are sent.

example_send_logfile.py sends data to the Contact broker.
example_subscribe.py listens to the Contact broker.
example_with_certificae.py sends data to the BIBA broker using certificates.

## Format of log file
### IMU
imu: [unix epoch, uptime in seconds, accx, accy, accz, rotx_speed, roty_speed, rotz_speed, magnet_fieldx, magnet_fieldy, magnet_fieldz]
unit: [X, s, g, g, g, deg/s, deg/s, deg/s, mu tesla, mu tesla, mu tesla]


### GPS
gps: [unix epoch, uptime in seconds, JSON from receiver]

JSON keys from receiver: 
 - 'mode' = [0,3], 0 = I have nothing, 1 = I have time fix (one satellite), 2 = 2D fix (at least two satellites), 3 = 3D fix (more than two satellites)
 - 'tune' = unix epoch in an ISO format (jahr-monat-tagThh:minmin:secsec:timezone)
 - 'leapseconds' = Schaltsekunden
 - 'ept' = we dont know
 - 'lat' = latitude
 - 'lon' = longitude
 - 'altHAE' = altitude
 - 'altMSL' = altitude from mean sea level
 - 'epx', 'epy' = current size of error (m)
 - 'epv' = current size of error (m/s)
 - 'magvar' = correction factor for lat/lon
