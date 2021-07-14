import logging
import random

from weather_symphony.components.scene_parser import Scene
from weather_symphony.components.sections.section import Section
from weather_symphony.music import Meter
from weather_symphony.music import util as mutil
from weather_symphony.music.chords import Chord


class HarmonySection(Section):
    def create_new_rhythm(self, scene):
        # rhythm settings are a tuple of
        # (max_subdivs, prob of repeating beats, density)
        # and set in the subclasses

        settings = (4, 0.0, 0.5)
        if self.mode == "chords":
            if scene in self.rhythm_settings_chords.keys():
                settings = self.rhythm_settings_chords[scene]
        elif self.mode == "arpeggios":
            if scene in self.rhythm_settings_arpeggios.keys():
                settings = self.rhythm_settings_arpeggios[scene]

        max_subdivs = settings[0]
        repeated_beats = True if random.random() < settings[1] else False
        density = settings[2]

        if max_subdivs == 0:
            self.rhythm = []
            return

        self.rhythm = mutil.generate_random_rhythm(max_subdivs, repeated_beats, density)

    def select_mode(self, scene):
        prob = 0.5
        if scene in self.arpeggio_probabilities.keys():
            prob = self.arpeggio_probabilities[scene]

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

        if (
            bar_num + 1 == len(self.weather_data) * Meter.bars_per_hour
            and len(self.rhythm) > 0
        ):
            self.mode = "chords"
            self.rhythm = [Meter.max_subdivs]

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

    def perform_chords(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        chord_root = self.keys[bar_num].get_note(self.chords[bar_num][0])
        chord = Chord(chord_root, self.chords[bar_num][1])

        time_in_bar = 0
        for duration in self.rhythm:
            voicing = self.get_voicing(chord)

            for note in voicing:
                self.track.add_note(
                    mutil.shift_octave(note, self.base_octave),
                    bar_base_time + time_in_bar,
                    duration,
                    self.velocities[bar_base_time + time_in_bar],
                )
            time_in_bar += duration

    def perform_arpeggios(self, bar_num):
        bar_base_time = bar_num * Meter.max_subdivs

        chord_root = self.keys[bar_num].get_note(self.chords[bar_num][0])
        chord = Chord(chord_root, self.chords[bar_num][1])
        voicing = self.get_voicing(chord, notes_in_voicing=len(self.motif[0]))

        expanded_motif = self.motif[0] * self.motif[1]

        time_in_bar = 0
        for i, duration in enumerate(self.rhythm):
            note = voicing[expanded_motif[i] % len(voicing)]

            self.track.add_note(
                mutil.shift_octave(note, self.base_octave),
                bar_base_time + time_in_bar,
                duration,
                self.velocities[bar_base_time + time_in_bar],
            )

            time_in_bar += duration

    def calculate_velocity_outline(self):
        # takes the wind data for the velocity and smoothes it
        scene_add = {
            Scene.OVERCAST_THUNDERSTORM: 100,
        }
        outline = []

        for i, hour in enumerate(self.weather_data):
            add = 0
            if self.scenes[i * Meter.bars_per_hour] in scene_add.keys():
                add = scene_add[self.scenes[i * Meter.bars_per_hour]]
            outline += (
                [int(mutil.map_range(hour["wind"], *self.velocity_range_map)) + add]
                * Meter.max_subdivs
                * Meter.bars_per_hour
            )

        smoothness = Meter.max_subdivs // 2
        smoothed_outline = []
        cumulated_sum = [0]
        for i, vel in enumerate(outline, 1):
            cumulated_sum.append(cumulated_sum[i - 1] + vel)
            if i >= smoothness:
                smoothed_vel = (
                    cumulated_sum[i] - cumulated_sum[i - smoothness]
                ) // smoothness
            else:
                smoothed_vel = vel

            if (i - 1) % Meter.max_subdivs == 0:
                smoothed_vel *= 1.2
            elif (i - 1) % (Meter.max_subdivs // 2) == 0:
                smoothed_vel *= 1.1

            smoothed_outline.append(int(min(smoothed_vel, 127)))

        self.velocities = smoothed_outline

    def perform(self):
        logging.debug(f"Performing {type(self).__name__}")

        self.calculate_velocity_outline()

        for i in range(len(self.weather_data) * Meter.bars_per_hour):
            self.perform_bar(i)

        return self.track.export()
