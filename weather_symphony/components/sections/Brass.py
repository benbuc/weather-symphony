import logging
from random import randint

import mido

from .Section import Section
from .. import Scene
from weather_symphony.music import Track, Meter

class BrassSection(Section):

    def __init__(self, *args):
        super().__init__(*args)
        
        self.track = Track(72)

    def generate_rhythm(self, max_subdivs, repeat_beats=True):
        """
        Returns an array of note durations
        The sum has to span a full bar

        max_subdivs per bar
        if larger than 1 it repeats for every beat 
        """

        assert not repeat_beats or max_subdivs > Meter.beats_per_bar
        assert max_subdivs <= Meter.max_subdivs

        if repeat_beats and max_subdivs > Meter.beats_per_bar:
            subdivs_per_beat = max_subdivs // Meter.beats_per_bar
            shortest_dur = Meter.max_subdivs // max_subdivs
            max_subdivided = [shortest_dur] *  (subdivs_per_beat // shortest_dur)
            assert sum(max_subdivided) == (Meter.max_subdivs // Meter.beats_per_bar)
        else:
            shortest_dur = Meter.max_subdivs // max_subdivs
            max_subdivided = [shortest_dur] * max_subdivs
            assert sum(max_subdivided) == Meter.max_subdivs

        return max_subdivided

    def perform(self):
        logging.debug("Performing Strings")

        for i in range(24):
            bar_base_time = i * Meter.max_subdivs

            max_subdivs = 1
            repeat_beats = False
            if self.scenes[i] == Scene.CLEAR_NICE:
                max_subdivs = 1
                repeat_beats = False
            elif self.scenes[i] == Scene.ANY:
                max_subdivs = 4
                repeat_beats = False
            elif self.scenes[i] == Scene.BROKEN_RAINY:
                max_subdivs = 2

            rhythm = self.generate_rhythm(max_subdivs, repeat_beats=repeat_beats)

            time_in_beat = 0
            for duration in rhythm:
                degree = randint(1,8)
                note = self.key.get_note(degree, octave=4)
                self.track.add_note(note, bar_base_time + time_in_beat, duration)
                time_in_beat += duration

        return self.track.export()