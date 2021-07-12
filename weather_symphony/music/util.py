from random import random

from weather_symphony.music import Meter

def generate_rhythm(max_subdivs, repeat_beats=True):
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
            max_subdivided = [shortest_dur] *  (Meter.subdivs_per_beat() // shortest_dur)
            assert (sum(max_subdivided) == Meter.subdivs_per_beat())
        else:
            shortest_dur = Meter.max_subdivs // max_subdivs
            max_subdivided = [shortest_dur] * max_subdivs
            assert sum(max_subdivided) == Meter.max_subdivs

        rhythm = max_subdivided[:1]
        for i in range(1, len(max_subdivided)):
            if random() > 0.5:
                rhythm.append(max_subdivided[i])
            else:
                rhythm[-1] += max_subdivided[i]

        if repeat_beats:
            rhythm = rhythm * Meter.beats_per_bar

        return rhythm