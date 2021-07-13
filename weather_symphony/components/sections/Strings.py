import logging
from random import randint

from weather_symphony.components.SceneParser import Scene
from weather_symphony.components.sections.Section import Section
from weather_symphony.music import Meter, Track
from weather_symphony.music import util as mutil


class StringSection(Section):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(48, self.channel_num)

    def create_new_rhythm(self, scene):

        max_subdivs = 4
        repeated_beats = False
        if scene == Scene.OVERCAST_THUNDERSTORM:
            max_subdivs = 16
            repeated_beats = True
            # TODO density
        elif scene == Scene.CLEAR_BROILING:
            max_subdivs = 2
            repeated_beats = False

        self.rhythm = mutil.generate_random_rhythm(max_subdivs, repeated_beats)

    def perform_bar(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        last_scene = self.scenes[bar_num - 1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if cur_scene != last_scene:
            self.create_new_rhythm(cur_scene)

        time_in_bar = 0
        for duration in self.rhythm:
            degree = randint(1, 8)
            note = self.key.get_note(degree, octave=5)
            self.track.add_note(
                note,
                bar_base_time + time_in_bar,
                duration,
            )
            time_in_bar += duration

    def perform(self):
        logging.debug("Performing Strings")

        for i in range(Meter.total_bars):
            self.perform_bar(i)

        return self.track.export()
