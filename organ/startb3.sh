#!/bin/sh

# Start JACK
echo "starting JackD..."
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket
jackd -P84 -p32 -t2000 -d alsa -dhw:Device -p 256 -n 2 -r 44100 -s -P -znone &

sleep 3

# Start setBfree
echo "starting setBfree..."
setBfree midi.driver=alsa midi.controller.upper.30=overdrive.enable whirl.speed-preset=1 whirl.horn.acceleration=1.0 whirl.horn.deceleration=1.3 whirl.horn.fastrpm=432.36 whirl.drum.fastrpm=357.3 reverb.wet=0.2 reverb.dry=0.8 &

sleep 3

# Connect setBFree to USB 1x1 interface:
echo "Connecting MIDI interface to setBfree..."
midi=$(aconnect -i | grep client | grep -i "USB MS1x1" | cut -d " " -f2 | tr -d ":")
echo "midi: $midi"
setbfree=$(aconnect -o | grep client | grep -i "SETBFREE" | cut -d " " -f2 | tr -d ":")
echo "setbfree: $setbfree"
aconnect $midi $setbfree

