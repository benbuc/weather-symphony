import logging
import random

from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.section import Section
from weather_symphony.music import Meter, Track
from weather_symphony.music import util as mutil
from weather_symphony.music.chords import Chord


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

        if self.mode == "chords":
            max_subdivs = 2
            repeated_beats = False

        self.rhythm = mutil.generate_random_rhythm(max_subdivs, repeated_beats)

    def create_mode(self, scene):
        self.mode = "chords"

        # if scene == Scene.NIGHT_CHILLY:
        #    self.mode = "arpeggio"

    def create_motif(self):
        if len(self.rhythm) % 4 == 0:
            self.motif = [
                random.randint(1, 8) for _ in range(len(self.rhythm) // 4)
            ] * 4
        else:
            self.motif = [random.randint(1, 8) for _ in self.rhythm]

    def perform_bar(self, bar_num):
        last_scene = self.scenes[bar_num - 1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if cur_scene != last_scene:
            self.create_mode(cur_scene)
            self.create_new_rhythm(cur_scene)
            self.create_motif()

        if self.mode == "chords":
            self.perform_chords(bar_num)

    def get_voicing(self, chord):
        notes_in_voicing = 3
        additional_octaves = 1

        possible_notes = []
        for note in chord.get_all_notes():
            possible_notes += mutil.notes_in_octave_range(note, additional_octaves)

        return random.sample(possible_notes, notes_in_voicing)

    # TODO: move to utils
    def map_range(self, value, origin_min, origin_max, target_min, target_max):
        new_value = target_min + (value - origin_min) * (target_max - target_min) / (
            origin_max - origin_min
        )
        return min(max(new_value, target_min), target_max)

    def perform_chords(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        time_in_bar = 0
        for duration in self.rhythm:
            chord_root = self.key.get_note(self.chords[bar_num][0])
            chord = Chord(chord_root, self.chords[bar_num][1])
            voicing = self.get_voicing(chord)

            velocity = self.weather_data[bar_num // Meter.bars_per_hour]["wind"]
            velocity = int(self.map_range(velocity, 0, 20, 30, 127))

            for note in voicing:
                self.track.add_note(
                    mutil.shift_octave(note, 2),
                    bar_base_time + time_in_bar,
                    duration,
                    velocity,
                )
            time_in_bar += duration

    def perform(self):
        logging.debug("Performing Strings")

        for i in range(len(self.weather_data) * Meter.bars_per_hour):
            self.perform_bar(i)

        return self.track.export()
