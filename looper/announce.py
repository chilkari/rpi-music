import rtmidi_python as rtmidi
from time import sleep

def announce():
    midi_out = rtmidi.MidiOut()
    
    nk = -1
    i = 0
    for port in midi_out.ports:
        print port
        if port.find('nanoKONTROL') > -1:
            nk = i
        i += 1
    
    if nk == -1:
        print "Unable to locate nanoKontrol"
        return
    
    
    midi_out.open_port(nk)
    
    # [rtmidi-python](https://github.com/superquadratic/rtmidi-python)

    # clear
    for i in range(24):
        midi_out.send_message([0x8C, i+24, 127])
    
    rep = 0
    while rep < 3:
        step = 0
        while step < 8:
            midi_out.send_message([0x9C, step+24, 127])
            midi_out.send_message([0x9C, 47-step, 127])
            step += 1
            sleep(0.1)
        for i in range(24):
            midi_out.send_message([0x8C, i+24, 127])
        rep += 1


if __name__ == '__main__':
    announce()
