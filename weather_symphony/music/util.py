from random import random

from weather_symphony.music import Meter


def default_octave(note):
    # map notes to the lowest piano octave
    # MIDI Code for C1 is 24
    # octaves are calculated based on this C
    return note % 12 + 24


def shift_octave(note, octave):
    return note + 12 * (octave - 1)


def at_octave(note, octave):
    note = default_octave(note)
    return shift_octave(note, octave)


# additional_octaves of 0 returns the note itself
def notes_in_octave_range(note, additional_octaves):
    return [shift_octave(note, octave + 1) for octave in range(additional_octaves + 1)]


def generate_random_rhythm(max_subdivs, repeat_beats=True, density=0.5):
    """
    Returns an array of note durations
    The sum has to span a full bar

    max_subdivs per bar
    if larger than 1 it repeats for every beat
    """

    assert not repeat_beats or max_subdivs > Meter.beats_per_bar
    assert max_subdivs <= Meter.max_subdivs

    if repeat_beats and max_subdivs > Meter.beats_per_bar:
        shortest_dur = Meter.max_subdivs // max_subdivs
        max_subdivided = [shortest_dur] * (Meter.subdivs_per_beat() // shortest_dur)
        assert sum(max_subdivided) == Meter.subdivs_per_beat()
    else:
        shortest_dur = Meter.max_subdivs // max_subdivs
        max_subdivided = [shortest_dur] * max_subdivs
        assert sum(max_subdivided) == Meter.max_subdivs

    rhythm = max_subdivided[:1]
    for i in range(1, len(max_subdivided)):
        if random() < density:
            rhythm.append(max_subdivided[i])
        else:
            rhythm[-1] += max_subdivided[i]

    if repeat_beats:
        rhythm = rhythm * Meter.beats_per_bar

    return rhythm


def map_range(value, origin_min, origin_max, target_min, target_max):
    new_value = target_min + (value - origin_min) * (target_max - target_min) / (
        origin_max - origin_min
    )
    return min(max(new_value, target_min), target_max)
