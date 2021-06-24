import logging

import mido

from .Section import Section
from .. import Scene

class StringSection(Section):

    def perform(self):
        logging.debug("Performing Strings")

        track = mido.MidiTrack()
        track.append(mido.Message('program_change', program=48, time=0))

        for i in range(24):
            if self.scenes[i] == Scene.MILD_SUMMER:
                track.append(mido.Message('note_on', note=64, velocity=64, time=0))
                track.append(mido.Message('note_off', note=64, velocity=127, time=512))
            else:
                track.append(mido.Message('note_on', note=32, velocity=70, time=0))
                track.append(mido.Message('note_off', note=32, velocity=127, time=256))
                track.append(mido.Message('note_on', note=39, velocity=100, time=0))
                track.append(mido.Message('note_off', note=39, velocity=127, time=256))

        return track