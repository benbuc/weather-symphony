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
        # (max_subdivs, prob of repeatin beats, density)
        rhythm_settings_arpeggios = {
            Scene.OVERCAST_THUNDERSTORM: (16, 0.8, 0.9),
            Scene.OVERCAST_WINDY: (16, 0.8, 0.75),
            Scene.BROKEN_RAINY: (8, 0.6, 0.4),
            Scene.BROKEN_GUSTY: (16, 0.9, 0.4),
            Scene.SCATTERED_WINDY: (16, 0.9, 0.4),
            Scene.CLEAR_BROILING: (4, 0.0, 0.3),
            Scene.CLEAR_NICE: (4, 0.0, 0.5),
            Scene.NIGHT_CHILLY: (8, 0.7, 0.5),
            Scene.NIGHT_WARM: (8, 0.8, 0.4),
        }
        rhythm_settings_chords = {
            Scene.OVERCAST_THUNDERSTORM: (4, 0.0, 0.7),
            Scene.OVERCAST_WINDY: (4, 0.0, 0.5),
            Scene.BROKEN_RAINY: (4, 0.0, 0.5),
            Scene.BROKEN_GUSTY: (4, 0.0, 0.5),
            Scene.SCATTERED_WINDY: (4, 0.0, 0.5),
            Scene.CLEAR_BROILING: (1, 0.0, 0.3),
            Scene.CLEAR_NICE: (2, 0.0, 0.5),
            Scene.NIGHT_CHILLY: (4, 0.0, 0.5),
            Scene.NIGHT_WARM: (2, 0.0, 0.5),
        }

        settings = (4, 0.0, 0.5)
        if self.mode == "chords":
            if scene in rhythm_settings_chords.keys():
                settings = rhythm_settings_chords[scene]
        elif self.mode == "arpeggios":
            if scene in rhythm_settings_arpeggios.keys():
                settings = rhythm_settings_arpeggios[scene]

        max_subdivs = settings[0]
        repeated_beats = True if random.random() < settings[1] else False
        density = settings[2]

        self.rhythm = mutil.generate_random_rhythm(max_subdivs, repeated_beats, density)

    def select_mode(self, scene):
        arpeggio_probabilities = {
            Scene.OVERCAST_THUNDERSTORM: 0.95,
            Scene.OVERCAST_WINDY: 0.8,
            Scene.BROKEN_RAINY: 0.8,
            Scene.BROKEN_GUSTY: 0.9,
            Scene.SCATTERED_WINDY: 0.9,
            Scene.SCATTERED_SWELTRY: 0.4,
            Scene.CLEAR_BROILING: 0.05,
            Scene.CLEAR_NICE: 0.15,
            Scene.NIGHT_CHILLY: 0.6,
            Scene.NIGHT_WARM: 0.5,
        }

        prob = 0.5
        if scene in arpeggio_probabilities.keys():
            prob = arpeggio_probabilities[scene]

        if random.random() < prob:
            self.mode = "arpeggios"
        else:
            self.mode = "chords"

    def create_motif(self):
        # the motif is a tuple:
        # (list of scale degrees, repitions of motif per bar)

        if len(self.rhythm) % 4 == 0 and len(self.rhythm) > 4:
            self.motif = (
                [random.randint(1, 8) for _ in range(len(self.rhythm) // 4)],
                4,
            )
        else:
            self.motif = ([random.randint(1, 8) for _ in self.rhythm], 1)

    def perform_bar(self, bar_num):
        last_scene = self.scenes[bar_num - 1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if last_scene is not None and cur_scene == Scene.ANY:
            cur_scene = last_scene

        if cur_scene != last_scene:
            self.select_mode(cur_scene)
            self.create_new_rhythm(cur_scene)
            self.create_motif()

        if self.mode == "chords":
            self.perform_chords(bar_num)
        elif self.mode == "arpeggios":
            self.perform_arpeggios(bar_num)

    def get_voicing(self, chord, notes_in_voicing=3):
        additional_octaves = 1
        if self.mode == "arpeggios":
            additional_octaves = 0

        possible_notes = []
        for note in chord.get_all_notes():
            possible_notes += mutil.notes_in_octave_range(note, additional_octaves)

        if additional_octaves == 0:
            possible_notes.append(mutil.shift_octave(chord.root, 1))

        if notes_in_voicing > len(possible_notes):
            return possible_notes

        return random.sample(possible_notes, notes_in_voicing)

    # TODO: move to utils
    def map_range(self, value, origin_min, origin_max, target_min, target_max):
        new_value = target_min + (value - origin_min) * (target_max - target_min) / (
            origin_max - origin_min
        )
        return min(max(new_value, target_min), target_max)

    def perform_chords(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        chord_root = self.key.get_note(self.chords[bar_num][0])
        chord = Chord(chord_root, self.chords[bar_num][1])

        time_in_bar = 0
        for duration in self.rhythm:
            voicing = self.get_voicing(chord)

            for note in voicing:
                self.track.add_note(
                    mutil.shift_octave(note, 2),
                    bar_base_time + time_in_bar,
                    duration,
                    self.velocities[bar_base_time + time_in_bar],
                )
            time_in_bar += duration

    def perform_arpeggios(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        chord_root = self.key.get_note(self.chords[bar_num][0])
        chord = Chord(chord_root, self.chords[bar_num][1])
        voicing = self.get_voicing(chord, notes_in_voicing=len(self.motif[0]))

        expanded_motif = self.motif[0] * self.motif[1]

        time_in_bar = 0
        for i, duration in enumerate(self.rhythm):
            note = voicing[expanded_motif[i] % len(voicing)]

            self.track.add_note(
                mutil.shift_octave(note, 2),
                bar_base_time + time_in_bar,
                duration,
                self.velocities[bar_base_time + time_in_bar],
            )

            time_in_bar += duration

    def calculate_velocity_outline(self):
        # takes the wind data for the velocity at smoothes it
        outline = []

        for hour in self.weather_data:
            outline += (
                [int(self.map_range(hour["wind"], 0, 20, 30, 127))]
                * Meter.max_subdivs
                * Meter.bars_per_hour
            )

        smoothness = Meter.max_subdivs // 2
        smoothed_outline = []
        cumulated_sum = [0]
        for i, vel in enumerate(outline, 1):
            cumulated_sum.append(cumulated_sum[i - 1] + vel)
            if i >= smoothness:
                smoothed_outline.append(
                    (cumulated_sum[i] - cumulated_sum[i - smoothness]) // smoothness
                )
            else:
                smoothed_outline.append(vel)

        self.velocities = smoothed_outline

    def perform(self):
        logging.debug("Performing Strings")

        self.calculate_velocity_outline()

        for i in range(len(self.weather_data) * Meter.bars_per_hour):
            self.perform_bar(i)

        return self.track.export()
