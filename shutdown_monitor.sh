#!/bin/sh

# This file is simply watching for the presence of a shutdown_request file
# which is typically put there by a mididings process, in response to some
# controller pushes. If this monitor sees that file, it stops the audio
# and shutdown down the RPi.

# Define your machine type here {looper|sampler|organ}
MACHINE_TYPE=looper

# First, see if shutdown_monitor is already running. (This happens if you
# boot the RPi, then login from a console, which tries to run it again)
echo "FIXME - NEED TO REPAIR CHECK FOR RUNNING IN SHUTDOWN MONITOR. IF LOGGING IN _ PLEASE KILL EXTRA PROCS"
# RUNNING=`ps -ef | sed -n /sudo.*[s]hutdown_monitor.sh/p`
# if [ "${RUNNING:-null}" != null ]; then
#     echo "Shutdown monitor already running. Aborting..."
#     exit 1
# fi

sfile="/home/pi/rpi-music/shutdown_request"
rfile="/home/pi/rpi-music/reboot_request"
# Upon booting, we don't immediately want to honor a shutdown request
if  [ -f $sfile ];
then
    rm $sfile
fi
# Reboot request - clear if present at startup
if  [ -f $rfile ];
then
    rm $rfile
fi


while true
do
if [ -f $sfile ];
then
   rm $sfile
   /home/pi/rpi-audio/looper/rpi-audio stop $MACHINE_TYPE
   sudo shutdown -h now
fi
if [ -f $rfile ];
then
   rm $rfile
   /home/pi/rpi-audio/looper/rpi-audio stop $MACHINE_TYPE
   sudo shutdown -r now
fi
sleep 5
done

