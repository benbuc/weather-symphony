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
        self.base_octave = 4
        self.velocity_range_map = (0, 20, 40, 110)

    def create_new_rhythm(self, scene):
        # settings are tuple of
        # (probability section plays, max_subdivs, density)
        rhythm_settings = {
            Scene.BROKEN_GUSTY: (0.3, 8, 0.4),
            Scene.SCATTERED_WINDY: (0.3, 8, 0.4),
            Scene.CLEAR_BROILING: (0.7, 4, 0.15),
            Scene.CLEAR_NICE: (0.8, 8, 0.4),
            Scene.NIGHT_CHILLY: (0.6, 16, 0.3),
            Scene.NIGHT_WARM: (0.3, 4, 0.5),
        }

        settings = (0.0, 0, 0.0)

        if scene in rhythm_settings.keys():
            settings = rhythm_settings[scene]

        max_subdivs = settings[1]
        density = settings[2]

        if random.random() < settings[0] or max_subdivs == 0:
            self.rhythm = []
            return

        self.rhythm = mutil.generate_random_rhythm(max_subdivs, False, density)

    def create_motif(self):
        self.motif = ([random.randint(1, 8) for _ in self.rhythm], 1)

    def perform_bar(self, bar_num):
        last_scene = self.scenes[bar_num - 1] if bar_num > 0 else None
        cur_scene = self.scenes[bar_num]

        if last_scene is not None and cur_scene == Scene.ANY:
            cur_scene = last_scene

        if cur_scene != last_scene or self.scene_repeat_count >= 5:
            self.scene_repeat_count = 0
            self.create_new_rhythm(cur_scene)
            self.create_motif()
        self.scene_repeat_count += 1
        bar_base_time = bar_num * Meter.max_subdivs

        chord_root = self.keys[bar_num].get_note(self.chords[bar_num][0])
        chord = Chord(chord_root, self.chords[bar_num][1])
        scale = Major(chord_root)
        if chord.quality == "min":
            scale = Minor(chord_root)

        expanded_motif = self.motif[0] * self.motif[1]

        time_in_bar = 0
        if bar_num + 1 == len(self.weather_data) * Meter.bars_per_hour:
            self.track.add_note(
                scale.get_note(scale.root, self.base_octave),
                bar_base_time,
                Meter.max_subdivs,
                self.velocities[bar_base_time + time_in_bar],
            )
            return

        for i, duration in enumerate(self.rhythm):
            note = scale.get_note(expanded_motif[i], self.base_octave)

            self.track.add_note(note, bar_base_time + time_in_bar, duration, 100)

            time_in_bar += duration

    def calculate_velocity_outline(self):
        # takes the wind data for the velocity and smoothes it
        scene_add = {}
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

        for bar_num in range(len(self.weather_data) * Meter.bars_per_hour):
            self.perform_bar(bar_num)

        return self.track.export()
