#!/bin/sh

### BEGIN INIT INFO
# Provides:          rpi-audio
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Script to start/stop jackd and audio software
# Description:       Script to start/stop jackd and audio software
### END INIT INFO

prep_system() {
    # Shutdown unneeded things.
    echo "rpi-audio: Stopping unnecessary services..."
    sudo service ntp stop 2>&1 &
    sudo service triggerhappy stop 2>&1 &
    #sudo service dbus stop 2>&1 &
    #sudo killall console-kit-daemon 2>&1 &  (doesn't exist)
    #sudo killall pokitd 2>&1 & (doesn't exist)
    
    sudo mount -o remount,size=128M /dev/shm
    sudo killall gvfsd 2>&1 &
    #sudo killall dbus-daemon 2>&1 &
    #sudo killall dbus-launch 2>&1 &
    
    echo "rpi-audio: Setting CPU governor to performance..."
    echo -n performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
}

start_jack() {
    echo "rpi-audio: starting JackD..."
    RUNNING=`pgrep jackd`
    if [ "${#RUNNING}" -gt 0 ] ; then
        echo "JackD already running."
    else
        export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket
        #sudo -u pi jackd -P84 -p32 -t2000 -d alsa -dhw:Device -p 2048 -r 44100 -s -D -znone >> /home/pi/jack.log 2>&1 &
        sudo -u pi jackd -P84 -p32 -t2000 -d alsa -dhw:1 -p 2048 -n 4 -r 44100 -s -D -znone >> /home/pi/jack.log 2>&1 &
    fi
}

start_sooperlooper() {
    # Start SooperLooper
    echo "rpi-audio: starting SooperLooper..."
    RUNNING=`pgrep sooperlooper`
    if [ "${#RUNNING}" -gt 0 ] ; then
        echo "sooperlooper already running."
    else
        sudo -u pi sooperlooper -L /home/pi/rpi-music/looper/session.slsess -m /home/pi/rpi-music/looper/nk2.slb >> /home/pi/sooperlooper.log 2>&1 &
    fi
}

connect_jack() {
    echo "Connecting sooper loop to jack..."
    jack_connect sooperlooper:common_out_1 system:playback_1
    jack_connect sooperlooper:common_out_2 system:playback_2
    jack_connect system:capture_1 sooperlooper:common_in_1
    jack_connect system:capture_1 sooperlooper:common_in_2
}

connect_midi() {
    # Connect SooperLooper to NanoKontrol2 interface:
    echo "rpi-audio: Connecting NanoKontrol2 interface to SooperLooper..."
    nk=$(aconnect -i | grep client | grep -i "nanoKONTROL2" | cut -d " " -f2 | tr -d ":")
    echo "rpi-audio: NanoKontrol2: $nk"
    sooperlooper=$(aconnect -o | grep client | grep -i "sooperlooper" | cut -d " " -f2 | tr -d ":")
    echo "rpi-audio: sooperlooper: $sooperlooper"

    echo "rpi-audio: connecting nk2, $nk to sooperlooper: $sooperlooper"
    aconnect $nk $sooperlooper
}

# Handling for start/stop args
case "$1" in
  start)
    echo "rpi-audio: starting..." 
    prep_system
    start_jack
    sleep 3
    start_sooperlooper
    sleep 3
    connect_jack
    sleep 2
    connect_midi
    ;;
  stop)
    echo "rpi-audio: stopping..."
    killall sooperlooper
    killall jackd
    ;;
  clear)
    if [ -f /home/pi/sooperlooper.log ]; then
        sudo rm /home/pi/sooperlooper.log
    fi
    if [ -f /home/pi/jack.log ]; then
        sudo rm /home/pi/jack.log
    fi
    ;;
  *)
    echo "Usage: /etc/init.d/rpi-audio {start|stop|clear}"
    exit 1
    ;;
esac

exit 0