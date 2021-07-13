# Experimenting with using Python as a midi device

import time

import mido

output = mido.open_output("My Output Device", virtual=True)

c_major = [60, 62, 64, 65, 67, 69, 71, 72]

for note in c_major:
    output.send(mido.Message("note_on", note=note))
    time.sleep(0.5)
    output.send(mido.Message("note_off", note=note))
