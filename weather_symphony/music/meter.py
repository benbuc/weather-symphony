class Meter:
    bars_per_hour = 2
    beats_per_bar = 4
    ticks_per_beat = 4
    max_subdivs = 16  # max subdivisions PER BAR
    bpm = 90

    @classmethod
    def total_beats(cls, total_hours):
        return total_hours * Meter.bars_per_hour * Meter.beats_per_bar

    @classmethod
    def subdivs_per_beat(cls):
        return Meter.max_subdivs // Meter.beats_per_bar
