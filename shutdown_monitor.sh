#!/bin/sh

# FIXME - We set this up to run from ~/.profile, which means it tries to
# run on any login. SSH'ing in will run it again (in addition to the one
# that runs on boot/auto-login). Modify this script so that if there
# is already a process, then bail out early.
# We should be able to simply grep the process table for shutdown_monitor

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

