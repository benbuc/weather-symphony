from random import randint

from weather_symphony.components.scene_parser import Scene
from weather_symphony.music import Meter
from weather_symphony.music.key import Major


class HarmonyGenerator:
    def __init__(self, weather_data, scenes):
        self.weather_data = weather_data
        self.scenes = scenes

    def get_harmony(self):

        inverted_chord_graph = invert_graph(chord_graph_major)

        total_bars = len(self.weather_data) * Meter.bars_per_hour

        keys = [Major(24)]
        for bar_num in range(1, total_bars):
            if (
                self.scenes[bar_num - 1] == Scene.OVERCAST_THUNDERSTORM
                and self.scenes[bar_num] != Scene.OVERCAST_THUNDERSTORM
            ):
                keys.append(Major(keys[bar_num - 1].root + 7))
                continue
            if (
                self.scenes[bar_num - 1] != Scene.CLEAR_NICE
                and self.scenes[bar_num] == Scene.CLEAR_NICE
            ):
                keys.append(Major(keys[bar_num - 1].root + 2))

            keys.append(keys[bar_num - 1])

        chords = [None] * (total_bars - 1) + [(1, "maj")]

        for bar_num in reversed(range(total_bars - 1)):
            possible_prev = [(1, "maj")] + inverted_chord_graph[chords[bar_num + 1]]

            sampled_prev = possible_prev[randint(0, len(possible_prev) - 1)]
            chords[bar_num] = sampled_prev

        return {
            "keys": keys,
            "chords": chords,
        }


chord_graph_major = {
    (1, "maj"): [],
    (2, "min"): [(1, "maj"), (5, "maj")],
    (3, "min"): [(6, "min")],
    (4, "maj"): [(5, "maj")],
    (5, "maj"): [(1, "maj")],
    (6, "min"): [(5, "maj")],
}


def invert_graph(graph):
    new_graph = {key: [] for key in graph.keys()}
    for key in graph.keys():
        for target in graph[key]:
            new_graph[target].append(key)

    return new_graph
