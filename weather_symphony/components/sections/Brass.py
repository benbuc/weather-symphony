import logging

from weather_symphony.components.sections.Section import Section
from weather_symphony.music import Meter, Track
from weather_symphony.music import util as mutil
from weather_symphony.music.Chords import Chord


class BrassSection(Section):
    def __init__(self, *args):
        super().__init__(*args)

        self.track_tuba = Track(58, self.channel_num)

    def create_new_rhythm(self, scene):
        self.rhythm = mutil.generate_random_rhythm(1, False)

    def perform_bar(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        last_scene = self.scenes[bar_num - 1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if cur_scene != last_scene:
            self.create_new_rhythm(cur_scene)

        time_in_bar = 0
        for duration in self.rhythm:
            chord_root = self.key.get_note(self.chords[bar_num][0])
            chord = Chord(chord_root, self.chords[bar_num][1])

            for note in chord.get_all_notes():
                self.track_tuba.add_note(
                    mutil.at_octave(note, 3),
                    bar_base_time + time_in_bar,
                    duration,
                )
            time_in_bar += duration

    def perform(self):
        logging.debug("Performing Strings")

        for i in range(len(self.weather_data) * Meter.bars_per_hour):
            self.perform_bar(i)

        return self.track_tuba.export()
