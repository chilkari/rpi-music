#!/usr/bin/python

import sys
import rtmidi_python as rtmidi
from time import sleep

# [rtmidi-python](https://github.com/superquadratic/rtmidi-python)


class Announcer(object):
    def __init__(self):
        self.open_nano()
        if not self.mo:
            sys.exit(1)

    def open_nano(self):
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
        self.mo = midi_out

    def clear(self):
        for i in range(24):
            self.mo.send_message([0x8C, i+24, 127])
        for i in range(11):
            self.mo.send_message([0x8C, i, 127])

    def cycle_on(self):
        self.mo.send_message([0x9C, 0, 127])

    def cycle_off(self):
        self.mo.send_message([0x8C, 0, 127])
    
    def rew_on(self):
        self.mo.send_message([0x9C, 1, 127])

    def fwd_on(self):
        self.mo.send_message([0x9C, 2, 127])

    def stop_on(self):
        self.mo.send_message([0x9C, 3, 127])

    def play_on(self):
        self.mo.send_message([0x9C, 4, 127])

    def rec_on(self):
        self.mo.send_message([0x9C, 5, 127])

    def shutdown(self):
        self.clear()
        for i in range(24):
            self.mo.send_message([0x9C, i+24, 127])
        step = 0
        while step < 8:
            self.mo.send_message([0x8C, 47-step, 127])
            self.mo.send_message([0x8C, 39-step, 127])
            self.mo.send_message([0x8C, 31-step, 127])
            sleep(0.1)
            step += 1

    
    def spiral(self):
        self.clear()
        rep = 0
        while rep < 2:
            step = 0
            while step < 8:
                self.mo.send_message([0x9C, step+24, 127])
                self.mo.send_message([0x9C, 47-step, 127])
                step += 1
                sleep(0.1)
            for i in range(24):
                self.mo.send_message([0x8C, i+24, 127])
            rep += 1
    
    def announce(self, args):
        if len(args) != 2:
            print "usage: python announce.py [scene]"
            sys.exit(1)
        scene = args[1]
        if hasattr(self, scene):
            getattr(self, scene)()


if __name__ == '__main__':
    an = Announcer()
    an.announce(sys.argv)
