#!/usr/bin/python

import sys
import os
import subprocess
from mididings import *
from mididings.extra import *
from mididings.extra.osc import SendOSC

import liblo

# some classes are defined in separate modules because they depend on
# additional Python packages to be installed. uncomment these imports if you
# need them
#from mididings.extra.osc import OSCInterface
#from mididings.extra.inotify import AutoRestart

# Overview/Notes
# Control SooperLooper from a NanoKontrol2
# track left/right, marker set, left, right have no lights, and are used
# as 'function' keys.

SLPORT = 9951

config(
    in_ports=['NK2_IN'],
    out_ports=['SL','NK2_OUT'],
)

# Uncomment for logging of all events
# pre = Print('input', portnames='in')
# post = Print('output', portnames='out')


# Function key handling.
# Track left is Func 1, Track right is Func 2

function_1 = False
function_2 = False

def function_handler(ev):
    """
    F1 + Record = Request shutdown (halt)
    F1 + Play   = Request restart
    F1 + Stop   = Bounce wlan0
    """
    global function_1
    global function_2
    if ev.type == NOTEON:
        if ev.note == 9:   # Track Left
            function_1 = True
        if ev.note == 10:  # Track Right
            function_2 = True
        if ev.note == 5:   # Record
            if function_1:
                # F1+Record: Signal shutdown request
                request_shutdown()
        if ev.note == 4:   # Play
            if function_1:
                # F1+Play: Signal reboot request
                request_reboot()
        if ev.note == 3:   # Stop
            if function_1:
                # F1+Stop: Bounce wlan0
                bounce_wlan()
        if ev.note == 2:   # Fwd
            if function_1:
                # F1+Fwd = ?
                pass
        if ev.note == 1:   # Rew
            if function_1:
                # F1+Rew = Reset Looper
                reset_looper()
    elif ev.type == NOTEOFF:
        if ev.note == 9:   # Track Left
            function_1 = False
        if ev.note == 10:  # Track Right
            function_2 = False
    

def request_shutdown():
    subprocess.call(["/home/pi/rpi-music/looper/announce.py", "blink_thrice"])
    with open('/home/pi/rpi-music/shutdown_request', 'w') as f:
	f.write('halt')

def request_reboot():
    subprocess.call(["/home/pi/rpi-music/looper/announce.py", "blink_twice"])
    with open('/home/pi/rpi-music/shutdown_request', 'w') as f:
	f.write('reboot')

def bounce_wlan():
    subprocess.call(["/home/pi/rpi-music/looper/announce.py", "blink_once"])
    subprocess.call(["/home/pi/rpi-music/bounce_wlan.sh"])

def reset_looper():
    subprocess.call(["/home/pi/rpi-music/looper/announce.py", "blink_once"])
    # Straight liblo here for OSC
    try:
        # ping for testing...
        # liblo.send(SLPORT, "/ping", "osc.udp://127.0.0.1:9999", "/pong")
        # Pause the loops
        liblo.send(SLPORT, "/sl/-1/hit", "pause")
        liblo.send(SLPORT, "/load_session", "/home/pi/rpi-music/looper/session.slsess", "osc.udp://127.0.0.1:9999", "/load_errors")
    except:
        print sys.exc_info()

scenes = {
    1: Scene("looper", [
        Channel(13) >> Port('NK2_OUT'),
        Filter(NOTEON) >> KeyFilter(0,10) >> Process(function_handler),
        Filter(NOTE) >> Port('SL'),
        Filter(CTRL) >> Port('SL'),
    ])
}

run(
    # pre=pre, 
    # post=post, 
    scenes=scenes
)

