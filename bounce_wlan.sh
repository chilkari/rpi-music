#!/bin/sh

# Simply take the wlan0 interface down and back up.
# Meant to be used for troubleshooting if the RPI drops its wifi connection.

sudo ifdown wlan0
sudo ifup wlan0
exit 0

