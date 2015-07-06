#!/bin/sh

while true
do
sfile="/home/pi/rpi-music/shutdown_request"
if [ -f $sfile ];
then
   echo "Shutdown requests exists. Shutting down!"
   /home/pi/rpi-audio/looper/rpi-audio stop
   sudo shutdown -h now
fi
sleep 5
done

