import mido

class Meter:
    total_bars=48
    beats_per_bar=4
    ticks_per_beat=4
    max_subdivs=4       # max subdivisions PER BEAT
    bpm=120

    def total_beats():
        return Meter.total_bars * Meter.beats_per_bar