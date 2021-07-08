import logging

import mido

from .Section import Section
from .. import Scene
from weather_symphony.music import Track

class StringSection(Section):

    def __init__(self, *args):
        super().__init__(*args)
        
        self.track = Track(48)

    def perform(self):
        logging.debug("Performing Strings")

        for i in range(24):
            if self.scenes[i] == Scene.NIGHT_CHILLY:
                self.track.addNote(64, i*16, 16)
            else:
                self.track.addNote(32, i*16, 8)
                self.track.addNote(39, i*16+8, 8)

        return self.track.export()