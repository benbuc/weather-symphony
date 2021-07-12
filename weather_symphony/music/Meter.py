import mido

class Meter:
    total_bars=48
    beats_per_bar=4
    ticks_per_beat=4
    max_subdivs=16       # max subdivisions PER BAR
    bpm=90

    def total_beats():
        return Meter.total_bars * Meter.beats_per_bar

    def subdivs_per_beat():
        return Meter.max_subdivs // Meter.beats_per_bar