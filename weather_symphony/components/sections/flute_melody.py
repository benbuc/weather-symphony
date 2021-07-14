import logging
import random

from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.section import Section
from weather_symphony.music import Meter, Track
from weather_symphony.music import util as mutil
from weather_symphony.music.chords import Chord
from weather_symphony.music.key import Major, Minor


class FluteMelody(Section):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(73, self.channel_num)
        self.base_octave = 5

    def create_new_rhythm(self, scene):
        settings = (8, 0.0, 0.3)

        max_subdivs = settings[0]
        repeatd_beats = False
        density = settings[2]

        if max_subdivs == 0:
            self.rhythm = []
            return

        self.rhythm = mutil.generate_random_rhythm(max_subdivs, repeatd_beats, density)

    def perform_bar(self, bar_num):
        last_scene = self.scenes[bar_num - 1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if last_scene is not None and cur_scene == Scene.ANY:
            cur_scene = last_scene

        if cur_scene != last_scene:
            self.create_new_rhythm(cur_scene)

        bar_base_time = bar_num * Meter.max_subdivs

        chord_root = self.keys[bar_num].get_note(self.chords[bar_num][0])
        chord = Chord(chord_root, self.chords[bar_num][1])
        scale = Major(chord_root)
        if chord.quality == "min":
            scale = Minor(chord_root)

        time_in_bar = 0
        for duration in self.rhythm:
            degree = random.randint(1, 8)
            note = scale.get_note(degree, self.base_octave)

            self.track.add_note(note, bar_base_time + time_in_bar, duration, 100)

            time_in_bar += duration

    def perform(self):
        logging.debug(f"Performing {type(self).__name__}")

        for bar_num in range(len(self.weather_data) * Meter.bars_per_hour):
            self.perform_bar(bar_num)

        return self.track.export()
