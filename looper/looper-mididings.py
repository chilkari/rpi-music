#!/usr/bin/python

import os
from mididings import *
from mididings.extra import *

# some classes are defined in separate modules because they depend on
# additional Python packages to be installed. uncomment these imports if you
# need them
#from mididings.extra.osc import OSCInterface
#from mididings.extra.inotify import AutoRestart

config(
    in_ports=['NK2_IN'],
    out_ports=['SL','NK2_OUT'],
)

# Uncomment for logging of all events
# pre = Print('input', portnames='in')
# post = Print('output', portnames='out')


# READY function - show user that we're ready to go:
# Blink the far right Solo/Mute/Record LEDs 3 times.
# They're mapped to notes 47(R), 39(M) and 31(S)
#    Hex versions: 2F(R), 27(M), and 1F(S)
# Knob 8 is CC 87, and Fader 8 is CC79 - should I think of something for them.
# def show_ready():
#     # NoteOnEvent(port, channel, note, velocity)
#     solo_on = NoteOnEvent('NK2_OUT', 13, 31, 127)


# FIXME - build some 'status' calls that can be invoked by sending midi events
# directly to mididings (which wouldn't normally come from the NK2) which then
# kick of lighting of status lights.


# To request a shutdown, user must hold all three of the
# 8th track's record, mute and solo buttons down. These
# flags store each state
shutdown_a = False
shutdown_b = False
shutdown_c = False
shutdown_d = False

def part_of_shutdown(ev):
    print "part_of_shutdown"
    global shutdown_a
    global shutdown_b
    global shutdown_c
    global shutdown_d
    if ev.type == NOTEON:
        if ev.note == 0:
            shutdown_a = True
        if ev.note == 6:
            shutdown_b = True
        if ev.note == 7:
            shutdown_c = True
        if ev.note == 8:
            shutdown_d = True
        if shutdown_a and shutdown_b and shutdown_c and shutdown_d:
            # TODO/FIXME - blink transport lights indicating shutdown
            # Ideally, rpi-audio stop will turn off 'power' light when done stopping
            # This won't work. I'm thinking I'll need to have a script running as root
            # which looks for the presence of some sort of 'shutdown request' file. If
            # it sees it (checks every 5-10 seconds or something), it deletes the file
            # then shuts down. I would write that file here.
            # Better approach if its running: use dbus to communicate from here to
            # the running-as-root shutdown script.
            print "SHUTDOWN REQUESTED. TODO - implement me."
            with open('/home/pi/rpi-music/shutdown_request', 'w') as f:
                f.write('shutdown, please!')

    if ev.type == NOTEOFF:
        if ev.note == 0:
            shutdown_a = False
        if ev.note == 6:
            shutdown_b = False
        if ev.note == 7:
            shutdown_c = False
        if ev.note == 8:
            shutdown_d = False


scenes = {
    1: Scene("looper", [
        Channel(13) >> Port('NK2_OUT'),
        KeyFilter(notes=[0,6,7,8]) >> Process(part_of_shutdown),
        Filter(NOTE) >> Port('SL'),
        Filter(CTRL) >> Port('SL'),
    ])
}

run(
    # pre=pre, 
    # post=post, 
    scenes=scenes
)

