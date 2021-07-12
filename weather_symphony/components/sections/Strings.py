import logging
from random import randint

from .Section import Section
from .. import Scene
from weather_symphony.music import Track, Meter
from weather_symphony.music import util as mutil

class StringSection(Section):

    def __init__(self, *args):
        super().__init__(*args)
        
        self.track = Track(48)

    def create_new_rhythm(self, scene):
        self.rhythm = mutil.generate_rhythm(4, False)

    def perform_bar(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        last_scene = self.scenes[bar_num-1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if cur_scene != last_scene:
            self.create_new_rhythm(cur_scene)

        time_in_bar = 0
        for duration in self.rhythm:
            degree = randint(1,8)
            note = self.key.get_note(degree, octave=2)
            self.track.add_note(note, bar_base_time + time_in_bar, duration)
            time_in_bar += duration

    def perform(self):
        logging.debug("Performing Strings")

        last_scene = None
        for i in range(Meter.total_bars):
            self.perform_bar(i)

        return self.track.export()