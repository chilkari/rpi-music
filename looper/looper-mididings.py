#!/usr/bin/python

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
pre = Print('input', portnames='in')
post = Print('output', portnames='out')


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
shutdown_r = False
shutdown_m = False
shutdown_s = False

def part_of_shutdown(ev):
    print "part_of_shutdown"
    global shutdown_r
    global shutdown_m
    global shutdown_s
    if ev.type == NOTEON:
        if ev.note == 47:
            shutdown_r = True
        if ev.note == 39:
            shutdown_m = True
        if ev.note == 31:
            shutdown_s = True
        if shutdown_r and shutdown_m and shutdown_s:
            print "ALL THREE DOWN! Would invoke audio/system shutdown here"
    if ev.type == NOTEOFF:
        if ev.note == 47:
            shutdown_r = False
        if ev.note == 39:
            shutdown_m = False
        if ev.note == 31:
            shutdown_s = False


scenes = {
    1: Scene("looper", [
        Channel(13) >> Port('NK2_OUT'),
        KeyFilter(notes=[47,39,31]) >> Process(part_of_shutdown),
        Filter(NOTE) >> Port('SL'),
    ])
}

run(
    # pre=pre, 
    # post=post, 
    scenes=scenes
)

