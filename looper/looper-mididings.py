#!/usr/bin/python

import sys
import os
import subprocess
from time import sleep
import rtmidi_python as rtmidi
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

mo = None

def open_nano():
    global mo
    midi_out = rtmidi.MidiOut()
    nk = -1
    i = 0
    for port in midi_out.ports:
        if port.find('nanoKONTROL') > -1:
            nk = i
        i += 1
    
    if nk == -1:
        print "Unable to locate nanoKontrol"
        return None
    midi_out.open_port(nk)
    mo = midi_out
    blink = 0
    while blink < 5:
        blink += 1
        mo.send_message([0x9C, 0, 127])
        sleep(0.25)
        mo.send_message([0x8C, 0, 127])
        sleep(0.1)

open_nano()

# Track how button states for tracks should be lit
# Array length 24, 0-7 = lit state of S buttons (1=on, 0=off)
#     8-13  = lit state of M buttons
#     14-23 = lit state of R buttons
btn_state = [0] * 24

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

def state_change(ev):
    """ Handle these as toggles. """
    index = ev.note - 24
    if ev.type == NOTEON:
        btn_state[index] = 0 if btn_state[index] else 1
        # S/M for a track with R on, disables R. Reflect that...
        if index < 16:
            rindex = index + 8
            if index < 8:
                rindex = index + 16
            if btn_state[rindex]:
                btn_state[rindex] = 0
    else:
        send_state()

def send_state():
    global btn_state
    global mo
    for i in range(24):
        note = i + 24
        if btn_state[i]:
            mo.send_message([0x9c, note, 127])
        else:
            mo.send_message([0x8c, note, 127])

def function_handler(ev):
    """
    F1 + Record = Request shutdown (halt)
    F1 + Play   = Request restart
    F1 + Stop   = Bounce wlan0
    """
    global function_1
    global function_2
    global mo
    if ev.type == NOTEON:
        # Pass the noteon event through to the nano
        mo.send_message([0x9c, ev.note, 127])
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
                # F1+Rew = Reset Looper State
                reset_looper()
            if function_2:
                # F2+Rew - Refresh looper (stop SL/Restart, Reconnect)
                refresh_looper()
    elif ev.type == NOTEOFF:
        # Pass the noteoff event through to the nano
        # As long as its not the 'cycle' button
        if ev.note != 0:
            mo.send_message([0x8c, ev.note, 127])
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
    with open('/home/pi/rpi-music/reboot_request', 'w') as f:
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

def refresh_looper():
    subprocess.call(["/home/pi/rpi-music/looper/announce.py", "blink_twice"])
    subprocess.call(["/home/pi/rpi-music/rpi-audio", "refresh", "looper"])

scenes = {
    1: Scene("looper", [
        Channel(13) >> Filter(NOTE) >> KeyFilter(0,11) >> Process(function_handler),
        Channel(13) >> Filter(NOTE) >> KeyFilter(24,48) >> Process(state_change),
        Channel(13) >> Filter(NOTE) >> Port('SL'),
        Channel(13) >> Filter(CTRL) >> Port('SL'),
    ])
}

run(
    # pre=pre, 
    # post=post, 
    scenes=scenes
)

