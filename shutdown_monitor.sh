#!/bin/sh

sfile="/home/pi/rpi-music/shutdown_request"
# Upon booting, we don't immediately want to honor a shutdown request
if  [ -f $sfile ];
then
    rm $sfile
fi

while true
do
if [ -f $sfile ];
then
   rm $sfile
   /home/pi/rpi-audio/looper/rpi-audio stop
   sudo shutdown -h now
fi
sleep 5
done

