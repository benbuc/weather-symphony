from weather_symphony.music.Key import Major
from weather_symphony.music.Chords import Chord
from weather_symphony.music import Meter

from random import randint

class HarmonyGenerator:
    def __init__(self, weather_data, scenes):
        self.weather_data = weather_data
        self.scenes = scenes

    def get_harmony(self):

        chords = []
        last = (1, 'maj')
        for bar in range(Meter.total_bars):
            if last == (1, 'maj'):
                possible_nexts = list(chord_graph_major.keys())
            else:
                possible_nexts = [last] + chord_graph_major[last]

            sampled_next = possible_nexts[randint(0,len(possible_nexts)-1)]
            chords.append(sampled_next)
            last = sampled_next


        return {
            'key': Major(24), # C Major
            'chords': chords
        }

chord_graph_major = {
    (1, 'maj'): [],
    (2, 'min'): [(1, 'maj'), (5, 'maj')],
    (3, 'min'): [(6, 'min')],
    (4, 'maj'): [(5, 'maj')],
    (5, 'maj'): [(1, 'maj')],
    (6, 'min'): [(5, 'maj')],
}